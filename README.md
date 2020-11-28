| **Authors**  | **Project** |  **Build Status** | **License** | **Code Quality** | **Coverage** |
|:------------:|:-----------:|:-----------------:|:-----------:|:----------------:|:------------:|
| [**R. Biondi**](https://github.com/RiccardoBiondi) <br/> [**N. Curti**](https://github.com/Nico-Curti) | **COVID-19 Lung Segmentation** | **Linux/MacOS** : [![Build Status](https://travis-ci.com/RiccardoBiondi/segmentation.svg?branch=master)](https://travis-ci.com/RiccardoBiondi/segmentation) <br/>  **Windows** : [![Build status](https://ci.appveyor.com/api/projects/status/om6elsnkoi22xii3?svg=true)](https://ci.appveyor.com/project/RiccardoBiondi/segmentation) | [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/RiccardoBiondi/segmentation/blob/master/LICENSE.md) | **Codacy** : [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc0fd47ae8e44ab1943b1f74c2a3d7e2)](https://www.codacy.com/manual/RiccardoBiondi/segmentation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RiccardoBiondi/segmentation&amp;utm_campaign=Badge_Grade) <br/> **Codebeat** : [![CODEBEAT](https://codebeat.co/badges/927db14b-36fc-42ed-88f1-09b2a9e1b9c0)](https://codebeat.co/projects/github-com-riccardobiondi-segmentation-master) | [![codecov](https://codecov.io/gh/RiccardoBiondi/segmentation/branch/master/graph/badge.svg)](https://codecov.io/gh/RiccardoBiondi/segmentation) |

![Project CI](https://github.com/RiccardoBiondi/segmentation/workflows/CTLungSeg%20CI/badge.svg)
![Docs CI](https://github.com/RiccardoBiondi/segmentation/workflows/CTLungSeg%20Docs%20CI/badge.svg)

[![docs](https://readthedocs.org/projects/covid-19-ggo-segmentation/badge/?version=latest)](https://covid-19-ggo-segmentation.readthedocs.io/en/latest/?badge=latest)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/pulls)
[![GitHub issues](https://img.shields.io/github/issues/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/issues)

[![GitHub stars](https://img.shields.io/github/stars/RiccardoBiondi/segmentation.svg?label=Stars&style=social)](https://github.com/RiccardoBiondi/segmentation/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/RiccardoBiondi/segmentation.svg?label=Watch&style=social)](https://github.com/RiccardoBiondi/segmentation/watchers)

# COVID-19 Lung Segmentation

This package provides a fast way to isolate lung region and identify ground glass lesions on CT images of patients affected by COVID-19. The segmentation approach is based on color quantization, performed by kmeans clustering. This package provides a series of scripts to isolate lung regions, pre-process the images, estimate kmeans centroids and labels the lung regions.
1. [Overview](#Overview)
2. [Contents](#Contents)
3. [Prerequisites](#prerequisites)
4. [Installation](#Installation)
5. [Usage](#usage)
6. [License](#license)
7. [Contribution](#contribution)
8. [Authors](#authors)
9. [Acknowledgments](#acknowledgments)
10. [Citation](#citation)

## Overview

This package provides an automatic pipeline for the segmentation of ground glass
opacities and consolidation areas on CT chest scans of patient affected by COVID-19.

The segmentation is achieved by color quantization: each voxel is groped by color
simiarity: The characteristic color of each tissue was fond, and the voxel are classified
to the nearest tissue.

**Example of segmentation**. **Left:** Original image: **Right** original image with identified ground glass areas.

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/images/results.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/images/results.png" width="800" height="400">
  </div>
</a>


## Contents

COVID-19 Lung segmentation is composed of scripts and modules:
- scripts allows to isolate lung regions, find the centroids for colours quantization and segment the images.
- modules allows to load and save the images from and in different extensions and perform operations on stack of images.

To refer to script documentation:

| **Script** | **Description** |
|:----------:|:---------------:|
| [lung_extraction](./docs/pipeline/lung_extraction.md) | Extract lung from CT scans 										 																																				|
| [train](./docs/pipeline/train.md) | Apply colour quantization on a series of stacks in order to estimate the centroid to use for segmentation																																													|
| [labeling](./docs/pipeline/labeling.md) |Segment the input image by using pre-estimated centroids or user provided set|

To refer to modules documentation:

| **Module**| **Description**|
|:---------:|:--------------:|
| [utils](./docs/CTLungSeg/utils.md) | method to load, save and preprocess stack																																										|
| [method](./docs/CTLungSeg/method.md) | method to filter the image tensor |
| [segmentation](./docs/CTLungSeg/segmentation.md) | contains useful function to segment stack of images and select ROI																										|

For each script described below there are a powershell and a shell script which allow to execute the script on multiple patient.

## Prerequisites

Supported python version: ![Python version](https://img.shields.io/badge/python-3.5|3.6|3.7|3.8-blue.svg)

First of all ensure to have the right python version installed.

This script use opencv-python, numpy, pandas, functool and pickle: see [requirements](#./requirements.txt) for more informations.

The lung extraction is performed by using apre-trained UNet, so plese ensure to
have installed the [lungmask](https://github.com/JoHof/lungmask) package. For
more information about how the network is trained, plese refers to https://doi.org/10.1186/s41747-020-00173-2 .

## Installation

Download the project or the latest release:

```bash
git clone https://github.com/RiccardoBiondi/segmentation
cd segmentation
```

Now you can simply install all the required packages with the command:

```bash
pip install -r requirements.txt
```

Now in ```segmentation``` directory execute:
```bash
python setup.py install
```

### testing

Testing routines use ```PyTest``` and ```Hypothesis``` packages. please install
these packages to perform the test.
All the full set of test is provided in [testing](./testing) directory.
You can run the full list of test with:
```bash
python -m pytest
```


## Usage


### Single Patient Case

Once you have installed you can directly start to segment the images.
Input CT scans must be in hounsfield units(HU), gray-scale images are not allowed.
The input allowed formats are the one supported by SimpleITK. If the input is a dicom series, simply pass the path to the directory which contains
the series files, please ensure that in the folder there is only one series.
This will return the GGO and CS labels is as '.nrrd'.


To segment a single CT scan, simply run the following command from the bash or
pawershell :

```bash
   python -m CTLungSeg --input='/path/to/input/series'  --output='/path/to/output/file'
```



### Train your own centroids


Lets consider the case where you have an high number of patient and you. In this case the two main step of segmentation are execute separately.

First of all you have to create three folders :

- input folder : contains all and oly the CT scans to segment
- temporary folder : empty folder. Will contain the scans after the lung segentation
- output folder : empty folder, will contains the labels files.

Now you can proceed with the lung segmentation. To achive this purpose simply run
from powershell the  script .:
 ```powershell
PS \> ./lung_extraction.ps1 path/to/input/folder/ path/to/temporary/folder/
 ```

 Or its equal version in bash :

  ```bash
    $ ./lung_extraction.sh path/to/input/folder/ path/to/temporary/folder/
  ```

 Once you have successfully isolated the lung, you are ready to perform the actual segmentation. Simply run the labeling scrip from powershell :

```powershell
PS /> ./labeling.ps1 path/to/temporary/folder/ p /path/to/output/folder/
```

Or its corresponding version in bash:
```powershell
$ ./labeling.sh path/to/temporary/folder/ p /path/to/output/folder/
```

## License

The `COVID-19 Lung Segmentation` package is licensed under the MIT "Expat" License. [![License](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE.md)

## Contribution

Any contribution is more than welcome. Just fill an [issue](./.github/ISSUE_TEMPLATE/ISSUE_TEMPLATE.md) or a [pull request](./.github/PULL_REQUEST_TEMPLATE/PULL_REQUEST_TEMPLATE.md) and we will check ASAP!

See [here](https://github.com/RiccardoBiondi/segmentation/blob/master/CONTRIBUTING.md) for further informations about how to contribute with this project.

## Authors

* <img src="https://avatars3.githubusercontent.com/u/48323959?s=400&v=4" width="25px"> **Riccardo Biondi** [git](https://github.com/RiccardoBiondi)

* <img src="https://avatars0.githubusercontent.com/u/24650975?s=400&v=4" width="25px"> **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)

* <img src="https://avatars2.githubusercontent.com/u/1419337?s=400&v=4" width="25px;"/> **Enrico Giampieri** [git](https://github.com/EnricoGiampieri), [unibo](https://www.unibo.it/sitoweb/enrico.giampieri)

See also the list of [contributors](https://github.com/RiccardoBiondi/segmentation/contributors) [![GitHub contributors](https://img.shields.io/github/contributors/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/graphs/contributors/) who participated to this project.

### Citation

If you have found `COVID-19 Lung Segmentation` helpful in your research, please consider citing the project

```tex
@misc{COVID-19 Lung Segmentation,
  author = {Riccardo Biondi, Nico Curti, Enrico Giampieri, Gastone Castellani},
  title = {COVID-19 Lung Segmentation},
  year = {2020},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/RiccardoBiondi/segmentation}},
}
```
