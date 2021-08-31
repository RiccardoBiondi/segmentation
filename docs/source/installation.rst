Installation
=================

Supported python versions :
|python version|

The full list of prerequisites is the following:

- numpy>=1.17
- opencv-python
- tdqm
- SimpleITK

And, for testing:

- PyTest>=3.0.7
- Hypothesis>=4.13.0

The lung extraction is performed by using pre-trained UNet, so please ensure to
have installed the lungmask_ package. For more information about how the network
is trained, please refers here_

Installation
------------

First of all, ensure to have the right python version and the package for the
lung extraction correctly installed

To install this package first of all you have to clone the repositories from GitHub:

.. code-block:: bash

  git clone https://github.com/RiccardoBiondi/segmentation
  cd segmentation

The installation is managed by setup.py, which will install also the full dependency.
So, from the segmentation folder simply run

.. code-block:: bash

  pip install -r requirements.txt
  python setup.py install

Testing
-------

Testing routines use pytest_ and hypothesis_ packages. please install
these packages to perform the test:

.. code-block:: bash

  pip install pytest>=3.0.7
  pip install hypothesis>=4.13.0

.. warning::
  Pytest versions above 6.1.2 are not available for python 3.5


All the full set of test is provided in the testing_ directory.
You can run the full list of test with:

.. code-block:: bash

  python -m pytest


.. |python version| image:: https://img.shields.io/badge/python-3.5|3.6|3.7|3.8-blue.svg
.. _pytest: https://pypi.org/project/pytest/6.0.2/
.. _hypothesis: https://hypothesis.readthedocs.io/en/latest/
.. _testing: https://github.com/RiccardoBiondi/segmentation/tree/master/testing
.. _lungmask: https://github.com/JoHof/lungmask
.. _here: https://eurradiolexp.springeropen.com/articles/10.1186/s41747-020-00173-2
