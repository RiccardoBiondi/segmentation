import pytest
import hypothesis.strategies as st
from hypothesis import given, settings, example
from  hypothesis import HealthCheck as HC


from CTLungSeg.metrics import precision
from CTLungSeg.metrics import recall
from CTLungSeg.metrics import dice
from CTLungSeg.metrics import specificity
from CTLungSeg.metrics import accuracy



import numpy as np
import SimpleITK as sitk


__author__ = ['Riccardo Biondi', 'Nico Curti']
__email__  = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


################################################################################
###                                                                          ###
###                         Define Test Samples                              ###
###                                                                          ###
################################################################################

# a sample consisting of only 1 values
white = np.ones(10)

# a sample consisting of only 0 values
black = np.zeros(10)

# some other example arrays

ex_1 = np.asarray([1, 0, 0, 0, 1, 0, 0, 1, 1, 1])
ex_2 = np.asarray([1, 1, 1, 0, 0, 0, 1, 0 ,1, 0])
ex_3 = np.asarray([0, 1, 0, 1, 1, 0, 0, 1, 1, 1])

# prepare the testing samples
# each sample is a tuple containing the ground truth array, the predicted array and
# the true metric value

precision_samples = [(white, black, 0.), (white, white, 1.), (ex_1, ex_2, .4), (ex_2, ex_3, 1./3.)]
recall_samples = [(white, black, 0.), (white, white, 1.), (ex_1, ex_2, .4), (ex_2, ex_3, .4)]
dice_samples = [(white, black, 0.), (white, white, 1.), (ex_1, ex_2, .4), (ex_2, ex_3, 4 / 11)]
specificity_samples = [(white, black, 0.), (white, white, 0.), (black, black, 1.), (ex_1, ex_2, 2. / 5.), (ex_2, ex_3, 1. / 5.)]
accuracy_samples = [(white, black, 0.), (white, white, 1.), (ex_1, ex_2, .4), (ex_2, ex_3, .3)]

# recall

# dice 

# accuracy


################################################################################
###                                                                          ###
###                                 TESTING                                  ###
###                                                                          ###
################################################################################


@given(st.sampled_from(precision_samples))
def test_precision_score(sample):
    '''
    Given:
        - true sample
        - predictited sample
        - ground truth precision value
    Then:
        - compute precision metric

    Assert:
        - computed precision value is close to the ground truth one
    '''

    val = precision(sample[0], sample[1])

    assert np.isclose(val, sample[2])


@given(st.integers(2, 5), st.integers(7, 10))
def test_precision_score_raise_value_error(y_true_shape, y_pred_shape):
    '''
    Given: 
        - y_true, y_pred s.t. y_true.shae != y_pred.shape
    Than:
        - compute precision
    Assert:
        - Raise Value error 
    '''
    
    with pytest.raises(ValueError):
        value = precision(np.ones(y_true_shape), np.ones(y_pred_shape))


@given(st.sampled_from(recall_samples))
def test_recall_score(sample):
    '''
    Given:
        - true sample
        - predictited sample
        - ground truth recall value
    Then:
        - compute recall metric

    Assert:
        - computed recall value is close to the ground truth one
    '''

    val = recall(sample[0], sample[1])

    assert np.isclose(val, sample[2])


@given(st.integers(2, 5), st.integers(7, 10))
def test_recall_score_raise_value_error(y_true_shape, y_pred_shape):
    '''
    Given: 
        - y_true, y_pred s.t. y_true.shae != y_pred.shape
    Than:
        - compute recall
    Assert:
        - Raise Value error 
    '''
    
    with pytest.raises(ValueError):
        value = recall(np.ones(y_true_shape), np.ones(y_pred_shape))


@given(st.sampled_from(dice_samples))
def test_dice_score(sample):
    '''
    Given:
        - true sample
        - predictited sample
        - ground truth dice value
    Then:
        - compute dice metric

    Assert:
        - computed dice value is close to the ground truth one
    '''

    val = dice(sample[0], sample[1])

    assert np.isclose(val, sample[2])


@given(st.integers(2, 5), st.integers(7, 10))
def test_dice_score_raise_value_error(y_true_shape, y_pred_shape):
    '''
    Given: 
        - y_true, y_pred s.t. y_true.shae != y_pred.shape
    Than:
        - compute dice
    Assert:
        - Raise Value error 
    '''
    
    with pytest.raises(ValueError):
        value = dice(np.ones(y_true_shape), np.ones(y_pred_shape))



@given(st.sampled_from(specificity_samples))
def test_specificity_score(sample):
    '''
    Given:
        - true sample
        - predictited sample
        - ground truth precision value
    Then:
        - compute specificity metric

    Assert:
        - computed specificity value is close to the ground truth one
    '''

    val = specificity(sample[0], sample[1])

    assert np.isclose(val, sample[2])


@given(st.integers(2, 5), st.integers(7, 10))
def test_specificity_score_raise_value_error(y_true_shape, y_pred_shape):
    '''
    Given: 
        - y_true, y_pred s.t. y_true.shae != y_pred.shape
    Than:
        - compute specificity
    Assert:
        - Raise Value error 
    '''
    
    with pytest.raises(ValueError):
        value = specificity(np.ones(y_true_shape), np.ones(y_pred_shape))


@given(st.sampled_from(accuracy_samples))
def test_accuracy_score(sample):
    '''
    Given:
        - true sample
        - predictited sample
        - ground truth accuracy value
    Then:
        - compute accuracy metric

    Assert:
        - computed accuracy value is close to the ground truth one
    '''

    val = accuracy(sample[0], sample[1])

    assert np.isclose(val, sample[2])


@given(st.integers(2, 5), st.integers(7, 10))
def test_accuracy_score_raise_value_error(y_true_shape, y_pred_shape):
    '''
    Given: 
        - y_true, y_pred s.t. y_true.shae != y_pred.shape
    Than:
        - compute accuracy
    Assert:
        - Raise Value error 
    '''
    
    with pytest.raises(ValueError):
        value = accuracy(np.ones(y_true_shape), np.ones(y_pred_shape))