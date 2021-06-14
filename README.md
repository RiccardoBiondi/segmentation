| **Authors**  | **Project** |  **Build Status** | **License** | **Code Quality** | **Coverage** |
|:------------:|:-----------:|:-----------------:|:-----------:|:----------------:|:------------:|
| [**R. Biondi**](https://github.com/RiccardoBiondi) <br/> [**N. Curti**](https://github.com/Nico-Curti) | **COVID-19 Lung Segmentation** | **Linux** : [![Build Status](https://travis-ci.com/RiccardoBiondi/segmentation.svg?branch=master)](https://travis-ci.com/RiccardoBiondi/segmentation) <br/>  **Windows** : [![Build status](https://ci.appveyor.com/api/projects/status/om6elsnkoi22xii3?svg=true)](https://ci.appveyor.com/project/RiccardoBiondi/segmentation) | [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/RiccardoBiondi/segmentation/blob/master/LICENSE.md) | **Codacy** : [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc0fd47ae8e44ab1943b1f74c2a3d7e2)](https://www.codacy.com/manual/RiccardoBiondi/segmentation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RiccardoBiondi/segmentation&amp;utm_campaign=Badge_Grade) <br/> **Codebeat** : [![CODEBEAT](https://codebeat.co/badges/927db14b-36fc-42ed-88f1-09b2a9e1b9c0)](https://codebeat.co/projects/github-com-riccardobiondi-segmentation-master) | [![codecov](https://codecov.io/gh/RiccardoBiondi/segmentation/branch/master/graph/badge.svg)](https://codecov.io/gh/RiccardoBiondi/segmentation) |

![Project CI](https://github.com/RiccardoBiondi/segmentation/workflows/CTLungSeg%20CI/badge.svg)
![Docs CI](https://github.com/RiccardoBiondi/segmentation/workflows/CTLungSeg%20Docs%20CI/badge.svg)

[![docs](https://readthedocs.org/projects/covid-19-ggo-segmentation/badge/?version=latest)](https://covid-19-ggo-segmentation.readthedocs.io/en/latest/?badge=latest)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/pulls)
[![GitHub issues](https://img.shields.io/github/issues/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/issues)

[![GitHub stars](https://img.shields.io/github/stars/RiccardoBiondi/segmentation.svg?label=Stars&style=social)](https://github.com/RiccardoBiondi/segmentation/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/RiccardoBiondi/segmentation.svg?label=Watch&style=social)](https://github.com/RiccardoBiondi/segmentation/watchers)

# COVID-19 Lung Segmentation

This package allows to isolate the lung region and identify ground glass lesions
on chest CT scans of patients affected by COVID-19.
The segmentation approach is based on color quantization, performed by K-means
clustering.
This package provides a series of scripts to isolate lung regions, pre-process
the images, estimate K-means centroids and labels of the lung regions.

1. [Overview](#Overview)
2. [Contents](#Contents)
3. [Prerequisites](#Prerequisites)
4. [Installation](#Installation)
5. [Usage](#Usage)
6. [License](#License)
7. [Contribution](#Contribution)
8. [References](#References)
9. [Authors](#Authors)
10. [Acknowledgments](#Acknowledgments)
11. [Citation](#Citation)

## Overview

COronaVirus Disease (COVID-19) has widely spread all over the world since the
beginning of 2020. It is acute, highly contagious, viral infection mainly
involving the respiratory system. Chest CT scans of patients affected by this
condition have shown peculiar patterns of Ground Glass Opacities (GGO) and Consolidation (CS) related to the severity and the stage of the disease.

In this scenario, the correct and fast identification of these patterns is a
fundamental task. Up to now this task is performed mainly using manual or
semi-automatic techniques, which are time-consuming (hours or days) and
subjected to the operator expertise.

This project provides an automatic pipeline for the segmentation of
GGO areas on chest CT scans of patient affected by COVID-19.
The segmentation is achieved with a color quantization algorithm, based on
k-means clustering, grouping voxel by color and texture similarity.

**Example of segmentation**. **Left:** Original image: **Right** original image with identified ground-glass areas.

<a href="https://github.com/RiccardoBiondi/segmentation/blob/master/images/results.png">
  <div class="image">
    <img src="https://github.com/RiccardoBiondi/segmentation/blob/master/images/results.png" width="800" height="400">
  </div>
</a>

The pipeline was tested on 15 labeled chest CT scans, manually segmented by
expert radiologist.
The goodness of the segmentation was estimated using Dice(0.67 ± 0.12),
Sensitivity(0.666 ± 0.15), Specificity(0.9993 ± 0.0005) and
Precision(0.75± 0.20) scores.

These results make the pipeline suitable as initialization for more accurate
methods

## Contents

COVID-19 Lung segmentation is composed of scripts and modules:
- scripts allows to isolate lung regions, find the centroids for colour quantization and segment the images.
- modules allows to load and save the images from and to different extensions and perform operations on image series.

To refer to script documentation:

| **Script** | **Description** |
|:----------:|:---------------:|
| [lung_extraction](./docs/pipeline/lung_extraction.md) | Extract lung from CT scans 										 																																				|
| [train](./docs/pipeline/train.md) | Apply colour quantization on a series of stacks to estimate the centroid to use for segmentation																																													|
| [labeling](./docs/pipeline/labeling.md) |Segment the input image by using pre-estimated centroids or user-provided set|

To refer to modules documentation:

| **Module**| **Description**|
|:---------:|:--------------:|
| [utils](./docs/CTLungSeg/utils.md) | method to load, save and preprocess stack																																										|
| [method](./docs/CTLungSeg/method.md) | method to filter the image tensor |
| [segmentation](./docs/CTLungSeg/segmentation.md) | contains useful function to segment stack of images and select ROI																										|

For each script described below, there are a PowerShell and a shell script that
allows their execution on multiple patients scans. Moreover it also provide a
snekemake pipeline.

## Prerequisites

Supported python version: ![Python version](https://img.shields.io/badge/python-3.5|3.6|3.7|3.8-blue.svg)

First of all ensure to have the right python version installed.

This script use opencv-python, numpy and SimpleITK: see
[requirements](https://github.com/RiccardoBiondi/segmentation/blob/master/requirements.txt)
for more informations.

The lung extraction is performed by using a pre-trained UNet, so please ensure to
have installed the [lungmask](https://github.com/JoHof/lungmask) package.
For more information about how the network is trained, please refer
to https://doi.org/10.1186/s41747-020-00173-2.

> :warning: The OpenCV requirement binds the minimum Python version of this project
> to Python 3.5!

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

and build the package using the command:

```bash
python setup.py install
```

### Testing

Testing routines use ```PyTest``` and ```Hypothesis``` packages. please install
these packages to perform the test.
A full set of test is provided in [testing](https://github.com/RiccardoBiondi/segmentation/blob/master/testing) directory.
You can run the full list of test with:

```bash
python -m pytest
```

## Usage

### Single Scan

Once you have installed it, you can directly start to segment the images.
Input CT scans must be in Hounsfield units(HU) since grey-scale
images are not allowed.
The input allowed formats are the ones supported by SimpleITK.
If the input is a DICOM series, pass the path to the directory containing
the series files.
Please ensure that the folder contains only one series.
As output will save the segmentation as *nrrd*.

To segment a single CT scan run the following from the bash or PowerShell:

```bash
   python -m CTLungSeg --input='/path/to/input/series/'  --output='/path/to/output/file/'
```

### Multiple Scans

We have provided a snakemake pipeline and bash(or PowerShell) scripts to
automate the process and make it  easier to segment many scans.

#### Snakemake

First of all, you have to create two folders :
  - INPUT : contains all and only the CT scans to segment
  - OUTPUT : empty folder, will contain the segmented scans as *nrrd*.

Execute from command line

```bash
  snakemake --cores 1 --config input_path='/path/to/INPUT/'
  --output_path='/path/to/OUTPUT/'
```

**Note**: It will create a folder named **LUNG** inside the INPUT,
which contains the results of the lung extraction step.

#### Bash and Powershell script

It is possible to achieve the same results as before.
First of all, you have to create three folders :

- input folder: contains all and only the CT scans to segment
- temporary folder: empty folder. Will contain the scans after the lung segmentation
- output folder: empty folder, will contain the labels files.

Now you can proceed with the lung segmentation. To achieve this purpose simply run
from PowerShell the  script:

 ```PowerShell
  PS \> ./lung_extraction.ps1 path/to/input/folder/ path/to/temporary/folder/
 ```

Or its equivalent bash version:

```bash
  $ ./lung_extraction.sh path/to/input/folder/ path/to/temporary/folder/
```

Once you have successfully isolated the lung, you are ready to perform the GGO
segmentation. Run the labelling scrip from PowerShell :

```PowerShell
  PS /> ./labeling.ps1 path/to/temporary/folder/ p /path/to/output/folder/
```

Or its corresponding bash version:

```bash
$ ./labeling.sh path/to/temporary/folder/ p /path/to/output/folder/
```

### Train your own centroids set

It is possible to train your centroid set instead of using the pre-trained one.
To do that, you can use a snakemake or a bash or PowerShell script.

#### Snakemake

Prepare three folders :
  - INPUT: will contains all the scans to segment
  - OUTPUT: will contain the segmented scans
  - TRAIN: will contain all the scans of the training set. (**NOTE** Cannot be the INPUT folder)

Now run Snakemake with the following configuration parameters :

```bash
  snakemake --cores 1 --config input_path='/path/to/INPUT/'
  --output_path='/path/to/OUTPUT/' --train_path='/path/to/TRAIN/' --centroid_path='/path/to/save/your/centorid/set.pkl.npy'
```

#### Bash and PowerShell scrirpt

In this case you have to prepare two folder :
  - TRAIN : will contain the scans in the training set
  - LUNG : will stores the scans after lung extraction

First of all, you have to perform the lung extraction on the train scans,
as before run:

```bash
  $ ./lung_extraction.sh path/to/TRAIN/ path/to/LUNG/
```

or its corresponding PowerShell version. Now, to estimate the centroid set, run:

```bash
  $ ./train.sh path/to/LUNG/ path/to/centroid.pkl.npy
```

or its corresponding PowerShell version.

## License

The `COVID-19 Lung Segmentation` package is licensed under the MIT "Expat" License.
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE.md)

## Contribution

Any contribution is more than welcome.
Just fill an [issue](./.github/ISSUE_TEMPLATE/ISSUE_TEMPLATE.md) or a
[pull request](./.github/PULL_REQUEST_TEMPLATE/PULL_REQUEST_TEMPLATE.md)
and we will check ASAP!

See [here](https://github.com/RiccardoBiondi/segmentation/blob/master/CONTRIBUTING.md)
for further informations about how to contribute with this project.

## References

<blockquote>1- Hofmanninger, J., Prayer, F., Pan, J. et al. Automatic lung segmentation in routine imaging is primarily a data diversity problem, not a methodology problem. Eur Radiol Exp 4, 50 (2020). https://doi.org/10.1186/s41747-020-00173-2. </blockquote>

<blockquote>2- Bradski, G. (2000). The OpenCV Library. Dr. Dobb&#x27;s Journal of Software Tools.</blockquote>

<blockquote>3- Yaniv, Z., Lowekamp, B.C., Johnson, H.J. et al. SimpleITK Image-Analysis Notebooks: a Collaborative Environment for Education and Reproducible Research. J Digit Imaging 31, 290–303 (2018). https://doi.org/10.1007/s10278-017-0037-8.</blockquote>

<blockquote>4- Lowekamp Bradley, Chen David, Ibanez Luis, Blezek Daniel The Design of SimpleITK  Frontiers in Neuroinformatics 7, 45 (2013) https://www.frontiersin.org/article/10.3389/fninf.2013.00045.</blockquote>


## Authors

* <img src="https://avatars3.githubusercontent.com/u/48323959?s=400&v=4" width="25px"> **Riccardo Biondi** [git](https://github.com/RiccardoBiondi)

* <img src="https://avatars0.githubusercontent.com/u/24650975?s=400&v=4" width="25px"> **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)

* <img src="https://avatars2.githubusercontent.com/u/1419337?s=400&v=4" width="25px;"/> **Enrico Giampieri** [git](https://github.com/EnricoGiampieri), [unibo](https://www.unibo.it/sitoweb/enrico.giampieri)

* <img src="https://www.unibo.it/uniboweb/utils/UserImage.aspx?IdAnagrafica=236217&IdFoto=bf094429" width="25px;"/> **Gastone Castellani** [unibo](https://www.unibo.it/sitoweb/gastone.castellani)

See also the list of [contributors](https://github.com/RiccardoBiondi/segmentation/contributors) [![GitHub contributors](https://img.shields.io/github/contributors/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/graphs/contributors/) who participated to this project.

### Citation

If you have found `COVID-19 Lung Segmentation` helpful in your research, please
consider citing the original paper

```BibTeX
@article{app11125438,
  author = {Biondi, Riccardo and Curti, Nico and Coppola, Francesca and Giampieri, Enrico and Vara, Giulio and Bartoletti, Michele and Cattabriga, Arrigo and Cocozza, Maria Adriana and Ciccarese, Federica and De Benedittis, Caterina and Cercenelli, Laura and Bortolani, Barbara and Marcelli, Emanuela and Pierotti, Luisa and Strigari, Lidia and Viale, Pierluigi and Golfieri, Rita and Castellani, Gastone},
  title = {Classification Performance for COVID Patient Prognosis from Automatic AI Segmentation—A Single-Center Study},
  journal = {Applied Sciences},
  volume = {11},
  year = {2021},
  number = {12},
  article-number = {5438},
  url = {https://www.mdpi.com/2076-3417/11/12/5438},
  issn = {2076-3417},
  doi = {10.3390/app11125438}
}
```

or just this project

```BibTeX
@misc{COVID-19 Lung Segmentation,
  author = {Biondi, Riccardo and Curti, Nico and Giampieri, Enrico and Castellani, Gastone},
  title = {COVID-19 Lung Segmentation},
  year = {2020},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/RiccardoBiondi/segmentation}},
}

```
