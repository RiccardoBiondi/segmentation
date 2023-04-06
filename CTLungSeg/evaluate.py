import os
import argparse
import numpy as np
import pandas as pd
import SimpleITK as sitk

from CTLungSeg.utils import read_image

from CTLungSeg.metrics import dice
from CTLungSeg.metrics import recall
from CTLungSeg.metrics import precision
from CTLungSeg.metrics import specificity
from CTLungSeg.metrics import accuracy

__author__ = ['Riccado Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

def parse_args():
    description='Script to evaluate the goodness of the segmentation against the ground truth'

    parser = argparse.ArgumentParser(description=description)

    _ = parser.add_argument('--gt',
                            dest='gt',
                            action='store',
                            type=str,
                            required=True,
                            help='Path to the ground truth image')
    
    _ = parser.add_argument('--pred',
                            dest='pred',
                            action='store',
                            type=str,
                            required=True,
                            help='Path to the predicted image to evaluate')
    
    _ = parser.add_argument('--output',
                            dest='output',
                            action='store',
                            type=str,
                            required=False,
                            default=None,
                            help='Path to the output .csv file  to store the evaluation results')
    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    # read the images
    gt = read_image(args.gt)
    pred = read_image(args.pred)

    # convert to array

    gt = sitk.GetArrayFromImage(gt)
    pred = sitk.GetArrayFromImage(pred)


    # and compute all the required metrics

    metrics_dict = {
                "ground truth": [args.gt],
                "prediction": [args.pred],
                "dice score": [dice(gt, pred)],
                "recall": [recall(gt, pred)],
                "precision": [precision(gt, pred)],
                "specificity": [specificity(gt, pred)],
                "accuracy": [accuracy(gt, pred)]
                }
    
    # and display the metrics
    print(f'**Evaluation Results**')
    for key, val in metrics_dict.items():
        print(f'\t{key}: {val[-1]}')

    # now save the output results
    # if specified, check the output file validity
    
    if args.output is not None:
        ext = args.output.split('.')[-1]
        # check it is a .csv
        if ext != 'csv':
            raise ValueError(f'output file must be a .csv, received .{ext} instead')
        
        # and save the results
        df = pd.DataFrame().from_dict(metrics_dict)
        _ = df.to_csv(args.output, sep=',', index=False)

if __name__ == '__main__':
    main()