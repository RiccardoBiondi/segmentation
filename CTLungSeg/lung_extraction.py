#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import SimpleITK as sitk

from time import time
from lungmask.mask import apply
from CTLungSeg.utils import read_image, write_volume
from CTLungSeg.utils import shift_and_crop
from CTLungSeg.method import apply_mask
from CTLungSeg.segmentation import remove_vessels


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Lung Extraction'
    parser = argparse.ArgumentParser(description = description)

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


def main(image) :

    # find the lungmask
    mask = apply(image)
    # remove the distinction between left and right lung label
    mask = (mask != 0).astype(np.uint8)
    mask = sitk.GetImageFromArray(mask)
    mask.CopyInformation(image)

    masked = apply_mask(image, mask, outside_value = -1000)

    print('Remove Vessels', flush = True)
    wo_vessels = remove_vessels(masked)
    out = shift_and_crop(wo_vessels)

    return out


if __name__ == '__main__' :

    start = time()

    args = parse_args()
    volume = read_image(args.input)
    lung = main(volume)
    write_volume(lung, args.output)

    stop = time()
    print('Process ended after {} seconds'.format(stop -start))
