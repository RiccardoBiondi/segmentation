#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example

from CTLungSeg.method import erode
from CTLungSeg.method import dilate
from CTLungSeg.method import connected_components_wStats
from CTLungSeg.method import imfill
from CTLungSeg.method import median_blur
from CTLungSeg.method import gaussian_blur
from CTLungSeg.method import otsu_threshold
from CTLungSeg.method import gl2bit
from CTLungSeg.method import get_bit

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


@given(image, kernel, st.integers(2, 300),st.integers(5,30), st.integers(1, 5))
@settings(max_examples = 20, deadline = None)
def test_erode_stack(data, kernel, n_imgs, k_dim,iter):
    eroded = erode(data(n_imgs, 300, 300), kernel((k_dim, k_dim)),iter )
    assert eroded.shape == (n_imgs,300, 300)


@given(image, kernel, st.integers(5,30), st.integers(1,5))
@settings(max_examples = 20, deadline = None)
def test_erode(data, kernel, k_dim, iter):
    eroded = erode(data(300, 300), kernel((k_dim, k_dim)), iter)
    assert eroded.shape == (300, 300)


@given(image, kernel, st.integers(2,300), st.integers(5,30), st.integers(1,5))
@settings(max_examples = 20, deadline = None)
def test_dilate_stack(data, kernel, n_img, k_dim, iter):
    dilated = dilate(data(n_img, 300, 300), kernel((k_dim, k_dim)), iter)
    assert dilated.shape == (n_img, 300, 300)


@given(image, kernel, st.integers(3,11), st.integers(1,5))
@settings(max_examples = 3, deadline = None)
def test_dilate(data, kernel,k_dim, iter):
    dilated = dilate(data(300, 300), kernel((k_dim, k_dim)), iter)
    assert dilated.shape == (300, 300)


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
def test_imfill_stack(white_image, n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    to_fill = np.array([image for i in range(n_img)])
    compare = 255 * white_image(to_fill.shape)
    filled = imfill(to_fill)
    assert (filled == compare).all()


def test_connected_components_wStats() :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = np.logical_not(image)
    n_regions = 4
    retval, labels, stats, centroids = connected_components_wStats(image)
    print(np.unique(labels))
    assert len(np.unique(labels)) == n_regions
    assert len(np.unique(centroids)) == n_regions


@given(st.integers(2,300))
@settings(max_examples = 20, deadline = None )
def test_connected_components_wStats_stack(n_img) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = np.logical_not(image)
    input =np.array([image for i in range(n_img)])
    n_regions = 4
    retval, labels, stats, centroids = connected_components_wStats(input)
    print(np.unique(labels))
    assert len(np.unique(labels)) == n_regions
    assert len(np.unique(centroids)) == n_regions


@given(image)
@settings(max_examples = 20, deadline = None)
def test_otsu_threshold(data):
    input = (255 * data(512, 512)).astype(np.uint8)
    out = otsu_threshold(input)
    assert np.all(np.unique(out) == np.array([0, 1]))


@given(image, st.integers(2, 300))
@settings(max_examples = 20, deadline = None)
def test_otsu_threshold_stack(data, n_imgs):
    input = (255 * data(n_imgs, 512, 512)).astype(np.uint8)
    out = otsu_threshold(input)
    assert np.all(np.unique(out) == np.array([0, 1]))


@given(st.integers(1,30))
@settings(max_examples = 20, deadline = None)
def test_gl2bit(n_imgs) :
    input = np.ones((n_imgs, 100, 100), dtype = np.uint8)
    result = gl2bit(input, 8)
    assert np.unique(result) == ["00000001"]


@given(image, st.integers(1,30), st.integers(1,8))
@settings(max_examples = 20, deadline = None)
def test_get_bit(data, n_imgs, bit_number) :
    input = (255 * data(n_imgs, 100, 100)).astype(np.uint8)
    input = gl2bit(input, 8)
    result = get_bit(input, bit_number)
    assert (np.unique(result) == [0, 2**(bit_number -1)]).all()
