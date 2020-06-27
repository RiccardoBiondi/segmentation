# SEGMENTATION

## Contents

- lung_ROI_selection : Isolate body, lung and define a ROI which contains mainly the lungs

- medianBlur : Apply a median filter on the images tensor

- clustering : Apply a kmean clustering

## Usage
Before running the scripts you have to create 2 folders:
- data : which must contain the image tensors as '\*.pkl.npy'
- results : which must be empty

After that the script must be runned in the following order:
- lung_ROI_selection
- medianBlur
- clustering

Note: each script saves the output in the results folder
