#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np

from time import time

from CTLungSeg.utils import read_image, load_pickle, hu2gl, normalize
from CTLungSeg.utils import write_volume
from CTLungSeg.method import median_blur, std_filter
from CTLungSeg.method import histogram_equalization, adjust_gamma
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

#pre-trained centroids
centroids = { 'parenchima': [1.3822415, 2.4269834, 1.1459424, 1.832688 ],
                'edges'   : [1.6750793, 2.6646569, 3.829929 , 2.1440172],
                'Bronchi' : [3.4454546, 3.0228717, 1.9430293, 3.3130786],
                'Noise'   : [6.0392303, 2.7451596, 4.861056 , 5.6319346],
                'GGO'     : [6.359824 , 6.218402 , 3.42476  , 5.9504952]}


def main(volume, centroids):


    # prepare the image
    volume = hu2gl(volume)
    weight = (volume != 0).astype(np.uint8)

    equalized = histogram_equalization(volume, 2, (10, 10))
    mc = np.stack([     normalize(equalized),
                        normalize(median_blur(volume, 11)),
                        normalize(std_filter(volume, 3)),
                        normalize(adjust_gamma(volume, 1.5))], axis = -1)


    labels = imlabeling(mc, centroids, weight)
    labels = (labels == 4).astype(np.uint8)
    labels = median_blur(labels, 5)

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
