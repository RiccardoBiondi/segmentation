# segmentation

This module contains useful functions to segment stack of images

1. [opening](#opening)
2. [closing](#closing)
3. [remove_spots](#remove_spots)
4. [select_greater_connected_regions](#select_greater_connected_regions)
5. [reconstruct_gg_areas](#reconstruct_gg_areas)
6. [find_ROI](#find_ROI)

## opening

Perform an erosion followed by a dilation

**Parameters**

  *img* : array-like, image tensor

  *kernel* : array-like, kernel used for the morphological operations

**Returns**

  *opened* : array-like, opened image

## closing

Perform a dilation followed by an erosion

**Parameters**

  *img* : array-like, image tensor

  *kernel* : array-like, kernel used for the morphological operations

**Returns**

  *closed* : array-like, closed image.

## remove_spots

Set to zero the GL of all the connected region with area lesser than area

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

  *mask* : array-like, lung mask to reconstruct

**Return**

  *reconstructed* : array-like, reconstructed lung mask

## find_ROI

Found the upper and lower corner of the smallest rectangle that still contains the lung regions for each image of the input stack

**Parameter**

  *stats*: pandas dataframe, dataframe that contains the stats of the connected regions. columns must be ...

**Return**

  *corners*: array-like, array which contains the coordinates of the upper and lower corner of the ROI organized as [x_top, y_top, x_bottom, y_bottom]
