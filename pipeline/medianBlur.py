import cv2
import numpy as np
import pylab as plt
import pandas as pd
import argparse
from segmentation.method import load_pickle, save_pickle
from segmentation.method import erode, medianBlur, rescale

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__ = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def parse_args() :
    description = 'Median Blurring'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--mask', dest='mask', required=False, type=str, action='store', help='Lung mask filename', default = '')
    parser.add_argument('--output', dest = 'output', required= True, type=str, action='store', help='Output filename')
    parser.add_argument('--kernel_size', dest='kernel_size', required=False, type=int, action='store', help='Kernel Size', default = 14)
    parser.add_argument('--blur_ksize', dest='k_size', required=False, type=int, action='store', help ='blur apertur linear size, must be odd', default=5)

    args = parser.parse_args()
    return args




def main():
    args = parse_args()
    #load file
    dicom = load_pickle(args.filename)
    if args.mask !='' :
        lung = load_pickle(args.mask)
    else :
        lung = np.ones(dicom.shape)
    #rescale dicom
    dicom[dicom < 0] = 0
    dicom = rescale(dicom, dicom.max(), 0)
    #apply the mask
    masked = dicom * np.where(lung != 0, 1, 0)
    masked = (masked * 255).astype('uint8')

    blur = medianBlur(masked, args.k_size)
    #reapply a mask
    kernel = np.ones((args.kernel_size, args.kernel_size), np.uint8)
    masked = erode(lung.astype('uint8'), kernel, iterations=1)
    blur = blur * np.where(masked != 0, 1, 0)
    blur =255 * rescale(blur, blur.max(), 0)

    save_pickle(args.output, blur.astype('uint8'))


if __name__ == '__main__':
    main()
