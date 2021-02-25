#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, assume
from  hypothesis import HealthCheck as HC

from CTLungSeg.utils import shuffle_and_split

from CTLungSeg.segmentation import imlabeling
from CTLungSeg.segmentation import kmeans_on_subsamples

import cv2
import numpy as np
from numpy import ones
from numpy.random import randint

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

################################################################################
##                          Define Test strategies                            ##
################################################################################
@st.composite
def integer_stack_strategy(draw) :
    '''
    Generates a stack o N 512x512 images with Gl between [0, 7]
    '''
    gl_max = draw(st.integers(3, 10))
    n_imgs = draw(st.integers(20, 70))
    stack = randint(0, gl_max, (n_imgs, 512, 512), dtype = np.uint8)
    return stack.reshape(n_imgs, 512, 512), gl_max

################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################



@given(integer_stack_strategy(), st.integers(1, 6))
@settings(max_examples  = 4, deadline=None)
def test_imlabeling(stack, channels) :
    '''
    Given :
        - image tensor with GL in [0, 7]
        - number of channels
    So :
        - build the mulcti channel image
        - build the centroids vector(1 value for each GL)
    Assert:
        - each voxel is assigned to the correct cluster
    '''
    mc = np.stack([stack[0] for i in range(channels)], axis = -1)
    centroids = np.stack([np.arange(stack[1]) for _ in range(channels)],axis=-1)

    labeled = imlabeling(mc, centroids)

    assert (labeled == stack[0]).all()



@given(integer_stack_strategy(), st.integers(1, 4))
@settings(max_examples  = 4, deadline=None)
def test_imlabeling_wWeigth(stack, channels) :
    '''
    Given :
        - image tensor with GL in [0, 7]
        - number of channels
    So :
        - build the mulcti channel image
        - build the weight tensor
        - build the centroids vector(1 value for each GL except 0)
    Assert:
        - each voxel is assigned to the correct cluster
    '''
    #build the ground truth reference
    gt = stack[0]
    gt[gt != 0] = gt[gt != 0] - 1

    w = (stack[0] != 0).astype(np.uint8)
    mc = np.stack([stack[0] for i in range(channels)], axis = -1)
    centroids = np.stack([np.arange(stack[1]) for _ in range(channels)],axis=-1)

    labeled = imlabeling(mc, centroids, w)

    assert (labeled == gt).astype(np.uint8).all()



@given(integer_stack_strategy(), st.integers(100, 200))
@settings(max_examples  = 4, deadline=None)
def test_imlabeling_raise_weight_exception(stack, dim) :
    '''
    Given :
        - image tensor
        - weight tensor with shape != image tensor shape
    Assert :
        - Exception is raised
    '''
    mc = np.stack(stack for _ in range(3))
    centroids = ones((5, 3), dtype = np.uint8)
    weight = ones((dim, dim, dim), dtype = np.uint8)
    with pytest.raises(Exception) as exc:
        labels  =  imlabeling(mc, centroids, weight )
        assert exc == 'Weight shape doesn t match image one : {} != {}\
                            '.format( weight.shape, mc.shape[:-1])


@given(integer_stack_strategy())
@settings(max_examples  = 4, deadline=None)
def test_imlabeling_raise_centroids_exception(stack) :
    '''
    Given :
        - multi channel image tensor
        - centroid with wron dimension
    Assert :
        - Exception is raise
    '''
    mc = np.stack(stack for _ in range(3))
    centroids = ones((5, 4), dtype = np.uint8)

    with pytest.raises(Exception) :
        assert imlabeling(mc, centroids)


@given(integer_stack_strategy(), st.integers(1, 4),st.integers(1, 5))
@settings(max_examples = 1, deadline = None)
def test_kmeans_on_subsamples(stack, n_features, n_subsamples) :
    '''
    Given :
        - image tensor with GL in [0, 7]
        - number of image channel
        - number of subsamoles
    So :
        - Create a multichannel image
        - Divide it into subsamples
        - Perform kmenas of subsamples with number fo centroids equal to numebr
            different GL
    Assert :
        - the correct number of centroids is estimated
        - the correct value of centroids is returned
        - the backgrond isn't removed
    '''
    stopping_criteria =  (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                          10, 1.0)
    mc = np.stack([stack[0] for _ in range(n_features) ], axis = -1)
    mc = shuffle_and_split(mc, n_subsamples)
    _, centr = kmeans_on_subsamples(mc,
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
        Given :
            - image tensor with GL in [0, 7]
            - number of subsamoles
        So :
            - Create a multichannel image with background removal
            - Divide it into subsamples
            - Perform kmenas of subsamples with number fo centroids equal to numebr
                different GL(except 0)
        Assert :
            - the correct number of centroids is estimated
            - the correct value of centroids is returned
            - the backgrond is removed

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
    mc = shuffle_and_split(mc, n_subsamples)
    _, centr = kmeans_on_subsamples(mc,
                                 stack[1] - 1,
                                 stopping_criteria,
                                 cv2.KMEANS_RANDOM_CENTERS,
                                 True)

    # true value for each centroid
    gt = np.repeat(np.arange(1, stack[1], 1), n_subsamples * 2, axis = -1)

    assert centr.size == n_subsamples * (stack[1] - 1)* 2
    assert np.isclose(np.sort(centr.reshape((-1,))), gt).all()
