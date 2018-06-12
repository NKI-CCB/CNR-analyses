"""Miscalleanous utilty functions for personal use."""

import numpy as np
import pandas as pd
import random
import re


def flatten_list(lst):
    """Flatten list of lists."""
    return [item for sublist in lst for item in sublist]


def add_noise(mat_input, noise=.1):
    """Add noise to the elements of a matrix.

    Matrix should be either numpy array pandas DataFrame.
    Noise is added by multiplying values with a random variable with mu = 1.
    Sigma van be given as input. Default value is 0.1.
    Returns a copy of the matrix. Input is unchanged.
    """
    mat = mat_input.copy()
    dims = mat.shape
    for i in range(dims[0]):
        for j in range(dims[1]):
            if isinstance(mat, np.ndarray):
                mat[i][j] = mat[i][j] * random.normalvariate(1, noise)
            elif isinstance(mat, pd.DataFrame):
                mat.ix[i, j] = mat.ix[i, j] * random.normalvariate(1, noise)
            else:
                raise TypeError("argument mat should be numpy array or pandas \
                DataFrame.")
    return(mat)
