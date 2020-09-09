#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

import CTLungSeg.utils as utils
from CTLungSeg.method import connected_components_wStats

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def opening(img, kernel):
    pass

def closing(img, kernel):
    pass

def remove_spots(img, area):
    '''Set to zero the GL of all the connected region with area lesser than area

    Parameters
    ----------
    img: array-like
        binary image from which remove spots
    area: int
        maximun area in pixels of the removed spots

    Returns
    -------
    filled: array-like
        binary image with spot removed
    '''
    columns = ['TOP', 'LEFT', 'WIDTH', 'HEIGHT', 'AREA']
    _, lab, stats, _ = connected_components_wStats(img.astype(np.uint8))

    stats = utils.to_dataframe(stats, columns)
    for i,stat in enumerate(stats):
        for j in stat.query('AREA <' + str(area)).index:
            lab[i][lab[i] == j] = 0

    lab = np.where(lab == 0, 0, 1)
    return lab.astype(np.uint8)


def select_greater_connected_regions(img, n_reg):
    pass

def reconstruct_gg_areas(imgs):
    pass

def find_ROI(stats) :
    '''Found the upper and lower corner of the rectangular ROI according to the connected region stats

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
    corner = np.array([stats.min(axis = 0)['LEFT'], stats.min(axis = 0)['TOP'], np.max(stats['LEFT'] + stats['WIDTH']), np.max(stats['TOP'] + stats['HEIGHT'])])

    return np.where(corner == np.nan, np.int16(0), np.int16(corner))
