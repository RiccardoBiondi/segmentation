#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example

from CTLungSeg.method import erode
from CTLungSeg.method import dilate
from CTLungSeg.method import connected_components_wStats
from CTLungSeg.method import bitwise_not
from CTLungSeg.method import imfill
from CTLungSeg.method import median_blur
from CTLungSeg.method import gaussian_blur
from CTLungSeg.method import otsu_threshold


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



@given(image, st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_median_blur (img, n_pix) :
    input = 255 * img(n_pix, n_pix)
    blurred = median_blur(input.astype(np.float32), 5)
    assert blurred.shape == input.shape


@given(image, st.integers(2, 30), st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_median_blur_stack (img, n_img, n_pix) :
    input = 255 * img(n_img, n_pix, n_pix)
    blurred = median_blur(input.astype(np.float32), 5)
    assert blurred.shape == input.shape


@given(image, st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_gaussian_blur_stack (img, n_pix) :
    input = 255 * img(n_pix, n_pix)
    blurred = gaussian_blur(input.astype(np.float32), ksize=(5, 5))
    assert blurred.shape == input.shape


#Test gaussian blur filter function
@given(image, st.integers(2, 30), st.integers(300, 512))
@settings(max_examples = 20, deadline = None)
def test_gaussian_blur_stack (img, n_img, n_pix) :
    input = 255 * img(n_img, n_pix, n_pix)
    blurred = gaussian_blur(input.astype(np.float32), ksize=(5, 5))
    assert blurred.shape == input.shape




@given(white_image)
@settings(max_examples = 20, deadline = None)
def test_imfill(to_compare) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    compare = 255 * to_compare(image.shape)
    filled = imfill(image)
    assert (filled == compare).all()


@given(white_image, st.integers(2, 300))
@settings(max_examples = 20, deadline = None)
def test_imfill_stack(to_compare, n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    to_fill = np.array([image for i in range(n_img)])
    compare = 255 * to_compare(image.shape)
    filled = imfill(to_fill)
    assert  ((im == compare).all() for im in filled)



def test_connected_components_wStats() :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = bitwise_not(image)
    n_regions = 4
    retval, labels, stats, centroids = connected_components_wStats(image)
    print(np.unique(labels))
    assert len(np.unique(labels)) == n_regions
    assert len(np.unique(centroids)) == n_regions



@given(st.integers(2,300))
@settings(max_examples = 20, deadline = None )
def test_connected_components_wStats_stack(n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = bitwise_not(image)
    input =np.array([image for i in range(n_img)])
    n_regions = 4
    retval, labels, stats, centroids = connected_components_wStats(input)
    print(np.unique(labels))
    assert len(np.unique(labels)) == n_regions
    assert len(np.unique(centroids)) == n_regions

#test otsu single image
@given(image)
@settings(max_examples = 20, deadline = None)
def test_otsu_threshold(data):
    input = (255 * data(512, 512)).astype(np.uint8)
    out = otsu_threshold(input)
    assert np.all(np.unique(out) == np.array([0, 1]))



#testing otsu threshold
@given(image, st.integers(2, 300))
@settings(max_examples = 20, deadline = None)
def test_otsu_threshold_stack(data, n_imgs):
    input = (255 * data(n_imgs, 512, 512)).astype(np.uint8)
    out = otsu_threshold(input)
    assert np.all(np.unique(out) == np.array([0, 1]))
