import numpy as np
import argparse
from segmentation.utils import load_pickle, save_pickle
from segmentation.utils import to_dataframe
from segmentation.method import connectedComponentsWithStats
from segmentation.method import corner_finder

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
    lung = np.where(lung == 0, 0, 1)
    #find connected components
    ret, labels, stats, _ = connectedComponentsWithStats(lung.astype('uint8'))
    #manage stats into dataframe
    columns = ['LEFT', 'TOP', 'WIDTH', 'HEIGHT', 'AREA']
    stats = to_dataframe(stats, columns)
    #for each slice find the upper left and lower righ corner
    corners = []
    for stat in stats:
        corners.append(corner_finder(stat))
    corners = np.array(corners, dtype= np.int16)
    save_pickle(args.output, corners)


if __name__ == '__main__' :
    main()
