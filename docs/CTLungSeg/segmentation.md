# segmentation

This module contains useful functions to segment stack of images

1. [opening](#opening)
2. [closing](#closing)
3. [remove_spots](#remove_spots)
4. [select_largest_connected_region_3](#select_lergest_connected_region_3d)
5. [reconstruct_gg_areas](#reconstruct_gg_areas)
6. [find_ROI](#find_ROI)
7. [bit_plane_slices](#bit_plane_slices)
8. [imlabeling](#imlabeling)
9. [kmeans_on_subsamples](#kmeans_on_subsamples)

## opening

Perform an opening operations( erosion followed by a dilation) on the whole stack of images, according to the provided structuring element (kernel)

**Parameters**

  *img* : array-like, image tensor

  *kernel* : array-like, kernel used for the morphological operations

**Returns**

  *opened* : array-like, opened image

## closing

Perform a closing operations( erosion followed by a dilation) on the whole stack of images, according to the provided structuring element (kernel)

**Parameters**

  *img* : array-like, image tensor

  *kernel* : array-like, kernel used for the morphological operations

**Returns**

  *closed* : array-like, closed image.

## remove_spots

Set to zero the GL of all the connected region with area lesser than a minimum value.

**Parameters**

  *img*: array-like, binary image from which remove spots
  *area*: int, maximun area in pixels of the removed spots

**Return**

  *filled*: array-like, binary image with spot removed

```python

from CTLungSeg.utils import load_image, save_pickle
from CTLungSeg.utils import preprocess
from CTLungSeg.method import otsu_threshold
from CTLungSeg.segmentation import remove_spots

#load the image
img = load_image('./images/image.pkl.npy')
img = preprocess(img)

#apply a threshold
img = otsu_threshold(img)
#fill the smallest holes
filled = remove_spots(img, 500)
save_pickle('./images/filled.pkl.npy')
```

## select_larger_connected_region_3d

Select the larger connected regions of the image tesor.
*NOTE*: do not consider background as connected region

**Parameters**

  *img* : array-like, binary image tesnor

**Return**

  *dst* : array-like, binary image with only the largest connected region

**TODO** add usage example and images

## reconstruct_gg_areas

This function interpolate each slice of the input mask to reconstruct the missing gg areas.

**Parameter**

  *mask* : array-like, lung mask to reconstruct, must be a binary image.

**Return**

  *reconstructed* : array-like, reconstructed lung mask

## find_ROI

Found the upper and lower corner of the smallest rectangle that still contains the lung regions for each image of the input stack

**Parameter**

  *stats*: pandas dataframe, dataframe that contains the stats of the connected regions.

**Return**

  *corners*: array-like, array which contains the coordinates of the upper and lower corner of the ROI organized as [x_top, y_top, x_bottom, y_bottom]

#bit_plane_slices

Convert each voxel GL into its 8-bit binary rapresentation and return as output the stack resulting from the sum of all the bit specified in bits, with them significance.

**Parameters**

  *stack* : array-like, image stack. each GL must be an 8-bit unsigned int

  *bits*: tuple, tuple that specify which bit sum

**Returns**

  *output* : array-like, images stack in which each GL depends only to the significance of each specfied bit

## bit_plane_slices

Convert each voxel GL into its 8-bit binary rapresentation and return as output the stack resulting from the sum of all the bit specified in bits, with them significance.

**Parameters**

  *stack* : array-like, image stack. each GL must be an 8-bit unsigned int
  *bits*: tuple, tuple that specify which bit sum

**Returns**

  *output* : array-like, images stack in which each GL depends only to the significance of each specified bit

## imlabeling

Label an input stack of multichannel images according to the provided
centroids and weight.

**Parameters**

 *image* : array-like of shape (n_images, height, width, n_channels), image
          stack to label

 *centroids* : array-like of shape (n_centroids, n_channels), Centroids vector
                for KMeans clustering.
 *weight* : array-like of shape (n_images, height, width), The weights for each
            observation in image. If None, all observations are assigned
            equal weight.

**Return**

  *labeled* : array-like of shape (n_images, height, width ), Image in which
              each GL ia assigned to the corresponding label

## kmeans_on_subsamples

Apply the kmenas clustering on each stack of images in subsample.
Allow also to choose if consider or not some voxel during the segmentation.
To allow these feature simply raise the flag 'weight' and provide as last
channel a binary mask with 0 on each voxel you want to exclude

**Parameters** :

  *imgs* : array-like of shape (n_subsamples, n_imgs, heigth, width, n_channels)
           array of images tensor
  *n_centroids* : int, number of centroids to find

  *stopping_criteria* :It is the iteration termination criteria.
                       When this criteria is satisfied, algorithm iteration
                       stops.
  *center_init* : centroid initialization technique; can be
                  cv2.KMEANS_RANDOM_CENTERS or cv2.KMEANS_PP_CENTERS.
  *weight* : Bool , flag that allow to not consider some voxel in images.
             Default = False

**Return**

  *centroids* : array-like, array that contains the n_centroids estimated
                for each subsample
