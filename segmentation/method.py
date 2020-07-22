import cv2
import pickle
import numpy as np
import pandas as pd
from functools import partial


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def load_pickle(filename) :
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


def save_pickle(filename, data):
    '''
    Save the image stack as pickle

    Parameters
    ----------
    filename: str
        file name or path to dump as pickle file
    data: array-like
        image or stack to save

    Return
    ------
    None
    '''
    with open('{}.pkl.npy'.format(filename), 'wb') as fp:
        pickle.dump(data, fp)


def rescale(img, max, min) :
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
    Return
    ------
    rescaled: array-like
        Image rescaled according to min, max
    '''
    #TODO : condition to exclue min == max
    return (img.astype(float) - min) * (1. / (max - min))


def erode(img, kernel, iterations = 1):
    '''
    Apply the erosion on the full image stack

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

    vectorized = np.vectorize(partial(cv2.erode, kernel=kernel, iterations=iterations), signature= '(m,n)->(m,n)')
    return vectorized(img.astype('uint8'))


def dilate(img, kernel, iterations = 1 ):
    '''
    Apply dilation to a whole stack of images

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

    vectorized = np.vectorize(partial(cv2.dilate, kernel=kernel, iterations=iterations), signature = '(m,n)->(m,n)')
    return vectorized(img.astype('uint8'))


def connectedComponentsWithStats(img):
    '''
    computes the connected components labeled image of boolean image and also
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
        return [retval, labels, stats, controids]
    out = list(zip(*list(map(cv2.connectedComponentsWithStats, img.astype('uint8')))))
    return [np.array(out[0]), np.array(out[1]), list(out[2]), list(out[3])]


def bitwise_not(img):
    '''
    Calculates per-element bit-wise inversion of the input array

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




def _imfill(img):
    '''
    Internal function. Fill the holes of a single image.
    Parameters
    ----------
    img : array-like
        Image to fill
    Return
    ------
    filled : array-like
        filled image
    '''
    # Copy the thresholded image.
    img = np.pad(img.astype('uint8'), pad_width=((1, 1), (1, 1)),
                      mode='constant', constant_values=(0., 0.))
    im_floodfill = img.copy()
    # Mask used to flood filling.
    h, w = im_floodfill.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    filled = img | im_floodfill_inv
    return filled[1:-1, 1:-1]


def imfill(img):
    '''
    Fill the holes of the input image or stack of images

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
        return _imfill(img.astype('uint8'))
    filled = np.vectorize(_imfill, signature='(m,n)->(m,n)')
    return filled(img.astype('uint8'))


def medianBlur(img, k_size):
    '''
    Apply median blurring filter on an image or stack of images
    Parameters
    ----------
    img: array-like
        image or stack of images to filter
    k_size : int
        aperture linear size; it must be odd and greater than 1
    Return
    ------
    blurred : array-like
        median blurred image
    '''
    if len(img.shape) == 2: #single image case
        return cv2.medianBlur(img.astype('uint8'), k_size)
    blurred = np.vectorize(partial(cv2.medianBlur, ksize = k_size), signature = '(m,n)->(m,n)')
    return blurred(img.astype('uint8'))


def fill_holes(imgs, kernel):
    '''
    Fill the remaining holes in the input binary images

    Parameters
    ----------
    imgs : array-like
        stack f binary images to fille
    kernel: array-like
        erosion kernel

    Return
    ------
    filled : array-like
        filled image stack
    '''
    filled = erode(imgs.astype('uint8'), kernel)
    filled = bitwise_not(filled)
    filled = imfill(filled)
    return filled
