import cv2
import numpy as np
import argparse
from segmentation.utils import save_pickle, load_pickle


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it, nico.curti2@unibo.it']


def parse_args() :
    description = 'kmeans clustering'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--centroid', dest='output', required=True, type=str, action='store', help = 'output file for centroids')
    parser.add_argument('--ROI', dest='ROI', required=False, type=str, action='store', help=' ', default='')
    parser.add_argument('--labels', dest='labels', required=True, type=str, action='store', help='output file for labels')
    parser.add_argument('--n_clust', dest='K', required=False, type=int, action='store', help='number of cluster', default=4)
    parser.add_argument('--centr_init', dest='c_init', required=False,
    type=int, action='store', help='Centroid initialization technique', default=0)

    args = parser.parse_args()
    return args



def main() :
    args = parse_args()
    #load file and roi
    stack = load_pickle(args.filename)
    print(stack.shape)
    if args.ROI != '' :
        ROI = load_pickle(args.ROI)
        print(ROI.shape)

    else :
        S = np.array([0., 0., stack.shape[1], stack.shape[2]])
        print(S)
        ROI = np.full((stack.shape[0], 4), S, dtype=np.int16)
        print(ROI.shape)
    #arrange all images into a vector
    sample = np.float32(np.concatenate([stack[i, ROI[i,1]:ROI[i,3], ROI[i,0]:ROI[i,2]].reshape(-1,1) for i in range(stack.shape[0])]))

    sizes = list(np.cumsum(np.array([np.absolute((R[1] - R[3]) * (R[2] - R[0])) for R in ROI], dtype=np.int16)))

    #compute kmenas clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    init = [cv2.KMEANS_RANDOM_CENTERS, cv2.KMEANS_PP_CENTERS]
    _, labels, centroids = cv2.kmeans(sample, args.K, None, criteria, 10, init[args.c_init])

    save_pickle(args.output, centroids)
    #remap labels
    labels = np.split(labels, sizes)
    print(len(labels))
    labeled = []
    for i in range(ROI.shape[0]) :

        res = centroids[labels[i].flatten()]
        reshaped = res.reshape((np.absolute(ROI[i,3] - ROI[i,1]),np.absolute(ROI[i,2] - ROI[i,0])))
        #conctruct fullsize image
        output = np.zeros(stack[i].shape)
        output[ROI[i,1] : ROI[i,3] , ROI[i,0] : ROI[i,2]] = reshaped
        #set background to zero
        output = np.where(output < 0, 0, output)
        labeled.append(output)
    #save results
    save_pickle(args.labels, np.array(labeled).astype('uint8'))


if __name__ == '__main__' :
    main()
