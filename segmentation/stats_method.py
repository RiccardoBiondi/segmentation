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


def background_discriminator(img, stats):
    '''
    discriminate the background to othe object in a single binary image according to stats provided by connectedComponentsWithStats

    Parameters
        ----------
    img: array-like
        binary image from which separate the background from the rest of the image
    stats: pandas DataFrame
        stats provided by connectedComponentsWithStats function

    Return
    ------
    out: array-like
        image in which the background GL is set to zero and the other object to 255
    '''
    out = img.copy()
    stats.sort_values('AREA', inplace=True, ascending=False)
    stats.drop(stats.query('TOP == 0 and LEFT == 0').index, inplace=True)
    out[out != stats.index[0]] = 255
    out[out == stats.index[0]] = 0
    return out.astype('uint8')


def fill_spots(img, stats, area):
    '''
    fill all the spots with area less than a specified values

    Parameters
    ----------
    img: array_like
        binary image to fill
    stats: pandas dataframe
        stats provided by cv2.conncetedComponentsWithStats function
    area: int
        minimum spot area allowed

    Return
    ------
    filled: array-like
        binary image with filled small spots
    '''
    filled = img.copy()
    for j in stats.query('AREA <' +str(area)).index :
        filled[filled == j ] = 0
    return filled



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
