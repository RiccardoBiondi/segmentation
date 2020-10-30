#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import logging
import numpy as np

from tqdm import tqdm
#from sklearn.cluster import KMeans

from CTLungSeg.utils import gl2bit
from CTLungSeg.method import connected_components_wStats
from CTLungSeg.method import connected_components_wVolumes_3d
from CTLungSeg.method import erode, dilate
from CTLungSeg.method import imfill

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def opening(img, kernel):
    '''
    Perform an erosion followed by a dilation

    Parameters
    ----------

    img : array-like
        image tensor
    kernel : array-like
        kernel used for the morphological operations

    Returns
    -------

    opened : array-like
        Opened image

    Example
    -------
    >>> from CTLungSeg.utils import load_image
    >>> from CTLungSeg.segmentation import opening
    >>>
    >>> filename = 'path/to/input/image'
    >>> image = load_image(filename)
    >>> #define the kernel
    >>> kernel = np.ones((5, 5), dtype = np.uint8)
    >>> opened = opening(image, kernel = kernel)

    Note
    ----

    .. note::
        This function will raise a warning if the input image is not binary. The
        function will be executed, however the resukts may not be corrected.
    '''
    if len(np.unique(img)) != 2 :
        logging.warning('The image is not binary, the connected components may \
                            not be accurate')
    opened = erode(img, kernel=kernel)
    return dilate(opened, kernel=kernel)


def closing(img, kernel):
    '''
    Perform a dilation followed by an erosion

    Parameters
    ----------

    img : array-like
        image tensor
    kernel : array-like
        kernel used for the morphological operations

    Results
    -------

    closed : array-like
        closed image stack

    Example
    -------
    >>> from CTLungSeg.utils import load_image
    >>> from CTLungSeg.segmentation import closing
    >>>
    >>> filename = 'path/to/input/image'
    >>> image = load_image(filename)
    >>> #define the kernel
    >>> kernel = np.ones((5, 5), dtype = np.uint8)
    >>> closed = closing(image, kernel = kernel)

    Note
    ----
    .. note::
        This function will raise a warning if the input image is not binary. The
        function will be executed, however the resukts may not be corrected.
    '''
    if len(np.unique(img)) != 2 :
        logging.warning('The image is not binary, the connected components may \
                            not be accurate')
    closed = dilate(img, kernel=kernel)
    return erode(closed, kernel=kernel)


def remove_spots(img, area):
    '''
    Set to zero the GL of all the connected region with
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

    Example
    -------
    >>> from CTLungSeg.utils import load_image
    >>> from CTLungSeg.segmentation import remove_spots
    >>> # load image to process
    >>> filename = '/path/ti/input/image'
    >>> image = load_image(filename)
    >>> max_spot_area = 100
    >>> filled = remove_spots(image, max_spot_area)
    .. note::
        This function will raise a warning if the input image is not binary. The
        function will be executed, however the resukts may not be corrected.
    '''
    _, lab, stats, _ = connected_components_wStats(img)
    for i,stat in enumerate(stats):
        for j in stat.query('AREA < {}'.format(str(area + 1))).index:
            lab[i][lab[i] == j] = 0
    lab = lab != 0
    return lab.astype(np.uint8)


def select_largest_connected_region_3d(img):
    '''
    Select the larger connected regions of the iamge tesor.
    NOTE: do not consider backgroung as connected region

    Parameters
    ----------

    img : array-like
        binary image tensor

    Returns
    -------

    dst : array-like
        binary image with only the largest connected region

    if len(np.unique(img)) != 2 :
        logging.warning('The image is not binary, the connected components may \
                            not be accurate')
    '''
    connected, volumes = connected_components_wVolumes_3d(img)
    dst = (connected == np.argsort(volumes)[-2])
    return dst


def bit_plane_slices(stack, bits, nbits = 8):
    '''
    Convert each voxel GL into its 8-bit binary
    rapresentation and return as output the stack
    resulting from the sum of all the bith
    specified in bits, with them significance.

    Parameters
    ----------

    stack : array-like
        image stack. each GL must be an 8-bit unsigned int

    bits: tuple
        tuple that specify which bit sum

    nbits: int
        number of bit of the input image, must be 8 or 16


    Returns
    -------

    output : array-like
        images stack in which each GL depends only to
        the significance of each specfied bit
    '''
    binary = gl2bit(stack, nbits)
    bit = np.asarray(bits)
    selection = binary[nbits - bit, ...]
    significance = np.asarray([2**(i - 1) for i in bit]).reshape(len(bits), 1, 1, 1)
    return (np.sum(selection * significance, axis=0))


