import cv2
import numpy as np
import pandas as pd
import argparse
from segmentation.method import load_pickle, save_pickle
from segmentation.method import connectedComponentsWithStats
from segmentation.stats_method import corner_finder
from segmentation.stats_method import to_dataframe

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


def parse_args() :
    description = 'ROI selection'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input', dest='filename', required=True, type=str, action='store', help='Input filename')
    parser.add_argument('--output', dest='output', required=True, type=str, action='store', help='output filename')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    #load data
    lung = load_pickle(args.filename)
    #find connected components
    ret, labels, stats, _ = connectedComponentsWithStats(lung.astype('uint8'))
    #manage stats into dataframe
    columns = ['LEFT', 'TOP', 'WIDTH', 'HEIGHT', 'AREA']
    stats = to_dataframe(stats, columns)
    #for each slice find the upper left and lower righ corner
    corners = []
    for stat in stats:
        corners.append(corner_finder(stat))
    save_pickle(args.output, np.array(corners))


if __name__ == '__main__' :
    main()
