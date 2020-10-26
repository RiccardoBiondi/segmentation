#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np

from time import time

from CTLungSeg.utils import read_image, write_volume, hu2gl, center_hu
from CTLungSeg.method import gaussian_blur, imfill
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
                        help='Input filename, must be .pkl.npy format')
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        type=str,
                        action='store',
                        help='Masked image filename')

    args = parser.parse_args()
    return args


def main() :

        #load image
    start = time()
    args = parse_args()
    volume, info = read_image(args.input)
    ####################################
    ##          OLD VERSION           ##
    ####################################
    #volume[volume < 0] = 0 # remove tube
    #volume[volume > 2000]  = 2000 # remove metallic artifacts
    #compute the lung_mask
    #lung_mask = create_lung_mask(volume, args.thr)
    #lung_mask = median_blur(lung_mask.astype(np.uint8), 5)
    #lung_mask = select_largest_connected_region_3d(lung_mask.astype(np.uint16))
    #save the results
    #save_pickle(args.output ,volume * lung_mask)
    #lung = itk.image_from_array((volume * lung_mask)# itk o logica
    #write_nii(args.output, lung)
    #stop = time()
    #print('Process ended after {} seconds'.format(stop - start))

        ####################################
        ##          NEW VERSION           ##
        ####################################

    volume = center_hu(volume)
    bit = bit_plane_slices(volume, (11, 10, 9), 16)
    bit = hu2gl(bit)
    bit = gaussian_blur(bit, (7, 7))
    body = imfill((bit > 100).view(np.uint8)) # substitute with lung extraction
    lung_mask = (body == 255) & (bit < 100)

    lung_mask = remove_spots(lung_mask, 100)
    lung_mask = remove_spots((lung_mask == 0).view(np.uint8), 100)
    lung_mask = select_largest_connected_region_3d((lung_mask == 0).view(np.uint8))


    write_volume((lung_mask * volume), args.output, info, '.nii')
    stop = time()
    print('Process ended after {} seconds'.format(stop -start))



if __name__ == '__main__' :

    main()
