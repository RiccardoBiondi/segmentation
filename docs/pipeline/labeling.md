# labeling

This script allow to segment an image once you know the centroids.
By using *sklearn.clustering.KMeans* this script will assign at each pixel the label such that the distance between the label centroid and the pixel GL is minimum. Notice that this script doesn't compute the centroids but only segment an image by using pre-existing ones. In order to remove the outliers, a median blurring filter is applied on the labeled image. In the end the labels will be saved as *.pkl.npy'.

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/lung.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/pipeline/images/lung.png" width="500" height="500">
  </div>
  <div class="text_caption"> Image to segment </div>
</a>

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/labeled.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/pipeline/images/labeled.png" width="500" height="500">
  </div>
  <div class="text_caption"> Labeled image </div>
</a>

# Usage

To use this script call it from powershell or bash and provide the required arguments.

```bash
python -m CTLungSeg.labeling --input='path/to/image/to/segment/filename.pkl.npy' --centroids='path/to/centroids/file/centroids.pkl.npy' --label='path/to/label1/output/folder/'
```
 All the input files must be in *.pkl.npy* format, such as the output one.

Required parameters:

* *--input* :str, path to input image or stack. the file must be in *.pkl.npy* format
* *--centroids* : str, path to the file that contains the centroids to use to label the image
* *--label* :str, path to the output folder for the set of labels that will be saved in *pkl.npy* format


You can also run this script on multiple samples by calling it from the provided powershell(or bash) script. In this case you have to create three folders: the first one(input) will contains the *.pkl.npy* files to label(the ones with the extracted lung), the second and the third one the results. Now you simply call the script from powershell(or bash) by providing as the first parameter the path to the input older, as second parameter the path to the centroids file:
```shell
PS /> ./labeling.ps1 path/to/input/folder/  path/to/centroids/file/centroids.pkl.npy path/to/output/folder/
```
