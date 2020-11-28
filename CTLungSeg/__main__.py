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
                'parenchima': [1.3822415, 2.4269834, 1.1459424, 1.832688 ],
                'edges'   : [1.6750793, 2.6646569, 3.829929 , 2.1440172],
                'Bronchi' : [3.4454546, 3.0228717, 1.9430293, 3.3130786],
                'Noise'   : [6.0392303, 2.7451596, 4.861056 , 5.6319346],
                'GGO'     : [6.359824 , 6.218402 , 3.42476  , 5.9504952]}


if __name__ == '__main__':
    start = time()
    args = parse_args()
    volume, info = read_image(args.input)

    if args.center != '' :
        center = load_pickle(args.center)
    else :
        center = np.asarray([np.array(v) for _, v in centroids.items()])

    lung = lung_extraction.main(volume, info)
    labels = labeling.main(lung, center)

    write_volume(labels, args.output, info, '.nrrd')
    stop = time()
    print('Process anded after {} seconds'.format((stop - start)))
