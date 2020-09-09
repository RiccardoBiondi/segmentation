| **Authors**  | **Project** |  **Build Status** | **License** | **Code Quality** | **Coverage** |
|:------------:|:-----------:|:-----------------:|:-----------:|:----------------:|:------------:|
| [**R. Biondi**](https://github.com/RiccardoBiondi) <br/> [**N. Curti**](https://github.com/Nico-Curti) | **COVID-19 Lung Segmentation** | **Linux/MacOS** : **TODO** <br/>  **Windows** : [![Build status](https://ci.appveyor.com/api/projects/status/om6elsnkoi22xii3?svg=true)](https://ci.appveyor.com/project/RiccardoBiondi/segmentation) | [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/RiccardoBiondi/segmentation/blob/master/LICENSE.md) | **Codacy** : [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc0fd47ae8e44ab1943b1f74c2a3d7e2)](https://www.codacy.com/manual/RiccardoBiondi/segmentation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RiccardoBiondi/segmentation&amp;utm_campaign=Badge_Grade) <br/> **Codebeat** : [![CODEBEAT](https://codebeat.co/badges/927db14b-36fc-42ed-88f1-09b2a9e1b9c0)](https://codebeat.co/projects/github-com-riccardobiondi-segmentation-master) |[![codecov](https://codecov.io/gh/RiccardoBiondi/segmentation/branch/master/graph/badge.svg)](https://codecov.io/gh/RiccardoBiondi/segmentation)|

![Project CI](https://github.com/RiccardoBiondi/segmentation/workflows/Project%20CI/badge.svg)

[![GitHub pull-requests](https://img.shields.io/github/issues-pr/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/pulls)
[![GitHub issues](https://img.shields.io/github/issues/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/issues)

[![GitHub stars](https://img.shields.io/github/stars/RiccardoBiondi/segmentation.svg?label=Stars&style=social)](https://github.com/RiccardoBiondi/segmentation/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/RiccardoBiondi/segmentation.svg?label=Watch&style=social)](https://github.com/RiccardoBiondi/segmentation/watchers)

# COVID-19 Lung Segmentation

This package provides a fast way to isolate lung regions and identify ground glass lesions on CT images of patients affected by COVID-19.
The segmentation approach is based on color quantization, performed by kmeans clustering.
This package provides a series of scripts to isolate lung regions, pre-process the images, estimate kmeans centroids and labels the lung regions; together with methods to perform thresholding, morphological and statistical operations on stack of images.

## Table of Contents

1. [Introduction](#Introduction)
2. [Structure](#Structure)
3. [Installation](#installation)
4. [Contribution](#contribution)
5. [Authors](#authors)
6. [Acknowledgments](#acknowledgments)
7. [Citation](#citation)

## Introduction

SARS-CoV-2 virus has widely spread all over the world since the beginning of 2020. This virus affect lung areas and causes respiratory illness.
In this scenario is highly desirable a method to identify in CT images the lung injuries caused by COVID-19.
The approach proposed here is based on color quantization to identify the ground glass regions inside lung.
The implementation makes extensive use of ```Numpy``` and ```opencv-python```, in this way it is very light and fast.

## Structure

COVID-19 Lung segmentation is composed of scripts and modules:
- scripts allows to isolate lung regions, find the centroids for colours quantization and segment the images.
- modules allows to load and save the images from and in different extensions and perform operations on stack of images.

To refer to script documentation:

| **Script** | **Description** |
|---              |---              |
| [lung_extraction](./pipeline/lung_extraction.md)   |  Extract lung from TAC images										 																																|
| [slice_and_ROI](./pipeline/slice_and_ROI.md)  | Select only slices and areas containing the lungs 										 																																 |
| [train](./pipeline/train.md)  | Apply colour quantization on a series of stacks in order to estimate the centroids to use to segment other images |
| [labeling](./pipeline/labeling.md)  |  Segment the input image by using pre-estimated centroids 										 																																|

To refer to modules documentation:

| **Module**| **Description**|
|---              |---              |
| [utils](./CTLungSeg/utils.md) | method to load, save and preprocess stack																									|
| [method](./CTLungSeg/method.md) | method to apply morphological, thresholding and statistical operation on stack of images |

## Installation

Supported python version: ![Python version](https://img.shields.io/badge/python-3.5,3.6,3.7,3.8-blue.svg)

First of all ensure to have the right python version installed.

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

Testing routines use ```PyTest``` and ```Hypothesis``` packages; please install these packages to perform the test.
All the full set of test is provided in [testing]() directory. You can run the full list of test with:

```bash
python -m pytest
```

The continuous integration using `Travis` and `Appveyor` tests each function in every commit, thus pay attention to the status badges before use this package or use the latest stable version available.

## Contribution

Any contribution is more than welcome. Just fill an [issue](https://github.com/RiccardoBiondi/segmentation/blob/master/ISSUE_TEMPLATE.md) or a [pull request](https://github.com/RiccardoBiondi/segmentation/blob/master/PULL_REQUEST_TEMPLATE.md) and we will check ASAP!

See [here](https://github.com/RiccardoBiondi/segmentation/blob/master/CONTRIBUTING.md) for further informations about how to contribute with this project.

## Authors

* <img src="https://avatars3.githubusercontent.com/u/48323959?s=400&v=4" width="25px"> **Riccardo Biondi** [git](https://github.com/RiccardoBiondi)

* <img src="https://avatars0.githubusercontent.com/u/24650975?s=400&v=4" width="25px"> **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)

* <img src="https://avatars2.githubusercontent.com/u/1419337?s=400&v=4" width="25px;"/> **Enrico Giampieri** [git](https://github.com/EnricoGiampieri), [unibo](https://www.unibo.it/sitoweb/enrico.giampieri)

See also the list of [contributors](https://github.com/RiccardoBiondi/segmentation/contributors) [![GitHub contributors](https://img.shields.io/github/contributors/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/graphs/contributors/) who participated to this project.
