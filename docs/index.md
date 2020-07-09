| **Authors**  | **Project** |  **Build Status** | **License** | **Code Quality** | **Coverage** |
|:------------:|:-----------:|:-----------------:|:-----------:|:----------------:|:------------:|
| [**R. Biondi**](https://github.com/RiccardoBiondi) <br/> [**N. Curti**](https://github.com/Nico-Curti) | **COVID-19 Lung Segmentation** | **Linux/MacOS** : [![travis]()]() <br/>  **Windows** : [![appveyor]()]() | [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/RiccardoBiondi/segmentation/blob/master/LICENSE.md) | **Codacy** : [![Codacy]()]() <br/> **Codebeat** : [![CODEBEAT]()]() | [![codecov]()]() |

![Project CI](https://github.com/RiccardoBiondi/segmentation/workflows/Project%20CI/badge.svg)

[![GitHub pull-requests](https://img.shields.io/github/issues-pr/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/pulls)
[![GitHub issues](https://img.shields.io/github/issues/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/issues)

[![GitHub stars](https://img.shields.io/github/stars/RiccardoBiondi/segmentation.svg?label=Stars&style=social)](https://github.com/RiccardoBiondi/segmentation/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/RiccardoBiondi/segmentation.svg?label=Watch&style=social)](https://github.com/RiccardoBiondi/segmentation/watchers)

# COVID-19 Lung Segmentation



1. [Introduction](#Introduction)
2. [Contents](#Contents)
3. [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [Contribution](#contribution)
6. [Authors](#authors)
7. [Acknowledgments](#acknowledgments)
8. [Citation](#citation)

## Introduction
COVID-19 Lung segmentation offers a series of scripts to isolate the lung from
TAC images and to discriminate the different areas by using the k-means
 clustering algorithm.
## Contents

COVID-19 Lung segmentation is composed of scripts, stored in pipeline, and a libraries, stored in segmentation, which implements all the useful function used by the scripts.

The scripts are:

1. [lungselection](./pipeline/lungselection.md)
2. [medianBlur](./pipeline/medianBlur.md)
3. [slice_and_ROI](./pipeline/slice_and_ROI.md)
4. [clustering](./pipeline/clustering.md)

And a library description is in [method](method.md).

## Usage
  **TODO**

## Contribution
  **TODO**

## Authors

* <img src="https://avatars3.githubusercontent.com/u/48323959?s=400&v=4" width="25px"> **Riccardo Biondi** [git](https://github.com/RiccardoBiondi)

* <img src="https://avatars0.githubusercontent.com/u/24650975?s=400&v=4" width="25px"> **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)

* <img src="https://avatars2.githubusercontent.com/u/1419337?s=400&v=4" width="25px;"/> **Enrico Giampieri** [git](https://github.com/EnricoGiampieri), [unibo](https://www.unibo.it/sitoweb/enrico.giampieri)

See also the list of [contributors](https://github.com/RiccardoBiondi/segmentation/contributors) [![GitHub contributors](https://img.shields.io/github/contributors/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/graphs/contributors/) who participated to this project.
