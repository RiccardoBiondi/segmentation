#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np

from time import time

from CTLungSeg.utils import read_image, write_volume, load_pickle


from CTLungSeg import labeling
from CTLungSeg import lung_extraction

def parse_args() :
    description = 'ggo identifications'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--input',
                        dest='input',
                        required=True,
                        type=str,
                        action='store',
                        help='Input filename')
    parser.add_argument('--output',
                        dest='output',
                        required=True,
                        type=str,
                        action='store',
                        help='output filename')
    parser.add_argument('--centroids',
                        dest='center',
                        required=False,
                        type=str,
                        action='store',
                        default='')

    args = parser.parse_args()
    return args





#pre-trainded centroids:
centroids = {
                'parenchima' : [1.425793, 2.0734222, 1.4296921, 0.],
                'bronchi'    : [3.3890672, 4.4695177, 1.8599507, 255.],
                'GG0'        : [4.9716797, 6.632072, 2.2960727, 0.],
                'noise'      :  [ 6.169081, 2.0313184, 4.8563914, 0.]
                }


if __name__ == '__main__':
    start = time()
    args = parse_args()
    volume, info = read_image(args.input)

    if args.center != '' :
        center = load_pickle(args.center)
    else :
        center = np.asarray([np.array(v) for k, v in centroids.items()])

    lung = lung_extraction.main(volume)
    labels = labeling.main(lung, center)

    write_volume(labels, args.output, info, '.nrrd')
    stop = time()
    print('Process anded after {} seconds'.format((stop - start)))
