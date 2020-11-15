Modules
=======

Together with the scripts, a series of modules are provides. Each modules
contains a series of functions for image processing which are used  during the
scrip developing. The modules are the following,each of them provides a different
kind of functions.


Utils
-----

This modules provides all the functions t read and write images in medical image
format like '.nrrd' or '.nifti'. All the format supported by SimpleITK_ are supported.


.. _SimpleITK: https://simpleitk.readthedocs.io/en/master/IO.html

.. automodule:: CTLungSeg.utils
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members:

Method
------

This module contains the implementation of  all the filter used for the
processing of images inside the script. This functions extend some OpenCV_
functions  and allow to perform operations on a stack of images by repeating
the filter slice by slice.


.. _OpenCV: https://opencv.org/

.. automodule:: CTLungSeg.method
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members:

segmentation
------------


This module contains the implementation of the functions used to perform the
tasks on each script.


.. automodule:: CTLungSeg.segmentation
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members:
