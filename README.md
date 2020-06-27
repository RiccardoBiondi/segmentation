# SEGMENTATION

## Contents

- lungselection : Isolate body and lung regions and save the mask in results folder

- medianBlur : Apply a median filter on the images tensor

- slice_and_ROI : allow manual selection of slice and made an automatic ROI selection

- clustering : Apply a kmean clustering

## Usage
Before running the scripts you have to create 2 folders:
- data : which must contain the image tensors as '\*.pkl.npy'
- results : which must be empty

After that the script must be run in the following order:
- lungselection
- medianBlur
- slice_and_ROI
- clustering

Note: each script saves the output in the results folder
