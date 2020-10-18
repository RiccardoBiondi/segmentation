#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, assume
from  hypothesis import HealthCheck as HC

from CTLungSeg.utils import subsamples

from CTLungSeg.segmentation import opening
from CTLungSeg.segmentation import closing
from CTLungSeg.segmentation import remove_spots
from CTLungSeg.segmentation import select_largest_connected_region_3d
from CTLungSeg.segmentation import find_ROI
from CTLungSeg.segmentation import create_lung_mask
from CTLungSeg.segmentation import bit_plane_slices
from CTLungSeg.segmentation import imlabeling
from CTLungSeg.segmentation import kmeans_on_subsamples


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
def rand_stack_strategy(draw, n_imgs = st.integers(10, 30)) :
    """Create a stack of white noise 8-bit images"""
    N = draw(n_imgs)
    return (255 * np.random.rand(N, 300, 300)).astype(np.uint8)


@st.composite
def kernel_strategy(draw, k_size = st.integers(3,9)) :
    """Create a random kernel for the morphological operation"""
    k = draw(k_size)
    return ones((k,k), dtype=np.uint8)

@st.composite
def centroids_strategy(draw) :
    n_centr = draw(st.integers(2, 6))
    n_features = draw(st.integers(1, 6))
    centroids = np.asarray([draw(st.integers(0, 255))] * (n_centr * n_features))
    assume(len(np.unique(centroids) > 4 ))

    return centroids.reshape(n_centr, n_features)

#square image strategy
@st.composite
def square_stack_strategy(draw, side =st.integers(50, 200), n_imgs = st.integers(2, 100)) :
    N = draw(n_imgs)
    L = draw(side)
    image = ones((L, 512, 512), dtype=np.uint8)
    image[ : , 100 : 100 + L, 100 : 100 + L ] = zeros((L,L), dtype=np.uint8)
    return (image,L)


#####################################################
###                TESTING                        ###
#####################################################


@given(square_stack_strategy(), kernel_strategy())
@settings(max_examples = 20, deadline = None)
def test_opening(img, kernel) :
    opened = opening(img[0], kernel )
    square_area = opened.size - np.sum(opened)
    assert (square_area >= (img[1] ** 2)*opened.shape[0])


@given(square_stack_strategy(), kernel_strategy())
@settings(max_examples = 20, deadline = None)
def test_closing(img, kernel) :
    closed = closing(img[0], kernel)
    square_area = closed.size - np.sum(closed)
    assert (square_area <= (img[1]**2)*closed.shape[0])

#@given()
#@settings()
#def test_remove_spots(stack, area)


@given(square_stack_strategy())
@settings(max_examples = 20, deadline = None)
def test_select_largest_connected_regions_3d(img):
    input = np.logical_not(img[0])
    res = select_largest_connected_region_3d(input.astype(np.uint8))
    assert (np.sum(res) == (img[1] ** 2)*img[0].shape[0])


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


@given(rand_stack_strategy(), st.integers(100, 200))
@settings(max_examples=15, deadline=None, suppress_health_check=(HC.too_slow,))
def test_create_lung_mask(volume, threshold) :
    mask = create_lung_mask(volume, threshold)
    masked = volume * mask
    assert ((np.unique(mask.astype(np.uint8))) == [0, 1]).all
    assert masked.max() < (threshold + 1)


@given(rand_stack_strategy())
@settings(max_examples = 2, deadline = None, suppress_health_check=(HC.too_slow,))
def test_bit_plane_slices(stack) :
    ground_truth = [0, 16, 64, 80, 128, 144, 192, 208]
    result = bit_plane_slices(stack, (5,7,8))

    assert result.shape == stack.shape
    assert ( np.unique(result) == ground_truth).all()


@given(rand_stack_strategy(), centroids_strategy() )
@settings(max_examples  = 4, deadline=None)
def test_imlabeling(stack, centroids) :
    mc = np.stack([stack for i in range(centroids.shape[1])], axis = -1)
    labeled = imlabeling(mc, centroids)
    assert len(np.unique(labeled)) == centroids.shape[0]
    assert labeled.shape == stack.shape


@given(rand_stack_strategy(),st.integers(2, 3),st.integers(2,3),st.integers(1,3))
@settings(max_examples = 4, deadline = None)
def test_kmeans_on_subsamples(stack, n_centroids, n_subsamples, n_features) :
    stopping_criteria =  (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                          10, 1.0)
    mc = np.stack([stack for i in range(n_features)], axis = -1)
    mc = subsamples(mc, n_subsamples)
    centr = kmeans_on_subsamples(mc,
                                 n_centroids,
                                 stopping_criteria,
                                 cv2.KMEANS_RANDOM_CENTERS)

    assert centr.size == (n_subsamples * n_centroids * n_features)

'''
@given(rand_stack_strategy(),st.integers(2, 3),st.integers(2,3),st.integers(1,3))
@settings(max_examples = 4, deadline = None)
def test_kmeans_on_subsamples_wobkg(stack, n_centroids, n_subsamples, n_features) :
    stopping_criteria =  (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                          10, 1.0)
    mc = np.stack([stack for i in range(n_features)], axis = -1)
    mc = np.stack([mc, (stack > 100).astype(np.uint8)], axis = -11)
    mc = subsamples(mc, n_subsamples)
    centr = kmeans_on_subsamples(mc,
                                 n_centroids,
                                 stopping_criteria,
                                 cv2.KMEANS_RANDOM_CENTERS,
                                 True)

    assert centr.size == (n_subsamples * n_centroids * n_features)
    assert (np.unique(centr) > 100).all()
'''
