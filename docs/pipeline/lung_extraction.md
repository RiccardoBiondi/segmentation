# Lung Extraction

This script allows to isolate the lung regions from the rest of the body in an image stack. To achieve this purpose it will use some threshold and morphological operation.

It takes as input the stack of images as *.pkl.npy* format.
At the end of the execution the script save the stack with the extracted lung as *.pkl.npy* format. It is also possible to chose to save or not the binary lung mask.

<p style="text-align:center;"><img src="./images/dicom.png" alt="dicom"
	title="dicom slice" width="250" height="250" />
  <caption>Rescaled image</caption><img src="./images/lung_mask.png" alt=lung_mask"
	title="lung_mask slice" width="250" height="250" />
  <caption>estimated lung mask</caption>

<p style="text-align:center;">
	<img src="./images/lung.png" alt="lung"
	title="lung" width="250" height="250" />
  <caption>lung regions</caption>

## Usage

To use this script call it from powershell or bash and provide the required arguments.

```
python -m pipeline.lung_extraction --input='path/to/input/folder/filename.pkl.npy' --output='path/to/output/folder/outputname'
```

Required arguments:

* --input :str, path to input image or stack. the file must be in '.pkl.npy' format
* --output :str, path to the output folder, here we be saved the extracted lung regions in '.pkl.npy' format

Optional arguments:

* --lung: str, path to output folder. If provided will save the lung mask in '.pkl.npy' format
