#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import SimpleITK as sitk
import numpy as np


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']



def load_pickle(filename):
    '''
    Load the pickle image file

    Parameters
    ----------

    filename: str
        filename or path to load the file as pickle

    Returns
    -------

    data: array_like
        array loaded from the given file
    '''
    with open(filename, 'rb') as fp:
        data = np.load(fp, allow_pickle = True)
    return data



def _read_dicom_series(filedir):
    '''
    Define and initialize the SimpleITK reader for the image series
    Parameters
    ----------

    filedir: str
        path to the directory that contains the DICOM series

    Returns
    -------
    imgs: SimpleITK image series reader
        initialized, but not executed, reader for the DICOM series
    '''

    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(filedir)
    reader.SetFileNames(dicom_names)
    return reader


def _read_image(filename) :
    '''
    Define and initialize the SimpleITK image reader

    Parameters
    ----------
    filename : str
        Path to the image file

    Returns
    -------
    image_array : sitk reader
        initialized image reader
    '''
    reader = sitk.ImageFileReader()
    reader.SetFileName(filename)
    return reader



def read_image(filename):
    '''
    Read an image or a series from a format supported by SimpleITK.
    .. note: Will raise FileNotFoundError if the image path is incorrect
    or the image file does not exist.
    .. warn: If you want to read a DICOM series, please ensure that the folder
        contains only the .dcm file of a single series
    Parameters
    ----------
    filename: str
        Path to the image file, each format supported by SimpleITK is allowed.
        To load a DICOM series, provide the path to the directory containing
        only the .dcm files for the single series

    Returns
    -------
    volume: SimpleITK image
        Image red from the input file

    Example
    -------
    >>> from CTLungSeg.utils import read_image
    >>>
    >>> path = 'dicom/series/path/
    >>> # load a DICOM series
    >>> dicom = read_image(path)
    >>> # load a Nifti image
    >>> filename = 'path/to/nifti/file.nii'
    >>> image = read_image(filename)

    '''
    if os.path.exists(filename) :
        if os.path.isfile(filename) :
            reader = _read_image(filename)
        else :
            reader = _read_dicom_series(filename)

        image = reader.Execute()
    else :
        raise FileNotFoundError()
    return image



def write_volume(image, output_filename) :
    '''
    Write the image volume in a specified format. Each format supported by
    SimpleITK is supported.
    .. note: It does not write as .dcm series.

    Parameters
    ----------

    image : SimpleITk image file
        image to write
    output_filename : str
        output filename

    Example
    -------
    >>> from CTLungSeg.utils import read_image, write_volume
    >>>
    >>> input_file = 'path/ti/input/image'
    >>> image = read_image(input_file)
    >>> # process the image
    >>> # write the image as nrrd
    >>> output_name = 'path/to/output/filename.nrrd'
    >>> write_volume(image, output_name)
    >>> #or write the image as nifti
    >>  output_name = 'path/to/output/filename.nii'
    >>> write_volume(image, output_name)
    '''
    writer = sitk.ImageFileWriter()
    writer.SetFileName(output_filename )
    writer.Execute(image)


def save_pickle(filename, data):
    '''
    Save the image tensor as pickle

    Parameters
    ----------

    filename: str
        file name or path to dump as pickle file
    data: array-like
        image or stack to save

    '''
    with open(filename, 'wb') as fp:
        pickle.dump(data, fp)


def normalize(image) :
    '''
    Rescale each GL according to the mean and std of the whole image
    .. note:
        Will raise ZeroDivisionError if the provided image has constant pixel GL.

    Parameters
    ----------

    image : SimpleITK image object
        image to normalize

    Returns
    -------

    normalized : SimpleITK image
        normalized image
    '''
    # check if the image is not constant
    stats = sitk.StatisticsImageFilter()
    stats.Execute(image)

    if np.isclose(stats.GetSigma(), 0) :
        raise ZeroDivisionError('Cannot normalize image with Sigma == 0')
    norm = sitk.NormalizeImageFilter()

    return norm.Execute(image)


def shift_and_crop(image) :
    '''
    Ensure that the air peak of HU is centerd on -1000 and shift it to reach 0.
    After that, ensure that the maximum HU value is +2048

    Parameters
    ----------
    image: SimpleITK image
        image or stack of images, each pixel value must be expressed in hounsfield
        units (HU)

    Returns
    -------
    centered : SimpleITK image
        image or stack of images in whch the air value in HU is shifted to zero
    '''
    shifted = sitk.ShiftScale(image, 1000, 1.0)
    cropped = sitk.Threshold(shifted, 0, 2048, 0)

    return cropped



def shuffle_and_split(data, number_of_subarrays):
    '''
    Shuffle the input array and divide it into number_of_subarrays sub-arrays

    Parameters
    ----------
    data: array-like
        input sample to divide
    number_of_subarrays: int
        number of subsamples

    Returns
    -------

    out: list of array-like
        list of random subsamples
    '''
    np.random.shuffle(data)
    img = np.array_split(data, number_of_subarrays)
    return np.array(img, dtype = np.ndarray)


def deep_copy(image) :
    '''
    Return a copy of the input image

    Parameter
    ---------
    image : SimpleITK image
        Image to Copy

    Return
    ------
    copy : SimpleITK image
        copy of the input image
    '''
    copy = sitk.GetArrayFromImage(image).copy()
    copy = sitk.GetImageFromArray(copy)
    copy.CopyInformation(image)

    return copy
