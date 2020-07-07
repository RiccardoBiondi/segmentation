import cv2
import numpy as np
import pandas as pd
import argparse
from functools import partial
from segmentation.method import save_pickle, load_pickle


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it, nico.curti2@unibo.it']


def parse_args() :
    description = 'kmeans clustering'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--ROI', dest='ROI', required=False, type=str, action='store', help=' ', default='')
    parser.add_argument('--output', dest='output', required=True, type=str, action='store', help = 'output file for centroids')
    parser.add_argument('--labels', dest='labels', required=True, type=str, action='store', help='output file for labels')
    parser.add_argument('--n_clust', dest='K', required=False, type=int, action='store', help='number of cluster', default=4)

    args = parser.parse_args()
    return args


def main() :
    args = parse_args()
    #load file and roi
    stack = load_pickle(args.filename)
    if args.ROI != '' :
        ROI = load_pickle(args.ROI)
    else :
        ROI = np.array([np.array([0., 0., stack.shape[1], stack.shape[2]])])
    #arrange all images into a vector
    sample = np.float32(np.concatenate([stack[i, ROI[i,1]:ROI[i,3], ROI[i,0]:ROI[i,2]].reshape(-1,1) for i in range(stack.shape[0])]))
    sizes =list(np.cumsum([np.absolute((R[1] - R[3]) * (R[2] - R[0])) for R in ROI]))
    #compute kmenas clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, labels, centroids = cv2.kmeans(sample, args.K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    #save centroids
    save_pickle(args.output, centroids)
    #remap labels

    labels = np.split(labels, sizes)
    labeled = []
    for i in range(ROI.shape[0]) :
        res = centroids[labels[i].flatten()]
        reshaped = res.reshape((np.absolute(ROI[i,3] - ROI[i,1]),np.absolute(ROI[i,2] - ROI[i,0])))
            #made the image complete
        output = np.zeros(stack[i].shape)
        output[ROI[i,1] : ROI[i,3] , ROI[i,0] : ROI[i,2]] = reshaped
        labeled.append(output)
    #save results
    save_pickle(args.labels, np.array(labeled))


if __name__ == '__main__' :
    main()
