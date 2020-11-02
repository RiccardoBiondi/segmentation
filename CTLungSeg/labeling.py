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
                        help='output name label')

    args = parser.parse_args()
    return args

#pre-trainded centroids:
centroids = {
                'parenchima' : [1.6444744, 2.152333 , 1.9559685, 0.  ],
                'bronchi'    : [4.315418 , 5.3087306, 2.6431215, 255.],
                'noise'      : [5.5954723, 2.288158 , 3.316695 , 0.  ],
                'GGO'        : [ 5.746537, 6.8778925, 3.4054325, 0.  ]}

def main(volume, centroids):


    # prepare the image
    volume = hu2gl(volume)
    weight = (volume != 0).astype(np.uint8)
    edge_map = canny_edge_detection(volume, 241, 25)
    # build multi channel
    mc = np.stack([
                    normalize(volume),
                    normalize(median_blur(volume, 11)),
                    normalize(std_filter(volume, 7)),
                    median_blur(edge_map, 9)], axis = -1)


    labels = imlabeling(mc, centroids, weight)
    labels = (labels == 3).astype(np.uint8)
    labels = median_blur(labels, 11)

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
