import cv2
import os
import numpy as np
import pylab as plt
import pandas as pd
from glob import glob


def load (filename):
    with open(filename, 'rb') as fp:
        data = np.load(fp)
    return data

def rescale(im,max,min):
    return(im.astype(float)-min)*(1./(max-min))

def apply_blurring(img) :
    """
    extend cv2.medianBlur on a stack of images and subtract the blurred image
    to the original one
    img -> input stack of images
    """
    blur = np.empty(img.shape, dtype= np.uint8)
    res = np.empty(img.shape, dtype = np.uint8)
    for i in range(blur.shape[0]):
        blur[i] = cv2.medianBlur(img[i], 5)
        res[i] = (masked[i] - blur[i])**2
    return [res,blur]


def erode(img , kernel, iterations = 1):
    """
    extension of cv2.erosion for a tensor of images
    img -> image tensor
    """
    for i in range(img.shape[0]):
        img[i] = cv2.erode(img[i], kernel, iterations)
    return img


#starting the algorithm
dicom_files = sorted(glob('./data/*[0-9].pkl.npy'))
lung_files  = sorted(glob('./results/*_lung.pkl.npy'))

for i in range(len(dicom_files)):
    lung  = load(lung_files[i])
    dicom = load(dicom_files[i])

    id = os.path.basename(dicom_files[i]).replace('.pkl.npy','')

    dicom[dicom < 0] = 0
    dicom = rescale(dicom, dicom.max(), 0)

    #select lung
    masked = dicom * np.where(lung != 0, 1, 0)
    masked = (masked * 255).astype('uint8')

    res,blur = apply_blurring(masked)

    kernel = np.ones((14, 14), np.uint8)
    masked = erode(lung.astype('uint8'), kernel, iterations=1)

    res = res * np.where(masked != 0, 1, 0)
    blur = blur * np.where(masked != 0, 1, 0)

    np.save("./results/"+idx+"_blur.pkl.npy",blur)
    np.save("./results/"+idx+"_res.pkl.npy",res)
