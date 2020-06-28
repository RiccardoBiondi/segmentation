import cv2
import os
import numpy as np
import pylab as plt
import pandas as pd
import pickle
from glob import glob

def load (filename):
    with open(filename, 'rb') as fp:
        data = np.load(fp)
    return data

def rescale(im,max,min):
    return(im.astype(float) - min) * (1. / (max - min))

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
    return [ret, labels,stats]


def ROI (img, stats):
    """
    Select the smaller rectangular region of the image that contain the lung.
    Return a list of cropped images
    img   -> Imput stack of images
    stats -> list that contanins all the ndarrays with the stats beloging from
    connectedComponentsWithStats function.
    """

    crop = []
    for i in range(img.shape[0]):

        stats[i] = pd.DataFrame(stats[i], columns=['LEFT','TOP', 'WIDTH', 'HEIGHT', 'AREA'])
        stats[i] = stats[i].drop([0], axis = 0) #remove the background label
        x_top = stats[i].min(axis = 0)['LEFT']
        y_top = stats[i].min(axis = 0)['TOP']
        x_bottom = np.max(stats[i]['LEFT']+stats[i]['WIDTH'])
        y_bottom = np.max(stats[i]['TOP']+stats[i]['HEIGHT'])
        crop.append(img[i,y_top:y_bottom,x_top:x_bottom])
    return crop

#read data

blur_files =  sorted(glob('./results/*_blur.pkl.npy'))
lung_files = sorted(glob('./results/*_lung.pkl.npy'))

trackbar_first= 'first slice'
trackbar_last = 'last slice'

for i in range(len(blur_files)) :
    blur = load(blur_files[i])
    lung = load(lung_files[i])
    blur = blur.astype('uint8')
    lung = lung.astype('uint8')
    id = os.path.basename(blur_files[i]).replace('_blur.pkl.npy','')

    cv2.namedWindow(id)

    def on_trackbar(val):
        cv2.imshow(id , blur[val])
    #create the trackbar for the lower slicec selection
    cv2.createTrackbar(trackbar_first  , id , 0 , blur.shape[0]-1 , on_trackbar)
    cv2.createTrackbar(trackbar_last , id , 0 , blur.shape[0]-1 , on_trackbar)
    key = cv2.waitKey(0)
    #TODO : add a text box to explain how to
    if key == ord('P') :
        first  = cv2.getTrackbarPos(trackbar_first  , id)
        last = cv2.getTrackbarPos(trackbar_last , id)
    cv2.destroyAllWindows()

    blur_cropped = blur[first : last, : , :]
    lung_cropped = lung[first : last, : , :]

    ret, prova, stats= connectedComponentsWithStats(lung_cropped.astype('uint8'))


    select = ROI(lung_cropped,stats)

    cv2.namedWindow('ROI')
    def show(val):
        cv2.imshow('ROI',select[val])

    cv2.createTrackbar('mm', 'ROI' , 0 , len(select)-1 , show)
    cv2.waitKey(0)






    #save the results
    #np.save("./results/"+id+"_blur_cropped.pkl.npy",blur_cropped)
    #np.save("./results/"+id+"_lung_cropped.pkl.npy",blur_cropped)

    #trova le regioni connesse
    #usa le stats per trovare la roi giusta
