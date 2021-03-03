#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings
from  hypothesis import HealthCheck as HC

from CTLungSeg.method import median_filter
from CTLungSeg.method import std_filter
from CTLungSeg.method import gauss_smooth
from CTLungSeg.method import threshold
from CTLungSeg.method import adaptive_histogram_equalization
from CTLungSeg.method import adjust_gamma
from CTLungSeg.method import vesselness
from CTLungSeg.method import cast_image
from CTLungSeg.method import apply_mask

import numpy as np
import SimpleITK as sitk
from numpy import ones, zeros
from numpy.random import rand, choice


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


################################################################################
###                                                                          ###
###                         Define Test strategies                           ###
###                                                                          ###
################################################################################


legitimate_chars = st.characters(whitelist_categories = ('Lu','Ll'),
                                    min_codepoint = 65, max_codepoint = 90)

text_strategy = st.text(alphabet = legitimate_chars, min_size = 1,
                            max_size = 15)

sitk_types = [sitk.sitkInt16, sitk.sitkFloat32, sitk.sitkUInt32, sitk.sitkUInt64,
             sitk.sitkFloat64, sitk.sitkUInt16]

type_as_string = {
                sitk.sitkInt16 : '16-bit signed integer',
                sitk.sitkFloat32 :  '32-bit float',
                sitk.sitkUInt32 :'32-bit unsigned integer' ,
                sitk.sitkUInt64 : '64-bit unsigned integer',
                sitk.sitkFloat64 : '64-bit float',
                sitk.sitkUInt16 : '16-bit unsigned integer'
}


@st.composite
def gauss_noise_strategy(draw) :
    origin = draw(st.tuples(*[st.floats(0., 100.)] * 3))
    spacing = draw(st.tuples(*[st.floats(.1, 1.)] * 3))
    direction = tuple([0., 0., 1., 1., 0., 0., 0., 1., 0.])
    size = (draw(st.integers(10, 100)), 50, 50)

    filter_ = sitk.GaussianImageSource()
    filter_.SetSize(size)
    filter_.SetOrigin(origin)
    filter_.SetSpacing(spacing)
    filter_.SetDirection(direction)

    return filter_.Execute()


@st.composite
def median_noise_strategy(draw) :
    '''
    Generates a black image with salt and pepper noise
    '''
    origin = draw(st.tuples(*[st.floats(0., 100.)] * 3))
    spacing = draw(st.tuples(*[st.floats(.1, 1.)] * 3))
    direction = tuple([0., 0., 1., 1., 0., 0., 0., 1., 0.])
    size = (draw(st.integers(10, 100)), 50, 50)

    image = sitk.Image(size, sitk.sitkUInt8)
    image.SetOrigin(origin)
    image.SetSpacing(spacing)
    image.SetDirection(direction)

    # add salt and pepper noise
    noise = sitk.SaltAndPepperNoiseImageFilter()
    noise.SetProbability(.02)

    return noise.Execute(image)


################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################


@given(median_noise_strategy(), st.integers(1, 13))
@settings(max_examples = 20,
        deadline = None,
        suppress_health_check = (HC.too_slow,))
def test_median_filter (image, radius) :
    '''
    Given :
        - image tensor of salt and pepper
        - kernel size
    So :
        - apply median blurring
    Assert that :
        - shape is preserved
        - return a stack of uniform image
    '''
    blurred = median_filter(image, radius)
    array = sitk.GetArrayFromImage(blurred)
    im = sitk.GetArrayFromImage(image)

    assert (blurred.GetSize() == image.GetSize())
    assert (np.sum(array) < np.sum(im))



@given(median_noise_strategy())
@settings(max_examples = 20,
        deadline = None,
        suppress_health_check = (HC.too_slow,))
def test_median_filter_raise_value_error(image) :
    '''
    Given :
        - SimpleITK image
        - radius == 0
    Then :
        - apply median filter
    Assert :
        - value error is raised
    '''
    with pytest.raises(ValueError) :
        image = median_filter(image, 0)


@given(gauss_noise_strategy(), st.floats(1., 4.))
@settings(max_examples = 20,
        deadline = None,
        suppress_health_check = (HC.too_slow,))
def test_gauss_smooth (image, sigma ) :
    '''
    Given :
        - Random Gaussian Noise Image
        - Sigma
    Then :
        - apply a gaussian smoothing
    Assert :
        - the global image variance is reduced
    '''
    smoothed = gauss_smooth(image, sigma)

    stats = sitk.StatisticsImageFilter()
    stats.Execute(image)
    orig_sigma = stats.GetSigma()
    stats.Execute(smoothed)
    sm_sigma = stats.GetSigma()

    assert orig_sigma > sm_sigma



@given(gauss_noise_strategy())
@settings(max_examples = 20,
            deadline = None,
            suppress_health_check=(HC.too_slow,))
def tast_adjust_gamma_exception(image) :
    '''
    Given:
        - image tensor
    So :
        - adjust_gamma with gamma == 0
    Assert :
        exception is raised
    '''

    with pytest.raises(Exception) as excinfo :

        gamma_stack = adjust_gamma(image, 0)
        assert excinfo == 'gamma vlaue cannot be zero'



@given(gauss_noise_strategy(), text_strategy)
@settings(max_examples = 20,
            deadline = None,
            suppress_health_check = (HC.too_slow,))
def test_adjust_gamma_raise_image_type_exception(image, image_type):
    '''
    Given :
        - Image
        - Random text image type
    Then :
         - apply adjust_gamma
    Assert :
        - Exception is raised
    '''
    with pytest.raises(Exception) as excinfo :

        gamma_stack = adjust_gamma(image, 3, image_type)


@given(gauss_noise_strategy())
@settings(max_examples = 20,
          deadline = None,
          suppress_health_check = (HC.too_slow,))
def test_std_filter_raise_value_error(image) :
    '''
    Given :
        - Image
        - Radius = 0
    Then :
        - Apply std_filter
    assert :
        - ValueError is raised
    '''
    with pytest.raises(Exception) as excinfo :
        image = std_filter(image, 0)



@given(gauss_noise_strategy(), st.integers(10, 100), st.integers(150, 250))
@settings(max_examples = 20,
          deadline = None,
          suppress_health_check = (HC.too_slow,))
def test_threshold_and_apply_mask(image, lower, upper) :
    '''
    Given :
        - Image
        - Upper threshold value
        - Lower threshold value
    Then :
        - apply threshold
        - ,ask the image
    assert :
        - minimum pixel value is higher than lower threshold value
        - maximum pixel value is lower than threshold value
    '''

    thr = threshold(image, upper = upper, lower = lower)
    masked = apply_mask(image, thr, outside_value = lower + 1)
    stats = sitk.StatisticsImageFilter()
    _ = stats.Execute(masked)


    assert stats.GetMinimum() > lower
    assert stats.GetMaximum() < upper



@given(gauss_noise_strategy(), st.sampled_from(sitk_types))
@settings(max_examples = 20,
          deadline = None,
          suppress_health_check = (HC.too_slow,))
def test_cast_image(image, new_type) :
    '''
    Given :
        - image
        - sitk image type
    then :
        - cast the image
    assert :
        - new type is orrect
    '''
    cast = cast_image(image, new_type)

    assert cast.GetPixelIDTypeAsString() == type_as_string[new_type]