def imlabeling(image, centroids, weight = None) :
    '''
    Label an input stack of multichannel images according to the provided
    centroids and weight.

    Parameters
    ----------

    image : array-like of shape (n_images, height, width, n_channels)
        image stack to label

    centroids : array-like of shape (n_centroids, n_channels)
        Centroids vector for KMeans clustering. M

    weight : array-like of shape (n_images, height, width)
        int array, each element marked as 0 will be removes from the
        labeling.

    Returns
    -------
    labeled : array-like of shape (n_images, height, width )
        Image in which each GL ia assigned to the corresponding label

    Example
    -------
    >>> import cv2
    >>> import numpy as np
    >>> from CTLungSeg.utils import load_image
    >>> from CTLungSeg.segmentation import imlabeling
    >>>
    >>> filename = 'path/to/input/file'
    >>> centroids_file = 'path/to/centroids/file'
    >>> to_label = load_image(filename)
    >>> centroids = load_image(centroids_file)
    >>> labeled = imlabeling(to_label, centroids)
    '''

    # old version
    #if weight is not None :
    #    weight = weight.reshape((-1, ))
    #
    #to_label = image.reshape((-1, image.shape[-1]))
    #kmeans = KMeans(n_clusters = centroids.shape[0], init=centroids, n_init = 1)
    #lab = kmeans.fit_predict(to_label.astype(np.float32), sample_weight = weight)
    #return lab.reshape(image.shape[:3])

    # new version
    if centroids.shape[1] != image.shape[-1] :
        raise Exception('Number of image channel doesn t match the number of \
                            centroids features : {} != {}\
                            '.format(image.shape[-1], centroids.shape[1]))
    if weight  is not None :
          if weight.shape != image.shape[:-1] :
              raise Exception('Weight shape doesn t match image one : {} != {}\
                                '.format( weight.shape, image.shape[:-1]))
          distances = np.asarray([np.linalg.norm(image[weight != 0] -c, axis = 1) for c in centroids])
          weight[weight != 0] = np.argmin(distances, axis = 0)
          return weight
    else :
        distances = np.asarray([np.linalg.norm(image -c, axis = 3) for c in centroids])
        labels = np.argmin(distances, axis = 0)
        return labels




def kmeans_on_subsamples(imgs,
                         n_centroids,
                         stopping_criteria,
                         centr_init,
                         weight = False) :
    '''
    Apply the kmenas clustering on each stack of images in subsample.
    Allow also to choose if consider or not some voxel during the segmentation.
    To allow these feature simply raise the flag 'weight' and provide as last
    channel a binary mask with 0 on each voxel you want to exclude

    Parameters
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

    Returns
    -------

    centroids : array-like
        array that contains the n_centroids estimated for each
        subsample

    Examples
    --------
    >>> import cv2
    >>> import numpy as np
    >>> from CTLungSeg.utils import load_image, subsamples
    >>> from CTLungSeg.segmentation import kmeans_on_subsamples
    >>>
    >>> filename = '/path/to/multichannel/image'
    >>> image = load_image(filename)
    >>> # create mask for background removal
    >>> mask = (image[:, :, :, 0] != 0).astype(np.uint8)
    >>> mc = np.stack([image, mask], axis = -1)
    >>> # define stopping criteria and init technique
    >>> stop_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    >>>                   10, .001)
    >>> init = cv2.KMEANS_RANDOM_CENTERS
    >>> n_centroids = 3
    >>>
    >>> sub = subsamples(mc)
    >>> center = kmeans_on_subsamples(sub, n_centroids,  stop_criteria, init, True)
    '''
    ns = imgs[0].shape[-1]
    if weight :
        vector = np.asarray([el[:, :, :, :ns - 1][el[: , :, :, ns - 1] != 0] for el in imgs])
    else :
        vector = np.asarray([el.reshape((-1, ns)) for el in imgs],
                            dtype=np.ndarray)

    centroids = []
    for el in tqdm(vector) :

        _, _, centr = cv2.kmeans(el.astype(np.float32),
                                 n_centroids,
                                 None,
                                 stopping_criteria,
                                 10,
                                 centr_init)
        centroids.append(centr)
    return np.asarray(centroids, dtype= np.float32)
