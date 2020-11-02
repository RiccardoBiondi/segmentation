#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import logging
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
from skimage.util import random_noise


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


# define strategies

#random image stack
@st.composite
def rand_stack_strategy(draw, n_imgs = st.integers(1, 50)) :
    '''
    Generate a stack of n_imgs 512x512 with pixel values normal distributed in
    range [0, 255]
    '''
    N = draw(n_imgs)
    return (np.abs(255 * np.random.randn(N, 512, 512))).astype(np.uint8)

@st.composite
def rand_image_strategy(draw) :
    '''
    Generate a stack of n_imgs 512x512 with pixel values normal distributed in
    range [0, 255]
    '''

    return (255 * np.random.randn(512, 512)).astype(np.uint8)


@st.composite
def square_image_strategy(draw, side = st.integers(50,200)) :
    '''
    Generate a binary image with 0 values on the background and a square of
    random areas with pixel value 1
    '''
    L = draw(side)
    square = zeros((512,512), dtype=np.uint8)
    square[100 : 100 + L, 100 : 100 + L ] = ones((L,L), dtype=np.uint8)
    return (square, L)

#Kernel strategies
@st.composite
def kernel_strategy(draw, k_size = st.integers(3,9)) :
    '''
    return a matrix of ones with random size
    '''
    k = draw(k_size)
    return ones((k,k), dtype=np.uint8)

@st.composite
def median_noise_strategy(draw) :
    '''
    Generates a black image with salt and pepper noise
    '''
    img = zeros((512, 512), dtype=np.uint8)
    image = random_noise(img, mode='s&p', salt_vs_pepper = .15)
    return image


################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################


@given(square_image_strategy(),
        kernel_strategy(),
        st.integers(2,5),
        st.integers(1, 50))
@settings(max_examples=20, deadline=None)
def test_erode_square(image, kernel, iter, n_imgs) :
    '''
    Given an balck image with a white square inside, assert that:

    - the square area after the erosion is less than before
    - the parallepiped volume after the erosion is less than before(stack case)
    '''
    stack = np.asarray([image[0] for _ in range(n_imgs)])
    eroded_image = erode(image[0], kernel, iter)
    eroded_stack = erode(stack, kernel, iter)

    assert np.sum(eroded_image) < np.sum(image[0])
    assert np.sum(eroded_stack) < np.sum(stack)


@given(median_noise_strategy(), st.integers(10, 50), kernel_strategy())
@settings(max_examples=20, deadline=None)
def test_erode_on_sp_image(image, n_imgs, kernel) :
    '''
    Given as inpup a black image with salt and pepper noise, assert that:
    - the eroded image is a uniform black image for small amount of salt
    '''
    stack = np.asarray([image for _ in range(n_imgs)])
    eroded_image = erode(image, kernel)
    eroded_stack = erode(stack, kernel)

    assert (eroded_image == zeros((512, 512), dtype = np.uint8)).all()
    assert (eroded_stack == zeros(stack.shape, dtype = np.uint8)).all()


@given(square_image_strategy(),
        kernel_strategy(),
        st.integers(2,5),
        st.integers(1, 50))
@settings(max_examples=20, deadline=None)
def test_dilate_square(image, kernel, iter, n_imgs) :
    '''
    Given an balck image with a white square inside, assert that:

    - the square area after the dilation is higher than before
    - the parallepiped volume after the dilate is higher than before(stack case)
    '''
    stack = np.asarray([image[0] for _ in range(n_imgs)])
    dilated_image = dilate(image[0], kernel, iter)
    dilated_stack = dilate(stack, kernel, iter)

    assert np.sum(dilated_image) > np.sum(image[0])
    assert np.sum(dilated_stack) > np.sum(stack)


@given(median_noise_strategy(), st.integers(10, 50), kernel_strategy())
@settings(max_examples=20, deadline=None)
def test_dilated_on_sp_image(image, n_imgs, kernel) :
    '''
    Given as inpup a black image with salt and pepper noise, assert that:
    - the dilated image has an higher amount of salt
    '''
    stack = np.asarray([image for _ in range(n_imgs)])
    dilated_image = dilate(image, kernel)
    dilated_stack = dilate(stack, kernel)

    assert np.sum(dilated_image) > np.sum(image)
    assert np.sum(dilated_stack) > np.sum(stack)


