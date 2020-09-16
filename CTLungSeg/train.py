#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import argparse
import numpy as np

from glob import glob
from tqdm import tqdm

from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import subsamples

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it']


def parse_args():
    description = 'kmeans clustering training'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='folder', required=True, type=str, action='store', help='Input folder')
    parser.add_argument('--output', dest='out', required=True, type=str, action='store', help='dst folder')
    parser.add_argument('--n', dest='n', required=False, type=int, action='store', help='number of subsamples', default=100)
    parser.add_argument('--init', dest='init', required=False, type=int, action='store', help='centroid initialization technique', default=0)

    args = parser.parse_args()
    return args


def main():
    init = [ "KMEANS_RANDOM_CENTERS", "KMEANS_PP_CENTERS"]
    centroid_init =  [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    iter_stop_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    args = parse_args()
    #read files and create the sample vector
    print('Loading...', flush=True )

    files = sorted(glob(args.folder + '/*.pkl.npy'))
    imgs = np.concatenate(np.array([load_image(f) for f in files]))

    print('Loaded {:d} files from {}'.format(len(files), args.folder), flush=True)

    samples = subsamples(imgs, args.n)
    #Recap for better parameter control
    print('*****Starting custering*****', flush=True)
    print('Number of subsamples--> {:d}'.format(args.n) , flush=True)
    print('Total images --> {:d}'.format(imgs.shape[0]), flush=True)
    print('Centroid initzialization technique--> {}'.format(init[args.init]), flush=True)


    centroids = []
    for i,el in enumerate(tqdm(samples)) :
        to_cluster = np.concatenate([x.reshape((-1,1)) for x in el])
        _, _, centr = cv2.kmeans(to_cluster.astype(np.float32), 4, None, iter_stop_criteria, 10, centroid_init[args.init])
        centroids.append(np.array(centr))


    print("\nStarting second clustering", flush=True)

    centroids = np.array(centroids).reshape((-1,1))
    _, _, centr = cv2.kmeans(centroids, 4, None, iter_stop_criteria, 10, centroid_init[args.init])
    save_pickle(args.out, centr)

    print('[DONE]', flush =True)

if __name__ == '__main__' :
    main()
