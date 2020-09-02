import numpy as np
import argparse
from segmentation.utils import load_image, save_pickle
from segmentation.utils import preprocess, rescale
from segmentation.method import erode, dilate
from segmentation.method import imfill, remove_spots
from segmentation.method import medianBlur, gaussianBlur,otsu


__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def parse_args():
    description = 'Lung Segmentation'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='input', required=True, type=str, action='store', help='Input filename, must be .pkl.npy format')
    parser.add_argument('--lung', dest='lung', required=True, type=str, action='store', help='Masked image filename')
    parser.add_argument('--mask', dest='mask', required=False, type=str, action='store', help='Lung mask filename', default='')
    parser.add_argument('--int_spot_area', dest='isa', required=False, type=int, action='store', default=700, help='minimum internal spot area')
    parser.add_argument('--ext_spot_area', dest='esa', required=False, type=int, action='store', default=200, help='minimum external spot area')

    args = parser.parse_args()
    return args




def main():

    args = parse_args()
    DICOM = load_image(args.input)
    DICOM = preprocess(DICOM)
    imgs = DICOM.copy()
    #DICOM = medianBlur(DICOM, 5)
    DICOM = gaussianBlur(DICOM, (5,5))

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
    #refine the mask
    imgs = np.where(imgs == 0, 1, 0)
    imgs = remove_spots(imgs, args.isa)
    imgs = np.where(imgs == 0, 1, 0)
    #filter out small external spots
    imgs = remove_spots(imgs, args.esa)
    #apply mask
    DICOM = DICOM * imgs
    DICOM = rescale(DICOM, DICOM.max(),0)
    DICOM = DICOM * imgs

    if args.mask not in ['', None] :
        save_pickle(args.mask, imgs.astype(np.uint8))
    save_pickle(args.lung, DICOM.astype(np.float32))




if __name__ == '__main__' :
    main()
