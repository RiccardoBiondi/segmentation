# Lung Extraction

This script allows to isolate the lung regions from the rest of the body in an image stack. To achieve this purpose it will use some threshold and morphological operation.

It takes as input the stack of images as *.pkl.npy* format.
At the end of the execution the script save the stack with the extracted lung as *.pkl.npy* format. It is also possible to chose to save or not the binary lung mask.



<html>
  <head>
	<style>
	figure {
		border: thin #c0c0c0 solid;
    display: flex;
    flex-flow: column;
    padding: 5px;
		max-width: 500px;
	}

	figcaption {
		background-color: black;
    color: gray;
    font: italic smaller sans-serif;
    padding: 7px;
    text-align: center;
	}
</style>
</head>
<body>


<figure>
	<img src="./images/dicom.png" alt="dicom"
	title="dicom slice"  />
	<figcaption>
	Rescaled image from which extract lungs
	</figcaption>
</figure>

<figure>
	<img src="./images/lung_mask.png" alt=lung_mask"
title="lung_mask slice" />
	<figcaption>
	Computed lung mask
	</figcaption>
</figure>

<figure>
	<img src="./images/lung.png" alt="lung"
	title="lung"/>
	<figcaption>
	Extracted lung regions
	</figcaption>
</figure>

</body>
</html>


## Usage

To use this script call it from powershell or bash and provide the required arguments.

```bash
python -m CTLungSeg.lung_extraction --input='path/to/input/folder/filename.pkl.npy' --lung='path/to/output/folder/outputname'
```

Required arguments:

* --input :str, path to input image or stack. the file must be in '.pkl.npy' format

* --lung :str, path to the output folder, here we be saved the extracted lung regions in '.pkl.npy' format

Optional arguments:

* --mask: str, path to output folder. If provided will save the lung mask in '.pkl.npy' format

* --int_spot_area :int, default=700 **TODO**

* --ext_spot_area :int, default=200 **TODO**


You can also run this script on multiple samples by calling it from the provided powershell script. In this case you have to create two folders: the first one(input) will contains the *.pkl.npy* files to process, the second one the results. Now you simply call the script from powershell by providing as the first parameter the path to the input older and as second the path to output folder:
```powershell
> ./lung_extraction.ps1 path/to/input/folder/ path/to/output/folder/
```

If you want to provide the optional arguments you have to write them as third argument as follows:
```powershell
> ./lung_extraction.ps1 path/to/input/folder/ path/to/output/folder/  --int_spot_area=300
```

**NOTE** : in this case you can't provide the *--mask* argument as optional.
