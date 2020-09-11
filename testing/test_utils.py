import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example
from  hypothesis import HealthCheck as HC


from CTLungSeg.utils import load_pickle
from CTLungSeg.utils import save_pickle
from CTLungSeg.utils import load_npz
from CTLungSeg.utils import save_npz
from CTLungSeg.utils import load_dicom
from CTLungSeg.utils import load_image
from CTLungSeg.utils import rescale
from CTLungSeg.utils import preprocess
from CTLungSeg.utils import subsamples
from CTLungSeg.utils import imfill
from CTLungSeg.utils import stats2dataframe
from CTLungSeg.utils import imcrop

import cv2
import numpy as np
from numpy.random import randint
from numpy import ones


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


#Define Test strategies

#create filename
unicode_categories = ('Nd','Lu','Ll', 'Pc', 'Pd')
legitimate_chars = st.characters(whitelist_categories=(unicode_categories))
filename_strategy = st.text(alphabet=legitimate_chars, min_size=1, max_size=15)

#strategy to generate a random stack of 8-bit images
@st.composite
def rand_stack_strategy(draw, n_imgs = st.integers(2, 50)) :
    N = draw(n_imgs)
    return (255 * np.random.rand(N, 512, 512)).astype(np.uint8)

#START TESTING

@given(rand_stack_strategy(), filename_strategy)
@settings(max_examples = 20, deadline = None)
def test_save_and_load_pkl(imgs,  filename):
    save_pickle('./testing/images/' + filename, imgs)
    load = load_pickle('./testing/images/' + filename + '.pkl.npy')
    assert (load == imgs).all()


@given(rand_stack_strategy(), filename_strategy)
@settings(max_examples = 20, deadline = None)
def test_save_and_load_npz(imgs, filename):
    save_npz('./testing/images/' + filename, imgs)
    load = load_npz('./testing/images/' + filename + '.npz')
    assert (load == imgs).all()


'''
#testing load_dicom
def test_load_dicom():
    ref = load_pickle('./testing/images/test_dicom/DICOM_gt.pkl.npy')
    img = load_dicom('./testing/images/test_dicom/DICOM/')
    assert (ref == img).all()
'''


def test_load_img() :
    ref = load_pickle('./testing/images/test_dicom/DICOM_gt.pkl.npy')
    img_pkl = load_image('./testing/images/test_dicom/DICOM_gt.pkl.npy')
#    img_dcm = load_image('./testing/images/test_dicom/DICOM/')
    assert (ref == img_pkl).all()
#    assert (ref == img_dcm).all()
    with pytest.raises(FileNotFoundError) :
        assert load_image('./testing/images/DICOM_gt.pkl.npy')


@given(rand_stack_strategy())
@settings(max_examples=20,
deadline=None,suppress_health_check=(HC.too_slow,))
def test_rescale(img):

    rescaled = rescale(img, np.amax(img), 0 )
    assert np.isclose(rescaled.max(), 1.)
    assert np.amin(rescaled) >= 0.

    with pytest.raises(ZeroDivisionError) :
        assert rescale(img, 3, 3)


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_preprocess(img):

    out = preprocess(img)
    assert out.max() == 255
    assert out.min() == 0



@given(st.integers(200, 1000), st.integers(2, 200))
@settings(max_examples  = 20, deadline = None)
def test_subsamples(n_sample, n_subsamples):
    sample = np.array([np.ones((randint(1,301), randint(1, 301))) for i in range(n_sample)], dtype=np.ndarray)
    subsample = subsamples(sample, n_subsamples)
    
    assert subsample.shape[0] == n_subsamples



def test_imfill():
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    compare = 255 * ones(image.shape, dtype = np.uint8)
    filled = imfill(image)
    assert (compare == filled.astype(np.uint8)).all()


@given(st.integers(2,30), st.integers(2, 30))
@settings(max_examples = 20, deadline = None)
def test_stats2dataframe(n_slices, cc):
    shape = (cc, 5)
    input = [np.empty(shape) for i in range(n_slices)]
    df = stats2dataframe(input)
    assert len(df) == n_slices


@given(st.integers(0, 200), st.integers(0, 200), st.integers(1, 200), st.integers(1, 200))
@settings(max_examples = 20, deadline = None)
@example(x = 0, y = 0, h = 0, w = 0)
def test_imcrop(x, y, w, h) :
    roi = np.array([x, y, x + w, y + h], dtype = np.int16)
    crop = imcrop(ones((512, 512), dtype = np.uint8), roi)
    assert crop.shape == (h, w)
