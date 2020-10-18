#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from tqdm import tqdm
from sklearn.cluster import KMeans

from CTLungSeg.utils import gl2bit
from CTLungSeg.method import connected_components_wStats
from CTLungSeg.method import connected_components_wVolumes_3d
from CTLungSeg.method import erode, dilate
from CTLungSeg.method import imfill

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
    """Set to zero the GL of all the connected region with
    area lesser than the provided value

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
    connected, areas = connected_components_wVolumes_3d(img)
    areas = np.delete(areas, np.argmax(areas)) # remove background
    dst = (connected == np.argmax(areas) + 1)
    return dst


def reconstruct_gg_areas(mask):
    """This function interpolate each slice of the input mask
    to reconstruct the missing gg areas.

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
    """Found the upper and lower corner of the
    rectangular ROI according to the connected region stats

    Parameter
    ---------
    stats: pandas dataframe
        dataframe that contains the stats of the connected regions

    Return
    ------
    corners: array-like
        array which contains the coordinates of the upper and
        lower corner of the ROI organized as [x_top, y_top, x_bottom, y_bottom]
    """
    stats = stats.drop([0], axis = 0)
    corner = np.array([stats.min(axis = 0)['LEFT'], stats.min(axis = 0)['TOP'], np.max(stats['LEFT'] + stats['WIDTH']), np.max(stats['TOP'] + stats['HEIGHT'])])
    return np.nan_to_num(corner, copy=False).astype('int16')


def create_lung_mask(volume, threshold) :
    '''

    '''
    lung_mask = volume > threshold
    body_mask = imfill(lung_mask)
    return ((body_mask != 0) & ~lung_mask)


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
        images stack in which each GL depends only to
        the significance of each specfied bit
    """
    binary = gl2bit(stack)
    bit = np.asarray(bits)
    selection = binary[8 - bit, ...]
    significance = np.asarray([2**(i - 1) for i in bit]).reshape(3, 1, 1, 1)
    return (np.sum(selection * significance, axis=0)).astype(np.uint8)


def imlabeling(image, centroids, weight = None) :
    """
    Label an input stack of multichannel images according to the provided
    centroids and weight.

    Parameters
    ----------
    image : array-like of shape (n_images, height, width, n_channels)
        image stack to label

    centroids : array-like of shape (n_centroids, n_channels)
        Centroids vector for KMeans clustering. M

    weight : array-like of shape (n_images, height, width)
        The weights for each observation in image.
        If None, all observations are assigned equal weight.

    Return
    ------
    labeled : array-like of shape (n_images, height, width )
        Image in which each GL ia assigned to the corresponding label
    """
    if not weight is None :
        weight = weight.reshape((-1, ))

    to_label = image.reshape((-1, image.shape[3]))
    kmeans = KMeans(n_clusters = centroids.shape[0], init=centroids, n_init = 1)
    lab = kmeans.fit_predict(to_label.astype(np.float32), sample_weight = weight)
    return lab.reshape(image.shape[:3])




def kmeans_on_subsamples(imgs,
                         n_centroids,
                         stopping_criteria,
                         centr_init,
                         weight = False) :
    """
    Apply the kmenas clustering on each stack of images in subsample.
    Allow also to choose if consider or not some voxel during the segmentation.
    To allow these feature simply raise the flag 'weight' and provide as last
    channel a binary mask with 0 on each voxel you want to exclude

    Parameters :
    ----------
    imgs : array-like of shape (n_subsamples, n_imgs, heigth, width, n_channels)
        array of images tensor
    n_centroids : int
        number of centroids to find
    stopping_criteria :
        It is the iteration termination criteria. When this criteria
        is satisfied, algorithm iteration stops.
    center_init :
        centroid initialization technique; can be
        cv2.KMEANS_RANDOM_CENTERS or cv2.KMEANS_PP_CENTERS.
    weight : Bool ,
        flag that allow to not consider some voxel in images. Default = False

    Return
    ------
    centroids : array-like
        array that contains the n_centroids estimated for each
        subsample
    """
    ns = imgs[0].shape[3]
    if weight :
        vector = np.asarray([el[:, :, :, :ns - 1][el[: , :, :, ns - 1] != 0] for el in imgs])
    else :
        vector = np.asarray([el.reshape((-1, ns)) for el in imgs],
                            dtype=np.ndarray)

    centroids = []
    for el in tqdm(vector) :## TODO: improve efficiency

        _, _, centr = cv2.kmeans(el.astype(np.float32),
                                 n_centroids,
                                 None,
                                 stopping_criteria,
                                 10,
                                 centr_init)
        centroids.append(centr)
    return np.asarray(centroids, dtype= np.float32)
