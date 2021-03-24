Snakemake
=========

Since the segmentation of several patients is time-consuming, we have provided a
snakemake pipeline to automate the process. These pipeline also allows to train
other set of centroids and use it for the segmentation. This file allows also
to set the usage of the hardware resources, like the number of threads and the
amount of memory.

Segment Multiple Scan
---------------------

First of all, you have to creat two folders :
  - INPUT : contains all and only the CT scans to segment
  - OUTPUT : mpty folder, will contain the segmented scans as *nrrd*.

Now simply execute from command line

.. code-block:: bash

  snakemake --cores 1 --config input_path='/path/to/INPUT/' --output_path='/path/to/OUTPUT/'


**Note**: It will create a folder named **LUNG** inside the INPUT, which contains the results of the lung extraction step.


Train a Centroid Set
--------------------

Prepare three folders :
  - INPUT: will contains all the scans to segment
  - OUTPUT: will contain the segmented scans
  - TRAIN: will contain all the scans of the training set. (**Note** Cannot be the INPUT folder)

Now run Snakemake with the following configuration parameters :

.. code-block:: bash

  snakemake --cores 1 --config input_path='/path/to/INPUT/' --output_path='/path/to/OUTPUT/' --train_path='/path/to/TRAIN/' --centroid_path='/path/to/save/your/centorid/set.pkl.npy'

This will train the centroid set and use them to segment the input scans.

**Note** : This will create a folder named LUNG inside INPUT and TRAIN which
contains the scans after lung extraction.

Configuration
-------------

We have provided a configuration file (config.yaml) which allows to manage the
resources and the path, which we usually provide from command-line.

**Threads** :

  - *threads_labelling* : Set the number of threads to use for the labelling process (default = 8);

  - *threads_lung_extraction* : Set the number of threads to use for the lung_extraction (default = 8);

  - *threads_train* : Set the numebr of threads to use for the training porcess (defautl = 8).

**Memory**

  - memory_labelling : 8
  - memory_lung_extraction : 8
  - memory_train : 8

**Training Parameters**

It is possible to specify the parameters for the training step:
   - n_subsamples : number of subsamples in which the slice of the training set  will be divided during the training;
   - centroid_initialization : techinique to use for the initialization of the centroids during k-means (0 for random initialization, 1 for kmeans++)
