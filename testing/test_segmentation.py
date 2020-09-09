#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example

from CTLungSeg.segmentation import select_greater_connected_regions

import cv2
import numpy as np
from CTLungSeg.method import connected_components_wStats
from numpy import ones, zeros
from numpy.random import rand

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

image = st.just(rand)
black_image = st.just(zeros)
white_image = st.just(ones)
kernel = st.just(ones)


#def test_opening

#def test_closing

@given(st.integers(2, 300), st.integers(0,3))
@settings(max_examples = 20, deadline = None)
def test_select_greater_connected_regions(n_imgs, n_reg):
    image = cv2.imread('testing/images/test.png', cv2.IMREAD_GRAYSCALE)
    image = np.logical_not(image)
    image =np.array([image for i in range(n_imgs)])
    res = select_greater_connected_regions(image, n_reg)
    _, labeled, _, _ = connected_components_wStats(res)
    assert np.unique(labeled).shape == (n_reg + 1,)


#def test_reconstruct_gg_areas(imgs):


#def test_find_ROI
