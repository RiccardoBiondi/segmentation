#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
import numpy as np
import SimpleITK as sitk

from glob import glob
from time import time
from tqdm import tqdm

from CTLungSeg.utils import read_image, save_pickle
from CTLungSeg.utils import shuffle_and_split, normalize
from CTLungSeg.method import std_filter, adaptive_histogram_equalization
from CTLungSeg.method import median_filter, adjust_gamma, threshold
from CTLungSeg.segmentation import kmeans_on_subsamples


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it']


def parse_args():
    description = 'kmeans clustering training'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input',
                        dest='folder',
                        required=True,
                        type=str,
                        action='store',
                        help='Input folder')
    parser.add_argument('--output',
                        dest='out',
                        required=True,
                        type=str,
                        action='store',
                        help='dst of second centroids set')
    parser.add_argument('--n',
                        dest='n',
                        required=False,
                        type=int,
                        action='store',
                        help='number of subsamples',
                        default=100)
    parser.add_argument('--init',
                        dest='init',
                        required=False,
                        type=int,
                        action='store',
                        help='centroid initialization technique',
                        default=0)
    parser.add_argument('--format',
                        dest='format',
                        required=False,
                        type=str,
                        action='store',
                        help='centroid initialization technique',
                        default='.nii')

    args = parser.parse_args()
    return args


def main():

    # kmeans clustering aguments :
    # - initalization technique -> choose between random or kmeans++
    # - stop_criteria : criteria used to stop the kmeans algorithm
    init = [ "KMEANS_RANDOM_CENTERS", "KMEANS_PP_CENTERS"]
    centroid_init =  [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    stop_criteria = (cv2.TERM_CRITERIA_EPS
                     + cv2.TERM_CRITERIA_MAX_ITER, 10, .001)
    args = parse_args()

    print("I'm Loading...", flush = True)


    files = glob(args.folder + '/*{}'.format(args.format))
    stks = []
    for f in tqdm(files) :

        img = read_image(f)
        # create the mask to remove the background
        mask = threshold(img, 4000, 1)
        # filter all the images, normalize and convert to numpy array
        he = normalize(adaptive_histogram_equalization(img, 2))
        med = normalize(median_filter(img, 3))
        std = normalize(std_filter(img, 3))
        gamma = normalize(adjust_gamma(img, 1.5))

        he = sitk.GetArrayFromImage(he)
        med = sitk.GetArrayFromImage(med)
        std = sitk.GetArrayFromImage(std)
        gamma = sitk.GetArrayFromImage(gamma)
        mask = sitk.GetArrayFromImage(mask)

        stk = np.stack([he, med, gamma, std, mask], axis = -1)
        stks.append(stk)
    imgs = np.concatenate(stks)

    n_imgs = imgs.shape[0]


    print('Loaded {:d} files from {}\n'.format(len(files),args.folder),
            flush=True)

    imgs = shuffle_and_split(imgs, args.n)
    #Recap for better parameters control
    print('*****Starting clustering*****',flush=True)
    print('\tNumber of subsamples--> {:d}'.format(args.n) , flush=True)
    print('\tTotal images --> {:d}'.format(n_imgs), flush=True)
    print('\tCentroid initialization technique--> {}'.format(init[args.init]),
            flush=True)

    #First clustering
    print("\nI'm clustering...", flush = True)
    ret, centr = kmeans_on_subsamples(imgs,
                                  5,
                                  stop_criteria,
                                  centroid_init[args.init],
                                  True)

    center = centr[np.argmin(ret)]
    center = center[center[:, 0].argsort()]
    print("I'm saving..." , flush=True)
    save_pickle(args.out, center)


if __name__ == '__main__' :
    start = time()
    main()
    stop = time()
    print('[DONE] Total time: {:f} seconds'.format((stop - start)))
