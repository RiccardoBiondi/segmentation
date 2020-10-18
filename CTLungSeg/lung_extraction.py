#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np

from time import time

from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.method import imfill
from CTLungSeg.method import median_blur
from CTLungSeg.segmentation import select_largest_connected_region_3d
from CTLungSeg.segmentation import create_lung_mask

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Lung Extraction'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input',
                        dest='input',
                        required=True,
                        type=str,
                        action='store',
                        help='Input filename, must be .pkl.npy format')
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        type=str,
                        action='store',
                        help='Masked image filename')
    parser.add_argument('--thrshold',
                        dest='thr',
                        required=False,
                        type=int,
                        action='store',
                        default=800,
                        help='Threshold value for lung segmentation')

    args = parser.parse_args()
    return args





if __name__ == '__main__' :

    #load image
    start = time()
    args = parse_args()
    volume = load_image(args.input)

    volume[volume < 0] = 0 # remove tube
    volume[volume > 2000]  = 2000 # remove metallic artifacts
    #compute the lung_mask
    lung_mask = create_lung_mask(volume, args.thr)
    lung_mask = median_blur(lung_mask.astype(np.uint8), 5)
    lung_mask = select_largest_connected_region_3d(lung_mask.astype(np.uint16))
    #save the results
    save_pickle(args.output, (volume * lung_mask))
    stop = time()
    print('Process ended after {} seconds'.format(stop - start))
