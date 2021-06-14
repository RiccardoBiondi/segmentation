Script
======
Since the segmentation of several patients is time-consuming, some scripts
to automatize this process are provided. The scripts are in two versions: bash and
PowerShell. The segmentation approach is different, instead of to perform the
entire segmentation of all the patient all at once, the segmentation steps are
divided into two different steps :

- lung extraction
- labeling

Lung Extraction
---------------

This script allows to run the lung segmentation on the whole set of patients,
that is the preliminary step of the GGO identification. Its implemented both for
bash and PowerShell.
To perform the segmentation simply organize all the CT scans in the same folder
(input folder), and create an empty folder in which the results will be saved.
Ensure that in the input folder there are only the files corresponding to the scan
to segment. The supported input format are all the ones supported by SimpleITK_.
you can provide as input also DICOM series, simply arrange them into one folder
for each scan. Please ensure that all the subsamples contain only one series.

Now you can simply run the following command from bash :

.. code-block:: bash

  lung_extraction.sh /path/to/input/folder/ /path/to/output/folder/

or its equivalent for powershell

.. code-block:: powershell

  lung_extraction.ps1 /path/to/input/folder/ /path/to/output/folder/

For lung extraction, a pre-trained UNet model was used. The model and the
code used to apply it belong to this_ repository. For more details, please
refers here_.

Labeling
--------

Once you have isolated the lung, you can run the actual segmentation. As for
lung extraction, simply arrange all the results of the previous script into an
input folder; as before creating an empty folder in which the resulting labels
will be saved in '.nrrd' format.
Simply run the bash script:

.. code-block:: bash

  labeling.sh /path/to/input/folder/ /path/to/output/folder/

or its equivalent for powershell

  .. code-block:: powershell

    labeling.ps1 /path/to/input/folder/ /path/to/output/folder/

This will run the segmentation by using the already estimated centroids. If you
want to use another set of centroids, simply provide as third arguments the path
of the file in which the set of centroids is saved

Train
-----

Even if with the script a set of pre-estimated centroids is provided, we also provide
a script to train another set of centroids. To perform the training simply organize
the scans resulting from the lung extraction into the same folder, this will be the
training set. Now simply the training script:

.. code-block:: bash

  python -m CTLungSeg.train --input='/path/to/input/folder/' --output='/path/to/output/centroids'

Once you have run this script, a brief recap of the training parameter will be
displayed :

.. code-block:: bash

  I'm Loading...
  Loaded 20 files from /path/to/input/folder/
  *****Starting clustering*****
  Number of subsamples--> 100
  Total images --> 4000
  Centroid initialization technique-->KMEANS_RANDOM_CENTERS
  I'm clustering...
  100%|█████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:14<00:00,  2.86s/it]
  I'm saving...
  [DONE]

All the images will be divided into N subsamples, and a K-means clustering is
performed for each subsample, after that a second clustering is performed in order
to refine the clustering and provide the set of centroids.
To control the parameters simply provides the following arguments when the script
is execute:

* init : centroid initialization algorithm: if 0 the centroids will be initialized
            randomly, if 1 the K-means++ center will be used.

* n : number of subsamples, as default as 100.

Once the training is complete, the centroid file will be stored in `.pkl.npy`
format.

.. note::

  please notice that this process may be time consuming and computational expansive

.. _SimpleITK: https://simpleitk.readthedocs.io/en/master/IO.html
.. _this: https://github.com/JoHof/lungmask
.. _here: https://eurradiolexp.springeropen.com/articles/10.1186/s41747-020-00173-2
