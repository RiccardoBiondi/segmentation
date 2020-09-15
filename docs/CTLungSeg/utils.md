# utils

This modules contains useful functions to mange input and output image stacks and simple operations on single images


1. [load_image](#load_image)
2. [save_pickle](#save_pikle)
3. [save_npz](#save_npz)
4. [rescale](#rescale)
5. [preprocess](#preprocess)


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

## preprocess

Set to zero all the negative pixel values, rescale the image and convert it a 8bit GL image. The returned image tensor is a 3D numpy array that contains np.uint8 values.

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
