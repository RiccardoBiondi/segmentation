#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
import numpy as np

from CTLungSeg.utils import load_image, save_pickle, preprocess
from CTLungSeg.method import median_blur
from CTLungSeg.segmentation import opening, imlabeling

__author__ = ['Riccado Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@tudio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Image labeling'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--centroids', dest='centroids', required=True, type=str, action='store', help='Centroids')
    parser.add_argument('--output', dest='out', required=True, type=str, action='store', help='output filename')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    images = load_image(args.filename)
    centroid = load_image(args.centroids)
    n_clusters = centroid.shape[0]

    labels = imlabeling(images, centroid)

    labels = median_blur(labels, 5)
    #create mask from labels
    labels[labels == 2] = 0
    labels[labels == 3] = 1
    labels = opening(labels, np.ones((5,5), np.uint8))
    #
    images = labels * images
    images = (median_blur(preprocess(images), 9)).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS +cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    init = [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    _, labels,_ = cv2.kmeans(images.reshape(-1,), 3, None,criteria, 10, init[1])

    labels = (labels.reshape(images.shape)).astype(np.uint8)
    labels = median_blur(labels, 7)
    labels[labels == 2] = 1




    save_pickle(args.out, labels)


if __name__ == '__main__' :
    main()
