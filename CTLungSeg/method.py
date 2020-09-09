#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import CTLungSeg.utils as utils
from functools import partial


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def erode(img, kernel, iterations = 1):
    '''Apply the erosion on the full image stack

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
    '''
    if len(img.shape) == 2 :
        return cv2.erode(img.astype('uint8'), kernel, iterations)
    return np.asarray(list(map(partial(cv2.erode, kernel=kernel, iterations=iterations),img)))


def dilate(img, kernel, iterations = 1 ):
    '''Apply dilation to a whole stack of images

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
    '''
    if len(img.shape) == 2 :
        return cv2.dilate(img.astype('uint8'), kernel, iterations)
    return np.asarray(list(map(partial(cv2.dilate, kernel=kernel, iterations=iterations),img)))


def connected_components_wStats(img):
    '''computes the connected components labeled image of boolean image and also
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

    stats: list of array-like
        statistic for each lablel for each image of the stack

    centroids: array-like
        centroid for each label fr each image of the stack
    '''
    if len(img.shape) == 2 :
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(img.astype('uint8'))
        return [retval, labels, stats, centroids]

    out = list(zip(*list(map(cv2.connectedComponentsWithStats, img.astype('uint8')))))
    return [np.array(out[0]), np.array(out[1]), list(out[2]), list(out[3])]


def bitwise_not(img):
    '''Compute per-element bit-wise inversion of the input array

    Parameters
    ----------
    img: array_like
        image or stack of images
    Returns
    -------
    dst: array-like
        inverted image or stack of images
    '''
    if img.shape == 2: #single image case
        return cv2.bitwise_not(img)
    dst = np.vectorize(cv2.bitwise_not, signature='(m,n)->(m,n)')
    return dst(img.astype('uint8'))


def imfill(img):
    '''Fill the holes of the input image or stack of images

    Parameter
    ---------
    img: array-like
        binary image to fill
    Return
    ------
    filled: array-like
        binary image or stack with filled holes
    '''

    if len(img.shape) == 2: #one image case
        return utils.imfill(img.astype(np.uint8))

    return np.asarray(list(map(utils.imfill,img.astype(np.uint8))))


def median_blur(img, ksize):
    '''Apply median blurring filter on an image or stack of images
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
    '''
    if len(img.shape) == 2: #single image case
        return cv2.medianBlur(img, ksize)
    return np.asarray(list(map(partial(cv2.medianBlur, ksize=ksize),img)))


def gaussian_blur(img, ksize, sigmaX=0,
                    sigmaY=0,borderType=cv2.BORDER_DEFAULT):
    '''Apply a gaussian blurring filter on an image or stack of images

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
        '''
    if len(img.shape) == 2: #single image case
        return cv2.GaussianBlur(img, ksize,sigmaX=tuple(sigmaX), sigmaY=tuple(sigmaY), borderType = borderType)
    return np.asarray(list(map(partial(cv2.GaussianBlur, ksize = ksize,sigmaX=sigmaX, sigmaY=sigmaY, borderType = borderType),img)))


def otsu_threshold(img):
    '''Compute the best threshld value for each slice of the input image stack by using otsu algorithm

    Parameters
    ----------
    img: array-like
        input image or stack of images. must be uint8 type

    Return
    ------
    out: array-like
        threshlded image stack
    '''
    if len(img.shape) == 2  :
        _, out = cv2.threshold(img, 0., 1., cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return out
    else:
        out = []
        for im in img :
            _, thr = cv2.threshold(im.astype(np.uint8), 0., 1., cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            out.append(np.array(thr))
        return np.array(out)


def gl2bit(img, width) :
    '''Convert the gray level of each voxel of a stack of images into its binary representation.

    Parameters
    ----------
    img : array-like
        image tensor to convert
    width : int
        number of bit to display

    Return
    ------
    binarized:  array-like
        image trensor in which each voxel GL value is replaced by a str that contains its binary representation.

    '''
    img_vector = img.reshape(-1, )
    return (np.asarray(list(map(partial(np.binary_repr, width=width), img_vector)))).reshape(img.shape)


def get_bit(img, bit_number) :
    '''
    Return an image in which each voxel GL corresponds only to the required bit with its level of significance.

    Parameters
    ----------
    img : array_like :
        image converted in bit from which extract the required bit
    bit_number : int
        number of bit to extract: 8 for MSB, 1 for LSB

    Return
    ------
    
    '''
    img_vector = img.reshape(-1, )
    significance = 2**(bit_number - 1)
    pos = 8 - bit_number
    return  (np.array([int(i[pos]) for i in img_vector], dtype = np.uint8) * significance).reshape(img.shape)
