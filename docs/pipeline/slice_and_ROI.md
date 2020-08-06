# slice_and_ROI
This script allow to find the rectangular region with the smallest area which still contains the lung. It requires as input the path to the lung mask and save as output an np.ndarray which contains the top left and bottom right corner of the ROI. To find the ROI this script will use the stats provided by
`cv2.connectedComponentsWithStats` function. Refers to `opencv-python` for more details.




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







## Usage

To use this script call it from powershell or bash and provide the required arguments.

```
python -m pipeline.slice_and_ROI --input='path/to/input/folder/filename.pkl.npy' --output='path/to/output/folder/output_name'
```

Required arguments:

* --input :str, path to the input file, must be the stack of images with the extracted lung
* --output :str, path to the output file in which data are stored
