#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from sklearn.cluster import KMeans
from tqdm import tqdm

from CTLungSeg.method import connected_components_wStats
from CTLungSeg.method import connected_components_wAreas_3d
from CTLungSeg.method import erode, dilate
from CTLungSeg.method import gl2bit

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def opening(img, kernel):
    """Perform an erosion followed by a dilation

    Parameters
    ----------
    img : array-like
        image tensor
    kernel : array-like
        kernel used for the morphological operations
    """
    opened = erode(img, kernel=kernel)
    return dilate(opened, kernel=kernel)


def closing(img, kernel):
    """Perform a dilation followed by an erosion

    Parameters
    ----------
    img : array-like
        image tensor
    kernel : array-like
        kernel used for the morphological operations
    """
    closed = dilate(img, kernel=kernel)
    return erode(closed, kernel=kernel)


def remove_spots(img, area):
    """Set to zero the GL of all the connected region with area lesser than area

    Parameters
    ----------
    img: array-like
        binary image from which remove spots
    area: int
        maximun area in pixels of the removed spots

    Returns
    -------
    filled: array-like
        binary image with spot removed
    """
    _, lab, stats, _ = connected_components_wStats(img)

    for i,stat in enumerate(stats):
        for j in stat.query('AREA < {}'.format(str(area))).index:
            lab[i][lab[i] == j] = 0
    lab = lab != 0
    return lab.astype(np.uint8)


def select_largest_connected_region_3d(img):
    """Select the larger connected regions of the iamge tesor.
        NOTE: do not consider backgroung as connected region

    Parameters
    ----------
    img : array-like
        binary image tensor
    Return
    ------
    dst : array-like
        binary image with only the largest connected region
    """
    connected, areas = connected_components_wAreas_3d(img)
    areas = np.delete(areas, np.argmax(areas))
    dst = (connected == np.argmax(areas) + 1)
    return dst


def reconstruct_gg_areas(mask):
    """This function interpolate each slice of the input mask to reconstruct the missing gg areas.

    Parameter
    ---------
    mask : array-like
        lung mask to reconstruct
    Return
    ------
    reconstructed : array-like
        reconstructed lung mask
    """
    first  = mask.copy()
    second = mask.copy()
    reconstructed = mask.copy()

    for i in range(first.shape[0] -1):
        first[i + 1] = np.bitwise_or(first[i], first[i + 1], dtype=np.uint8)

    for i in reversed(range(1, second.shape[0], 1)):
        second[i - 1] = np.bitwise_or(second[i - 1], second[i], dtype = np.uint8)

    for i in range(reconstructed.shape[0]):
        reconstructed[i] = np.bitwise_and(first[i], second[i], dtype = np.uint8)
    return reconstructed




def find_ROI(stats) :
    """Found the upper and lower corner of the rectangular ROI according to the connected region stats

    Parameter
    ---------
    stats: pandas dataframe
        dataframe that contains the stats of the connected regions

    Return
    ------
    corners: array-like
        array which contains the coordinates of the upper and lower corner of the ROI organized as [x_top, y_top, x_bottom, y_bottom]
    """
    stats = stats.drop([0], axis = 0)
    corner = np.array([stats.min(axis = 0)['LEFT'], stats.min(axis = 0)['TOP'], np.max(stats['LEFT'] + stats['WIDTH']), np.max(stats['TOP'] + stats['HEIGHT'])])
    return np.nan_to_num(corner, copy=False).astype('int16')


def bit_plane_slices(stack, bits):
    """Convert each voxel GL into its 8-bit binary
    rapresentation and return as output the stack
    resulting from the sum of all the bith
    specified in bits, with them significance.

    Parameters
    ----------
    stack : array-like
        image stack. each GL must be an 8-bit unsigned int
    bits: tuple
        tuple that specify which bit sum

    Returns
    -------
    output : array-like
        images stack in which each GL depends only to the significance of each specfied bit
    """
    binary = gl2bit(stack)
    bit = np.asarray(bits)
    selection = binary[8 - bit, ...]
    significance = np.asarray([2**(i - 1) for i in bit]).reshape(3, 1, 1, 1)
    return (np.sum(selection * significance, axis=0)).astype(np.uint8)


def imlabeling(image, centroids) :
    """Return the labeled image given the original image
    tensor and the centroids

    Parameters
    ----------
    image : array-like
    image to label

    centroids : array-like
        Centroids vector for KMeans clustering

    Return
    ------
    labeled : array-like
        Image in which each GL ia assigned on its label.
    """
    weigth = (image != 0).astype(np.uint8)
    to_label = image.reshape((-1,1))
    res = KMeans(n_clusters=centroids.shape[0], init=centroids, n_init=1).fit_predict(to_label, sample_weight = weigth.reshape(-1,))

    return res.reshape(image.shape)


def subsamples_kmeans_wo_bkg(imgs, n_centroids, stopping_criteria, centr_init) :
    """
    Apply the kmenas clustering on each stack of images in subsample.
    During clustering do not consider the background pixels that must be set to 0.

    Parameters :
    ----------
    imgs : array-like
        array of images tensor
    n_centroids : int
        number of centroids to find
    stopping_criteria :
        It is the iteration termination criteria. When this criteria
        is satisfied, algorithm iteration stops.
    center_init :
        centroid initialization technique; can be
        cv2.KMEANS_RANDOM_CENTERS or cv2.KMEANS_PP_CENTERS.

    Return
    ------
    centroids : array-like
        array that contains the n_centroids estimated for each
        subsample
    """
    centroids = []

    for el in tqdm(imgs) :
        to_cluster = el[el != 0] # remove bkg pixel
        to_cluster =  to_cluster.astype(np.float32) # cast to correct type
        _,_,centr = cv2.kmeans(to_cluster.reshape((-1,1)), n_centroids, None, stopping_criteria, 10, centr_init)
        centroids.append(centr)
    return np.asarray(centroids, dtype= np.float32)
