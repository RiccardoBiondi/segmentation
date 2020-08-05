import cv2
import numpy as np
import pandas as pd
from functools import partial

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studo.unibo.it', 'nico.curti2@unibo.it']




def to_dataframe (arr, columns) :
    '''
    Convert  3D numpy array into a list of pandas dataframes

    Parameter
    ---------
    arr: array-like
        input array to convert in a dataframe
    columns: list of string
        labels of the dataframe
    Return
    ------
    df: list of dataframe
        list of dataframe made from arr
    '''
    #if len(arr) == 2 :
        #return pd.DataFrame(arr, columns=columns)
    df = list(map(partial(pd.DataFrame, columns=columns), arr))
    return df


def corner_finder(stats) :
    '''
    Found the upper and lower corner of the rectangular ROI according to the connected region stats

    Parameter
    ---------
    stats: pandas dataframe
        dataframe that contains the stats of the connected regions

    Return
    ------
    corners: array-like
        array which contains the coordinates of the upper and lower corner of the ROI organized as [x_top, y_top, x_bottom, y_bottom]
    '''
    stats = stats.drop([0], axis = 0)
    x_top = stats.min(axis = 0)['LEFT']
    y_top = stats.min(axis = 0)['TOP']
    x_bottom = np.max(stats['LEFT'] + stats['WIDTH'])
    y_bottom = np.max(stats['TOP'] + stats['HEIGHT'])
    return np.array([x_top,y_top,x_bottom,y_bottom])
