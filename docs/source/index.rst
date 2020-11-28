.. CTLungSeg documentation master file, created by
   sphinx-quickstart on Wed Oct 21 12:55:39 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CTLungSeg's documentation!
=====================================

Automatic Pipeline for the segmentation of Ground Glass Opacities on CT thorax
scans of COVID-19 affected patients.

This package provides a fast way to isolate lung region and identify ground glass
lesions on CT images of patients affected by COVID-19.
The segmentation approach is based on colour quantization,
performed by K-means clustering. This package provides a series of scripts to
isolate lung regions, pre-process the images, estimate K-means centroids and
labels the lung regions; together with methods to perform thresholding,
morphological and statistical operations on the stack of images.

.. image :: ../../images/results.png


Usage Example
=============

Once you have installed you can directly start to segment the images.
Input CT scans must be in Hounsfield units(HU), gray-scale images are not allowed.
The input allowed formats are the one supported by SimpleITK_ .

Single Patient Example
----------------------

To segment a single CT scan, run the following command from the bash or
pawershell :

.. code-block:: bash

   python -m CTLungSeg --input='/path/to/input/series'  --output='/path/to/output/file'

Which takes as input the CT scan in each format supported by SimpleITK_. If the
input is a Dicom series, simply pass the path to the directory which contains
the series files, please ensure that in the folder there is only one series.

The output label will be saved as '.nrrd'.




Multiple Patient Example
------------------------

Segmenting many patients can be time-consuming, so a series of bash and
PowerShell scripts are provided, to automatize the procedure for more
then one patient.
In this case, the segmentation is divided into two different steps :

- lung extraction
- actual segmentation

First of all you have to organize all the input scans into the input folder,
and crate an empty folder in which the results of the first step will be saved
as '.nii'.
After that simply run the bash or the PowerShell script:

.. code-block:: bash

   ./lung_extraction.sh /path/to/input/folder/ /path/to/lung/folder/

.. code-block:: bash

  ./lung_extraction.sh /path/to/input/folder/ /path/to/output/folder/


Once this step is completed, you can perform the actual segmentation. First of
all create an empty output folder in which the resulting labels will be saved
as '.nrrd' and run the bash or powershell script .


.. code-block:: bash

  ./labeling.sh /path/to/lung/folder/ /path/to/output/folder/


.. _SimpleITK: https://simpleitk.org/


.. toctree::
  :maxdepth: 2
  :caption: Contents:

  installation
  theory
  modules
  script
  references


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
