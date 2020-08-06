import pytest
import hypothesis.strategies as st
from hypothesis import given, settings

from segmentation.utils import load_pickle
from segmentation.utils import save_pickle
from segmentation.utils import load_npz
from segmentation.utils import save_npz
from segmentation.utils import rescale
from segmentation.utils import preprocess
from segmentation.utils import imfill
from segmentation.utils import to_dataframe

import cv2
import numpy as np
from numpy.random import rand
from numpy import ones, zeros


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']



image = st.just(rand)
black_image = st.just(zeros)
white_image = st.just(ones)
kernel = st.just(ones)

#testing save and load pickle functions
@given(image, st.integers(1,200), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_save_and_load_pkl(data, n_img, n_pixels):
    input = data(n_img, n_pixels, n_pixels)
    save_pickle('./testing/images/test_file', input)
    load = load_pickle('./testing/images/test_file.pkl.npy')
    assert (load == input).all()


#testing save and load npz functions
@given(image, st.integers(1,200), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_save_and_load_npz(data, n_img, n_pixels):
    input = data(n_img, n_pixels, n_pixels)
    save_npz('./testing/images/test_file', input)
    load = load_npz('./testing/images/test_file.npz')
    assert (load == input).all()


#testing rescale function
@given(image, st.integers(1,200), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_rescale(data, n_img, n_pixels):
    input =  255. * data(n_img, n_pixels, n_pixels)
    rescaled = rescale(input, np.amax(input), 0 )
    assert np.isclose(rescaled.max(), 1.)
    assert np.amin(rescaled) >= 0.

    with pytest.raises(ZeroDivisionError) :
        assert rescale(input, 3, 3)


#testing preprocess function
@given(image, st.integers(1,200), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_preprocess(data, n_img, n_pixels):
    input =  255. * data(n_img, n_pixels, n_pixels)
    out = preprocess(input)
    assert np.amax(out) == 255
    assert np.amin(out) == 0


#testing imfill
@given(white_image)
@settings(max_examples = 20, deadline = None)
def test_imfill(white_image):
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    compare = 255 * white_image(image.shape)
    filled = imfill(image)
    assert (compare.astype(np.uint8) == filled.astype(np.uint8)).all()


#test to dataframe
@given(st.integers(2,30), st.integers(2, 30))
@settings(max_examples = 20, deadline = None)
def test_to_dataframe(n_slices, cc):
    shape = (cc, 5)
    columns = ['LEFT', 'TOP', 'WIDTH', 'HEIGHT', 'AREA']
    input = [np.empty(shape) for i in range(n_slices)]
    df = to_dataframe(input , columns)
    assert len(df) == n_slices
