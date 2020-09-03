#!/usr/bin/env python

import cv2
import argparse
import progressbar
import numpy as np
from glob import glob
from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import subsamples

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it']


def parse_args():
    description = 'kmeans clustering training'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='folder', required=True, type=str, action='store', help='Input folder')
    parser.add_argument('--output', dest='out', required=True, type=str, action='store', help='dst folder')
    parser.add_argument('--k', dest='k', required=False, type=int, action='store', help='number of clusters', default=4)
    parser.add_argument('--n', dest='n', required=False, type=int, action='store', help='number of subsamples', default=100)
    parser.add_argument('--init', dest='init', required=False, type=int, action='store', help='centroid initialization technique', default=0)
    parser.add_argument('--intermediate', dest='intermediate', required=False, type=bool, action='store', help='chose if save or not the intermediate centroids', default=False)

    args = parser.parse_args()
    return args


def main():
    init =  [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    args = parse_args()
    #read files and create the sample vector
    print('Loading...', flush=True )

    files = sorted(glob(args.folder + '/*.pkl.npy'))
    imgs = np.concatenate(np.array([load_image(f) for f in files]))

    print('Loaded ', len(files), ' files from ', args.folder, flush=True)

    samples = subsamples(imgs, args.n)
    #Recap for better parameter control
    print('*****Starting custering*****', flush=True)
    print('Number of custers-->', args.k , flush=True)
    print('Number of subsamples-->', args.n , flush=True)
    print('Total images --> ', imgs.shape[0])
    print('Centroid initzialization technique-->', str(init[args.init]), flush=True)
    print('Save intermediate centroids-->', args.intermediate , flush=True)
    #first clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    centr = []

    widgets = ['Computing:', progressbar.Bar('*')]
    bar = progressbar.ProgressBar(widgets=widgets).start()

    for i,el in enumerate(samples) :
        for x in el :
            sample = np.concatenate(x.reshape(-1, 1))
        sample = sample.astype(np.float32)
        _, labels, centroids = cv2.kmeans(sample, args.k, None, criteria, 10,init[args.init])
        centr.append(np.array(centroids))
        if args.intermediate :#non molto performante
            save_pickle(args.out + '('+str(i)+')', centroids)
        bar.update(i)

    #starting the second clustering
    print("\nStarting second clustering", flush=True)

    centr = np.array(centr).reshape(-1,)
    ret, labels, centroids = cv2.kmeans(centr, args.k, None, criteria, 10, init[args.init])
    save_pickle(args.out, centroids)

    print('Complete', flush =True)

if __name__ == '__main__' :
    main()
