#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import SimpleITK as sitk

from time import time

from CTLungSeg.utils import read_image, write_volume, hu2gl, shift_and_crop
from CTLungSeg.method import imfill, median_blur
from CTLungSeg.segmentation import select_largest_connected_region_3d
from CTLungSeg.segmentation import bit_plane_slices, remove_spots


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
                        help='Input filename')
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        type=str,
                        action='store',
                        help='Masked image filename')

    args = parser.parse_args()
    return args


def main(volume) :


    volume = shift_and_crop(volume)
    bit = bit_plane_slices(volume, (11, 10, 9), 16)
    bit = hu2gl(bit)
    body = imfill((bit > 100).view(np.uint8))
    lung_mask = (body == 255) & (bit < 100)
    lung_mask = median_blur(lung_mask.view(np.uint8), 5)
    lung_mask = remove_spots(lung_mask, 113)
    lung_mask = select_largest_connected_region_3d(lung_mask.view(np.uint8))


    return lung_mask * volume


if __name__ == '__main__' :

    start = time()


    args = parse_args()
    volume, info = read_image(args.input)

    lung = main(volume)


    write_volume(lung, args.output, info, '.nii')

    stop = time()
    print('Process ended after {} seconds'.format(stop -start))
