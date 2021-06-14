Modules
=======

Together with the scripts, a series of modules are provided. Each module
contains a series of functions for image processing which are used during the
script developing. The modules are the following, each of them provides a different
kind of functions.

Utils
-----

This modules provides all the functions to read and write images in a medical image
format like '.nrrd' or '.nifti'. All the formats supported by SimpleITK_ are allowed.

.. _SimpleITK: https://simpleitk.readthedocs.io/en/master/IO.html

.. automodule:: utils
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members: _read_dicom_series, _read_image
   :special-members:

Method
------

This module contains the implementation of all the filter used for the
processing of images inside the script. The functions are based on SimpleITK_
methods

.. _OpenCV: https://opencv.org/

.. automodule:: method
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members:

segmentation
------------

This module contains the implementation of the functions used to perform the
tasks on each script.


.. automodule:: segmentation
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members:
