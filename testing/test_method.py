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
from CTLungSeg.method import adjust_gamma

import cv2
import numpy as np
from numpy import ones, zeros
from numpy.random import rand, choice



__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

################################################################################
##                          Define Test strategies                            ##
################################################################################

@st.composite
def rand_stack_strategy(draw) :
    '''
    Generate a stack of n_imgs 512x512 with pixel values normal distributed in
    range [0, 255]
    '''
    N = draw(st.integers(1, 50))
    return (np.abs(255 * np.random.randn(N, 512, 512))).astype(np.uint8)

@st.composite
def rand_image_strategy(draw) :
    '''
    Generate a stack of n_imgs 512x512 with pixel values normal distributed in
    range [0, 255]
    '''
    return (255 * np.random.randn(512, 512)).astype(np.uint8)


@st.composite
def square_image_strategy(draw) :
    '''
    Generate a stack of binary image with 0 values on the background and a
    square of random areas with pixel value 1
    '''
    L = draw(st.integers(50,200))
    N = draw(st.integers(1, 100))
    square = zeros((N, 512,512), dtype=np.uint8)
    square[: ,100 : 100 + L, 100 : 100 + L ] = ones((L,L), dtype=np.uint8)
    return square

#Kernel strategies
@st.composite
def kernel_strategy(draw) :
    '''
    return a matrix of ones with random size
    '''
    k = draw(st.integers(3,9))
    return ones((k,k), dtype=np.uint8)

@st.composite
def median_noise_strategy(draw) :
    '''
    Generates a black image with salt and pepper noise
    '''

    N = draw(st.integers(1, 20))
    image = choice([0, 1], (N, 512, 512),p = [.995, .005])

    return image.astype(np.uint8)


################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################


@given(square_image_strategy(),
        kernel_strategy(),
        st.integers(2,5))
@settings(max_examples = 20, deadline = None)
def test_erode_square(stack, kernel, iter) :
    '''
    Given :
         - black image with a white square
         - kernel
         - number of iterations
    So :
        - apply an erosion
    Assert :
        - the area of the square is diminshed(image case)
        - the volume of the parallepiped is diminshed(stack case)
    '''
    image = stack[0]
    eroded_image = erode(image, kernel, iter)
    eroded_stack = erode(stack, kernel, iter)

    assert np.sum(eroded_image) < np.sum(image)
    assert np.sum(eroded_stack) < np.sum(stack)


@given(median_noise_strategy(), st.integers(10, 50), kernel_strategy())
@settings(max_examples = 20,
        deadline = None,
        suppress_health_check = (HC.too_slow,))
def test_erode_on_sp_image(stack, iter, kernel) :
    '''
    Given :
        - input stack of salt and pepper image
        - numeber of iterations
        - kernel
    So :
        - apply erosion
    Assert :
        - the eroded image is a uniform black image for small amount of salt

    '''
    image = stack[0]
    eroded_image = erode(image, kernel, iter)
    eroded_stack = erode(stack, kernel, iter)

    assert (eroded_image == zeros((512, 512), dtype = np.uint8)).all()
    assert (eroded_stack == zeros(stack.shape, dtype = np.uint8)).all()


@given(square_image_strategy(),
        kernel_strategy(),
        st.integers(2,5))
@settings(max_examples = 20, deadline = None)
def test_dilate_square(stack, kernel, iter) :
    '''
        Given :
             - black image with a white square
             - kernel
             - number of iterations
        So :
            - apply dilation
        Assert :
            - the area of the square is increased(image case)
            - the volume of the parallepiped is increased(stack case)
    '''
    image = stack[0]
    dilated_image = dilate(image, kernel, iter)
    dilated_stack = dilate(stack, kernel, iter)

    assert np.sum(dilated_image) > np.sum(image)
    assert np.sum(dilated_stack) > np.sum(stack)


@given(median_noise_strategy(), st.integers(10, 50), kernel_strategy())
@settings(max_examples = 20, deadline = None)
def test_dilated_on_sp_image(stack, iter, kernel) :
    '''
        Given :
            - input stack of salt and pepper image
            - numeber of iterations
            - kernel
        So :
            - apply dilation
        Assert :
            - the areas of salt is insreased (image)
            - the volume of salt is increased (stack)
    '''
    image = stack[0]
    dilated_image = dilate(image, kernel, iter)
    dilated_stack = dilate(stack, kernel, iter)

    assert np.sum(dilated_image) > np.sum(image)
    assert np.sum(dilated_stack) > np.sum(stack)


@given(median_noise_strategy(), st.integers(0, 13))
@settings(max_examples = 20,
        deadline = None,
        suppress_health_check = (HC.too_slow,))
def test_median_blur (stack, ksize) :
    '''
    Given :
        - image tensor of salt and pepper
        - kernel size
    So :
        - apply median blurring
    Assert that :
        - value error is raised if ksize is not odd
        - shape is preserved
        - return a stack of uniform image
    '''
    image = stack[0]
    if ksize % 2 == 0 or ksize <= 1 :
        with pytest.raises(ValueError) :
            assert median_blur(image.astype(np.uint8), ksize)
            assert median_blur(stack.astype(np.uint8), ksize)
    else :
        blurred_image = median_blur(image.astype(np.uint8), ksize)
        blurred_stack = median_blur(stack.astype(np.uint8), ksize)

        assert blurred_image.shape == (512, 512)
        assert blurred_stack.shape == stack.shape

        assert (blurred_image == zeros((512, 512))).all()
        assert (blurred_stack == zeros(stack.shape)).all()


@given(rand_stack_strategy(), st.integers(3, 14))
@settings(max_examples = 20,
        deadline = None,
        suppress_health_check = (HC.too_slow,))
def test_gaussian_blur (stack, size, ) :
    '''
    Given :
        - image tensor
        - kernel size
    So :
        - apply a gaussian blurring
    Assert :
        - shape is presrved
        - stack std is lower
        - if ksize is not odd a value error is raised

    '''
    image = stack[0]
    if size % 2 == 0 :
        with pytest.raises(ValueError) :
            assert gaussian_blur(image, (size, size))
    else :
        blurred_image = gaussian_blur(image, ksize = (size, size))
        blurred_stack = gaussian_blur(stack, ksize = (size, size))

        assert blurred_image.shape == (512, 512)
        assert blurred_stack.shape == stack.shape

        assert np.std(blurred_image) < np.std(image)
        assert np.std(blurred_stack) < np.std(stack)


@given(st.integers(20, 30))
@settings(max_examples = 20, deadline = None)
def test_imfill(N) :
    '''
    Given :
        - white image with different black spots
    So :
        - apply imfill
    Assert :
        - the output image is white
        - the output stack is white
        - the shape is preserved
    '''
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = (image != 0).astype(np.uint8) #ensure that the input image is binary
    stack = np.asarray([ image for _ in range(N)])


    filled_image = imfill(image)
    filled_stack = imfill(stack)

    assert (filled_image == 255 * ones((512, 512), dtype = np.uint8)).all()
    assert (filled_stack == 255 * ones(filled_stack.shape, dtype = np.uint8)).all()

    assert filled_image.shape == (512, 512)
    assert filled_stack.shape == stack.shape


@given(square_image_strategy())
@settings(max_examples = 20, deadline = None)
def test_imfill_square(stack) :
    '''
    Given:
        - stack of white images with a black square
    So :
        - apply imfill
    Assert :
        - the resulting image is white
        - the shape is preserved
    '''
    # invert the provided image -> from black with a whirte square to white with
    #black square
    image = stack[0]
    stack = (stack == 0).astype(np.uint8)
    image = (image == 0).astype(np.uint8)

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
    Given :
        - image whith 4 connected regions
    Assert :
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
def test_connected_components_wStats_centr_pos(stack, n_imgs) :
    '''
    Given:
        - image tensor with white suqare
    So :
        - compute the connected components
    Assert :
        - the centroids position is correct
    given an image with a white square, assert that:

    - the position of the centroids is correct
    '''
    image = stack[0]
    L = int(np.sqrt(np.sum(image)))
    connected_image = connected_components_wStats(image)
    connected_stack = connected_components_wStats(stack)

    gt = [(199 + L) / 2, (199 + L) / 2] # truth centroid position

    assert  (connected_image[3][1] == gt).all()
    for i in range(stack.shape[0]) :
        assert (connected_stack[3][i][1] == gt).all()


@given(rand_stack_strategy())
@settings(max_examples = 20,
            deadline = None,
            suppress_health_check = (HC.too_slow,))
def test_otsu_threshold(stack):
    '''
    Given :
        - image tensor
    So :
        - apply otsu threshold
    Assert :
        - the returned image is binary
        - the returned stack is binary
        - the minimum non zero value of the iage convolved with the binary image
            created, is higher than the estimated threshold
    '''
    image = stack[0]

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
def test_connected_components_wVolumes_3d(stack) :
    '''
    Given :
        - stack of black images with a white square

    So :
        - found the connected compontens
    Assert  :
        - two connected components are found
        - the volume is correct
    '''
    L = np.sqrt(np.sum(stack[0]))
    N = stack.shape[0]
    res = connected_components_wVolumes_3d(stack)

    assert (np.unique(res[0]) == [0,1]).all()
    assert (res[1][1] == N * L * L)


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
    Ginven:
        - image tensor
    So :
        - apply canny edge detection
    Assert :
        - A binary image is preserved
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
@settings(max_examples = 20,
            deadline = None,
            suppress_health_check=(HC.too_slow,))
def test_adjust_gamma_null(stack) :
    '''
    Given :
        - Image tensor
    So :
        - adjustd gamma with gamma == 1
    Assert :
        - no change in the image
    '''
    gamma_stack = adjust_gamma(stack)
    gamma_image = adjust_gamma(stack[0])

    assert np.isclose(gamma_stack, stack).all()
    assert np.isclose(gamma_image, stack[0]).all()


@given(rand_stack_strategy())
@settings(max_examples = 20,
            deadline = None,
            suppress_health_check=(HC.too_slow,))
def tast_adjust_gamma_exception(stack) :
    '''
    Given:
        - image tensor
    So :
        - adjust_gamma with gamma == 0
    Assert :
        exception is raised
    '''

    with pytest.raises(Exception) as excinfo :

        gamma_stack = adjust_gamma(stack, 0)
        gamma_image = adjust_gamma(stack[0], 0)
        assert excinfo == 'gamma vlaue cannot be zero'



@given(rand_stack_strategy())
@settings(max_examples = 20,
            deadline = None,
            suppress_health_check=(HC.too_slow,))
def test_raise_error(stack) :
    '''
    Given :
         - image tensor of float type
    So :
         - perform median blur with high kernel
         - perform otsu threshold
         - equalize histogram
         -  Cenny edge detection
    Assert:
         - Exception is raised
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
        assert canny_edge_detection(image)
        assert canny_edge_detection(stack)


@given(rand_stack_strategy())
@settings(max_examples = 20, deadline = None, suppress_health_check=(HC.too_slow,))
def test_warnings(stack) :
    '''
    Given :
         - image tensor
    So:
        - perform operations that requires binary images
    Assert :
        - a warning is raised
    '''
    with pytest.warns(None):
        connected_components_wStats(stack)
        imfill(stack)
        connected_components_wVolumes_3d(stack)
