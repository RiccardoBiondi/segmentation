import cv2
import numpy as np
import pandas as pd
import argparse
from segmentation.method import rescale, load_pickle, save_pickle, erode, dilate, connectedComponentsWithStats, bitwise_not, to_dataframe, imfill


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

#definition of some useful functions



def parse_args():
    description = 'Lung Segmentation'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--output', dest='output', required=False, type=str, action='store', help='Output filename', default='')
    parser.add_argument('--body_thr', dest='body_thr', required=False, type=float, action='store', help='Threshold to apply for the patient body segmentation', default=0.1)
    parser.add_argument('--lung_thr', dest='lung_thr', required=False, type=float, action='store', help='Threshold to apply for the patient lung segmentation', default=0.2)
    #Add area small spots

    args = parser.parse_args()

    return args


def main():

    args = parse_args()
    dicom = load_pickle(args.filename)
    #remove the tube
    dicom[dicom < 0] = 0
    dicom = rescale(dicom, dicom.max(), 0)
    #find a body mask
    th= np.where(dicom < args.body_thr, 0, 1)
    ret, labels, stats, centroid = connectedComponentsWithStats(th)
    #organize stats
    columns = ['TOP', 'LEFT', 'WIDTH', 'HEIGHT', 'AREA']
    stats = to_dataframe(stats, columns)
    #create a binary image
    for i in range(len(stats)):
        stats[i].sort_values('AREA', inplace=True, ascending=False)
        stats[i].drop(stats[i].query('TOP == 0 and LEFT == 0').index, inplace=True)
        labels[i][labels[i] != stats[i].index[0]] = 255
        labels[i][labels[i] == stats[i].index[0]] = 0
    #filling the remaining holes
    kernel = np.ones((3, 3), np.uint8)
    labels = erode(labels, kernel)
    labels = bitwise_not(labels)
    labels = imfill(labels)
    kernel = np.ones((20, 20), np.uint8)
    labels = erode(labels.astype('uint8'), kernel, iterations=1)

    #start to find lung Mask
    #connected components
    dicom = dicom * np.where(labels != 0, 1,0)
    th= np.where(((dicom < args.lung_thr) & (dicom > 0)), 1, 0)
    ret, lung, stats, centroids = connectedComponentsWithStats(th.astype('uint8'))
    kernel = np.ones((5, 5), np.uint8)
    stats = to_dataframe(stats, columns)
    for i in range(len(stats)):
        for j in stats[i].query('AREA <10').index:
            lung[i][lung[i] == j] = 0
    lung = np.where(lung != 0, 1, 0)
    lung = dilate(lung, kernel)
    lung = imfill(lung.astype('uint8'))

    save_pickle(args.output, lung)


if __name__ == '__main__' :
    main()
