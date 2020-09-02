import pytest
import hypothesis.strategies as st
from hypothesis import given, settings

from segmentation.method import erode
from segmentation.method import dilate
from segmentation.method import connectedComponentsWithStats
from segmentation.method import bitwise_not
from segmentation.method import imfill
from segmentation.method import medianBlur
from segmentation.method import gaussianBlur
from segmentation.method import otsu

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


#testing erosion for a stack
@given(image, kernel, st.integers(5,30), st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_erode_stack(data, kernel, n_img, n_pix, k_dim):
    eroded = erode(data(n_img, n_pix, n_pix), kernel((k_dim, k_dim)))
    assert eroded.shape == (n_img, n_pix, n_pix)


#test erosion for a single images
@given(image, kernel, st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_erode(data, kernel, n_pix, k_dim):
    eroded = erode(data(n_pix, n_pix), kernel((k_dim, k_dim)))
    assert eroded.shape == (n_pix, n_pix)


#testing dilation for a stack
@given(image, kernel, st.integers(5,30), st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 20, deadline = None)
def test_dilate_stack(data, kernel, n_img, n_pix, k_dim):
    dilated = dilate(data(n_img, n_pix, n_pix), kernel((k_dim, k_dim)))
    assert dilated.shape == (n_img, n_pix, n_pix)


#test dilation for a single images
@given(image, kernel, st.integers(300, 512), st.integers(3,11))
@settings(max_examples = 3, deadline = None)
def test_dilate(data, kernel, n_pix, k_dim):
    dilated = dilate(data(n_pix, n_pix), kernel((k_dim, k_dim)))
    assert dilated.shape == (n_pix, n_pix)


#test bitwise not for a single images
@given(black_image, white_image, st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_bitwise_not(input, expected_output, n_pix):
    inverted = bitwise_not(input((n_pix, n_pix)))
    assert (inverted == 255 * expected_output((n_pix, n_pix))).all()


#test bitwise not for a stack
@given(black_image, white_image, st.integers(2,30), st.integers(300,512))
@settings(max_examples = 20, deadline = None)
def test_bitwise_not_stack(input, expected_output, n_img, n_pix):
    inverted = bitwise_not(input((n_img, n_pix, n_pix)))
    assert (inverted == 255 * expected_output((n_img, n_pix, n_pix))).all()


@given(image, st.integers(2, 30), st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_medianBlur_stack (img, n_img, n_pix) :
    input = 255 * img(n_img, n_pix, n_pix)
    blurred = medianBlur(input.astype(np.float32), 5)
    assert blurred.shape == input.shape


#Test gaussian blur filter function
@given(image, st.integers(2, 30), st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_gaussianBlur_stack (img, n_img, n_pix) :
    input = 255 * img(n_img, n_pix, n_pix)
    blurred = gaussianBlur(input.astype(np.float32), ksize=(5, 5))
    assert blurred.shape == input.shape


@given(white_image, st.integers(2, 300))
@settings(max_examples = 20, deadline = None)
def test_imfill(to_compare, n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    to_fill = np.array([image for i in range(n_img)])
    compare = 255 * to_compare(image.shape)
    filled = imfill(to_fill)
    assert  ((im == compare).all() for im in filled)


@given(st.integers(2,300))
@settings(max_examples = 20, deadline = None )
def test_connectedComponentsWithStats(n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = bitwise_not(image)
    input =np.array([image for i in range(n_img)])
    n_regions = 4
    retval, labels, stats, centroids = connectedComponentsWithStats(input)
    print(np.unique(labels))
    assert len(np.unique(labels)) == n_regions
    assert len(np.unique(centroids)) == n_regions


#testing otsu threshold
@given(image, st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_otsu(data, n_imgs):
    input = (255 * data(n_imgs, 512, 512)).astype(np.uint8)
    out = otsu(input)
    assert np.all(np.unique(out) == np.array([0, 1]))
