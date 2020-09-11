#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import argparse
from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import imcrop
from CTLungSeg.method import connected_components_wStats
from CTLungSeg.segmentation import find_ROI

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def select_slice_wlung(img, min_area, stats):
    """description

    Parameters
    ----------
    img: array-like

    min_area : int

    stats : list of pandas DataFrame

    Return
    ------
    reduced : array-like

    """
    corners = np.array(list(map(find_ROI, stats)), dtype = np.int32)
    AREAS = np.array([np.absolute((R[1] - R[3]) * (R[0] - R[2])) for R in corners], dtype = np.int64)
    out = img[AREAS > min_area]
    return out



def select_regions_wlung(img, stats) :
    """Description

    Parameters
    ----------
    img : array-like

    stats : list of pandas dataframe

    Returns
    -------
    cropped : arra of 2D arrays
    """
    corners = np.array(list(map(find_ROI, stats)), dtype = np.int32)
    return np.array([imcrop(im.astype(np.float32), r) for (im, r) in zip(img, corners)], dtype=np.ndarray)


def parse_args() :
    description = 'ROI selection'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--output', dest='out', required=True, type=str, action='store', help='output filename')
    parser.add_argument('--area', dest='area', required=False, type=int, action='store', default= 1000, help='area under which we can consider the slice doesn t contains lungs' )

    args = parser.parse_args()
    return args


def main():

    args = parse_args()

    stack = load_image(args.filename)
    mask = stack.copy()
    mask[mask != 0] = 1

    print("Slice selection...", flush=True)

    _, _, stats, _ = connected_components_wStats(mask)
    stack = select_slice_wlung(stack,args.area, stats)
    print('Selected ', stack.shape[0], ' slices of ', mask.shape[0], flush = True)

    print("ROI selection...", flush=True)
    mask = stack.copy()
    mask[mask!= 0] = 1
    _, _, stats, _ = connected_components_wStats(mask)
    stack = select_regions_wlung(stack, stats)

    print("\tDone", flush=True)
    print("Saving...")
    save_pickle(args.out, stack)

if __name__ == '__main__' :
    main()
