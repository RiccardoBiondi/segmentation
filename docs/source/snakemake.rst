Snakemake
=========

Since the segmentation of several patients is time-consuming, we have provided a
snakemake pipeline to automate the process. This pipeline also allows to train
other set of centroids and use it for the segmentation. This file allows to
customize the usage of the hardware resources, like the number of threads and the
amount of memory.

As before, this examples will use he data previously downloaded from the public dataset

Segment Multiple Scan
---------------------

First of all, you have to create two folders:

  - INPUT : contains all and only the CT scans to segment
  - OUTPUT : empty folder, will contain the segmented scans as *nrrd*.

Now simply execute from command line

.. code-block:: bash

  snakemake --cores 1 --config input_path='./Examples/INPUT/' --output_path='./Examples/OUTPUT/'

.. note::

  It will create a folder named **LUNG** inside the INPUT, which
  contains the results of the lung extraction step.

Train a Centroid Set
--------------------

Prepare three folders:
  - INPUT: will contains all the scans to segment
  - OUTPUT: will contain the segmented scans
  - TRAIN: will contain all the scans of the training set.

Now run Snakemake with the following configuration parameters :

.. code-block:: bash

  snakemake --cores 1 --config input_path='./Examples/INPUT/' --output_path='./Examples/OUTPUT/'
  --train_path='./Examples/TRAIN/' --centroid_path='.Examples/centorid_set.pkl.npy'

This will train the centroid set and use them to segment the input scans.

.. note::

  This will create a folder named LUNG inside INPUT and TRAIN which
  contains the scans after lung extraction.

.. warning::

  The `TRAIN` folder cannot be the same of `INPUT`!

Configuration
-------------

We have provided a configuration file (config.yaml) which allows to manage the
resources and the path, which we usually provide from command-line.

**Threads**:

  - *threads_labelling* : Set the number of threads to use for the labelling process (default = 8);

  - *threads_lung_extraction* : Set the number of threads to use for the lung_extraction (default = 8);

  - *threads_train* : Set the number of threads to use for the training process (default = 8).

**Memory**:

  - memory_labelling : 8
  - memory_lung_extraction : 8
  - memory_train : 8

**Training Parameters**:

It is possible to specify the parameters for the training step:

  - n_subsamples : number of subsamples in which the slice of the training set  will be divided during the training;

  - centroid_initialization : technique to use for the initialization of the centroids during k-means (0 for random initialization, 1 for k-means++)
