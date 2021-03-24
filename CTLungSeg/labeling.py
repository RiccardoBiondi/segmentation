#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import SimpleITK as sitk

from time import time

from CTLungSeg.utils import read_image, load_pickle, normalize
from CTLungSeg.utils import write_volume
from CTLungSeg.method import median_filter, std_filter, threshold
from CTLungSeg.method import adaptive_histogram_equalization, adjust_gamma
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
centroids = {
                'healthy lung': [1.0291475, 1.7986686, 1.3147535, 1.6199226],
                'lung'   :  [2.4449115, 2.8337748, 1.556249,  2.9394238],
                'Edges' :  [3.4244044, 2.1809669, 4.172402,  3.652266 ],
                'GGO'   :  [5.1485806, 5.3843336, 2.7543516, 4.812335 ],
                'Noise'     : [8.233303,  1.9194404, 6.503928,  6.670035 ]}


def main(volume, centroids):


    # prepare the image
    weight = sitk.GetArrayFromImage(threshold(volume, 4000, 1))
    equalized = normalize(adaptive_histogram_equalization(volume, 5))
    median = normalize(median_filter(volume, 3))
    std = normalize(std_filter(volume, 3))
    gamma = normalize(adjust_gamma(volume, 1.5))

    mc = np.stack([sitk.GetArrayFromImage(equalized),
                   sitk.GetArrayFromImage(median),
                   sitk.GetArrayFromImage(gamma),
                   sitk.GetArrayFromImage(std)], axis = -1)


    labels = imlabeling(mc, centroids, weight)
    labels = (labels == 3).astype(np.uint8)
    labels = sitk.GetImageFromArray(labels)
    labels.CopyInformation(volume)
    labels = median_filter(labels, 3)

    return labels


if __name__ == '__main__' :

    start = time()
    #load parameters
    args = parse_args()
    volume = read_image(args.filename)
    if args.centroids != '' :
        center = load_pickle(args.centroids)
    else :
        center =np.asarray([np.array(v) for _, v in centroids.items()])

    labels = main(volume, center)

    write_volume(labels, args.output)

    stop = time()
    print('Process ended after {:f} seconds'.format(stop- start))
