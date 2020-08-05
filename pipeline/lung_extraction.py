import cv2
import numpy as np
import pandas as pd
import argparse
from segmentation.method import load_pickle, save_pickle
from segmentation.method import erode, dilate, imfill
from segmentation.method import rescale,medianBlur
from segmentation.method import otsu


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Lung Segmentation'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='input', required=True, type=str, action='store', help='Input filename, must be .pkl.npy format')
    parser.add_argument('--output', dest='output', required=True, type=str, action='store', help='Masked image filename')
    parser.add_argument('--lung', dest='lung', required=False, type=str, action='store', help='Lung mask filename')

    args = parser.parse_args()
    return args




def main():

    args = parse_args()

    DICOM = load_pickle(args.input)
    DICOM[DICOM < 0] = 0
    DICOM = (255 * rescale(DICOM, DICOM.max(), 0)).astype(np.uint8)
    imgs = DICOM.copy()
    DICOM = medianBlur(DICOM, 5)

    imgs = otsu(imgs)
    kernel = np.ones((5,5), dtype = np.uint8)
    imgs = erode(imgs, kernel)
    imgs = dilate(imgs, kernel)
    kernel = np.ones((11,11), dtype = np.uint8)
    imgs = erode(imgs, kernel)
    imgs = dilate(imgs, kernel)
    #body mask
    body = imgs.copy()
    body = imfill(body)
    body = np.where(body == 255, 1, 0)
    #lung mask
    imgs = np.where(imgs == 0, 1, 0)
    imgs = imgs * body
    #apply mask
    DICOM = DICOM * imgs
    DICOM = rescale(DICOM, DICOM.max(),0)
    if args.lung != '' :
        save_pickle(args.lung, imgs.astype(np.uint8))
    save_pickle(args.output, DICOM.astype(np.float32))




if __name__ == '__main__' :
    main()
