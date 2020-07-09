# clustering

This script allow to perform a kmeans clustering on a stack of images. As output save two '.pkl.npy'. the first will contains the centroid information, the second contains the labelled images.

## Usage


```
 python -m pipeline.clustering --input='path to input file.pkl.npy' --centroid='path to centroid output file' --labels='path to labels output file'
```

Required arguments:

* --input :str, path to the input stack, mut be '3'.pkl.npy'
* --centroid :str, path to centroid output file
* --labels :str, path to labels output file

Optional arguments:
* --ROI :str, path to a file that contains ROI information
* --n_clus :int, number of clusters to consider
