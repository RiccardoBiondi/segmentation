#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pandas as pd
import CTLungSeg.utils as utils
from functools import partial
from cc3d import connected_components


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def erode(img, kernel, iterations = 1):
    """Apply the erosion on the full image stack

    Parameters
    ----------
    img: array-like
        image or stack of images to erode
    kernel: (2D)array-like
        kernel to apply to the input stack
    iterations: int
        number of iterations to apply

    Return
    ------
    processed: array-like
        eroded stack
    """
    if len(img.shape) == 2 :
        return cv2.erode(img.astype('uint8'), kernel, iterations)
    return np.asarray(list(map(partial(cv2.erode, kernel=kernel, iterations=iterations),img)))


def dilate(img, kernel, iterations = 1 ):
    """Apply dilation to a whole stack of images

    Parameters
    ----------
    img: array-like
        input image or stack to dilate
    kernel: (2D)array-like
        kernel to apply to the input stack
    iterations: int
        number of iterations to apply

    Return
    ------
    processed: array-like
        dilated stack
    """
    if len(img.shape) == 2 :
        return cv2.dilate(img.astype('uint8'), kernel, iterations)
    return np.asarray(list(map(partial(cv2.dilate, kernel=kernel, iterations=iterations),img)))


def connected_components_wStats(img):
    """computes the connected components labeled image of boolean image and also
    produces a statistics output for each label

    Parameters
    ----------
    img: array-like
        input image or stack of images

    Results
    -------
    retval: array-like

    labels: array-like
        labelled image or stack

    stats: list of pandas DataFrame
        statistic for each lablel for each image of the stack

    centroids: array-like
        centroid for each label fr each image of the stack
    """
    columns = ['LEFT', 'TOP', 'WIDTH', 'HEIGHT', 'AREA']
    if len(img.shape) == 2 :
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(img.astype(np.uint8))
        return [retval, labels, pd.DataFrame(np.array(stats), columns=columns), centroids]


    out = list(zip(*list(map(cv2.connectedComponentsWithStats, img.astype(np.uint8)))))
    return [np.array(out[0]), np.array(out[1]), utils.stats2dataframe(list(out[2])), list(out[3])]


def imfill(img):
    """Fill the holes of the input image or stack of images

    Parameter
    ---------
    img: array-like
        binary image to fill
    Return
    ------
    filled: array-like
        binary image or stack with filled holes
    """

    if len(img.shape) == 2: #one image case
        return utils.imfill(img.astype(np.uint8))
    return np.asarray(list(map(utils.imfill,img.astype(np.uint8))))


def median_blur(img, ksize):
    """Apply median blurring filter on an image or stack of images

    Parameters
    ----------
    img: array-like
        image or stack of images to filter
    ksize : int
        aperture linear size; it must be odd and greater than 1

    Return
    ------
    blurred : array-like
        median blurred image
    """
    if len(img.shape) == 2: #single image case
        return cv2.medianBlur(img, ksize)
    return np.asarray(list(map(partial(cv2.medianBlur, ksize=ksize),img)), dtype=np.uint8)


def gaussian_blur(img, ksize, sigmaX=0,
                    sigmaY=0,borderType=cv2.BORDER_DEFAULT):
    """Apply a gaussian blurring filter on an image or stack of images

    Parameters
    ----------
    img: array-like
        image or stack of images to filter
    ksize : tuple of int
        aperture linear size; it must be odd and greater than 1
    sigmaX: float
        Gaussian kernel standard deviation in X direction
    sigmaY: float
        Gaussian kernel standard deviation in Y direction; if sigmaY is zero, it is set to be equal to sigmaX, if both sigmas are zeros, they are computed from ksize
    borderType:
        Specifies image boundaries while kernel is applied on image borders
    Return
    ------
    blurred : array-like
        blurred image
    """
    if len(img.shape) == 2: #single image case
        return cv2.GaussianBlur(img, ksize,sigmaX=tuple(sigmaX), sigmaY=tuple(sigmaY), borderType = borderType)
    return np.asarray(list(map(partial(cv2.GaussianBlur, ksize = ksize,sigmaX=sigmaX, sigmaY=sigmaY, borderType = borderType),img)), dtype=np.uint8)


def otsu_threshold(img):
    """Compute the best threshld value for each slice of the input image stack by using otsu algorithm

    Parameters
    ----------
    img: array-like
        input image or stack of images. must be uint8 type

    Return
    ------
    out: array-like
        thresholded image stack
    """
    if len(img.shape) == 2  :
        _, out = cv2.threshold(img, 0., 1., cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return out
    else:
        out = list(zip(*list(map(partial(cv2.threshold, thresh=0, maxval=1, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU), img))))
        return np.asarray(out[1])


def gl2bit(img) :
    """Convert the gray level of each voxel of a stack of images into its binary representation.

    Parameters
    ----------
    img : array-like
        image tensor to convert
    width : int
        number of bit to display

    Return
    ------
    binarized:  array-like
        tensor of shape (8, img shape) composed by 1 image tesnor for each bit psition.

    """
    x = np.unpackbits(img.reshape(1, -1), axis=0)
    x = x.reshape(8, *img.shape)
    return np.asarray(x, dtype=np.uint8)


def connected_components_wAreas_3d(image) :
    """
    Found the connected components in three dimensions of  the image tensor and te corresponding areas. THhe used connectivity is 26.

    Parameter
    ---------
    image : array-like
        Binary stack of images

    Return
    ------
    labeled : array-like
        image in which each voxel is assigned to a connected region
    areas :array-like
        array of areas(in pixel) of each connected region.
    """
    connected = connected_components(image)
    areas =  np.asarray([np.sum((connected == i)) for i in np.unique(connected)])
    return [connected, areas]
