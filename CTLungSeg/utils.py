#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import pickle
import pydicom
import numpy as np
import pandas as pd

from functools import partial
from glob import glob



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


def load_npz(filename):
    """Load the .npz image file

    Parameters
    ----------
    filename: str
        file name or path to load file

    Returns
    -------
    data: array_like
        array loaded from a given file
    """
    with open(filename, 'rb') as fp:
        data_npz = np.load(fp, allow_pickle = True)
        data = [data_npz[key] for key in data_npz.keys()]

    return np.array(data)


def load_dicom(filedir):
    """Load image and store it into a 3D numpy array

    Parameter
    ---------
    filedir: str
        path to the directory that contains the dicom files
    Returns
    -------
    imgs: array-like
        image tensor
    """
    dicoms = glob('{}/*'.format(filedir))
    z = [float(pydicom.dcmread(f, force = True)[('0020', '0032')][-1]) for f in dicoms]
    order = np.argsort(z)
    dicoms = np.asarray(dicoms)[order]
    imgs = np.asarray([pydicom.dcmread(f, force = True).pixel_array for f in dicoms])
    return imgs


def load_nifti(filename):
    pass


def load_image(filename):
    """Load a stack of images and return a 3D numpy array. The input file format can by .pkl.npy, .npz or a folder that contains .dcm files.

    Parameter
    ---------
    filename: str
        path to the image file(.pkl.npy or .npz) or folder that contains .dcm files.
    Return
    ------
    imgs: array-like
        image tensor
    """
    if os.path.exists(filename) :
        if os.path.isfile(filename) :
            imgs = load_pickle(filename)
        else :
            imgs = load_dicom(filename)
    else :
        raise FileNotFoundError()
    return imgs



def save_pickle(filename, data):
    """Save the image stack as pickle

    Parameters
    ----------
    filename: str
        file name or path to dump as pickle file
    data: array-like
        image or stack to save

    Return
    ------
    None
    """
    with open('{}.pkl.npy'.format(filename), 'wb') as fp:
        pickle.dump(data, fp)



def save_npz(filename, data):
    """Save the image stack as uncompressed npz file

    Parameters
    ----------
    filename: str
        file name or path to dump as npz file
    data: array-like
        image or stack to save

    Return
    ------
    None
    """
    with open('{}.npz'.format(filename), 'wb') as fp :
        np.savez_compressed(file=fp, a=data)


def rescale(img, Max, Min):
    """Rescale the image accodring to max, min input

    Parameters
    ----------
    img: array-like
        input image or stack to rescale
    max: float
        Maximum value of the output array
    min: float
        minimum value of the output array
    Return
    ------
    rescaled: array-like
        Image rescaled according to min, max
    """
    if min == max :
        raise ZeroDivisionError
    return (img.astype(np.float32) - Min) * (1. / (Max - Min))


def preprocess(img):
    """Set to zero all the negative pixel values, rescale the image and convert it a 8bit GL image.

    Parameter
    ---------
    img: array-like
        input image or stack of images

    Return
    ------
    out: array like
        rescaled image
    """
    out = img.copy()
    out[out < 0] = 0
    out = 255 * rescale(out, np.amax(out), 0)#???
    return out.astype(np.uint8)


def subsamples(data, n_sub):
    """Randomly divide the sample into n_sub subsamples

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
    """
    #shuffle the sample list
    img = data.copy()
    np.random.shuffle(img)
    img = np.array_split(img, n_sub)
    return np.array(img)



def imfill(img):
    """Internal function. Fill the holes of a single image.

    Parameters
    ----------
    img : array-like
        Image to fill

    Return
    ------
    filled : array-like
        filled image
    """
    img = np.pad(img.astype('uint8'), pad_width=((1, 1), (1, 1)),
                      mode='constant', constant_values=(0., 0.))
    im_floodfill = img.copy()
    h, w = im_floodfill.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    filled = img | im_floodfill_inv
    return filled[1:-1, 1:-1]



def to_dataframe (arr, columns) :
    """Convert 3D numpy array into a list of pandas dataframes

    Parameter
    ---------
    arr: array-like
        input array to convert in a dataframe
    columns: list of string
        columns of the dataframe
    Return
    ------
    df: list of dataframe
        list of dataframe made from arr
    """
    return list(map(partial(pd.DataFrame, columns=columns), arr))



def imcrop(img, ROI) :
    """Crop the image according to ROI

    Parameters
    ----------
    img : array-like
        image to crop
    ROI : array-like
        array with the coordinate of ROI vertex

    Return
    ------
    cropped : array-like
        cropped image
    """
    return img[ROI[1] : ROI[3], ROI[0] : ROI[2]]
