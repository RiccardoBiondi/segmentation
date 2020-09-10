#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example

from CTLungSeg.segmentation import select_greater_connected_regions
from CTLungSeg.segmentation import find_ROI

import cv2
import numpy as np
import pandas as pd
from CTLungSeg.method import connected_components_wStats
from numpy import ones, zeros
from numpy.random import rand

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']

image = st.just(rand)
black_image = st.just(zeros)
white_image = st.just(ones)
kernel = st.just(ones)


#@given(image, st.integers(1,20), st.integers(1,11))
#@settings(max_examples = 20, deadline = None)
#def test_opening(img, stack_size, kernel_size) :
#    opened = closing(img(stack_size, 300, 300), np.ones((kernel_size, kernel_size), dtype=np.uint8))


#@given(image, st.integers(1,20), st.integers(1,11))
#@settings(max_examples = 20, deadline = None)
#def test_closing(img, stack_size, kernel_size) :
#    closed = closing(img(stack_size, 300, 300), np.ones((kernel_size, kernel_size), dtype=np.uint8))


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


@given(st.integers(1,200), st.integers(1,200), st.integers(1,200), st.integers(1,200))
@settings(max_examples = 200, deadline = None)
def test_find_ROI(x, y, w, h) :
    image = np.zeros((512, 512), dtype=np.uint8)
    corners = [x, y, x + w, y + h]
    columns = ['TOP', 'LEFT', 'WIDTH', 'HEIGHT', 'AREA']

    image[y : y + h, x : x + w] = np.ones((h, w), dtype=np.uint8)
    _, _, stats, _ = connected_components_wStats(image)
    assert (find_ROI(pd.DataFrame(stats, columns=columns)) == corners).all
