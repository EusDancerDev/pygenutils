#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import scipy.optimize as sco

#------------------#
# Define functions #
#------------------#

# Polynomial fitting #
#--------------------#

def polynomial_fitting(y, poly_ord, fix_edges=False, poly_func=None, poly_params=None):
    """
    Fits a polynomial to 1D data using least squares or a custom function.

    This function fits a polynomial of specified order to the data and 
    optionally allows for a custom polynomial function using curve fitting.
    It can also fix the edges of the data to preserve original values.

    Parameters
    ----------
    y : list or numpy.ndarray
        The y-coordinates (dependent variable) of the sample points.
    poly_ord : int
        The order of the polynomial to fit.
    fix_edges : bool, optional, default: False
        If True, fixes the first and last values of the fitted data 
        to match the original edges.
    poly_func : callable, optional
        A custom polynomial function to use for fitting. If provided, 
        `scipy.optimize.curve_fit` will be used instead of `numpy.polyfit`.
    poly_params : list or dict, optional
        Parameters for the custom polynomial function.

    Returns
    -------
    numpy.ndarray
        The fitted data based on the polynomial.

    Notes
    -----
    - If a custom polynomial function is provided, its parameters must 
      be compatible with `scipy.optimize.curve_fit`.
    - For large datasets, consider using polynomial fitting methods that 
      handle edge cases like fixed boundaries or specific parameter tuning.
    """
    # Flatten the input array if it's multi-dimensional
    y = np.ravel(y)
    x = np.arange(len(y))

    # Polynomial fitting using numpy or custom function
    if poly_func is None:
        coefficients = np.polyfit(x, y, poly_ord)
        polynomial = np.poly1d(coefficients)
        fitted_y = polynomial(np.linspace(x[0], x[-1], len(y)))
    else:
        popt, _ = sco.curve_fit(poly_func, x, y, p0=poly_params)
        fitted_y = poly_func(x, *popt)

    # Optionally fix the edges to original values
    if fix_edges:
        fitted_y[0], fitted_y[-1] = y[0], y[-1]

    return fitted_y
