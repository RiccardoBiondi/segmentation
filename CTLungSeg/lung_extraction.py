#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import SimpleITK as sitk

from time import time
from lungmask.mask import apply
from CTLungSeg.utils import read_image, write_volume, hu2gl, shift_and_crop, normalize
from CTLungSeg.method import compute_eigenvals


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


def main(array, info) :


    image = sitk.GetImageFromArray(array)
    image.SetOrigin(info[0])
    image.SetSpacing(info[1])
    image.SetDirection(info[2])

    # find the lungmask
    mask = apply(image)
    mask = (mask != 0).astype(np.uint8)
    
    array = shift_and_crop(array)
    lung = array * mask
    lung = hu2gl(lung)
    e1 = np.max(compute_eigenvals(lung, 5, 9), axis = 3)
    e1 = normalize(e1)
    m1 = (e1 < 10.)
    l1 = lung * m1
    e2 = np.max(compute_eigenvals(l1, 5, 9), axis = 3)
    e2 = normalize(e2)
    lung = l1 * (e2 < 10.)
    
    return lung


if __name__ == '__main__' :

    start = time()

    args = parse_args()
    volume, info = read_image(args.input)
    lung = main(volume, info)
    write_volume(lung, args.output, info, '.nii')

    stop = time()
    print('Process ended after {} seconds'.format(stop -start))
