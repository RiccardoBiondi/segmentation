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
                'healthy lung': [1.0291475, 1.7986686, 1.3147535, 1.6199226],
                'lung'   :  [2.4449115, 2.8337748, 1.556249,  2.9394238],
                'Edges' :  [3.4244044, 2.1809669, 4.172402,  3.652266 ],
                'GGO'   :  [5.1485806, 5.3843336, 2.7543516, 4.812335 ],
                'Noise'     : [8.233303,  1.9194404, 6.503928,  6.670035 ]}


if __name__ == '__main__':
    start = time()
    args = parse_args()
    volume = read_image(filename=args.input)

    if args.center != '' :
        center = load_pickle(filename=args.center)
    else :
        center = np.asarray([np.array(v) for _, v in centroids.items()])

    lung = lung_extraction.main(volume)
    labels = labeling.main(lung, center)


    write_volume(image=labels, output_filename=args.output)
    stop = time()
    print('Process anded after {0:.3} seconds'.format((stop - start)))
