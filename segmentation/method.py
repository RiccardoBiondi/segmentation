import cv2
import pickle
import numpy as np
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
        return cv2.erode(img.astype('uint8'), kernel, iterations)

    vectorized = np.vectorize(partial(cv2.dilate, kernel=kernel, iterations=iterations), signature = '(m,n)->(m,n)')
    return vectorized(img.astype('uint8'))




#TODO bitwise not
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


#TODO to pandas
