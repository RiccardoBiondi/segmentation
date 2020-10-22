#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import numpy as np

from time import time

from CTLungSeg.utils import load_image, save_pickle, hu2gl, normalize
from CTLungSeg.method import median_blur, canny_edge_detection, std_filter
from CTLungSeg.segmentation import imlabeling

__author__ = ['Riccado Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@tudio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Image labeling'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input',
                        dest='filename',
                        required=True,
                        type=str,
                        action='store',
                        help='Input filename')
    parser.add_argument('--centroids',
                        dest='centroids',
                        required=True,
                        type=str,
                        action='store',
                        help='centroids')
    parser.add_argument('--label',
                        dest='lab',
                        required=True,
                        type=str,
                        action='store',
                        help='output name of first label')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    volume = load_image(args.filename)
    centroids = load_image(args.centroids)

    # prepare the image
    volume = hu2gl(volume)
    weight = (volume != 0).astype(np.uint8)
    edge_map = canny_edge_detection(volume)
    # build multi channel
    mc = np.stack([
                    normalize(volume),
                    normalize(median_blur(volume, 11)),
                    normalize(std_filter(volume, 3)),
                    median_blur(edge_map, 7)], axis = -1)

    labels = imlabeling(mc, centroids, weight)
    labels = (labels == 4).astype(np.uint8)
    #
    save_pickle(args.lab, labels)

if __name__ == '__main__' :

    start = time()
    main()
    stop = time()
    print('Process ended after {:f} seconds'.format(stop- start))
