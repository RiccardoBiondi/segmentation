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
from CTLungSeg.segmentation import create_lung_mask
from CTLungSeg.segmentation import bit_plane_slices
from CTLungSeg.segmentation import imlabeling
from CTLungSeg.segmentation import kmeans_on_subsamples


import cv2
import numpy as np
import pandas as pd
from CTLungSeg.method import connected_components_wStats
from numpy import ones, zeros
from numpy.random import rand, randint

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


 # Strategies definitions

@st.composite
def rand_stack_strategy(draw, n_imgs = st.integers(10, 30)) :
    """Create a stack of white noise 8-bit images"""
    N = draw(n_imgs)
    return (255 * rand(N, 300, 300)).astype(np.uint8)


@st.composite
def kernel_strategy(draw, k_size = st.integers(3,9)) :
    """Create a random kernel for the morphological operation"""
    k = draw(k_size)
    assume (k % 2) == 0
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
def square_stack_strategy(draw) :
    '''
    Generate a stack of white images with a black square with random side
    '''
    N = draw(st.integers(2, 25))
    L = draw(st.integers(10, 50))
    image = ones((N, 512, 512), dtype=np.uint8)
    image[ : , 100 : 100 + L, 100 : 100 + L ] = zeros((L,L), dtype=np.uint8)
    return image, L

# integer stack strategy
@st.composite
def integer_stack_strategy(draw) :
    '''
    Generates a stack of images with pixel value between 0 and a random integer
    less than 7.
    '''
    gl_max = draw(st.integers(3, 10))
    n_imgs = draw(st.integers(20, 70))
    stack = randint(0, gl_max, (n_imgs, 512, 512))
    return stack.reshape(n_imgs, 512, 512), gl_max


################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################


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


@given(square_stack_strategy(), st.integers(45, 201))
@settings(max_examples = 20, deadline = None)
def test_remove_spots_on_single_square(stack, side):
    '''
    Receive as input a black image with a white square and the maximum spot area,
    assert that:
    - if max area < square area, square is not removed
    - else a black image is returned
    '''
    volume = (stack[0] == 0).astype(np.uint8)
    side_of_square = stack[1]

    filtered = remove_spots(volume, side**2)
    if side < side_of_square :
        assert (filtered == volume).all()
    else :
        assert (filtered == zeros(filtered.shape, dtype = np.uint8)).all()


@given(square_stack_strategy())
@settings(max_examples = 20, deadline = None)
def test_select_largest_connected_regions_3d(img):
    input = np.logical_not(img[0])
    res = select_largest_connected_region_3d(input.astype(np.uint8))
    assert (np.sum(res) == (img[1] ** 2)*img[0].shape[0])


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
    result = bit_plane_slices(stack, (5,7,8), 8)

    assert result.shape == stack.shape
    assert ( np.unique(result) == ground_truth).all()


@given(rand_stack_strategy(), centroids_strategy() )
@settings(max_examples  = 4, deadline=None)
def test_imlabeling(stack, centroids) :
    '''

    '''
    mc = np.stack([stack for i in range(centroids.shape[1])], axis = -1)
    labeled = imlabeling(mc, centroids)
    assert len(np.unique(labeled)) == centroids.shape[0]
    assert labeled.shape == stack.shape

@given(rand_stack_strategy(), centroids_strategy() )
@settings(max_examples  = 4, deadline=None)
def test_imlabeling_wWeigth(stack, centroids) :
    '''
    '''
    w = (stack != 0).astype(np.uint8)
    mc = np.stack([stack for i in range(centroids.shape[1])], axis = -1)
    labeled = imlabeling(mc, centroids, w)

    assert len(np.unique(labeled)) == centroids.shape[0]
    assert labeled.shape == stack.shape



@given(integer_stack_strategy(), st.integers(1, 4),st.integers(1, 5))
@settings(max_examples = 1, deadline = None)
def test_kmeans_on_subsamples(stack, n_features, n_subsamples) :
    '''
    Receive a stack of images with itegers value in [0, max] where max in
    [0, 7].
    Create a multichannel image with a random number of channels and divide
    it in subsamples.
    Apply a kmeans with a number of centroids equal to the number of different
    values.

    assert that:
    - the correct number of centroids is estimated
    - the correct value of centroids is returned
    - the backgrond isn't removed
    '''
    stopping_criteria =  (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                          10, 1.0)
    mc = np.stack([stack[0] for _ in range(n_features) ], axis = -1)
    mc = subsamples(mc, n_subsamples)
    centr = kmeans_on_subsamples(mc,
                                 stack[1],
                                 stopping_criteria,
                                 cv2.KMEANS_RANDOM_CENTERS)

    #true value for each centroid
    gt = np.repeat(np.arange(stack[1]), n_subsamples * n_features, axis = -1)

    assert centr.size == n_subsamples * stack[1] * n_features
    assert np.isclose(np.sort(centr.reshape((-1,))), gt).all()


@given(integer_stack_strategy(), st.integers(2,10))
@settings(max_examples = 1, deadline = None)
def test_kmeans_on_subsamples_wobkg(stack, n_subsamples) :
    '''
    Receive a stack of images with itegers value in [0, max] where max in [0, 7],
    Create a multichannel image with a 2 channel corresponding to the stack, and
    last one contains the mask for the background removal
    Apply a kmeans with a number of centroids equal to the number of different
    values.

    assert that:
    - the correct number of centroids is estimated
    - the correct value of centroids is returned
    - there isn't a centroid corresponding to the background
    '''
    stopping_criteria =  (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                          10, 1.0)
    mc = np.stack([stack[0], stack[0], (stack[0] != 0).astype(np.uint8)],
                    axis = -1)
    mc = subsamples(mc, n_subsamples)
    centr = kmeans_on_subsamples(mc,
                                 stack[1] - 1,
                                 stopping_criteria,
                                 cv2.KMEANS_RANDOM_CENTERS,
                                 True)

    # true value for each centroid
    gt = np.repeat(np.arange(1, stack[1], 1), n_subsamples * 2, axis = -1)

    assert centr.size == n_subsamples * (stack[1] - 1)* 2
    assert np.isclose(np.sort(centr.reshape((-1,))), gt).all()
