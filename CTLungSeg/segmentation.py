#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from tqdm import tqdm

from CTLungSeg.method import gauss_smooth
from CTLungSeg.method import vesselness
from CTLungSeg.method import apply_mask
from CTLungSeg.method import threshold


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']



def remove_vessels(image, sigma = 2., thr = 8) :
    '''
    Remove vessels by applying a fixed threshold to the vesselness map.
    Before computing the vesselness a gaussian smoothing is applied.

    Parameters
    ----------
    image : SimpleITK image
        input image
    sigma : float
        sigma of the gaussian smoothing filter
    thr : float
        fixed threshold value
    Return
    ------
    wo_vessels : SimpleITK image
        Image without the vessels
    '''
    smooth = gauss_smooth(image, sigma)
    vessel = vesselness(smooth)
    mask = threshold(vessel, 4000, thr, 0, 1)
    return apply_mask(image, mask, outside_value = -1000)



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
    retval : array-like
         It is vector of the sum of squared distance from each point to their corresponding centers for each subsample

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
    >>> ret, center = kmeans_on_subsamples(sub, n_centroids,  stop_criteria, init, True)
    '''
    ns = imgs[0].shape[-1]
    if weight :
        vector = np.asarray([el[:, :, :, :- 1][el[: , :, :, - 1] != 0] for el in imgs],
                                dtype = np.ndarray)
    else :
        vector = np.asarray([el.reshape((-1, ns)) for el in imgs],
                            dtype=np.ndarray)

    centroids = []
    ret = []
    for el in tqdm(vector) :

        r, _, centr = cv2.kmeans(el.astype(np.float32),
                                 n_centroids,
                                 None,
                                 stopping_criteria,
                                 10,
                                 centr_init)
        centroids.append(centr)
        ret.append(r)
    return [np.asarray(ret, dtype = np.float32), np.asarray(centroids, dtype= np.float32)]
