import cv2
import argparse
import numpy as np
from sklearn.cluster import KMeans
from segmentation.method import load_pickle, save_pickle

__author__ = ['Riccado Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@tudio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Image labeling'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--centroids', dest='centroids', required=True, type=str, action='store', help='Centroids')
    parser.add_argument('--output', dest='out', required=True, type=str, action='store', help='output filename')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    images = load_pickle(args.filename)
    centroid = load_pickle(args.centroids)
    n_clusters = centroid.shape[0]

    shape = images.shape
    images = images.reshape((-1,1))
    res = KMeans(n_clusters=n_clusters, init=centroid, n_init=1).fit(images)

    save_pickle(args.out, res.labels_.reshape(shape))


if __name__ == '__main__' :
    main()
