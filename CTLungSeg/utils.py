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
        file name or path to load file as pickle

    Returns
    -------

    data: array_like
        array loaded from a given file
    '''
    with open(filename, 'rb') as fp:
        data = np.load(fp, allow_pickle = True)
    return data


def _read_dicom_series(filedir):
    '''
    Internal function to read a dicom series stored on filedir.

    Parameters
    ----------

    filedir: str
        path to the directory that contains the dicom files

    Returns
    -------
    imgs: array-like
        image tensor
    spatial_informations : list
        list of tuple which contains information about: series spatial origin,
        spacing between pixls, series direction.
    '''

    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(filedir)
    reader.SetFileNames(dicom_names)
    return reader


def _read_image(filename) :
    '''
    Internal function. Read an image from specified file in each format
    supported by SimpleITK.

    Parameters
    ----------
    filename : str
        Path to the image file

    Returns
    -------
    image_array : array-like
        image tensor

    spatial_informations : list
        list of tuple which contains information about: series spatial origin,
        spacing between pixels, series direction.
    '''
    reader = sitk.ImageFileReader()
    reader.SetFileName(filename)
    return reader



def read_image(filename):
    '''
    Read an image or a series from a format supported by SimpleITK.
    .. note: Will raise FileNotFoundError if the image path is incorrect,
    or the image file does not existis.
    Parameters
    ----------
    filename: str
        Path to image file, each format supported by SimpleITK is allowed.
        To load a dicom series simpli provide the path to the dicrectory which
        contains the .dcm files

    Returns
    -------
    volume: array-like
        image tensor
    spatial_informations : list of tuple which
        contains information about: series spatial origin,
        spacing between pixls, series direction.

    Example
    ------
    >>> from CTLungSeg.utils import read_image
    >>>
    >>> path = 'dicom/series/path'
    >>> # load a DICOM series
    >>> dicom, info = read_image(path)
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


def write_volume(image, output_filename, format_ = '.nrrd') :
    '''
    Write the image volume in a specified format. Each format supported by
    SimpleITK is supported.
    .. note: Does not support .dcm files.

    Parameters
    ----------

    image : SimpleITk image file
        image tensor to write
    output_filename : str
        name of the output file

    format_ : str
        output format, can be each of the one supported by SimpleITK. default is
        .nrrd. Each format supported by SimpleITk is allowed.

    Example
    -------
    >>> from CTLungSeg.utils import read_image, write_volume
    >>>
    >>> input_file = 'path/ti/input/image'
    >>> image = read_image(input_file)
    >>> # process the image
    >>> # write the image as nrrd
    >>> output_name = 'path/to/output/filename'
    >>> write_volume(image, output_name, info)
    >>> # write the image also as nifti
    >>> write_volume(image, output_name, '.nii')
    '''
    output_filename = output_filename + format_
    writer = sitk.ImageFileWriter()
    writer.SetFileName(output_filename )
    writer.Execute(image)


def save_pickle(filename, data):
    '''
    Save the image stack as pickle

    Parameters
    ----------

    filename: str
        file name or path to dump as pickle file
    data: array-like
        image or stack to save

    '''
    with open('{}.pkl.npy'.format(filename), 'wb') as fp:
        pickle.dump(data, fp)


def normalize(image) :
    '''
    Rescale each GL according to the mean and std of the whole stack
    .. note:
        Will rais ZeroDivisionError if the provided image is constant.

    Parameters
    ----------

    image : SimpleITK
        image or series to normalize

    Returns
    -------

    normalized : SimpleITK image
        normalized images stack
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
    Ensure that the air peack of hu is centerd on -1024 and shit it to reach 0.
    After that ensure that the maximum hu value is +2048

    Parameters
    ----------
    image: SimpleITK image
        image or stack of images, each pixel value must be expressed in hounsfield
        units

    Returns
    -------
    centered : SimpleITK image
        image or stack of images in whch the air value in HU is shifted to zero

    '''
    shifted = sitk.ShiftScale(image, 1000, 1.0)
    cropped = sitk.Threshold(shifted, 0, 2048, 0)

    return cropped



def shuffle_and_split(data, n_sub): #TODO: change name
    '''
    Shuffle the input array and divie it into n_sub sub-arrays

    Parameters
    ----------
    data: array-like
        input sample to divide
    n_sub: int
        number of subsamples

    Returns
    -------

    out: list of array-like
        list of random subsamples
    '''
    np.random.shuffle(data)
    img = np.array_split(data, n_sub)
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
