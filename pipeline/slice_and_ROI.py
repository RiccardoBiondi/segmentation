import cv2
import os
import numpy as np
import pylab as plt
import pandas as pd
import tkinter
import pickle
from glob import glob

def load (filename):
    with open(filename, 'rb') as fp:
        data = np.load(fp)
    return data


def save(filename, list):
    with open(filename, 'wb') as f:
       pickle.dump(list, f)


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
    return [ret, labels, stats]


def ROI (img, stats):
    """
    Select the smallest rectangular region of the image which contain the lung.
    Return a list of cropped images
    img   -> Imput stack of images
    stats -> list that contanins all the ndarrays with the stats beloging from
    connectedComponentsWithStats function.
    """
    crop = []
    for i in range(img.shape[0]):
        stats[i] = pd.DataFrame(stats[i], columns=['LEFT','TOP', 'WIDTH', 'HEIGHT', 'AREA'])
        if (0 in stats[i].index.values) :
            stats[i] = stats[i].drop([0], axis = 0) #remove the background label
        x_top = stats[i].min(axis = 0)['LEFT']
        y_top = stats[i].min(axis = 0)['TOP']
        x_bottom = np.max(stats[i]['LEFT'] + stats[i]['WIDTH'])
        y_bottom = np.max(stats[i]['TOP'] + stats[i]['HEIGHT'])
        crop.append(img[i, y_top : y_bottom , x_top : x_bottom])
    return crop


def rescale (im, max, min):
    return (im.astype(float) - min) * (1. / (max - min))

#read data
dicom_files = sorted(glob('./data/*[0-9].pkl.npy'))
gg_files = sorted(glob('./data/*_gg.pkl.npy'))
blur_files =  sorted(glob('./results/*_blur.pkl.npy'))
res_files = sorted(glob('./results/*_res.pkl.npy'))
lung_files = sorted(glob('./results/*_lung.pkl.npy'))
message = 'Select the first and last slice of interes \n Press y to confirm and proceed'

trackbar_first = 'first slice'
trackbar_last  = 'last slice'


for i in range(len(blur_files)) :

    dicom = load(dicom_files[i])
    gg = load(gg_files[i])
    res = load(res_files[i])
    blur = load(blur_files[i])
    lung = load(lung_files[i])

    dicom[dicom < 0] = 0
    dicom = rescale(dicom, dicom.max(), 0)
    blur = blur.astype('uint8')
    lung = lung.astype('uint8')

    id = os.path.basename(blur_files[i]).replace('_blur.pkl.npy', '')

    cv2.namedWindow(id)
    tkinter.messagebox.showinfo(message = message)

    def on_trackbar(val):
        cv2.imshow(id, dicom[val])

    #create the trackbar for the lower slice selection
    cv2.createTrackbar(trackbar_first, id, 0, lung.shape[0]-1, on_trackbar)
    cv2.createTrackbar(trackbar_last, id, 0, lung.shape[0]-1, on_trackbar)

    key = cv2.waitKey(0)
    if key == ord('y') :
        first  = cv2.getTrackbarPos(trackbar_first, id)
        last = cv2.getTrackbarPos(trackbar_last, id)
    cv2.destroyAllWindows()

    dicom_cropped = dicom[first : last, :, :]
    gg_cropped = gg[first : last, :, :]
    res_cropped = res[first : last, :, :]
    blur_cropped = blur[first : last, :, :]
    lung_cropped = lung[first : last, :, :]

    ret, prova, stats = connectedComponentsWithStats(lung_cropped.astype('uint8'))

    blur_ROI = ROI(blur_cropped, stats)
    res_ROI = ROI(res_cropped, stats)
    lung_ROI = ROI(lung_cropped, stats)


    save('./results/' + id + '_blur_ROI.pkl.npy', blur_ROI)
    save('./results/' + id + '_res_ROI.pkl.npy', res_ROI)
    save('./results/' + id + '_lung_ROI.pkl.npy', lung_ROI)

    save('./results/' + id + '_dicom_cropped.pkl.npy', dicom_cropped)
    save('./results/' + id + '_gg_cropped.pkl.npy', gg_cropped)
