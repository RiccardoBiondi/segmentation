import pytest
import hypothesis.strategies as st
from hypothesis import given, example, assume, settings

import numpy as np
from numpy import ones, zeros
from numpy.random import rand

from segmentation.method import save_pickle
from segmentation.method import load_pickle
from segmentation.method import rescale
from segmentation.method import erode
from segmentation.method import dilate
from segmentation.method import connectedComponentsWithStats
from segmentation.method import bitwise_not

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']



image = st.just(rand)
black_image = st.just(zeros)
white_imge = st.just(ones)
kernel = st.just(ones)


#testing save and load functions
@given(image, st.integers(1,200), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_save_and_load(data, n_img, n_pixels):
    input = data(n_img, n_pixels, n_pixels)
    save_pickle('./test_file', input)
    load = load_pickle('./test_file.pkl.npy')
    assert((load == input).all())


#testing rescale function
@given(image, st.integers(1,200), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_rescale(data, n_img, n_pixels):
    input =  255. * data(n_img, n_pixels, n_pixels)
    rescaled = rescale(input, np.amax(input), 0 )
    assert( np.amax(rescaled) <= 1. and np.amin(rescaled) >= 0)


#testing erosion for a stack
@given(image, kernel, st.integers(5,30), st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_erode_stack(data, kernel, n_img, n_pix, k_dim):
    eroded = erode(data(n_img, n_pix, n_pix), kernel((k_dim,k_dim)))
    assert ( eroded.shape == (n_img, n_pix, n_pix))


#test erosion for a single images
@given(image, kernel, st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_erode(data, kernel, n_pix, k_dim):
    eroded = erode(data(n_pix,n_pix), kernel((k_dim,k_dim)))
    assert (eroded.shape == (n_pix, n_pix))


#testing dilation for a stack
@given(image, kernel, st.integers(5,30), st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_dilate_stack(data, kernel, n_img, n_pix, k_dim):
    dilated = dilate(data(n_img, n_pix, n_pix), kernel((k_dim,k_dim)))
    assert ( dilated.shape == (n_img, n_pix, n_pix))


#test dilation for a single images
@given(image, kernel, st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 3, deadline = None)
def test_dilate(data, kernel, n_pix, k_dim):
    dilated = dilate(data(n_pix,n_pix), kernel((k_dim,k_dim)))
    assert (dilated.shape == (n_pix, n_pix))





#test bitwise not for a single images
@given(black_image, white_imge, st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_bitwise_not(input, expected_output, n_pix):
    inverted = bitwise_not(input((n_pix, n_pix)))
    assert ((inverted == 255 * expected_output((n_pix, n_pix))).all())



#test bitwise not for a stack
@given(black_image, white_imge, st.integers(2,30), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_bitwise_not_stack(input, expected_output, n_img, n_pix):
    inverted = bitwise_not(input((n_img, n_pix, n_pix)))
    assert((inverted == 255 * expected_output((n_img, n_pix, n_pix))).all())
