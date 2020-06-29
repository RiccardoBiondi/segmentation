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
        pickle.dump(data, f)


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
    labels -> list of array to remap
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
    criteria -> It is the iteration termination criteria.
    clusters -> number of clusters

    return:
    ret -> It is the list of the sum of squared distance from each point to their corresponding centers for each slice
    labels -> list of label array
    center -> list of array of centers of clusters.
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


#starting the script

#global variable definition
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
n_clusters = 4

ROI_files = sorted(glob('./results/*_blur_ROI.pkl.npy'))

for i in range(len(ROI_files)):

    #read the files
    ROI = load(ROI_files[i])
    id = os.path.basename(ROI_files[i]).replace('_blur_ROI.pkl.npy', '')
    #convert image to array
    vector,split, shape = shaping(ROI)
    each_img = [np.float32(vector[i]) for i in range(len(vector))]
    all_img = np.float32(np.concatenate(vector))

    #perform the clustering
    a_ret, a_label, a_center = cv2.kmeans(all_img, n_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    e_ret, e_label, e_center = kmeans(each_img, criteria, n_clusters)

    #rearrange all the labels to image
    a_center = np.uint8(a_center)
    e_center = [np.uint8(e_center[i]) for i in range(len(e_center))]

    a_label = np.split(a_label, split)
    a_res = remap(a_label, a_center, shape)

    e_res = []
    for i in range(len(shape)):
        res = e_center[i][e_label[i].flatten()]
        res2 =  res.reshape((shape[i]))
        e_res.append(res2)

    #save the results
    save('./results/' + id + '_blur_clustered_all.pkl.npy', a_res)
    save('./results/' + id + '_blur_clustered_each.pkl.npy', e_res)
