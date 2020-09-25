#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
import numpy as np

from glob import glob
from tqdm import tqdm

from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import preprocess, subsamples
from CTLungSeg.method import median_blur
from CTLungSeg.segmentation import subsamples_kmeans_wo_bkg

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it']


def parse_args():
    description = 'kmeans clustering training'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='folder', required=True, type=str, action='store', help='Input folder')
    parser.add_argument('--output', dest='out', required=True,  type=str, action='store', help='dst of second centroids set')
    parser.add_argument('--n', dest='n', required=False, type=int, action='store', help='number of subsamples', default=100)
    parser.add_argument('--init', dest='init', required=False, type=int, action='store', help='centroid initialization technique', default=0)

    args = parser.parse_args()
    return args


def main():
    #useful constants
    init = [ "KMEANS_RANDOM_CENTERS", "KMEANS_PP_CENTERS"]
    centroid_init =  [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    stop_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    args = parse_args()

    print("I'm Loading...", flush=True )

    files = glob(args.folder + '/*.pkl.npy')
    imgs = np.concatenate(np.array([preprocess(load_image(f)) for f in files]))
    imgs = median_blur(imgs, 5)

    print('Loaded {:d} files from {}\n'.format(len(files), args.folder), flush=True)

    samples = subsamples(imgs, args.n)
    #Recap for better parameter control
    print('*****Starting custering*****\n', flush=True)
    print('\tNumber of subsamples--> {:d}'.format(args.n) , flush=True)
    print('\tTotal images --> {:d}'.format(imgs.shape[0]), flush=True)
    print('\tCentroid initzialization technique--> {}'.format(init[args.init]), flush=True)

    #First clustering
    print("\nI'm clustering...", flush = True)
    center = subsamples_kmeans_wo_bkg(samples,3, stop_criteria,centroid_init[args.init])
    # clustering refinement
    _, _, center = cv2.kmeans(center.reshape((-1,1)), 3, None, stop_criteria, 10, centroid_init[args.init])
    center = np.sort(center.reshape((-1,1)), axis = 0)
    print("I'm saving..." , flush=True)
    save_pickle(args.out, center)

    print('[DONE]', flush =True)


if __name__ == '__main__' :
    main()
