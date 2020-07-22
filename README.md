| **Authors**  | **Project** |  **Build Status** | **License** | **Code Quality** | **Coverage** |
|:------------:|:-----------:|:-----------------:|:-----------:|:----------------:|:------------:|
| [**R. Biondi**](https://github.com/RiccardoBiondi) <br/> [**N. Curti**](https://github.com/Nico-Curti) | **COVID-19 Lung Segmentation** | **Linux/MacOS** : [![travis]()]() <br/>  **Windows** : [![appveyor]()]() | [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/RiccardoBiondi/segmentation/blob/master/LICENSE.md) | **Codacy** : [![Codacy](https://app.codacy.com/project/badge/Grade/38d6614cd0e04e7db2c38648e195087a)](https://www.codacy.com/manual/RiccardoBiondi/segmentation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RiccardoBiondi/segmentation&amp;utm_campaign=Badge_Grade)] <br/> **Codebeat** : [![CODEBEAT](https://codebeat.co/badges/927db14b-36fc-42ed-88f1-09b2a9e1b9c0)](https://codebeat.co/projects/github-com-riccardobiondi-segmentation-master)] | [![codecov](226de693-2815-426c-a3ee-d1169e09913c)]() |

![Project CI](https://github.com/RiccardoBiondi/segmentation/workflows/Project%20CI/badge.svg)

[![GitHub pull-requests](https://img.shields.io/github/issues-pr/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/pulls)
[![GitHub issues](https://img.shields.io/github/issues/RiccardoBiondi/segmentation.svg?style=plastic)](https://github.com/RiccardoBiondi/segmentation/issues)

[![GitHub stars](https://img.shields.io/github/stars/RiccardoBiondi/segmentation.svg?label=Stars&style=social)](https://github.com/RiccardoBiondi/segmentation/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/RiccardoBiondi/segmentation.svg?label=Watch&style=social)](https://github.com/RiccardoBiondi/segmentation/watchers)

# COVID-19 Lung Segmentation

The project is developed in order to provide an easy to use and fast way to segment lung TAC images. It will offers a series of script to pre-process and cluster the stack of lung images. This program allows to isolate body an lung regions, apply a median blurring  and reduce the background by selecting a ROI and in the clustering by using the kmeans clustering algorithm to perform the colour quantization.


1. [Contents](#Contents)
2. [Prerequisites](#prerequisites)
3. [Usage](#usage)
4. [License](#license)
5. [Contribution](#contribution)
6. [Authors](#authors)
7. [Acknowledgments](#acknowledgments)
8. [Citation](#citation)

## Contents

In pipeline is implemented a series of script to segment lung TAC images:

1. [lungselection](./docs/pipeline/lungselection.md)
2. [medianBlur](./docs/pipeline/medianBlur.md)
3. [slice_and_ROI](./docs/pipeline/slice_and_ROI.md)
4. [clustering](./docs/pipeline/clustering.md)
5. [training](./docs/pipeline/taining.md)
6. [labeling](./docs/pipeline/labeling.md)

Instead in segmentation is implemented the libraries [method](./docs/method.md) and [stats_method](./docs/stats_method.md) contains the functions used to implement the script and can be used as a useful library to process stack of images.

## Prerequisites

This script use opencv-python, numpy, matplotlib, pandas, functool and pickle.
Please ensure that your python version support these libraries before use these scripts. Only *labeling* script use sklearn.clustering.KMeans, so if you have to run it, please ensure to have installed sklearn.

## Usage

Lets consider the segmentation of a stack of lung TAC images saved as `stack.pkl.npy` in `data` folder.
First of all you have to create the lung mask by calling `lungselection` script from powershell or bash.
```
python -m pipeline.lungselection --input='path/to/data/folder/stack.pkl.npy' --lung='path/to/data/folder/lung_mask'
```
This will find a lung mask for each slice of `stack.pkl.npy` and save it in `data` folder as `lung_mask.pkl.npy`

After that we can apply a median blur filter by calling `medianBlur` script form powershell or bash and specify the path to the input data and lung mask:

```
python -m pipeline.medianBlur --input='path/to/data/folder/stack.pkl.npy' --mask='path/to/data/folder/lung_mask.pkl.npy'
--output='path/to/data/folder/blurred'
```

This will apply a median blurring filter to the masked image and save the results in `data` folder as `blurred.pkl.npy`

Before applying the kmeans clustering we have to remove as much as possible of the background by select a ROI, which is the rectangular region with the smaller area that still contains the lungs.

```
python -m pipeline.slice_and_ROI --input='path/to/data/folder/lung_mask.pkl.npy'
--output='path/to/data/folder/ROI'
```

To compute the ROI in the correct wat we have to provide as input the lung mask. the script will compute the ROI and save the coordinate of the upper left and bottom right corner of the region as `ROI.pkl.npy`.

Now we are able to perform the colour quantization by applying the kmenas clustering.
```
python -m pipeline.clustering --input='path/to/data/folder/blurred.pk.npy'
--ROI='path/to/data/folder/ROI.pkl.npy' --labels='path/to/data/folder/labels'
--centroid='path/to/data/folder/centroinds' --n_clust=4
```

We have performed the color quantization on the blurred image, by providing the *ROI* arguments we have clustered only the ROI. the arguments *--labels* and *--centroid* specify the path and the filename to save the labeled images and the computed centroids. last but not least *--n_clust* will specify the number of the clusters to consider.

Notice that each input file must be in `.pkl.npy` format; the output file will be in the same format.

s
Run these scripts in the presented order is not mandatory, it is also possible to avoid the execution of some scripts, for example it is possible to rub only clustering; however we suggest to execute the scripts in the presented order to obtain a good segmentation.

Refers to [docs](./docs/index.md) for more informations.


## License

The `COVID-19 Lung Segmentation` package is licensed under the MIT "Expat" License. [![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/RiccardoBiondi/segmentation/blob/master/LICENSE.md)

## Contribution

Any contribution is more than welcome `:heart:`. Just fill an [issue](https://github.com/RiccardoBiondi/segmentation/blob/master/ISSUE_TEMPLATE.md) or a [pull request](https://github.com/RiccardoBiondi/segmentation/blob/master/PULL_REQUEST_TEMPLATE.md) and we will check ASAP!

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
