| **Authors**  | **Project** |  **Build Status** | **License** | **Code Quality** | **Coverage** |
|:------------:|:-----------:|:-----------------:|:-----------:|:----------------:|:------------:|
| [**R. Biondi**](https://github.com/RiccardoBiondi) <br/> [**N. Curti**](https://github.com/Nico-Curti) | **COVID-19 Lung Segmentation** | **Linux/MacOS** : [![Build Status](https://travis-ci.com/RiccardoBiondi/segmentation.svg?branch=master)](https://travis-ci.com/RiccardoBiondi/segmentation) <br/>  **Windows** : [![Build status](https://ci.appveyor.com/api/projects/status/om6elsnkoi22xii3?svg=true)](https://ci.appveyor.com/project/RiccardoBiondi/segmentation) | [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/RiccardoBiondi/segmentation/blob/master/LICENSE.md) | **Codacy** : [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc0fd47ae8e44ab1943b1f74c2a3d7e2)](https://www.codacy.com/manual/RiccardoBiondi/segmentation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RiccardoBiondi/segmentation&amp;utm_campaign=Badge_Grade) <br/> **Codebeat** : [![CODEBEAT](https://codebeat.co/badges/927db14b-36fc-42ed-88f1-09b2a9e1b9c0)](https://codebeat.co/projects/github-com-riccardobiondi-segmentation-master) | [![codecov](https://codecov.io/gh/RiccardoBiondi/segmentation/branch/master/graph/badge.svg)](https://codecov.io/gh/RiccardoBiondi/segmentation) |

![Project CI](https://github.com/RiccardoBiondi/segmentation/workflows/CTLungSeg%20CI/badge.svg)
![Docs CI](https://github.com/RiccardoBiondi/segmentation/workflows/CTLungSeg%20docs%20CI/badge.svg)

[![docs](https://readthedocs.org/projects/covid-19-ggo-segmentation/badge/?version=latest)](https://covid-19-ggo-segmentation.readthedocs.io/en/latest/?badge=latest)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/pulls)
[![GitHub issues](https://img.shields.io/github/issues/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/issues)

[![GitHub stars](https://img.shields.io/github/stars/RiccardoBiondi/segmentation.svg?label=Stars&style=social)](https://github.com/RiccardoBiondi/segmentation/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/RiccardoBiondi/segmentation.svg?label=Watch&style=social)](https://github.com/RiccardoBiondi/segmentation/watchers)

# COVID-19 Lung Segmentation

This package provides a fast way to isolate lung region and identify ground glass lesions on CT images of patients affected by COVID-19. The segmentation approach is based on color quantization, performed by kmeans clustering. This package provides a series of scripts to isolate lung regions, pre-process the images, estimate kmeans centroids and labels the lung regions; together with methods to perform thresholding, morphological and statistical operations on stack of images.

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

SARS-CoV-2 virus has widely spread all over the world since the beginning of 2020. This virus affect lung areas and causes respiratory illness.
In this scenario is highly desirable a method to identify in CT images the lung injuries caused by COVID-19.
The approach proposed here is based on color quantization to identify the ground glass regions inside lung.
To achieve this purpose the presented approach will use an algorithm to isolate the lung regions and one to label the different lung areas.

The segmentation of lung regions involves three steps:
- Preprocessing: Involves lung, ROI and slice selection
- Training: this process will estimate the centroids for the clusters
- Labeling: In which the centroids estimated by using the train dataset are used to segment the CT images


**Example of segmentation**. **Left:** Original image: **Right** original image with identified ground glass areas.

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/images/results.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/images/results.png" width="400" height="725">
  </div>
</a>

## Contents

COVID-19 Lung segmentation is composed of scripts and modules:
- scripts allows to isolate lung regions, find the centroids for colours quantization and segment the images.
- modules allows to load and save the images from and in different extensions and perform operations on stack of images.

To refer to script documentation:

| **Script** | **Description** |
|:----------:|:---------------:|
| [lung_extraction](./docs/pipeline/lung_extraction.md) | Extract lung from TAC images 										 																																				|
| [train](./docs/pipeline/train.md) | Apply colour quantization on a series of stacks in order to estimate the centroid to use to segment other images  																																													|
| [labeling](./docs/pipeline/labeling.md) |Segment the input image by using pre-estimated centroids |

To refer to modules documentation:

| **Module**| **Description**|
|:---------:|:--------------:|
| [utils](./docs/CTLungSeg/utils.md) | method to load, save and preprocess stack																																										|
| [method](./docs/CTLungSeg/method.md) | method to apply morphological, thresholding and statistical operation on stack of images |
| [segmentation](./docs/CTLungSeg/segmentation.md) | contains useful function to segment stack of images and select			 ROI																										|

For each script described below there are a powershell and a shell script which allow to execute the script on multiple patient.

## Prerequisites

Supported python version: ![Python version](https://img.shields.io/badge/python-3.5|3.6|3.7|3.8-blue.svg)

First of all ensure to have the right python version installed.

This script use opencv-python, numpy, pandas, functool and pickle: see [requirements](#./requirements.txt) for more informations.

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
The input allowed formats are the one supported by SimpleITK_ .

Single Patient Example
----------------------

To segment a single CT scan, simply run the following command from the bash or
pawershell :

.. code-block:: bash

   python -m CTLungSeg --input='/path/to/input/series'  --output='/path/to/output/file'

Which takes as input the CT scan in each format supported by SimpleITK_ . If the
input is a dicom series, simply pass the path to the directory which contains
the series files, please ensure that in the folder there is only one series.

The output label will be saved as '.nrrd'.

### Train your own centroids


Lets consider the case where you have an high number of patient. First of all
you have to divide the data in train and test dataset: the first one to
estimate the centroids used to segment the second one.
To achieve these purpose create two folders named *train* and *test* and
organize your sample inside them. The supported input formats are the ones
availabel from SimpleITK. In case of DICOM series in each folder you have to
create a subfolder for each patient that contains the *.dcm* files.

### Training
 - first of all you have to create the *output* folder, in which all the results will be saved in  *.nii* format.
 - Now you have to isolate the lung from the rest of the body. To do that simply run lung_extraction.ps1 by providing as arguments the input folder and the output one:
 ```powershell
PS \> ./lung_extraction.ps1 path/to/input/folder/ path/to/output/folder/
 ```

 - Once you have successfully isolated the lung, you are ready to train and estimate the centroids. To start the training  simply run train.ps1 by providing as input folder the one that contains the files with the extracted lung, and the output filename in which save the resulting centroids.

```powershell
PS /> ./train.ps1 path/to/input/folder/ path/to/output/folder/centroids
```
This script will compute the centroids and save them into output folder as *centroids.pkl.npy*

### Labeling

Once you have compute the centroids by using the training dataset, you can use them to label the test dataset. To achieve this purpose you have to use two folders: an input one, that in this case is the test one, and an output one, in which the results will saved.

- First of all you have to prepare the images by extracting the lung regions, so run the powershell script as before:
```powershell
PS /> ./lung_extraction.ps1 path/to/input/folder/ path/to/output/folder/
```

- once you have extracted the lung you can start to label the dataset. To achieve this purpose simply run the *labeling.ps1* script by providing the required parameters:
```powershell
PS /> ./labeling.ps1 path/to/input/folder/ path/to/centroids/file/centroids.pkl.npy /path/to/output/folder/
```
The input directory is the one that contains the images with the extracted lung.
The resulting labels will be saved in the output folder as *.nrrd*

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
