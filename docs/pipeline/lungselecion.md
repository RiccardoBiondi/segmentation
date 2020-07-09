# Lung Selection
This script allows to create a mask for the lung and isolate them.
It takes as input the stack of images and performs the following operations :

* rescaling, to enhance contrast
* preliminary threshold followed by a connected components algorithm, filling operation and an erosion to isolate the body from the enviroment.
* second threshold followed by an hole filling and a dilation to isolates the lung from the rest of the body.

At the end of the execution the script save the lung and body mask as '.pkl.npy' in the output directory.

![](./images/dicom.png)

## Usage

To use this script call it from powershell or bash and provide the required arguments.

```
 python -m pipeline.lungselection --input='path to input file.pkl.npy' --lung='path to output file'
```

Required arguments:

* --input :str, path to input image or stack. the file must be in '.pkl.npy' format
* --lung :str, path to the output folder, here we be saved the lung mask in -pkl.npy format

The optional arguments:
* --body :str, path to output filename, if provided save the stasck of body mask
* --body_thr :float, threshold value for the body threshold
* --lung_thr :float, threshold value for the lung selection
