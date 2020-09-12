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


##
# STRATEGIES DEFINITIONS
##

@st.composite
def images_wlung_strategy(draw, heigt = st.integers(50, 70), width=st.integers(50, 70), n_imgs=st.integers(1, 100)) :
    h = draw(heigt)
    w = draw(width)
    n = draw(n_imgs)
    stack = zeros((n, 512, 512), dtype=np.uint8)
    stack[:, 100 : h+100, 100 : w+100] = ones((h, w))
    return stack


@st.composite
def images_wolung_strategy(draw, heigt = st.integers(5, 20), width=st.integers(5, 20), n_imgs=st.integers(1, 100)) :
    h = draw(heigt)
    w = draw(width)
    n = draw(n_imgs)
    stack = zeros((n, 512, 512), dtype=np.uint8)
    stack[:, 100 : h+100, 100 : w+100] = ones((h, w))
    return stack


###
#  START TESTING
###


@given(images_wlung_strategy(), images_wolung_strategy(), st.integers(600, 700))
@settings(max_examples=20, deadline=None)
def test_select_slice_wlung(stack_wlung, stack_wolung, min_area):

    stack = np.concatenate((stack_wlung, stack_wolung))
    _, _, stats, _ = connected_components_wStats(stack)

    assert (select_slice_wlung(stack, min_area, stats) == stack_wlung).all()


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
