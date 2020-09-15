# segmentation

This module contains useful functions to segment stack of images

1. [opening](#opening)
2. [closing](#closing)
3. [remove_spots](#remove_spots)
4. [select_greater_connected_regions](#select_greater_connected_regions)
5. [reconstruct_gg_areas](#reconstruct_gg_areas)
6. [find_ROI](#find_ROI)

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

## select_greater_connected_regions

Select the n_reg greater connected regions in each slice of the stack and remove the others. If the image contains less than n_reg regions, no region will be selected.

**Parameters**

  *img* : array-like, Image tensor; better if the images are binary

  *n_reg* : int, number of connected regions to select. The background it is not considered as connected regions

**Return**

  *dst* : array-like, binary image with only the n_reg connected regions

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

## imlabeling

eturn the labeled image given the original image
  tensor and the centroids

**Parameters**

  *image* : array-like, image to label

  *centroids* : array-like, Centroids vector for KMeans clustering

**Return**

  *labeled* : array-like, Image in which each GL ia assigned on its label.
