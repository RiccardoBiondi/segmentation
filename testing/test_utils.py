#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example
from  hypothesis import HealthCheck as HC

from CTLungSeg.utils import load_pickle
from CTLungSeg.utils import save_pickle
from CTLungSeg.utils import write_volume
from CTLungSeg.utils import  _read_image
from CTLungSeg.utils import read_image
from CTLungSeg.utils import normalize
from CTLungSeg.utils import shift_and_crop
from CTLungSeg.utils import shuffle_and_split
from CTLungSeg.utils import deep_copy

import numpy as np
import SimpleITK as sitk



__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

################################################################################
###                                                                          ###
###                         Define Test strategies                           ###
###                                                                          ###
################################################################################

legitimate_chars = st.characters(whitelist_categories=('Lu','Ll'),
                                    min_codepoint=65, max_codepoint=90)
filename_strategy = st.text(alphabet=legitimate_chars, min_size=1,
                            max_size=15)

medical_image_formats = ['.nii', '.nrrd', '.nhdr']


@st.composite
def rand_stack_strategy(draw):
    '''
    Generates a stack of N 512x512 white noise 8-bit GL images
    '''
    N = draw(st.integers(10, 100))
    return (255 * np.random.rand(N, 512, 512)).astype(np.uint8)



@st.composite
def sitk_image_strategy(draw):
    '''
    Generate a SimpleITK image of a gaussian
    '''
    origin = draw(st.tuples(*[st.floats(0., 100.)] * 3))
    spacing = draw(st.tuples(*[st.floats(.1, 1.)] * 3))
    direction = tuple([0., 0., 1., 1., 0., 0., 0., 1., 0.])
    size = (100 , 100, 100)

    filter_ = sitk.GaussianImageSource()
    filter_.SetSize(size)
    filter_.SetOrigin(origin)
    filter_.SetSpacing(spacing)
    filter_.SetDirection(direction)
    filter_.SetOutputPixelType(sitk.sitkInt16)
    filter_.SetScale(2**12)
    image = filter_.Execute()
    image = sitk.ShiftScale(image, -2000)
    return image


@st.composite
def sitk_constant_image(draw) :
    x_y = draw(st.integers(123, 512))
    z = draw(st.integers(1, 50))
    image = sitk.Image(x_y, x_y, z, sitk.sitkInt16)

    return image
################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################



@given(rand_stack_strategy(), filename_strategy)
@settings(max_examples=20,
        deadline=None,
        suppress_health_check=(HC.too_slow,))
def test_save_and_load_pkl(imgs,  filename):
    '''
    Given:
        - image tensor
        - random filename

    than :
        - save the array as .pkl.npy with the random name
        - reload the array
    and :
        - assert that the input array and the loaded one are equal
    '''
    save_pickle('./testing/images/{}.pkl.npy'.format(filename), imgs)
    load = load_pickle('./testing/images/{}.pkl.npy'.format(filename))
    assert (load == imgs).all()



@given(filename_strategy, st.sampled_from(medical_image_formats))
@settings(max_examples=20,
        deadline=None,
        suppress_health_check=(HC.too_slow,))
def test_reader(filename, format):
    '''
    Taking as input:
        - image tensor
        - random file name
        - file format supported by SimpleITK
    So:
        - create a SimpleITK.reader object
    And :
        - assert that the object paramenters are consistent with the input one
    '''
    fname = '{}{}'.format(filename, format)
    reader =  _read_image(fname)
    assert reader.GetFileName() == fname



@given(sitk_image_strategy(), filename_strategy,
       st.sampled_from(medical_image_formats))
@settings(max_examples=20,
          deadline=None,
          suppress_health_check=(HC.too_slow,))
def test_read_and_write_image(image, filename, format):
    '''
    Given :
        - SimpleITK
        - file format supported by SimpleITK
        - filename
    So :

        - write image to file
        - read the image
    And :
        - assert that the red image array is equal to the input one
        - assert that the red spatial information are aqual to the input one
    '''

    fname = './testing/images/{}.{}'.format(filename, format)
    write_volume(image, fname)
    red  = read_image(fname)

    assert (sitk.GetArrayFromImage(red) == sitk.GetArrayFromImage(image)).all()
    assert np.isclose(red.GetOrigin(), image.GetOrigin()).all()
    assert np.isclose(red.GetSize(), image.GetSize()).all()
    assert np.isclose(red.GetDirection(), image.GetDirection()).all()
    assert np.isclose(red.GetSpacing(), image.GetSpacing()).all()



@given(filename_strategy, st.sampled_from(medical_image_formats))
@settings(max_examples=20, deadline=None,
          suppress_health_check=(HC.too_slow,))
def test_reader_raise_file_not_found(path, format):
    '''
    Given :
        - path to a non existing image
        - image format
    then :
        - try to read
    - assert :
        - FileNotFoundError is raised
    '''
    fname = './testing/{}{}'.format(path, format)
    with pytest.raises(FileNotFoundError):
        image = read_image(fname)



@given(sitk_image_strategy())
@settings(max_examples=20, deadline=None,
          suppress_health_check=(HC.too_slow,))
def test_deep_copy(image):
    '''
    Given :
        - SimpleITK image
    And :
        - make a copy
    Assert
        - copy image equal to input image
    '''
    # TODO : Check image after transformation
    copy = deep_copy(image)

    assert (sitk.GetArrayFromImage(copy) == sitk.GetArrayFromImage(image)).all()
    assert np.isclose(copy.GetOrigin(), image.GetOrigin()).all()
    assert np.isclose(copy.GetSize(), image.GetSize()).all()
    assert np.isclose(copy.GetDirection(), image.GetDirection()).all()
    assert np.isclose(copy.GetSpacing(), image.GetSpacing()).all()



@given(sitk_constant_image())
@settings(max_examples=20, deadline=None,
          suppress_health_check=(HC.too_slow,))
def test_normalize_raise_error(image):
    '''
    Given :
        - Constant image
    Then :
        - try to normalize the image
    Assert :
        - ZeroDivisionError is raised
    '''
    with pytest.raises(ZeroDivisionError):
        res = normalize(image)


@given(sitk_image_strategy())
@settings(max_examples=20, deadline=None,
          suppress_health_check=(HC.too_slow,))
def test_shift_and_crop(volume):
    '''
    Given:
        - SimpleITK image
    So :
        - shif_and_crop is applied
    Assert that:
        - the shape if the tensor is preserved
        - the maximum value is lower than 2049
        - the minimum value is greater than -1
    '''
    res = shift_and_crop(volume)
    stats = sitk.StatisticsImageFilter()
    _ = stats.Execute(res)

    assert res.GetSize() == volume.GetSize()
    assert stats.GetMinimum() > -1
    assert stats.GetMaximum() < 2049



@given(rand_stack_strategy(), st.integers(2, 5))
@settings(max_examples=20,
            deadline=None,
            suppress_health_check=(HC.too_slow,))
def test_shuffle_and_split(sample, n_subsamples):
    '''
    Given :
        - image tensor
        - number of subsamples
    So :
        - apply shuffle_and_split
    Assert :
        - the correct number of subsamples is created
    '''

    subsample = shuffle_and_split(sample, n_subsamples)

    assert subsample.shape[0] == n_subsamples
