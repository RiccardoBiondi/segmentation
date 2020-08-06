# train

This script allow to perform color quantization on multiple stack of images at the same time and obtain only one centroid for each cluster.
This algorithm will divide all the sample in several subsamples and compute the centroid for each subsample by using the kmeans clustering, after that reapply the clustering on the centroids computed as below and obtain the desidered results.

# Usage

First of all you have to organize all the training files into the same folder in *.pkl.npy* and use the powershell or the bash to run the script and provide the required arguments:

```
python -m pipeline.train --input='path/to/input/folder' --output='path/to/output/folder/output_name'
```

And this will use all the image stored in the input folder to compute the  centroid and save them into output folder with output_name as *.pkl.npy*. The number of clusters is 4 as default and the number of subsamples is 100 as default.
To control these parameters you can provide the optional arguments:

* --k : int, the number of clusters, default 4
* --n : int, number of subsamples to use, default 100
* --init: int, initialization technique: if 0 will use the random center initialization ,if 1 will use the kmenas++ algorithm.
* --intermediate: bool, if true allows to save the centroid of the subsamples
* --ROI: str, path to ROI file folder, if provided allows ROI selection.
