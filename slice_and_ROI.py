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
    return(im.astype(float)-min)*(1./(max-min))ù


#read data

blur_files =  sorted(glob('./results/*_lung.pkl.npy'))

for i in blur_files :
    blur = load(i)
    id = os.path.basename(dicom_files[i]).replace('_blur.pkl.npy','')
