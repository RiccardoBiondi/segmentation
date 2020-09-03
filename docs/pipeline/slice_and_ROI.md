# slice_and_ROI
This script allow to find the rectangular region with the smallest area which still contains the lung. It requires as input the path to the lung mask and save as output an np.ndarray which contains the top left and bottom right corner of the ROI. To find the ROI this script will use the stats provided by
[cv2.connectedComponentsWithStats](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html).



<html>
  <head>
	<style>
	figure {
		border: thin #c0c0c0 solid;
    display: flex;
    flex-flow: column;
    padding: 5px;
		max-width: 500px;
	}

	figcaption {
		background-color: black;
    color: gray;
    font: italic smaller sans-serif;
    padding: 7px;
    text-align: center;
	}
</style>
</head>
<body>


<figure>
<img src="./images/lung.png" alt="lung"
	title="input image"/>
	<figcaption>
	Input image
	</figcaption>
</figure>

<figure>
<img src="./images/ROI.png" alt="ROI"
title="ROI"/>
	<figcaption>
Draw of the selected ROI
	</figcaption>
</figure>


</body>
</html>



After the ROI selection this script will automatically removed all the slices in which the ROI has an area in pixels smaller than a specified value(default 1000), since we  can  notice that the ROI with the smallest areas usually does not contains lung regions but other organ, like trachea and heart. After the ROI selection the script will remove all the slices with ROI area less then a certain values, that because the smallest ROI usually does not contains the lung regions.
Thus script will return the reduced stack of cropped images

## Usage

To use this script call it from powershell or bash and provide the required arguments.

```bash
python -m CTLungSeg.slice_and_ROI --input='path/to/input/folder/filename.pkl.npy' --output='path/to/output/folder/output_name'
```

Required arguments:

* --input :str, path to the input file, must be the stack of images with the extracted lung
* --output :str, path to the output file to save the selected and cropped slices

Optional arguments:

* -area: int, minimum ROI area in pixels to select the slice


You can also run this script on multiple samples by calling it from the provided powershell script. In this case you have to create two folders: the first one(input) will contains the *.pkl.npy* files to process, the second one the results. Now you simply call the script from powershell by providing as the first parameter the path to the input older and as second the path to output folder:

```powershell
> ./slice_and_ROI.ps1 path/to/input/folder/ path/to/output/folder/
```

If you want to provide the optional arguments you have to write them as third argument as follows:

```powershell
> ./slice_and_ROI.ps1 path/to/input/folder/ path/to/output/folder/  --area=300
```
