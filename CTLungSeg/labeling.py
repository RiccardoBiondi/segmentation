#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    parser.add_argument('--centroids', dest='centroids', required=True, type=str, action='store', help='centroids')
    parser.add_argument('--label1', dest='lab1', required=True, type=str, action='store', help='output name of first label')
    parser.add_argument('--label2', dest='lab2', required=True, type=str, action='store', help='output name of second label')


    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    images = load_image(args.filename)
    centroids = load_image(args.centroids)

    images = preprocess(images)
    images = median_blur(images, 5)

    labels = imlabeling(images, centroids)

    #separate the different labels
    lab_1 = (labels == 1).astype(np.uint8)
    lab_2 = (labels == 2).astype(np.uint8)
    #clean up the labels
    kernel = np.ones((5,5), dtype = np.uint8)
    lab_1 = opening(lab_1, kernel)
    lab_2 = opening(lab_2, kernel)
    #
    save_pickle(args.lab1, lab_1)
    save_pickle(args.lab2, lab_2)

if __name__ == '__main__' :
    main()