@given(median_noise_strategy(), st.integers(10, 50), st.integers(0, 13))
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_median_blur (noisy_image, n_imgs, ksize) :
    '''
    Test the median blur with an random kernel size black image and stack of image
    with a salt and pepper noise with small amount of salt.
    The image is blurred,  the test veriphy that :

    - Uniform image is returned
    - Uniform stak of images is returned
    - shape is preserved
    - if kernel isn't odd and greater than one a ValueError is raised
    '''
    stack = np.asarray([noisy_image for _ in range(n_imgs)])
    if ksize % 2 == 0 or ksize <= 1 :
        with pytest.raises(ValueError) :
            assert median_blur(noisy_image.astype(np.uint8), ksize)
            assert median_blur(stack.astype(np.uint8), ksize)
    else :
        blurred_image = median_blur(noisy_image.astype(np.uint8), ksize)
        blurred_stack = median_blur(stack.astype(np.uint8), ksize)

        assert blurred_image.shape == (512, 512)
        assert blurred_stack.shape == (n_imgs, 512, 512)

        assert (blurred_image == zeros((512, 512))).all()
        assert (blurred_stack == zeros((n_imgs, 512, 512))).all()


@given(rand_image_strategy(), st.integers(10 ,50), st.integers(3, 14))
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_gaussian_blur (image, n_imgs, size) :
    '''
    Takes an input an 8-bit image with random distributed pixels, after the
    application of the gaussian blur will assert that :

    - shape is preserved
    - image std is decreased
    - if wrong ksize a ValueError is rised
    '''
    if size % 2 == 0 :
        with pytest.raises(ValueError) :
            assert gaussian_blur(image, (size, size))
    else :
        stack = np.asarray([image for _ in range(n_imgs)])
        blurred_image = gaussian_blur(image, ksize = (size, size))
        blurred_stack = gaussian_blur(stack, ksize = (size, size))

        assert blurred_image.shape == (512, 512)
        assert blurred_stack.shape == (n_imgs, 512, 512)

        assert np.std(blurred_image) < np.std(image)
        assert np.std(blurred_stack) < np.std(stack)


@given(st.integers(20, 30))
@settings(max_examples = 20, deadline = None)
def test_imfill(n_imgs) :
    '''
    Given as input a white image with different black spots, assert that :
    - the output image is white
    - the output stack is white

    - the shape is preserved
    '''
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    # ensure that the input image is binary
    image = (image != 0).astype(np.uint8)
    stack = np.asarray([image for _ in range(n_imgs)])
    filled_image = imfill(image)
    filled_stack = imfill(stack)

    assert (filled_image == 255 * ones((512, 512), dtype = np.uint8)).all()
    assert (filled_stack == 255 * ones(filled_stack.shape, dtype = np.uint8)).all()

    assert filled_image.shape == (512, 512)
    assert filled_stack.shape == stack.shape


@given(square_image_strategy(), st.integers(10, 200))
@settings(max_examples = 20, deadline = None)
def test_imfill_square(image, n_imgs) :
    '''
    Given a white image with a blck square, apply imfill, assert that :
    - the resulting image is white
    - the shape is preserved
    '''
    # invert the provided image -> from black with a whirte square to white with
    #black square
    image = (image[0] == 0).astype(np.uint8)

    stack = np.array([image for _ in range(n_imgs)])
    filled_image = imfill(image)
    filled_stack = imfill(stack)

    assert (filled_image == 255 * ones((512, 512), dtype = np.uint8)).all()
    assert (filled_stack == 255 * ones(filled_stack.shape, dtype = np.uint8)).all()

    assert filled_image.shape == (512, 512)
    assert filled_stack.shape == stack.shape


@given(st.integers(10, 100))
@settings(max_examples = 20, deadline = None)
def test_connected_components_wStats(n_imgs) :
    '''
    Given an image(and a stack) with 4 connected regions, assert that
    - the correct number of different components is detected
    '''
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = np.logical_not(image)
    stack = np.array([image for _ in range(n_imgs)])
    n_regions = 4
    retval, labels, stats, centroids = connected_components_wStats(image)
    retval_s, labels_s, stats_s, centroids_s = connected_components_wStats(stack)

    assert len(np.unique(labels)) == n_regions
    assert len(np.unique(centroids)) == n_regions
    assert len(np.unique(labels_s)) == n_regions
    assert len(np.unique(centroids_s)) == n_regions


