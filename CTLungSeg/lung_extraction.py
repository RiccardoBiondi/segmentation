#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from time import time
from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import preprocess
from CTLungSeg.method import imfill
from CTLungSeg.method import median_blur,gaussian_blur, otsu_threshold
from CTLungSeg.segmentation import opening, closing
from CTLungSeg.segmentation import remove_spots, reconstruct_gg_areas, select_greater_connected_regions
from CTLungSeg.segmentation import bit_plane_slices


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
    kernel = np.ones((5,5), dtype=np.uint8)
    lung_mask = opening(lung_mask, kernel=kernel)
    kernel = np.ones((11,11), dtype=np.uint8)
    lung_mask = opening(lung_mask, kernel=kernel)

    body_mask = imfill(lung_mask)
    body_mask = body_mask == 255
    lung_mask = body_mask & np.logical_not(lung_mask)
    #filter out internal and external spots
    lung_mask = lung_mask == 0
    lung_mask = remove_spots(lung_mask, args.isa)
    lung_mask = lung_mask == 0
    lung_mask = remove_spots(lung_mask, args.esa)

    lung_mask = reconstruct_gg_areas(lung_mask)
    #BIT PLANE slices
    t_mask = bit_plane_slices(lung_mask * DICOM, (5,7,8))
    t_mask = otsu_threshold(preprocess(gaussian_blur(t_mask, (7,7))))

    t_mask = ~t_mask
    lung_mask= lung_mask & t_mask
    kernel = np.ones((7,7), dtype = np.uint8)
    lung_mask = closing(lung_mask,kernel=kernel)
    lung_mask = select_greater_connected_regions(lung_mask, 2)
    lung_mask = lung_mask != 0

    DICOM = lung_mask * DICOM

    if args.mask not in ['', None] :
        save_pickle(args.mask, t_mask.astype(np.uint8))
    save_pickle(args.lung, DICOM.astype(np.uint8))




if __name__ == '__main__' :
    main()
