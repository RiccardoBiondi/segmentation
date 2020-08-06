# labeling

This script allow to segment an image once you know the centroids.
By using *sklearn.clustering.KMeans* this script will assign at each pixel the label such that the distance between the label centroid and the pixel GL is minimum. Notice that this script doesn't compute the centroids but only segment an image by using pre-existing ones.



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
<img src="./images/lung.png" alt="input"
	title="Input image" />
	<figcaption>
	Image to segment
	</figcaption>
</figure>

<figure>
<img src="./images/labeled.png" alt="labeled"
title="body_mask slice"  />
	<figcaption>
	Labeled image
	</figcaption>
</figure>


</body>
</html>


# Usage

To use this script call it from powershell or bash and provide the required arguments.

```
python -m pipeline.lungselection --input='path/to/image/to/segment/filename.pkl.npy'
--centroids='path/to/centroids/file/centroids.pkl.npy'
--output='path/to/output/folder/outputname'
```
 All the input files must be in *.pkl.npy* format, such as the output one.

Required parameters:

* *--input* :str, path to input image or stack. the file must be in *.pkl.npy* format
* *--output* :str, path to the output folder, here we be saved the lung mask in *pkl.npy* format
