import cv2
import os
import numpy as np
import pylab as plt
import pandas as pd
import pickle
from glob import glob


def load(filename):
    data = pickle.load( open(filename, "rb" ) )
    return data


def save(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(list, f)


def shaping(img) :
    """
    reshape into a vector each image of a stack
    img -> list of images

    Return:
    res -> list of reshaped images
    split -> list of
    shape -> list of original shape of each image
    """
    res = []
    split = []
    shape = []
    value = 0
    for el in img:
        shape.append(el.shape)
        el = np.reshape(el, (-1, 1))
        value = value + el.shape[0]
        split.append(value)
        res.append(el)
    return [res,split,shape]


def remap(labels, center,shape):
    """
    remap the labels into the original image
    labels -> list of vector to remap
    center -> center from cv2.kmeans function
    shape  -> list of shape of original stack of images
    retun a list of images
    """
    out = []
    for i in range(len(labels)-1) :
        res = center[labels[i].flatten()]
        res2 =  res.reshape((shape[i]))
        out.append(res2)
    return out


def kmeans(img, criteria, clusters) :
    """
    Extent cv2.kmeans for an image stack
    img -> list of input images
    criteria ->
    clusters -> number of clusters

    return:
    ret ->
    labels ->
    center ->
    """
    ret = []
    labels = []
    center = []

    for i in img :
        t_ret, t_labels, t_center = cv2.kmeans(i, clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        ret.append(t_ret)
        labels.append(t_labels)
        center.append(t_center)
    return [ret,labels,center]
