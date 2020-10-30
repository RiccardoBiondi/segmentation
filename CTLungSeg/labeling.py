#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np

from time import time

from CTLungSeg.utils import read_image, load_pickle, hu2gl, normalize
from CTLungSeg.utils import write_volume
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
                        required=False,
                        type=str,
                        action='store',
                        help='centroids',
                        default='')
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        type=str,
                        action='store',
                        help='output name of first label')

    args = parser.parse_args()
    return args

#pre-trainded centroids:
centroids = {
                'parenchima' : [1.425793, 2.0734222, 1.4296921, 0.],
               'bronchi'    : [3.3890672, 4.4695177, 1.8599507, 255.],
                'GG0'        : [4.9716797, 6.632072, 2.2960727, 0.],
                'noise'      :  [ 6.169081, 2.0313184, 4.8563914, 0.]
                }

def main(volume, centroids):


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
    labels = (labels == 2).astype(np.uint8)

    return labels


if __name__ == '__main__' :

    start = time()
    #load parameters
    args = parse_args()
    volume, info = read_image(args.filename)
    if args.centroids != '' :
        center = load_pickle(args.centroids)
    else :
        center =np.asarray([np.array(v) for k, v in centroids.items()])

    labels = main(volume, center)

    write_volume(labels, args.output, info)

    stop = time()
    print('Process ended after {:f} seconds'.format(stop- start))
