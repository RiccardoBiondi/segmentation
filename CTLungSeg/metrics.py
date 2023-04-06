import numpy as np

__author__  = ['Riccardo Biondi', 'Nico Curti']
__email__   = ['riccardo.biondi4@studio.unibo.it', 'nico.curti2@unibo.it']


__all__ = ['dice', 'precision', 'recall', 'specificity', 'accuracy']


def precision(y_true, y_pred, eps=1e-9):
    '''
    Compute the precision score between two samples as the ratio of true positive and 
    the sum of true positive and false positives.

    Each sample must be a binary numpy array containing only 0 and 1 values.
    y_true and y_pred must have tha same shape

    Parameters
    ----------
    y_true: np.array
        binary array containing the ground truth

    y_pred: np.array
        binary array containing the prediction

    eps: float 
        small floating point value to avoid zero division error

    
    Return
    ------

    precision: float
        precision score (in [0, 1])
    '''
    
    # test y_true and y_pred have the same shape

    if y_true.shape != y_pred.shape:
        raise ValueError(f'y_true, y_pred must have the same shape: {y_true.shape} != {y_pred.shape}')

    # ensure binary images
    y_true = (y_true != 0).astype(np.uint8)
    y_pred = (y_pred != 0).astype(np.uint8)

    
    
    tp = np.sum(y_true * y_pred)
    fp = np.sum((1 - y_true) * y_pred)
    
    return  tp / (tp + fp + eps)


def recall(y_true, y_pred, eps=1e-9):
    '''
    Compute the recall score between two samples as the ratio of true positive and 
    the sum of true positive and false negatives.

    Each sample must be a binary numpy array containing only 0 and 1 values.
    y_true and y_pred must have tha same shape

    Parameters
    ----------
    y_true: np.array
        binary array containing the ground truth

    y_pred: np.array
        binary array containing the prediction

    eps: float 
        small floating point value to avoid zero division error

    
    Return
    ------

    recall: float
        precision score (in [0, 1])
    '''
   
    # test y_true and y_pred have the same shape

    if y_true.shape != y_pred.shape:
        raise ValueError(f'y_true, y_pred must have the same shape: {y_true.shape} != {y_pred.shape}')

    # ensure binary images
    y_true = (y_true != 0).astype(np.uint8)
    y_pred = (y_pred != 0).astype(np.uint8)

    tp = np.sum(y_true * y_pred)

    fn = np.sum(y_true * (1 - y_pred))

    return tp / (tp + fn + eps)



def dice(y_true, y_pred, eps=1e-9):
    
    '''
    Compute the dice score between two samples.

    Each sample must be a binary numpy array containing only 0 and 1 values.
    y_true and y_pred must have tha same shape

    Parameters
    ----------
    y_true: np.array
        binary array containing the ground truth

    y_pred: np.array
        binary array containing the prediction

    eps: float 
        small floating point value to avoid zero division error

    
    Return
    ------

    dice: float
        dice score (in [0, 1])
    '''
       
    # test y_true and y_pred have the same shape
    if y_true.shape != y_pred.shape:
        raise ValueError(f'y_true, y_pred must have the same shape: {y_true.shape} != {y_pred.shape}')

    # ensure binary images
    y_true = (y_true != 0).astype(np.uint8)
    y_pred = (y_pred != 0).astype(np.uint8)

    tp = np.sum(y_true * y_pred)
    fp = np.sum((1 - y_true) * y_pred)
    fn = np.sum(y_true * (1 - y_pred))


    return (2. * tp) / (2 * tp + fp + fn + eps)


def specificity(y_true, y_pred, eps=1e-9):
    '''
    Compute the specificity score between two samples as the ratio of true negative and 
    the sum of true negative and false positives.

    Each sample must be a binary numpy array containing only 0 and 1 values.
    y_true and y_pred must have tha same shape

    Parameters
    ----------
    y_true: np.array
        binary array containing the ground truth

    y_pred: np.array
        binary array containing the prediction

    eps: float 
        small floating point value to avoid zero division error

    
    Return
    ------

    specificity: float
        specificity score (in [0, 1])
    '''

   # test y_true and y_pred have the same shape
    if y_true.shape != y_pred.shape:
        raise ValueError(f'y_true, y_pred must have the same shape: {y_true.shape} != {y_pred.shape}')

    # ensure binary images
    y_true = (y_true != 0).astype(np.uint8)
    y_pred = (y_pred != 0).astype(np.uint8)

    tn = np.sum((1 - y_true) * (1 - y_pred))
    fp = np.sum((1 - y_true) * y_pred)

    return tn / (tn + fp + eps)


def accuracy(y_true, y_pred, eps=1e-9):
    '''
    Compute the accuracy score between two samples.
    Each sample must be a binary numpy array containing only 0 and 1 values.
    y_true and y_pred must have tha same shape

    Parameters
    ----------
    y_true: np.array
        binary array containing the ground truth

    y_pred: np.array
        binary array containing the prediction

    eps: float 
        small floating point value to avoid zero division error

    
    Return
    ------

    accuracy: float
        precision score (in [0, 1])
    '''
    # test y_true and y_pred have the same shape
    if y_true.shape != y_pred.shape:
        raise ValueError(f'y_true, y_pred must have the same shape: {y_true.shape} != {y_pred.shape}')

    # ensure binary images
    y_true = (y_true != 0).astype(np.uint8)
    y_pred = (y_pred != 0).astype(np.uint8)
    
    tp = np.sum(y_true * y_pred)
    tn = np.sum((1 - y_true) * (1 - y_pred))
    tot = y_pred.size

    return (tp + tn) / tot
