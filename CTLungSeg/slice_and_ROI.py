#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import argparse
from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import to_dataframe
from CTLungSeg.utils import imcrop
from CTLungSeg.method import connected_components_wStats
from CTLungSeg.segmentation import find_ROI

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


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
    lung = load_image(args.filename)
    lung_mask = lung.copy()
    lung_mask[lung_mask != 0] = 1
    _, _, stats, _ = connected_components_wStats(lung_mask)
    #manage stats into dataframe
    columns = ['LEFT', 'TOP', 'WIDTH', 'HEIGHT', 'AREA']
    stats = to_dataframe(stats, columns)
    print('Starting ROI selection', flush=True)
    ROI = np.array(list(map(find_ROI, stats)), dtype = np.int32)
    #starting the slice selection
    AREAS = np.array([np.absolute((R[1] - R[3]) * (R[0] - R[2])) for R in ROI], dtype = np.int64)
    #Remove all the regions that do not contains the lung
    ROI = ROI[AREAS > args.area]
    lung = lung[AREAS > args.area]
    print('Selected ', lung.shape[0], ' slices of ', AREAS.shape[0], flush = True)
    #crop the resulting images and save
    res = np.array([imcrop(im.astype(np.float32), r) for (im, r) in zip(lung, ROI)], dtype=np.ndarray)
    save_pickle(args.out, res)

if __name__ == '__main__' :
    main()
