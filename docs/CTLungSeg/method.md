# Method

This module contains functions useful for the script execution. This functions extend some open-cv functions  and allow to perform operations on a stack of images.


1. [erode](#erode)
2. [dilate](#dilate)
3. [connectedComponentsWithStats](#connectedComponentsWithStats)
4. [bitwise_not](#bitwise_not)
5. [imfill](#imfill)
6. [medianBlur](#medianBlur)
7. [gaussianBlur](#gaussianBlur)
8. [otsu](#otsu)
9. [find_ROI](#corner_finder)
10. [remove_spots](#remove_spots)


## erode
Compute the erosion for the whole stack of images. It is the extension for a stack of images of   [cv2.erode](https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#gaeb1e0c1033e3f6b891a25d0511362aeb) in opencv-python.

**Parameters**

*img* : array-like, image or stack of images to erode
*kernel* : (2D)array-like, kernel to apply to the input stack
*iterations* : int, number of iterations to apply, default 1

**Return**

*processed* : array-like, eroded stack

```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle, save_pickle
  from CTLungSeg.utils import rescale
  from CTLungSeg.method import erode

  stack = load_pikle('./images/image.pkl.npy')
  stack[stack < 0] = 0
  stack = rescale(stack, stack.max(), 0)# apply a rescaling
  stack = 255 * np.where(stack > 0.1, 0, 1)#apply a threshold
  kernel = np.ones((3,3), dtype='uint8') #erosion kernel
  eroded = erode(stack, kernel, iterations=1)
  save_pickle('./output_dir/output_filename',  eroded)
```
<p style="text-align:center;"><img src="./images/thresholded.png" alt="original"
	title="input image" width="220" height="220" />
  <caption>Thresholded image</caption>
  <img src="./images/eroded.png" alt="ROI"
	title="ROI" width="220" height="220" />
  <caption>Eroded image</caption>

## dilate
Compute the dilation for the whole stack of images. It is the extension for a stack of images of   [cv2.dilate](https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#ga4ff0f3318642c4f469d0e11f242f3b6c) in opencv-python.

**Parameters**

*img* : array-like, image or stack of images to dilate
*kernel* : (2D)array-like, kernel to apply to the input stack
*iterations* : int, number of iterations to apply, default 1

**Return**

*processed* : array-like, dilated stack


```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle, save_pickle
  from CTLungSeg.utils import rescale
  from CTLungSeg.method import dilate

  stack = load_pikle('./images/image.pkl.npy')
  stack[stack < 0] = 0
  stack = rescale(stack, stack.max(), 0)# apply a rescaling
  stack = 255 * np.where(stack > 0.1, 0, 1)#apply a threshold
  kernel = np.ones((3,3), dtype='uint8') #dilation kernel
  dilated = dilate(stack, kernel, iterations=1)
  save_pickle('./output_dir/output_filename',  dilated)
```
<p style="text-align:center;"><img src="./images/thresholded.png" alt="original"
	title="thresholded image" width="220" height="220" />
  <caption>Original image</caption>
  <img src="./images/dilated.png" alt="ROI
	title="ROI" width="220" height="220" />
  <caption>Dilated image</caption>

## connectedComponentsWithStats

computes the connected components labeled image of boolean image and also
produces a statistics output for each label. Is the extension for a stack of images of [cv2.connectedComponentsWithStats](https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html) function in opencv-python.

**Parameters**

*img* : array-like, input image or stack of images

**Return**

*retval* : array-like

*labels* : array-like, labelled image or stack

*stats* : list of array-like, statistic for each label for each image of the stack

*centroids* : array-like, centroid for each label for each image of the stack


```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle
  from CTLungSeg.method import connectedComponentsWithStats

  stack = load_pikle('./images/image.pkl.npy')
  stack= np.where(stack < 3, 0, 1) #apply a threshold to obtain boolean images
  ret, label, stats, centroids = connectedComponentsWithStats(stack)
```


## bitwise_not

Calculates per-element bit-wise inversion of the input stack of images. This function is an implementation for a stack of images of [cv2.bitwise_not](https://docs.opencv.org/3.4/d2/de8/group__core__array.html#ga0002cf8b418479f4cb49a75442baee2f) in opencv-python.

**Parameters**

*img* : array_like, image or stack of images to invert

**Returns**

*dst* : array-like, inverted image or stack of images


```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle, save_pickle
  from CTLungSeg.method import bitwise_not

  stack = load_pikle('./images/image.pkl.npy')
  stack = np.where(stack < 3, 0, 1) #apply a threshold to obtain boolean images
  inverted = bitwise_not(stack)
  save_pickle('./output_filename', inverted)
```
<p style="text-align:center;"><img src="./images/thresholded.png" alt="original"
	title="input image" width="220" height="220" />
  <caption>Thresholded image</caption>
  <img src="./images/inverted.png" alt="ROI"
	title="ROI" width="220" height="220" />
  <caption>Inverted image</caption>

## imfill

This function, based on `cv2.floodFill()` function, is useful to fill holes in the whole stack of images. Note that the input stack must be binary

**Parameter**

*img* : array-like, binary image to fill

**Return**

*filled* : array-like, binary image or stack with filled holes


```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle, save_pickle
  from CTLungSeg.utils import rescale
  from CTLungSeg.method import imfill

  stack = load_pikle('./images/image.pkl.npy')
  stack[stack < 0] = 0
  stack = rescale(stack, stack.max(), 0)# apply a rescaling
  stack = 255 * np.where(stack > 0.1, 0, 1)#apply a threshold
  filled = imfill(stack)

  save_pickle('./output_filename', filled)
```
<p style="text-align:center;"><img src="./images/thresholded.png" alt="original"
	title="image after threshold" width="220" height="220" />
  <caption>image after threshold</caption>
  <img src="./images/filled.png" alt="ROI"
	title="ROI" width="220" height="220" />
  <caption>Filled image</caption>

## medianBlur

Apply a median blur filter on the whole stack of images.
This function is an implementation for a stack of images of [cv2.medianBlur](https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html?highlight=medianblur#medianblur) function in opencv-python.

**Parameters**

*img* : array-like, image or stack of images to filter

*k_size* : int, aperture linear size; it must be odd and greater than 1

**Return**

*blurred* : array-like, median blurred image or stack


```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle, save_pickle
  from CTLungSeg.utils import rescale
  from CTLungSeg.method import medianBlur

  stack = load_pikle('./images/image.pkl.npy')
  stack[stack < 0] = 0
  stack = rescale(stack, stack.max(), 0)
  blurred = medianBlur(stack, 5)
  save_pickle('./output_filename', blurred)
```
<p style="text-align:center;"><img src="./images/rescaled.png" alt="original"
  title="rescaled" width="220" height="220" />
  <caption>rescaled image</caption>
  <img src="./images/blurred.png" alt="ROI"
  title="ROI" width="220" height="220" />
  <caption>blurred image</caption>


## gaussianBlur

Apply a gaussian blurring filter on an image or stack of images. This function is an implementation for a stack of images of [cv2.GaussianBlur](https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html?highlight=gaussianblur#gaussianblur) function in opencv-python.

**Parameters**

*img*: array-like, image or stack of images to filter

*ksize*: tuple of int, aperture linear size; it must be odd and greater than 1

*sigmaX*: float, Gaussian kernel standard deviation in X direction

*sigmaY*: float, Gaussian kernel standard deviation in Y direction; if sigmaY is zero, it is set to be equal to sigmaX, if both sigmas are zeros, they are computed from ksize

*borderType*: Specifies image boundaries while kernel is applied on image borders

**Return**

*blurred* : array-like, blurred image



```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle, save_pickle
  from CTLungSeg.utils import rescale
  from CTLungSeg.method import medianBlur

  stack = load_pikle('./images/image.pkl.npy')
  stack[stack < 0] = 0
  stack = rescale(stack, stack.max(), 0)
  blurred = gaussianBlur(stack, (5,5))
  save_pickle('./output_filename', blurred)
```

**TODO**: add images

## otsu

Compute the best threshold value for each slice of the input image stack by using otsu algorithm

**Parameters**

*img*: array-like
    input image or stack of images. must be uint8 type

**Return**

*out*: array-like
    threshlded image stack

```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_pickle, save_pickle
  from CTLungSeg.utils import rescale
  from CTLungSeg.method import otsu

  stack = load_pikle('./images/image.pkl.npy')
  stack[stack < 0] = 0
  stack = rescale(stack, stack.max(), 0)
  stack = (255 * stack).astype(np.uint8)
  thr = otsu(stack)
  save_pickle('./output_filename', thr)
```

<p style="text-align:center;"><img src="./images/rescaled.png" alt="original"
  title="rescaled" width="250" height="250" />
  <caption>input image</caption>
  <img src="./images/thresholded.png" alt="thr"
  title="thr" width="250" height="250" />
  <caption>thresholded image</caption>


## find_ROI

Found the upper and lower corner of the smallest rectangle that still contains the lung regions for each image of the input stack

**Parameter**

*stats*: pandas dataframe
    dataframe that contains the stats of the connected regions. columns must be ...

**Return**

*corners*: array-like
    array which contains the coordinates of the upper and lower corner of the ROI organized as [x_top, y_top, x_bottom, y_bottom]


## remove_spots

Set to zero the GL of all the connected region with area lesser than area

**Parameters**

*img*: array-like
    binary image from which remove spots

*area*: int
    maximun area in pixels of the removed spots

**Return**

*filled*: array-like
    binary image with spot removed

```python

from CTLungSeg.utils import load_pickle, save_pickle
from CTLungSeg.utils import preprocess
from CTLungSeg.method import remove_spots
from CTLungSeg.method import otsu

#load the image
img = load_pikle('./images/image.pkl.npy')
img = preprocess(img)

#apply a threshold
img = otsu(img)
#fill the smallest holes
filled = remove_spots(img, 500)
save_pickle('./images/filled.pkl.npy')
```
