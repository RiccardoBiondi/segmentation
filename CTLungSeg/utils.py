#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
#import itk
import pickle
import SimpleITK as sitk
import numpy as np
import pandas as pd

from functools import partial


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def load_pickle(filename):
    """Load the pickle image file

    Parameters
    ----------
    filename: str
        file name or path to load file as pickle

    Returns
    -------
    data: array_like
        array loaded from a given file
    """
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
    image = reader.Execute()
    spatial_informations = [image.GetOrigin(),
                            image.GetSpacing(),
                            image.GetDirection()]
    image_array = sitk.GetArrayFromImage(image)

    return image_array, spatial_informations


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
    image = reader.Execute();
    spatial_informations = [image.GetOrigin(),
                            image.GetSpacing(),
                            image.GetDirection()]
    arr_image = sitk.GetArrayFromImage(image)

    return arr_image, spatial_informations



def read_image(filename):
    '''
    Parameters
    ----------
    filename: str
        Path to image file, each format supported by SimpleITK is allowed
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
    >>> nifti, info2 = read_image(filename)

    '''
    if os.path.exists(filename) :
        if os.path.isfile(filename) :
            image, info = _read_image(filename)
        else :

            image, info = _read_dicom_series(filename)

    else :
        raise FileNotFoundError()
    return image, info


def write_volume(image, output_filename, spatial_informations = None, format_ = '.nrrd') :
    '''
    Write the image volume in a specified format. Each format supported by
    SimpleITK is supported

    Parameters
    ----------

    image : array-like
        image tensor to write
    output_filename : str
        name of the output file
    spatial_informations : list of tuple
        spatial information for the image, if None no spatial information is
        provided
    format_ : str
        output format, can be each of the one supported by SimpleITK. default is
        .nrrd

    Example
    -------
    >>> from CTLungSeg.utils import read_image, write_volume
    >>>
    >>> input_file = 'path/ti/input/image'
    >>> image, info = read_image(input_file)
    >>> # process the image
    >>> # write the image as nrrd
    >>> output_name = 'path/to/output/filename'
    >>> write_volume(image, output_name, info)
    >>> # write the image also as nifti
    >>> write_volume(image, output_name, info, '.nii')
    '''
    image = sitk.GetImageFromArray(image)
    if spatial_informations is not None :
        image.SetOrigin(spatial_informations[0])
        image.SetSpacing(spatial_informations[1])
        image.SetDirection(spatial_informations[2])

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

    Parameters:
    -----------

    image : array-like
        image or stack to normalize

    Returns
    -------

    normalized : array-like
        normalized images stack
    '''
    return ((image - np.mean(image)) / np.std(image)).astype(np.float32)


def rescale(img, Max, Min):
    '''
    Rescale the image accodring to max, min input

    Parameters
    ----------
    img: array-like
        input image or stack to rescale
    max: float
        Maximum value of the output array
    min: float
        minimum value of the output array

    Returns
    -------
    rescaled: array-like
        Image rescaled according to min, max
    '''
    if Min == Max :
        raise ZeroDivisionError
    return (img.astype(np.float32) - Min) * (1. / (Max - Min))


def gl2bit(img, width) :
    '''
    Convert the gray level of each voxel of a stack of images
    into its binary representation.

    Parameters
    ----------

    img : array-like
        image tensor to convert, each value mut be 8 or 16 unsigned bit
    width : int
        number of bit to display, can be 8 or 16 bits.

    Returns
    -------
    binarized:  array-like
        tensor of shape (width, img shape) composed by 1 image tesnor for each
        bit psition.

    '''
    if width != 8 and width != 16 :
        raise ValueError("Only 8 and 16 bit apresentation are allowed")

    x = np.unpackbits(img.reshape((1, -1)).astype('>i2').view(np.uint8), axis = 0)
    x = x.reshape(8, *img.shape,2)
    x = x.transpose(4, 0, 1, 2, 3)
    x = x.reshape((-1, *img.shape))
    return np.asarray(x[16 - width:])


def hu2gl(images):
    '''
    Convert an image from hounsfield unit to 8-bit gray scale

    Parameters
    ----------

    images: array-like
        input image or stack of images

    Returns
    -------
    out: array like
        8-bit rescaled image
    '''

    return (255 * rescale(images, images.max(), images.min())).astype(np.uint8)


def center_hu(image) :
    '''
    Ensure that the air peack of hu is centerd on -1024 and shit it to reach 0.
    After that ensure that the maximum hu value is +2048

    Parameters
    ----------
    image: array-like
        image or stack of images, each pixel value must be expressed in hounsfield
        units

    Returns
    -------
    centered : array-like
        image or stack of images in whch the air value in HU is shifted to zero

    '''
    image[image <  -1024] = image[image > -1024].min()
    image = image - image.min()
    image[image > 2048] = 0

    return image


def subsamples(data, n_sub): #TODO: change name
    '''
    Randomly divide the sample into n_sub subsamples

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



def imfill(img):
    '''
    Internal function. Fill the holes of a single image.

    Parameters
    ----------

    img : array-like
        Image to fill

    Returns
    -------
    filled : array-like
        filled image
    '''
    img = np.pad(img.astype('uint8'), pad_width=((1, 1), (1, 1)),
                      mode='constant', constant_values=(0., 0.))
    im_floodfill = img.copy()
    h, w = im_floodfill.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 1);
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    filled = img | im_floodfill_inv
    return filled[1:-1, 1:-1]



def stats2dataframe (arr) :
    '''
    Convert 3D numpy array into a list of pandas dataframes

    Parameters
    ----------

    arr: array-like
        input array to convert in a dataframe

    Returns
    -------
    df: list of dataframe
        list of dataframe made from arr
    '''
    columns = ['LEFT', 'TOP', 'WIDTH', 'HEIGHT', 'AREA']
    return list(map(partial(pd.DataFrame, columns = columns), arr))


def _std_dev(image, size) :
    '''
    compute the standard deviation of the neighborhood of each pixel

    Parameters
    ----------

    image : array-like
        image to filter
    size : int
        radius of the neighborhood

    Returns
    -------
     out: array-like
        filtered image
    '''
    ## Old version
    #image = itk.image_from_array(image)
    #std = itk.NoiseImageFilter.New(image)
    #std.SetRadius(size)
    #std.Update()
    #out = itk.array_from_image(std.GetOutput())
    image = sitk.GetImageFromArray(image)
    filter = sitk.NoiseImageFilter()
    filter.SetRadius(size)
    out = filter.Execute(image)
    out = sitk.GetArrayFromImage(out)

    return out
