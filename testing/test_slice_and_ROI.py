import pytest
import hypothesis.strategies as st
from hypothesis import given, settings

from CTLungSeg.slice_and_ROI import select_regions_wlung
from CTLungSeg.slice_and_ROI import  select_slice_wlung

import numpy as np
from numpy import ones, zeros
from numpy.random import rand
from CTLungSeg.method import connected_components_wStats

__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


@given(st.integers(2, 100), st.integers(2, 100), st.integers(50, 200), st.integers(100, 200))
@settings(max_examples=20, deadline=None)
def test_select_slice_wlung(slice_wlung, slice_wolung, w, h):

    image_wlung = zeros((512, 512), dtype=np.uint8)
    image_wolung = zeros((512, 512), dtype=np.uint8)
    image_wlung[100 : h+120, 100 : w+120] = np.ones((h+20, w+20), dtype=np.uint8)
    image_wolung[100 : h + 80, 100 : w + 80] = np.ones((h-20, w-20), dtype=np.uint8)

    stack_wlung = np.array([image_wlung for i in range(slice_wlung)])
    stack_wolung = np.array([image_wolung for i in range(slice_wolung)])
    stack = np.concatenate((stack_wlung, stack_wolung))

    _, _, stats, _ = connected_components_wStats(stack)

    assert (select_slice_wlung(stack, w * h, stats) == stack_wlung).all()


@given(st.integers(20, 200), st.integers(20, 200), st.integers(2, 200))
@settings(max_examples=20, deadline=None)
def test_select_regions_wlung(h, w, n_imgs):
    #create image stack
    image = zeros((512, 512), dtype=np.uint8)
    image[100 : 100 + h, 100 : 100 + w] = ones((h, w), dtype=np.uint8)
    stack = np.array([image for _ in range(n_imgs)])

    _, _, stats, _ = connected_components_wStats(stack)

    cropped = select_regions_wlung(stack, stats)
    for img in cropped :
        assert img.shape == (h, w)
