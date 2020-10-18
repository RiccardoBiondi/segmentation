# utils

This modules contains useful functions to mange input and output image stacks and simple operations on single images


1. [load_image](#load_image)
2. [save_pickle](#save_pikle)
3. [save_npz](#save_npz)
5. [normalize](#normalize)
4. [rescale](#rescale)
5. [gl2bit](#gl2bit)
6. [hu2gl](#hu2gl)


## load_image

Load a stack of images and return a 3D numpy array. The input file format can by .pkl.npy, .npz or a folder that contains .dcm files. Notice that this function doesn't provide any metadata informations, but only the image tensor.

**Parameter**

  *filename*: str, path to the image file(.pkl.npy or .npz) or folder that contains .dcm files.

**Return**

  *imgs*: array-like, image tensor

## save_pikle

Save in the processed stack of images '.pkl.npy' format. Data must be in a np.ndarray like format and the specified output file name doesn't requires to specify the extension.

**Parameters**

  *filename*: str, file name or path to dump as pickle file

  *data*: array-like, image or stack to save

**Return** None

```python
import cv2
import numpy as np
from CTLungSeg.utils import load_image, save_pickle

stack = load_pikle('./images/image.pkl.npy')
#
#Stack processing
#
save_pickle('./output_dir/output_filename', stack)
```

## save_npz

Save in the processed stack of images '.pkl.npy' format. Data must be in a np.ndarray like format and the specified output file name doesn't requires to specify the extension.

**Parameters**

  *filename*: str, file name or path to dump as   pickle file

  *data*: array-like, image or stack to save

**Return** None

```python
import cv2
import numpy as np
from CTLungSeg.utils import load_image, save_npz

stack = load_image('./images/image.pkl.npy')
#
#Stack processing
#
save_pickle('./output_dir/output_filename', stack)
```

## normalize

Rescale each GL according to the mean and std of the whole stack

**Parameters**

  *image* : array-like, image or stack to normalize

**Return**

  *normalized* : array-like, normalized images stack



## rescale

Rescale the image according to max, min input

**Parameters**

  *img* : array-like, input image or stack to rescale

  *max* : float, maximum value of the output array

  *min* : float, minimum value of the output array

**Return**

  *rescaled* : array-like, image rescaled according to min, max

```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_image, save_pickle
  from CTLungSeg.utils import rescale

  stack = load_image('./images/image.pkl.npy')
  rescaled = rescale(stack, stack.max(), 0)
  save_pickle('./output_dir/output_filename',  rescaled)
```
## gl2bit

Convert the grey level of each voxel of a stack of images into its binary representation.

**Parameters**

  *img* : array-like , image tensor to convert

  *width* : int, number of bit to display

**Return**

  *binarized* : array-like, image tensor in which each voxel GL value is replaced by a str that contains its binary representation.

## hu2gl

SRescale the image and convert it a 8bit GL image. The returned image tensor is
a 3D numpy array that contains np.uint8 values.

**Parameter**

  *img*: array-like, input image or stack of images

**Return**

  *out*: array like, rescaled image

```python
  import cv2
  import numpy as np
  from CTLungSeg.utils import load_image, save_pickle
  from CTLungSeg.utils import preprocess

  stack = load_pikle('./images/image.pkl.npy')
  stack = preprocess(stack)
  save_pickle('./output_dir/output_filename',  stack)
```

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/not_rescaled.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/not_rescaled.png" width="220" height="220">
  </div>
  <div class="text_caption"> Original image in HU units </div>
</a>

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/rescaled.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/docs/CTLungSeg/images/rescaled.png" width="220" height="220">
  </div>
  <div class="text_caption"> pre-processed image </div>
</a>
