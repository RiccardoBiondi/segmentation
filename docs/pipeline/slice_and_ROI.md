# slice_and_ROI

This script allow to find the rectangular region with the smallest area which still contains the lung. It requires as input the path to the lung mask and save as output an np.ndarray which contains the top left and bottom right corner of the ROI. This script performs also the slice selection

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/lung.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/pipeline/images/lung.png" width="500" height="500">
  </div>
  <div class="text_caption"> Input image </div>
</a>

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/ROI.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/pipeline/images/ROI.png" width="500" height="500">
  </div>
  <div class="text_caption"> Draw of the selected regions </div>
</a>

After the ROI selection this script will automatically remove all the slices in which the ROI has an area in pixels smaller than a specified value(default 1000), since we  can  notice that the ROI with the smallest areas usually does not contains lung regions but other organ, like trachea and heart.

## Usage

To use this script call it from powershell or bash and provide the required arguments.

```bash
python -m CTLungSeg.slice_and_ROI --input='path/to/input/folder/filename.pkl.npy' --output='path/to/output/folder/output_name'
```

Required arguments:

* *--input* :str, path to the input file, must be the stack of images with the extracted lung
* *--output* :str, path to the output file to save the selected and cropped slices

Optional arguments:

* *--area*: int, minimum ROI area in pixels to select the slice

You can also run this script on multiple samples by calling it from the provided powershell(or bash) script. In this case you have to create two folders: the first one(input) will contains the *.pkl.npy* files to process, the second one the results. Now you simply call the script from powershell(or bash) by providing as the first parameter the path to the input older and as second the path to output folder:

```powershell
PS /> ./slice_and_ROI.ps1 path/to/input/folder/ path/to/output/folder/
```

If you want to provide the optional arguments you have to write them as third argument as follows:

```powershell
PS /> ./slice_and_ROI.ps1 path/to/input/folder/ path/to/output/folder/  --area=300
```
