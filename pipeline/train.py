import os
import cv2
import argparse
import numpy as np
from glob import glob
from segmentation.method import load_pickle, save_pickle


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it']


def parse_args():
    description = 'kmeans clustering training'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='folder', required=True, type=str, action='store', help='Input folder')
    parser.add_argument('--output', dest='out', required=True, type=str, action='store', help='dst folder')
    parser.add_argument('--ROI', dest='ROI', required=False, type=str, action='store', help='Folder with ROI files', default='')
    parser.add_argument('--k', dest='k', required=False, type=int, action='store', help='number of clusters', default=4)
    parser.add_argument('--n', dest='n', required=False, type=int, action='store', help='number of subsamples', default=100)
    parser.add_argument('--init', dest='init', required=False, type=int, action='store', help='centroid initialization technique', default=0)
    parser.add_argument('--intermediate', dest='intermediate', required=False, type=bool, action='store', help='chose if save or not the intermediate centroids', default=False)

    args = parser.parse_args()
    return args


def main():
    init =  [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    args = parse_args()

    files = sorted(glob(args.folder + '/*.pkl.npy'))


    imgs = np.concatenate([load_pickle(f) for f in files])

    #TODO add ROI selection
    sub_size = int(len(imgs)/args.n)
    sub = []
    length = np.arange(0, len(imgs) + 1 , sub_size)
    #TODO: find a better way to split the subsamples
    for i in range(args.n) :
        sub.append(list([imgs[j] for j in range(length[i], length[i+1])]))
    #first clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    centr = []
    for i,el in enumerate(sub) :
        sample = np.concatenate([x.reshape(-1, 1) for x in el]).astype(np.float32)
        ret, labels, centroids = cv2.kmeans(sample, args.k, None, criteria, 10,init[args.init])
        centr.append(np.array(centroids))
        if args.intermediate :#non molto performante
            save_pickle(args.out + '('+str(i)+')', centroids)

    #starting the second clutering
    centr = np.array(centr).reshape(-1,)
    ret, labels, centroids = cv2.kmeans(centr, args.k, None, criteria, 10, init[args.init])
    save_pickle(args.out, centroids)


if __name__ == '__main__' :
    main()