@given(square_image_strategy(), st.integers(2, 5))
@settings(max_examples = 20, deadline = None)
def test_connected_components_wStats_centr_pos(image, n_imgs) :
    '''
    given an image with a white square, assert that:

    - the position of the centroids is correct
    '''
    stack = np.array([image[0] for _ in range(n_imgs)])
    connected_image = connected_components_wStats(image[0])
    connected_stack = connected_components_wStats(stack)

    gt = [(199 + image[1]) / 2, (199 + image[1]) / 2] # truth centroid position

    assert  (connected_image[3][1] == gt).all()
    for i in range(n_imgs) :
        assert (connected_stack[3][i][1] == gt).all()


@given(rand_image_strategy(), st.integers(2, 10))
@settings(max_examples = 20, deadline = None)
def test_otsu_threshold(image, n_imgs):
    '''
    given a stack of random 8-bit gl images, compute the otsu threshold,
    assert that:
    - the returned image is binary
    - the returned stack is binary
    - the minimum non zero value of the iamge convolved with the binary image
      created, is higher than the estimated threshold
    '''
    stack = np.array([image for _ in range(n_imgs)])

    tval_img, thr_image = otsu_threshold(image)
    tval_stack, thr_stack = otsu_threshold(stack)

    conv_image = thr_image * image
    conv_stack = thr_stack * stack

    assert (np.unique(thr_image) == [0, 1]).all()
    assert (np.unique(thr_stack) == [0, 1]).all()

    assert np.unique(conv_image)[1] > tval_img
    assert np.unique(conv_stack)[1] > tval_stack.min()


@given(square_image_strategy())
@settings(max_examples=2, deadline=None, suppress_health_check=(HC.too_slow,))
def test_connected_components_wVolumes_3d(image) :
    '''
    Given a stack of images with awhite square, assert that the area of the
    identified component is correct.
    '''
    res = connected_components_wVolumes_3d(image[0])
    assert (np.unique(res[0]) == [0,1]).all()
    assert (res[1][1] == image[1] ** 2)


@given(rand_stack_strategy(), st.integers(2, 6), st.integers(8, 12))
@settings(max_examples=20, deadline=None, suppress_health_check=(HC.too_slow,))
def test_histogram_equalization(volume, clip, size ) :
    '''
    Given a stack of random images, assert that:
    - the standard  deivation of the equalized image is higher than the original
        one
    '''
    image = volume[0]
    equalized_stack = histogram_equalization(volume, clip, (size, size))
    equalized_image = histogram_equalization(image, clip, (size, size))


    assert np.std(equalized_stack) > np.std(volume)
    assert np.std(equalized_image) > np.std(image)


@given(rand_stack_strategy())
@settings(max_examples=20, deadline=None, suppress_health_check=(HC.too_slow,))
def test_canny_edge_detection(stack) :
    '''
    Given as input a random stack strategy, assert that :
    - Return a binary image
    - the shape is preserved
    '''
    image = stack[0]
    edge_map_image = canny_edge_detection(image)
    edge_map_stack = canny_edge_detection(stack)

    assert (np.unique(edge_map_stack) == (0, 255)).all()
    assert edge_map_stack.shape == stack.shape

    assert (np.unique(edge_map_image) == (0, 255)).all()
    assert edge_map_image.shape == image.shape


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_raise_error(stack) :
    '''
    Assert that an error is raised ifwe pass as input an image or stack of
    of images of the wrong type
    '''
    image =  stack[0].astype(np.float32)
    stack = stack.astype(np.float32)
    with pytest.raises(Exception) :

        assert median_blur(image, 11)
        assert median_blur(stack, 11)
        assert otsu_threshold(image)
        assert otsu_threshold(stack)
        assert histogram_equalization(image)
        assert histogram_equalization(stack)
        assert test_canny_edge_detection(image)
        assert canny_edge_detection(stack)


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_warnings(stack) :
    '''
    Given as input an argument that will raise warinings:
    assert that all functions raise warnings
    '''
    with pytest.warns(None):
        connected_components_wStats(stack)
        imfill(stack)
        connected_components_wVolumes_3d(stack)
