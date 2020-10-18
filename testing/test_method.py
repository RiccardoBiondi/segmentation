#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings
from  hypothesis import HealthCheck as HC

from CTLungSeg.method import erode
from CTLungSeg.method import dilate
from CTLungSeg.method import connected_components_wStats
from CTLungSeg.method import imfill
from CTLungSeg.method import median_blur
from CTLungSeg.method import gaussian_blur
from CTLungSeg.method import otsu_threshold
from CTLungSeg.method import connected_components_wVolumes_3d
from CTLungSeg.method import histogram_equalization
from CTLungSeg.method import canny_edge_detection

import cv2
import numpy as np
from numpy import ones, zeros
from numpy.random import rand
from CTLungSeg.utils import load_image

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

# define strategies

#random image stack
@st.composite
def rand_stack_strategy(draw, n_imgs = st.integers(1, 50)) :
    N = draw(n_imgs)
    return (np.abs(255 * np.random.randn(N, 512, 512))).astype(np.uint8)

#square image strategy
@st.composite
def square_image_strategy(draw, side = st.integers(50,200)) :
    L = draw(side)
    square = zeros((512,512), dtype=np.uint8)
    square[100 : 100 + L, 100 : 100 + L ] = ones((L,L), dtype=np.uint8)
    return (square, L)


#square image stack
@st.composite
def square_stack_strategy(draw, side =st.integers(50, 200), n_imgs = st.integers(2, 100)) :
    N = draw(n_imgs)
    L = draw(side)
    image = zeros((L, 512, 512), dtype=np.uint8)
    image[ : , 100 : 100 + L, 100 : 100 + L ] = ones((L,L), dtype=np.uint8)
    return (image,L)

#Kernel strategies
@st.composite
def kernel_strategy(draw, k_size = st.integers(3,9)) :
    k = draw(k_size)
    return ones((k,k), dtype=np.uint8)


#####################################################
###                START TESTS                    ###
#####################################################


@given(square_image_strategy(), kernel_strategy(), st.integers(1,5))
@settings(max_examples = 20, deadline=None)
def test_erode(image, kernel, iterations) :
    eroded = erode(image[0], kernel, iterations)
    assert np.sum(eroded) < image[1]**2


@given(square_stack_strategy(), kernel_strategy(), st.integers(2,5))
@settings(max_examples=20, deadline=None)
def test_erode_stack(image, kernel, iter) :
    res = erode(image[0], kernel, iter)
    assert (np.sum(res) < (image[1]**2)*res.shape[0])


@given(square_image_strategy(), kernel_strategy(), st.integers(1,5))
@settings(max_examples = 20, deadline=None)
def test_dilate(image, kernel, iterations) :
    dilated = dilate(image[0], kernel, iterations)
    assert np.sum(dilated) > image[1]**2


@given(square_stack_strategy(),kernel_strategy(), st.integers(2,5))
@settings(max_examples=20, deadline=None)
def test_dilate_stack(image, kernel, iter) :
    res = dilate(image[0], kernel, iter)
    assert (np.sum(res) > (image[1]**2)*res.shape[0])


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_median_blur (stack) :
    blurred = median_blur(stack.astype(np.float32), 5)
    assert blurred.shape == stack.shape


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_gaussian_blur (stack) :
    blurred = gaussian_blur(stack.astype(np.float32), ksize=(5, 5))
    assert blurred.shape == stack.shape


def test_imfill() :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    ground_truth = 255 * ones(image.shape, dtype=np.uint8)
    filled = imfill(image)
    assert (filled == ground_truth).all()


@given(st.iterables(st.integers(), min_size=2, max_size=200))
@settings(max_examples = 20, deadline = None)
def test_imfill_stack(n_imgs) :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    to_fill = np.array([image for i in n_imgs])
    filled = imfill(to_fill)
    assert (filled == (255 *ones(to_fill.shape))).all()


def test_connected_components_wStats() :
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = np.logical_not(image)
    n_regions = 4
    retval, labels, stats, centroids = connected_components_wStats(image)

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

    assert len(np.unique(labels)) == n_regions
    assert len(np.unique(centroids)) == n_regions


def test_otsu_threshold():
    image = (255 * np.random.rand(512, 512)).astype(np.uint8)
    assert (np.unique(otsu_threshold(image)[1])==np.array([0, 1])).all()


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_otsu_threshold_stack(stack):
    assert np.all(np.unique(otsu_threshold(stack)[1])==np.array([0, 1]))


@given(square_image_strategy())
@settings(max_examples=2, deadline=None, suppress_health_check=(HC.too_slow,))
def test_connected_components_wVolumes_3d(image) :
    res = connected_components_wVolumes_3d(image[0])
    assert (np.unique(res[0]) == [0,1]).all()
    assert (res[1][1] == image[1] ** 2)


@given(rand_stack_strategy(), st.integers(2, 6), st.integers(8, 12))
@settings(max_examples=20, deadline=None, suppress_health_check=(HC.too_slow,))
def test_histogram_equalization(volume, clip, size ) :
    equalized = histogram_equalization(volume, clip, (size, size))
    assert np.std(equalized) > np.std(volume)


@given(rand_stack_strategy())
@settings(max_examples=20, deadline=None, suppress_health_check=(HC.too_slow,))
def test_canny_edge_detection(stack) :
    edge_map = canny_edge_detection(stack)

    assert (np.unique(edge_map) == (0, 255)).all()
    assert edge_map.shape == stack.shape
