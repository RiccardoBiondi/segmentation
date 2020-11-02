#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
import numpy as np

from glob import glob
from time import time

from CTLungSeg.utils import read_image, save_pickle
from CTLungSeg.utils import shuffle_and_split, hu2gl, normalize
from CTLungSeg.method import std_filter
from CTLungSeg.method import median_blur, canny_edge_detection
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

    # kmeans clustering
    init = [ "KMEANS_RANDOM_CENTERS", "KMEANS_PP_CENTERS"]
    centroid_init =  [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    stop_criteria = (cv2.TERM_CRITERIA_EPS
                     + cv2.TERM_CRITERIA_MAX_ITER, 10, .001)
    args = parse_args()

    print("I'm Loading...", flush = True)


    files = glob(args.folder + '/*{}'.format(args.format))

    imgs = np.concatenate(np.array(list(map(lambda f : hu2gl(read_image(f)[0]), files))))
    # convert to multichannel
    edge_map = canny_edge_detection(imgs, 241, 25)
    imgs = np.stack([
                    normalize(imgs),
                    normalize(median_blur(imgs, 11)),
                    normalize(std_filter(imgs, 7)),
                    median_blur(edge_map, 9),
                    (imgs != 0).astype(np.uint8)], axis = -1)
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
    center = kmeans_on_subsamples(imgs,
                                  4,
                                  stop_criteria,
                                  centroid_init[args.init],
                                  True)
    # clustering refinement
    _, _, center = cv2.kmeans(center.reshape((-1,4)),
                              4, None,
                              stop_criteria,
                              10,
                              centroid_init[args.init])
    center = center[center[:, 0].argsort()]
    print("I'm saving..." , flush=True)
    save_pickle(args.out, center)


if __name__ == '__main__' :
    start = time()
    main()
    stop = time()
    print('[DONE] Total time: {:f} seconds'.format((stop - start)))
