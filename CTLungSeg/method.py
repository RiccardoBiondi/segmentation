#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SimpleITK as sitk

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


bounding_values = {'uint8' : [0, 255],
                   'uint16': [0, 2**16],
                   'HU' : [0, 2**12]}
image_types = {'uint8' : sitk.sitkUInt8,
            'uint16': sitk.sitkUInt16,
            'HU' : sitk.sitkUInt16 }



def median_filter(img, radius):
    '''
    Apply median blurring filter on the specified image.

    Parameters
    ----------

    img: SimleITK image
        image or stack of images to filter
    radius : int
        neighbourhood radius. must be greater or equal than 1.

    Returns
    -------
    blurred : SimpleITK image
        median blurred image


    Examples
    --------
    >>> from CTLungSeg.utils import read_image
    >>> from CTLungSeg.method import median_filter
    >>> # load the DICOM series
    >>> seriesname = 'path/to/input/series/'
    >>> volume = read_image(seriesname)
    >>> # define the kernel size and apply the median filter
    >>> radius = 5
    >>> filtered = median_blur(volume, radius)
    '''

    if radius <=0 :
        raise ValueError('Radius must be greater or equal than one')
    median = sitk.MedianImageFilter()
    median.SetRadius(int(radius))
    return median.Execute(img)



def std_filter(image, radius):
    '''
    Replace each pixel value with the standard deviation computed on a circular
    neighbourhood with specified radius

    Parameters
    ----------

    image : SimpleITK image
        image to filter

    radius: int
        radius of the neighborhood

    Returns
    -------

    filtered : SimpleITK image
        filtered image
    '''
    if radius <=0 :
        raise ValueError('Radius must be greater or equal than one')

    std = sitk.NoiseImageFilter()
    std.SetRadius(radius)
    return std.Execute(image)



def gauss_smooth(image, sigma = 1.):
    '''
    Apply a gaussian smoothing to the input image

    Parameters
    ----------
    image : SimpleITK image
        image to smooth
    sigma : float
        noise sigma

    Returns
    -------
    smoothed : SimpleITK image
        smoothed image
    '''
    gauss = sitk.SmoothingRecursiveGaussianImageFilter()
    gauss.SetSigma(sigma)
    return  gauss.Execute(image)



def adaptive_histogram_equalization(image, radius):
    '''
    Apply the histogram equalization in a neighbourhood of each voxel.

    Parameters
    ----------
    image : SimpleITK image

    radius : int > 0
        neighbourhood radius

    Returns
    -------
    equalized : SimpleITK image
        equalized image or stack of images
    '''
    ahe = sitk.AdaptiveHistogramEqualizationImageFilter()
    ahe.SetAlpha(1)
    ahe.SetBeta(1)
    ahe.SetRadius(radius)

    return ahe.Execute(image)



def adjust_gamma(image, gamma=1.0, image_type='HU'):
    '''
    Apply a gamma correction on the input image: $GL_{out} = GL_{in}^{\gamma}$

    Parameters
    ----------
    image : SimpleITK image
        image stack to adjust
    gamma : float
        power of the correction
    image_type : str
        input data type: can be ['uint8', 'uint16', 'HU'].

    Returns
    -------
    out : SimpleITK image
        gamma corected image
    '''
    if gamma == 0 :
        raise Exception('gamma vlaue cannot be zero')
    if image_type not in ['HU', 'uint8', 'uint16'] :
        raise Exception('image type {} not supported'.format(type))
    invGamma = 1.0 / gamma

    # cast image to float
    img = cast_image(image, sitk.sitkFloat32)
    c = sitk.PowImageFilter()
    out = c.Execute(img, invGamma)
    # saturate out of bounds voxels
    bound = bounding_values[image_type]
    out = sitk.Threshold(out, bound[0], bound[1], bound[1])
    # cast to the correct type
    out = sitk.Cast(out, image_types[image_type])
    return out



def apply_mask(image, mask, masking_value=0, outside_value=-1500):
    '''
    Apply a mask to image

    Parameters
    ----------
    image : SimpleITK image
        image to mask
    mask : SimpleITK image
        image mask

    Return
    ------
    masked : SimpleITK image
    '''
    mf = sitk.MaskImageFilter()
    mf.SetMaskingValue(masking_value)
    mf.SetOutsideValue(outside_value)
    return mf.Execute(image, mask)



def vesselness(image):
    '''
    Apply Frangi filter to find the likelihood of image regions to contains
    vessels (tubular structures)

    Parameters
    ----------
    image : SimpleITK image

    Return
    ------
    vesseness_map : SimpleITK image
    '''
    vess = sitk.ObjectnessMeasureImageFilter()
    vess.SetObjectDimension(1)
    return vess.Execute(image)



def threshold(image, upper, lower, inside=1, outside=0):
    '''
    Apply an interval threshold to the image

    Parameters
    ----------
    image : SimpeITK image
        input image
    upper : int
        upper threshold value
    lower : int
        lower threshold value
    inside : int
        value to assign to the voxels with GL in [lower, upper]
    outside : int
        value to assign to the voxels with GL outside [lower, upper]

    Returns
    -------
    thr : SimpleITK image
        thresholded image
    '''

    thr = sitk.BinaryThresholdImageFilter()
    thr.SetLowerThreshold(lower)
    thr.SetUpperThreshold(upper)
    thr.SetOutsideValue(outside)
    thr.SetInsideValue(inside)
    return thr.Execute(image)



def cast_image(image, new_pixel_type):
    '''
    Cast image pixels type to new_pixel_type

    Parameters
    ----------
    image : SimpleITK image
        image to cast
    new_pixel_type : SimpleITK PixelIDValueEnum
        new pixel type

    Returns
    -------
    casted : SimpleITK image
        image with new pixel type
    '''
    caster = sitk.CastImageFilter()
    caster.SetOutputPixelType(new_pixel_type)
    return caster.Execute(image)
