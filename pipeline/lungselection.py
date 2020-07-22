import cv2
import numpy as np
import pandas as pd
import argparse
from segmentation.method import load_pickle, save_pickle
from segmentation.method import erode, dilate, imfill
from segmentation.method import connectedComponentsWithStats
from segmentation.method import bitwise_not, rescale
from segmentation.method import fill_holes
from segmentation.stats_method import background_discriminator
from segmentation.stats_method import fill_spots
from segmentation.stats_method import to_dataframe


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

#definition of some useful functions



def parse_args():
    description = 'Lung Segmentation'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--lung', dest='lungname', required=True, type=str, action='store', help='body mask output filename')
    parser.add_argument('--body', dest='bodyname', required=False, type=str, action='store', help='body mask output filename', default='')
    parser.add_argument('--body_thr', dest='body_thr', required=False, type=float, action='store', help='Threshold to apply for the patient body segmentation', default=0.1)
    parser.add_argument('--lung_thr', dest='lung_thr', required=False, type=float, action='store', help='Threshold to apply for the patient lung segmentation', default=0.2)
    parser.add_argument('--k_erosion', dest='k_er', required=False, type=int, action='store', help='Erosion kernel size', default=20)
    parser.add_argument('--min_hole_area', dest='area', required=False, type=int, action='store', help='', default=10)
    parser.add_argument('--k_dilation', dest='k_dil', required=False, type=int, action='store', help='Dilation kernel size', default=5)

    args = parser.parse_args()
    return args




def main():

    args = parse_args()
    dicom = load_pickle(args.filename)
    dicom[dicom < 0] = 0
    dicom = rescale(dicom, dicom.max(), 0)
    #find a body mask
    th= np.where(dicom < args.body_thr, 0, 1)

    ret, labels, stats, _ = connectedComponentsWithStats(th)
    columns = ['TOP', 'LEFT', 'WIDTH', 'HEIGHT', 'AREA']
    stats = to_dataframe(stats, columns)
    #create a binary
    for i in range(len(stats)):
        labels[i] = background_discriminator(labels[i], stats[i])
    #filling the remaining holes
    kernel = np.ones((3, 3), np.uint8)
    labels = fill_holes(labels, kernel)
    kernel = np.ones((args.k_er, args.k_er), np.uint8)
    labels = erode(labels.astype('uint8'), kernel, iterations=1)
    if args.bodyname != '':
        save_pickle(args.bodyname, labels)
    #start to find lung Mas
    dicom = dicom * np.where(labels != 0, 1,0)
    th= np.where(((dicom < args.lung_thr) & (dicom > 0)), 1, 0)
    ret, lung, stats, _ = connectedComponentsWithStats(th.astype('uint8'))
    stats = to_dataframe(stats, columns)
    kernel = np.ones((args.k_dil, args.k_dil), np.uint8)

    for i in range(len(stats)):
        lung[i] = fill_spots(lung[i], stats[i], args.area)
    lung = np.where(lung != 0, 1, 0)
    lung = dilate(lung, kernel)
    lung = imfill(lung.astype('uint8'))

    save_pickle(args.lungname, lung)


if __name__ == '__main__' :
    main()
