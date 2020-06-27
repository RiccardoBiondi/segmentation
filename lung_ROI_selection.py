import cv2
import os
import numpy as np
import pylab as plt
import pandas as pd
from glob import glob


#definition of some useful functions

def rescale (im, max, min):
    return (im.astype(float) - min) * (1. / (max - min))


def imfill (im_th):
    # Copy the thresholded image.
    im_th = np.pad(im_th, pad_width=((1, 1), (1, 1)),
                  mode='constant', constant_values=(0., 0.))
    im_floodfill = im_th.copy()
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_floodfill.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv
    return im_out[1:-1, 1:-1]


def load(filename):
    with open(filename, 'rb') as fp:
        data = np.load(fp)
    return data



def connectedComponentsWithStats(img):
    """
    extension of cv2.connectedComponentsWithStats to images tensor
    img-> stack of input images
    """
    ret = []
    labels = np.empty(img.shape)
    stats = []
    for i in range(img.shape[0]):
        t_ret, t_labels, t_stats, _ = cv2.connectedComponentsWithStats(img[i].astype('uint8'))
        ret.append(t_ret)
        labels[i] = t_labels
        stats.append(t_stats)
    return [ret, labels,stats]



def background_discriminator(stats , labels):
    """
    set the GL of the background region to 0 and the other to 255
    stats -> list of stats from connectedComponentsWithStats
    labels -> labels tensor from connectedComponentsWithStats
    """
    lab = np.empty(labels.shape)
    #ordina le stats in a dataframe
    for i in range(labels.shape[0])  :
        stats[i] = pd.DataFrame(stats[i], columns=['TOP', 'LEFT', 'WIDTH', 'HEIGHT', 'AREA'])
        stats[i].sort_values('AREA', inplace=True, ascending=False)
        stats[i].drop(stats[i].query('TOP == 0 and LEFT == 0').index, inplace=True)
        t_labels = labels[i]
    #divide in large connected area and others
        t_labels[t_labels != stats[i].index[0]] = 255
        t_labels[t_labels == stats[i].index[0]] = 0
        lab[i] = t_labels
    return lab



def filling(img, kernel) :
    """
    Used to fill holes in stack of binary images
    img -> stack of images
    kernel -> kernel for erosion operation
    """
    t_labels = np.empty(img.shape, dtype = np.uint8)
    for i in range(img.shape[0]):
        t_labels[i] = cv2.erode(img[i].astype('uint8'), kernel, iterations=1)
        t_labels[i] = cv2.bitwise_not(t_labels[i])
        t_labels[i] = imfill(t_labels[i])
    return t_labels


def filter_out_small_spots(img , stats, kernel) :
    for i in range(img.shape[0]):
        stats[i] = pd.DataFrame(stats[i], columns=['TOP', 'LEFT', 'WIDTH', 'HEIGHT', 'AREA'])
        for j in stats[i].query('AREA < 10').index:
            img[i][img[i] == j] = 0
        img[i] = np.where(img[i] != 0, 1, 0)
        img[i] = cv2.dilate(img[i].astype('uint8'), kernel, iterations=1)
        img[i] = imfill(img[i].astype('uint8'))
    return img


def erode(img , kernel, iterations = 1):
    """
    extension of cv2.erosion for a tensor of images
    img -> image tensor
    """
    for i in range(img.shape[0]):
        img[i] = cv2.erode(img[i], kernel, iterations)
    return img


#read the data and organiza them into a DataFrame
dicom_files = sorted(glob('./data/*[0-9].pkl.npy'))



#starting the elaboration
for Id in dicom_files:

    dicom = load(Id)
    #remove the tube
    dicom[dicom < 0] = 0
    dicom = rescale(dicom, dicom.max(), 0)

    #find a body mask
    th= np.where(dicom < 0.1, 0,1)
    ret, labels, stats = connectedComponentsWithStats(th)
    labels = background_discriminator(stats, labels)

    kernel = np.ones((3,3), np.uint8)
    labels = filling(labels, kernel)
    kernel = np.ones((20, 20), np.uint8)
    labels = erode(labels.astype('uint8'), kernel, iterations=1)
    #now I've created a mask for the patient body

    #TODO:
    #saving the results on results folder

    #isolate the lung
    dicom = dicom * np.where(labels != 0, 1,0)
    th= np.where(((dicom < 0.2) & (dicom > 0)), 1, 0)
    ret, lung, stats= connectedComponentsWithStats(th.astype('uint8'))

    kernel = np.ones((5, 5), np.uint8)
    lung = filter_out_small_spots(lung, stats,kernel)


    #TODO save mask to results

    #find lung mask
        #save results



#define roi
    #save results
