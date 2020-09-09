# segmentation

This module contains useful functions to segment stack of images

1. [opening](#opening)
2. [closing](#closing)
3. [remove_spots](#remove_spots)
4. [select_greater_connected_regions](#select_greater_connected_regions)
5. [reconstruct_gg_areas](#reconstruct_gg_areas)
6. [find_ROI](#find_ROI)

## opening

## closing

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

## reconstruct_gg_areas

## find_ROI

Found the upper and lower corner of the smallest rectangle that still contains the lung regions for each image of the input stack

**Parameter**

  *stats*: pandas dataframe, dataframe that contains the stats of the connected regions. columns must be ...

**Return**

  *corners*: array-like, array which contains the coordinates of the upper and lower corner of the ROI organized as [x_top, y_top, x_bottom, y_bottom]
