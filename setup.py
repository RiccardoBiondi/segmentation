#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
    from setuptools import find_packages
    

except ImportError:
    from distutils.core import setup
    from distutils.core import find_packages


def get_requires(requirements_filename):
    '''
    What packages are required for this module to be executed?

    Parameters
    ----------
    requirements_filename : str
        filename of requirements (e.g requirements.txt)

    Returns
    -------
    requirements : list
        list of required packages
    '''
    with open(requirements_filename, 'r') as fp:
        requirements = fp.read()

    return list(filter(lambda x: x != '', requirements.split()))

def format_requires(requirement):
    '''
    Check if the specified requirements is a package or a link to github report.
    If it is a link to a github repo, it will format it according to the specification 
    Of install requirements. 
    The git hub repo url is assumed to be in the form:
    git+https://github.com/UserName/RepoName

    and will be formatted as 
    RepoName @ git+https://github.com/UserName/RepoName

    Parameters
    ----------
    requirement : str
        str with the reuirement to be analyzed
    
    Returns
    -------
    foramt_requirement: str
        requirement formatted according to install_requires specs
    '''

    if "http" not in requirement:
        return requirement

    package_name = requirement.split('/')[-1]
    return f'{package_name} @ {requirement}'



def read_description(readme_filename):
    '''
    Description package from filename

    Parameters
    ----------
    readme_filename : str
        filename with readme information (e.g README.md)

    Returns
    -------
    description : str
        str with description
    '''

    try:

        with open(readme_filename, 'r') as fp:
            description = '\n'
            description += fp.read()

        return description

    except IOError:
        return ''


here = os.path.abspath(os.path.dirname(__file__))


# Package-Metadata
NAME = "CTLungSeg"
DESCRIPTION = 'Package for GGO and CS segmentation in lung CT scans'
URL = 'https://github.com/RiccardoBiondi/segmentation'
EMAIL = 'riccardo.biondi4@studio.unibo.it'
AUTHOR = 'Riccardo Biondi, Nico Curti'
VERSION = None
KEYWORDS = 'radiomics artificial-intelligence machine-learning deep-learning medical-imaging'
REQUIREMENTS_FILENAME = os.path.join(here, 'requirements.txt')
VERSION_FILENAME = os.path.join(here, 'CTLungSeg', '__version__.py')
README_FILENAME = os.path.join(here, 'README.md')

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    LONG_DESCRIPTION = read_description(README_FILENAME)

except IOError:
    LONG_DESCRIPTION = DESCRIPTION


# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(VERSION_FILENAME) as fp:
        exec(fp.read(), about)

else:
  about['__version__'] = VERSION

# parse version variables and add them to command line as definitions
Version = about['__version__'].split('.')

requirements = list(map(lambda x: format_requires(x), get_requires(REQUIREMENTS_FILENAME)))

print(requirements)

setup(
    name=NAME,
    version=about['__version__'],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    download_url=URL,
    keywords=KEYWORDS,
    packages=find_packages(include=['CTLungSeg','CTLungSeg.*'], exclude=('test', 'testing')),
    include_package_data=True, # no absolute paths are allowed
    platforms='any',
    install_requires=requirements,#get_requires(REQUIREMENTS_FILENAME),

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.5',
    license = 'MIT'
)
