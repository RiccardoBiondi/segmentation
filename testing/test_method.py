import pytest
import hypothesis.strategies as st
from hypothesis import given, example, assume, settings

from segmentation.method import save_pickle
from segmentation.method import load_pickle
from segmentation.method import rescale
from segmentation.method import erode
from segmentation.method import dilate
from segmentation.method import connectedComponentsWithStats
from segmentation.method import bitwise_not
from segmentation.method import imfill
from segmentation.method import medianBlur


import cv2
import numpy as np
from numpy import ones, zeros
from numpy.random import rand

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']



image = st.just(rand)
black_image = st.just(zeros)
white_image = st.just(ones)
kernel = st.just(ones)

#testing save and load functions
@given(image, st.integers(1,200), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_save_and_load(data, n_img, n_pixels):
    #create a random stack of images
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
    eroded = erode(data(n_img, n_pix, n_pix), kernel((k_dim, k_dim)))
    assert (eroded.shape == (n_img, n_pix, n_pix))


#test erosion for a single images
@given(image, kernel, st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_erode(data, kernel, n_pix, k_dim):
    eroded = erode(data(n_pix, n_pix), kernel((k_dim, k_dim)))
    assert (eroded.shape == (n_pix, n_pix))


#testing dilation for a stack
@given(image, kernel, st.integers(5,30), st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_dilate_stack(data, kernel, n_img, n_pix, k_dim):
    dilated = dilate(data(n_img, n_pix, n_pix), kernel((k_dim, k_dim)))
    assert (dilated.shape == (n_img, n_pix, n_pix))


#test dilation for a single images
@given(image, kernel, st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 3, deadline = None)
def test_dilate(data, kernel, n_pix, k_dim):
    dilated = dilate(data(n_pix, n_pix), kernel((k_dim, k_dim)))
    assert (dilated.shape == (n_pix, n_pix))


#test bitwise not for a single images
@given(black_image, white_image, st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_bitwise_not(input, expected_output, n_pix):
    inverted = bitwise_not(input((n_pix, n_pix)))
    assert ((inverted == 255 * expected_output((n_pix, n_pix))).all())


#test bitwise not for a stack
@given(black_image, white_image, st.integers(2,30), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_bitwise_not_stack(input, expected_output, n_img, n_pix):
    inverted = bitwise_not(input((n_img, n_pix, n_pix)))
    assert((inverted == 255 * expected_output((n_img, n_pix, n_pix))).all())


@given(image, st.integers(2, 30), st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_medianBlur_stack (img, n_img, n_pix) :
    input = 255 * img(n_img, n_pix, n_pix)
    blurred = medianBlur(input, 5)
    assert(blurred.shape == input.shape)


@given(white_image, st.integers(2, 300))
@settings(max_examples = 20, deadline = None)
def test_imfill(to_compare, n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    to_fill = np.array([image for i in range(n_img)])
    compare = 255 * to_compare(image.shape)
    filled = imfill(to_fill)
    assert ( (im == compare).all() for im in filled)


@given(st.integers(2,300))
@settings(max_examples = 20, deadline = None )
def test_connectedComponentsWithStats(n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = bitwise_not(image)
    input =np.array([image for i in range(n_img)])
    n_regions = 4
    retval, labels, stats, centroids = connectedComponentsWithStats(input)
    print(np.unique(labels))
    assert (len(np.unique(labels)) == n_regions)
    assert (len(np.unique(centroids)) == n_regions)


@given(st.integers(500, 12000), st.integers(2,8))
@settings(max_examples = 20, deadline = None)
def test_kMeansMod(data_len, K) :
    data = 255 * rand(data_len)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, labels, centroid = kMeansMod(np.float32(data), K, criteria)

    assert(centroid.shape[0] == K)
    assert(len(labels) == data_len)



@given(image, st.tuples(st.integers(3,9), st.integers(15, 30)))
@settings(max_examples = 20, deadline = None)
def test_fill_holes(imgs, k_size) :
    input = imgs(100, 512, 512)
    input = 255 * np.where(input > 0.5, 0, 1 )
    output = fill_holes(input.astype('uint8'), k_size)
    assert (output.shape == input.shape)
    assert (np.unique(output).shape <= (2,))
