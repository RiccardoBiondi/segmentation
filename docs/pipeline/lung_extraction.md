# Lung Extraction

This script allows to isolate the lung regions from the rest of the body in an image stack. To achieve this purpose it will use some threshold and morphological operation.

It takes as input the image tensor as numpy array stored into *.pkl.npy* or *.npz* format. An other accepted input is a path to a folder that contains the *.dcm* files.
At the end of the execution the script save the stack with the extracted lung as *.pkl.npy* format.

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/thresholded.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/pipeline/images/dicom.png" width="500" height="500">
  </div>
  <div class="text_caption"> Rescaled image from which extract lungs </div>
</a>

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/lung_mask.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/pipeline/images/lung_mask.png" width="500" height="500">
  </div>
  <div class="text_caption"> Obtained lung mask</div>
</a>

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/lung.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/pipeline/images/lung.png" width="500" height="500">
  </div>
  <div class="text_caption"> Extracted lung regions</div>
</a>

## Usage

To use this script call it from powershell or bash and provide the required arguments.

```bash
python -m CTLungSeg.lung_extraction --input='path/to/input/folder/filename.pkl.npy' --output='path/to/output/folder/outputname'
```

Required arguments:

* --input :str, path to input image or stack. the file must be in '.pkl.npy' format

* --output :str, path to the output folder, here we be saved the extracted lung regions in '.pkl.npy' format


You can also run this script on multiple samples by calling it from the provided powershell or bash scripts. In this case you have to create two folders: the first one(input) will contains the files to process, the second one the results. ll the data must be in *.pkl.npy* or in *.dcm* format. In the DICOM case in each folder you have to create a subfolder for each patient that contains the *.dcm* files.

 Now you simply call the script from powershell( or bash) by providing as the first parameter the path to the input older and as second the path to output folder:

```powershell
PS /> ./lung_extraction.ps1 path/to/input/folder/ path/to/output/folder/
```
