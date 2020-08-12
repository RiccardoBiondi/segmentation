# clustering

This script allow to perform a kmeans clustering on a stack of images. As output save two '.pkl.npy'. the first will contains the centroid information, the second contains the labelled images. This script use `cv2.kmeans()` function. Refers to `opencv-python` to more details


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
    padding: 3px;
    text-align: center;
	}
</style>
</head>
<body>


<figure>
	<img src="./images/lung.png" alt="lung" />
	<figcaption>
	Input image to segment
	</figcaption>
</figure>

<figure>
	<img src="./images/labeled.png" alt="labeled"/>
	<figcaption>
	Labeled image
	</figcaption>
</figure>

</body>
</html>


## Usage


```
 python -m pipeline.clustering --input='path/to/input/folder/filename.pkl.npy' --centroid='path/to/output/folder/centroid_filename' --labels='path/to/output/folder/labels_filename'
```

Required arguments:

* *--input* :str, path to the input stack, must be '.pkl.npy'
* *--centroid* :str, path to centroid output file
* *--labels* :str, path to labels output file

Optional arguments:
* *--ROI* :str, path to a file that contains ROI information, if not specified the whole image will be considered
* *--n_clust* :int, number of clusters to consider; default 4
* *--centr_init* : int, specify the technique to use to initzialize the centroids, can be 0 or 1:
  * 0: Random center
  * 1: kmeans++ center initzialization
Default is 0