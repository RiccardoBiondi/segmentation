#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, assume
from  hypothesis import HealthCheck as HC

from CTLungSeg.segmentation import opening
from CTLungSeg.segmentation import closing
from CTLungSeg.segmentation import select_greater_connected_regions
from CTLungSeg.segmentation import find_ROI
from CTLungSeg.segmentation import bit_plane_slices
from CTLungSeg.segmentation import imlabeling


import cv2
import numpy as np
import pandas as pd
from CTLungSeg.method import connected_components_wStats
from numpy import ones, zeros
from numpy.random import rand

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


 # Strategies definitions

@st.composite
def rand_stack_strategy(draw, n_imgs = st.integers(1, 20)) :
    """Create a stack of white noise 8-bit images"""
    N = draw(n_imgs)
    return (255 * np.random.rand(N, 300, 300)).astype(np.uint8)


@st.composite
def kernel_strategy(draw, k_size = st.integers(3,9)) :
    """Create a random kernel for the morphological operation"""
    k = draw(k_size)
    return ones((k,k), dtype=np.uint8)

@st.composite
def centroids_strategy(draw, centroid = st.integers(0, 255)) :
    a = draw(centroid)
    b = draw(centroid)
    c = draw(centroid)
    d = draw(centroid)
    assume(a < b)
    assume(b < c)
    assume(c < d)
    return np.array([a, b, c, d], dtype=np.uint8)

#square image strategy
@st.composite
def square_image_strategy(draw, side = st.integers(50,200)) :
    L = draw(side)
    square = ones((512,512), dtype=np.uint8)
    square[100 : 100 + L, 100 : 100 + L ] = zeros((L,L), dtype=np.uint8)
    return (square, L)


#####################################################
###                START TESTS                    ###
#####################################################


@given(square_image_strategy(), kernel_strategy())
@settings(max_examples = 20, deadline = None)
def test_opening(img, kernel) :
    opened = opening(img[0], kernel )
    square_area = opened.size - np.sum(opened)
    assert (square_area >= img[1] ** 2)


@given(square_image_strategy(), kernel_strategy())
@settings(max_examples = 20, deadline = None)
def test_closing(img, kernel) :
    closed = closing(img[0], kernel)
    square_area = closed.size - np.sum(closed)
    assert square_area <= img[1]**2


@given(st.integers(2, 300), st.integers(0,3))
@settings(max_examples = 20, deadline = None)
def test_select_greater_connected_regions(n_imgs, n_reg):
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = np.logical_not(image)
    image =np.array([image for i in range(n_imgs)])
    res = select_greater_connected_regions(image, n_reg)
    _, labeled, _, _ = connected_components_wStats(res)
    assert np.unique(labeled).shape == (n_reg + 1,)


#def test_reconstruct_gg_areas(imgs):


@given(st.integers(1,200), st.integers(1,200), st.integers(1,200), st.integers(1,200))
@settings(max_examples = 200, deadline = None)
def test_find_ROI(x, y, w, h) :
    image = np.zeros((512, 512), dtype=np.uint8)
    corners = [x, y, x + w, y + h]
    columns = ['TOP', 'LEFT', 'WIDTH', 'HEIGHT', 'AREA']

    image[y : y + h, x : x + w] = np.ones((h, w), dtype=np.uint8)
    _, _, stats, _ = connected_components_wStats(image)
    assert (find_ROI(pd.DataFrame(stats, columns=columns)) == corners).all


@given(rand_stack_strategy())
@settings(max_examples = 2, deadline = None, suppress_health_check=(HC.too_slow,))
def test_bit_plane_slices(stack) :
    ground_truth = [0, 16, 64, 80, 128, 144, 192, 208]
    result = bit_plane_slices(stack, (5,7,8))

    assert result.shape == stack.shape
    assert ( np.unique(result) == ground_truth).all()


@given(rand_stack_strategy(), centroids_strategy() )
@settings(max_examples  =20, deadline=None)
def test_imlabeling(stack, centroids) :
    labeled = imlabeling(stack, centroids.reshape(4,1))

    assert (np.unique(labeled) == [0, 1, 2, 3]).all()
    assert labeled.shape == stack.shape
