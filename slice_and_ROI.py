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
    return(im.astype(float) - min) * (1. / (max - min))



#read data

blur_files =  sorted(glob('./results/*_blur.pkl.npy'))

trackbar_low= 'lower slice'
trackbar_high = 'higher slice'

for i in blur_files :
    blur = load(i)
    blur = blur.astype('uint8')
    id = os.path.basename(i).replace('_blur.pkl.npy','')

    cv2.namedWindow(id)

    def on_trackbar(val):
        cv2.imshow(id , blur[val])
    #create the trackbar for the lower slicec selection
    cv2.createTrackbar(trackbar_low  , id , 0 , blur.shape[0]-1 , on_trackbar)
    cv2.createTrackbar(trackbar_high , id , 0 , blur.shape[0]-1 , on_trackbar)
    key = cv2.waitKey(0)
    if key == ord('P') :
        low_value  = cv2.getTrackbarPos(trackbar_low  , id)
        high_value = cv2.getTrackbarPos(trackbar_high , id)
    cv2.destroyAllWindows()

    crop = blur[low_value : high_value, : ,: ]

    #sace the results
    np.save("./results/"+id+"_crop.pkl.npy",crop)
