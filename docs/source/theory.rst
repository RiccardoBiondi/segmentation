COVID-19 Lung Segmentation
==========================

SARS-CoV-2 virus has widely spread all over the world since the beginning of 2020.
This virus affect lung areas and causes respiratory illness.In this scenario is
highly desirable a method to identify in CT images the lung injuries caused by COVID-19.
The approach proposed here is based on color quantization to identify the infection
regions inside lung(Ground Glass Opacities, Consolidation and Pleural Effusion).

To achieve this purpose we have used color quantization approach to segment the
chest CT scans of patients affected by COVID-19. Use this technique as medical
image segmentation means to reduce the number of colors in the image to the number
of anatomical structures and tissue present in the anatomical region; in this
way we are assign to each kind of tissue a characteristic color: so must exist a
relationship between the kind of tissue and the color used to represent it.

For CT scan which are in gray scale, each color is represented by a single value
given by the Hounsfield Units(HU) : voxels colors are proportional to HU, which
are defined as a linear transformation of the linear attenuation coefficient.
HU normalize the coefficient of a particular tissue according to a reference one,
usually water, as we can see in equation below :

.. math::

  	HU = k\times\frac{\mu - \mu_{H_2 O}}{\mu_{H_2 O}}

In the end each color results proportional to the linear attenuation coefficient,
different from each tissue, so exist a relation between the GL and the tissue type
that makes this techniques available.

Color quantization and the properties of digital images allow us to consider also
other properties of the image besides the single voxel intensity.
This purpose can be achieved by building a suitable color space:

In digital image processing, images are represented with a 3D tensor, in which the
first two dimensions represent the height and width of the image and the last one
the number of channels. Gray scale images requires only one channel, so each pixel
has a numeric values whose range may change according to the image format.
On the other hand color images requires 3 channels, and the value of each channel
represent the level of the primary color stored in this particular channel, so each
color is represented by 3 different values, according to Young model.
In this work the different channel are used to takes in account different properties,
exploited by the application of different filters. This allow us to consider also
neighboring voxels, that is really suitable for the segmentation since the
lesions areas involves many closest voxels, not only a single one. We have also
used this features to discriminate between other lung regions like bronchi by
exploit shape information.
The used image features are displayed in the figure below:

.. image:: images/Multi_Channel.png
   :height: 500px
   :width: 500 px
   :scale: 100 %
   :alt:
   :align: left


Once we have build the color space, we have to found the characteristic color of
each tissue under study, which is represented by a centroids in the color space.
In order to perform this task and achieve the centroids estimation a simple -means
clustering was used.
K-means clustering requires a prior knowledge about the number of cluster, which
in our case is given by the anatomical structure of the lung, so we can consider
a different cluster for each anatomical structure.
Once we have estimated the centroids for each tissue, we use that for the actual
segmentation by assign each voxel to the cluster of the closest centroids: in this
way the estimation step, that we will call "train", needs to be performed only once,
so can be time expansive since is not involved in the actual segmentation.


This package provides a set of already estimates centroids, toghether with scripts
to perform the actual segmentation. Also a script to train your own set of centroids
is provided.
