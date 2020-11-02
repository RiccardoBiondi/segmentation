import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example
from  hypothesis import HealthCheck as HC


from CTLungSeg.utils import load_pickle
from CTLungSeg.utils import save_pickle
from CTLungSeg.utils import write_volume
from CTLungSeg.utils import  _read_image
from CTLungSeg.utils import read_image
from CTLungSeg.utils import normalize
from CTLungSeg.utils import rescale
from CTLungSeg.utils import gl2bit
from CTLungSeg.utils import hu2gl
from CTLungSeg.utils import center_hu
from CTLungSeg.utils import shuffle_and_split
from CTLungSeg.utils import _imfill
from CTLungSeg.utils import stats2dataframe
from CTLungSeg.utils import _std_dev

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

# medical image format strategy


medical_image_formats = ['.nii', '.nrrd', '.nhdr', '.nii.gz']
#strategy to generate a random stack of 8-bit images
@st.composite
def rand_stack_strategy(draw, n_imgs = st.integers(2, 50)) :
    N = draw(n_imgs)
    return (255 * np.random.rand(N, 512, 512)).astype(np.uint8)

@st.composite
def gl16_stack_strategy(draw):

    n_imgs = draw(st.integers(1, 200))
    stack = randint(-4000, 4000,  (n_imgs, 512, 512), dtype = np.int16)

    return stack

@st.composite
def voxel_spatial_info_strategy(draw) :

    origin = draw(st.tuples(*[st.floats(0., 100.)] * 3))
    spacing = draw(st.tuples(*[st.floats(.1, 1.)] * 3))
    direction = tuple([0., 0., 1., 1., 0., 0., 0., 1., 0.])

    return [origin, spacing, direction]



################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################


@given(rand_stack_strategy(), filename_strategy)
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_save_and_load_pkl(imgs,  filename):
    '''
    Givena random 3D array and a random name :
    - save the array as .pkl.npy with the random name
    - reload the array
    - assert that the input array and the loaded one are equal
    '''
    save_pickle('./testing/images/' + filename, imgs)
    load = load_pickle('./testing/images/' + filename + '.pkl.npy')
    assert (load == imgs).all()


@given(filename_strategy, st.sampled_from(medical_image_formats))
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_reader(filename, format) :
    '''
    Given a filename and a file format, test that a reader object is created with the
    correct parameters
    '''
    fname = filename + format
    reader =  _read_image(fname)
    assert reader.GetFileName() == fname


@given(gl16_stack_strategy(), voxel_spatial_info_strategy(),
        filename_strategy, st.sampled_from(medical_image_formats))
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_read_and_write_image(volume, info, filename, format) :
    '''
    Given a random array, a random name, a random image format and random spatial
    information :
    - write the array as image
    - reead the image
    - assert that the red image array is equal to the input one
    - assert that the red spatial information are aqual to the input one
    '''

    fname = './testing/images/{}'.format(filename)
    write_volume(volume, fname, info, format)
    red, red_info = read_image(fname + format)

    assert (red == volume).all()
    assert np.isclose(info[0], red_info[0]).all()
    assert np.isclose(info[1], red_info[1]).all()
    assert np.isclose(info[2], red_info[2]).all()




@given(rand_stack_strategy())
@settings(max_examples=20,
deadline=None,suppress_health_check=(HC.too_slow,))
def test_normalize(stack) :
    normalized = normalize(stack)

    assert np.isclose(np.std(normalized), 1)
    assert np.isclose(np.mean(normalized), 0)


@given(rand_stack_strategy())
@settings(max_examples=20,
deadline=None,suppress_health_check=(HC.too_slow,))
def test_rescale(img):

    rescaled = rescale(img, np.amax(img), 0 )
    assert np.isclose(rescaled.max(), 1.)
    assert np.amin(rescaled) >= 0.

    with pytest.raises(ZeroDivisionError) :
        assert rescale(img, 3, 3)


@given(st.integers(1,30))
@settings(max_examples = 2, deadline = None, suppress_health_check=(HC.too_slow,))
def test_gl2bit(n_imgs) :
    input = np.ones((n_imgs, 100, 100), dtype = np.uint8)
    result = gl2bit(input, 8)
    assert (np.unique(result) == [0,1]).all()


@given(rand_stack_strategy(), st.integers(0, 7))
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_gl2bit_value_error(image, bits) :
    '''
    Given a wrong number of bits, assert that a value error is raised
    '''
    with pytest.raises(ValueError) :
        assert gl2bit(image, bits)


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_hu2gl(img):
    '''
    Given an image is hu to convert in an 8-bit image,
    assert that :
    - the minimum value is 0
    - the maximum value is 255
    '''
    out = hu2gl(img)
    assert out.max() == 255
    assert out.min() == 0


@given(gl16_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_center_hu(volume) :
    '''
    Given a stack of images whoch each values is a random 16-bit integers,
    assert that :
    - the shape is preserved
    - the maximum value lesser than 2049
    - the minimum value higher than -1S
    '''
    res = center_hu(volume)

    assert res.shape == volume.shape
    assert res.min() > -1
    assert res.max() < 2049


@given(st.integers(200, 1000), st.integers(2, 200))
@settings(max_examples  = 20, deadline = None)
def test_shuffle_and_split(n_sample, n_subsamples):
    '''
    Given
    '''
    sample = np.array([np.ones((randint(1,301), randint(1, 301))) for i in range(n_sample)], dtype=np.ndarray)
    subsample = shuffle_and_split(sample, n_subsamples)

    assert subsample.shape[0] == n_subsamples


def test_imfill():
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    compare = 255 * ones(image.shape, dtype = np.uint8)
    filled = _imfill(image)
    assert (compare == filled.astype(np.uint8)).all()


@given(st.integers(2,30), st.integers(2, 30))
@settings(max_examples = 20, deadline = None)
def test_stats2dataframe(n_slices, cc):
    shape = (cc, 5)
    input = [np.empty(shape) for i in range(n_slices)]
    df = stats2dataframe(input)
    assert len(df) == n_slices
