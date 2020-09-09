#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import preprocess, rescale
from CTLungSeg.method import imfill
from CTLungSeg.method import gaussian_blur, otsu_threshold
from CTLungSeg.method import gl2bit, get_bit
from CTLungSeg.segmentation import opening, closing
from CTLungSeg.segmentation import remove_spots, reconstruct_gg_areas, select_greater_connected_regions

from time import time

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Lung Segmentation'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='input', required=True, type=str, action='store', help='Input filename, must be .pkl.npy format')
    parser.add_argument('--lung', dest='lung', required=True, type=str, action='store', help='Masked image filename')
    parser.add_argument('--mask', dest='mask', required=False, type=str, action='store', help='Lung mask filename', default='')
    parser.add_argument('--int_spot_area', dest='isa', required=False, type=int, action='store', default=700, help='minimum internal spot area')
    parser.add_argument('--ext_spot_area', dest='esa', required=False, type=int, action='store', default=200, help='minimum external spot area')

    args = parser.parse_args()
    return args



def main():

    args = parse_args()
    DICOM = load_image(args.input)
    DICOM = preprocess(DICOM)

    lung_mask = otsu_threshold(gaussian_blur(DICOM, (5,5)))
    lung_mask = opening(lung_mask, kernel=np.ones((5,5), dtype=np.uint8))
    lung_mask = opening(lung_mask, kernel=np.ones((11,11), dtype=np.uint8))

    body_mask = imfill(lung_mask)
    body_mask = np.where(body_mask == 255, 1, 0)

    lung_mask = np.where(lung_mask == 0, 1, 0)
    lung_mask = lung_mask * body_mask
    #filter out internal and external spots
    #se inverti forse va meglio!! meno righe di codice
    lung_mask = np.where(lung_mask == 0, 1, 0)
    lung_mask = remove_spots(lung_mask, args.isa)
    lung_mask = np.where(lung_mask == 0, 1, 0)
    lung_mask = remove_spots(lung_mask, args.esa)

    lung_mask = reconstruct_gg_areas(lung_mask)

    save_pickle(args.lung + '_mask',lung_mask )
    #BIT PLANE slices
    bit_lung_mask = gl2bit(lung_mask * DICOM, 8)
    t_mask = get_bit(bit_lung_mask, 5) + get_bit(bit_lung_mask, 7) + get_bit(bit_lung_mask, 8)
    t_mask = gaussian_blur(t_mask, (7,7))
    t_mask = preprocess(t_mask)

    t_mask = otsu_threshold(t_mask)
    t_mask = np.where(t_mask == 0, 1, 0)

    lung_mask = (t_mask * lung_mask).astype(np.uint8)
    lung_mask = closing(lung_mask, np.ones((7,7), dtype=np.uint8))

    lung_mask = select_greater_connected_regions(lung_mask, 2)
    lung_mask[lung_mask == 255] = 1
    DICOM = lung_mask * DICOM


    if args.mask not in ['', None] :
        save_pickle(args.mask, imgs.astype(np.uint8))
    save_pickle(args.lung, DICOM.astype(np.float32))




if __name__ == '__main__' :
    main()
