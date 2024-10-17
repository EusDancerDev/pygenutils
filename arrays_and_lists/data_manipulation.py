#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
from pandas import Series, DataFrame

#-----------------------#
# Import custom modules #
#-----------------------#

#------------------#
# Define functions # 
#------------------#

# Sorting Methods #
#-----------------#

# Simple sorting methods #
#-#-#-#-#-#-#-#-#-#-#-#-#-

def sort_values_standard(array, key=None, reverse=False,
                         axis=-1, order=None,
                         want_numpy_array=False):
    """
    Sort values in an array (list, numpy, or pandas Series) using np.sort or list.sort.
    
    Parameters
    ----------
    array : list, numpy.ndarray, or pandas.Series
        Array containing values to be sorted.
    key : function, optional
        Key function to sort list items by their function values. Only for lists.
    reverse : bool
        Sort in ascending (False) or descending (True) order. Default is False.
    axis : int, optional
        Axis to sort for numpy arrays. Default is -1.
    order : str or list of str, optional
        Order fields for structured numpy arrays. Default is None.
    want_numpy_array : bool
        Return the result as a numpy array. Default is False.
          
    Returns
    -------
    sorted_array : list, numpy.ndarray, or pandas.Series
        Sorted array or list.
    """
    # Check input type (allow pandas Series as well)
    if isinstance(array, (list, np.ndarray, Series)):
        if isinstance(array, list):
            array.sort(key=key, reverse=reverse)
        elif isinstance(array, np.ndarray):
            array = np.sort(array, axis=axis, order=order)
        elif isinstance(array, Series):
            array = array.sort_values(ascending=not reverse)
        return np.array(array) if want_numpy_array else array
    else:
        raise TypeError(f"Unsupported type '{type(array)}' for sorting.")


def sort_1D_arr_rudimentary(obj, reverse=False):
    """
    Sort a 1D array or list without external libraries (rudimentary method).
    
    Parameters
    ----------
    obj : list or numpy.ndarray of int, float, complex, or str
        1D array or list with values to sort.
    reverse : bool
        Sort in ascending (False) or descending (True) order. Default is False.
    
    Returns
    -------
    obj : list or numpy.ndarray
        Sorted array.
    """
    for i in range(len(obj)):
        current = i
        for k in range(i+1, len(obj)):
            if not reverse and obj[k] < obj[current]:
                current = k
            elif reverse and obj[k] > obj[current]:
                current = k
        pos_swapper(obj, current, i)
    return obj


def pos_swapper(A, x, y):
    """
    Swap two elements in a list or numpy array at specified positions.
    
    This function exchanges the values located at positions `x` and `y` in the 
    provided list or numpy array `A`. It operates in-place, meaning the input
    object is modified directly without returning a new object.
    
    Parameters
    ----------
    A : list or numpy.ndarray
        The list or numpy array where the elements will be swapped.
    x : int
        The index of the first element to be swapped.
    y : int
        The index of the second element to be swapped.
    
    Returns
    -------
    None
        The input array `A` is modified in-place.
    
    Raises
    ------
    IndexError
        If `x` or `y` are out of bounds for the list or array `A`.
    
    Examples
    --------
    >>> A = [1, 2, 3, 4]
    >>> pos_swapper(A, 0, 2)
    >>> A
    [3, 2, 1, 4]
    
    >>> A = np.array([10, 20, 30, 40])
    >>> pos_swapper(A, 1, 3)
    >>> A
    array([10, 40, 30, 20])
    """
    A[x], A[y] = A[y], A[x]


# Advanced sorting methods #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def sort_rows_by_column(array, ncol, sort_order="ascending", order=None): 
    """
    Sort a 2D array by a specific column, preserving row structure.
    
    Parameters
    ----------
    array : list, numpy.ndarray, or pandas.DataFrame
        2D array to sort.
    ncol : int
        Column index to sort by.
    sort_order : {"ascending", "descending"}
        Sort order. Default is "ascending".
    order : str or list of str, optional
        Field order for structured arrays. Default is None.
    
    Returns
    -------
    sorted_array : numpy.ndarray or pandas.DataFrame
        Sorted array by column.
    """
    # Validate 'sort_order' arg
    if sort_order not in sort_order_ops:
        raise ValueError("Unsupported sorting criterium '{sort_order}', "
                         f"choose one from {sort_order_ops}.")
    
    # Sort values #
    if isinstance(array, DataFrame):
        return array.sort_values(by=array.columns[ncol], ascending=(sort_order == "ascending"))
    
    if isinstance(array, (list, np.ndarray)):
        array = np.array(array) if isinstance(array, list) else array
        sorted_indices = np.argsort(array[:, ncol]) if sort_order == "ascending" else np.argsort(array[:, ncol])[::-1]
        return array[sorted_indices]
    raise TypeError(f"Unsupported type '{type(array)}' for sorting.")


def sort_columns_by_row(array, nrow, sort_order="ascending"): 
    """
    Sort columns of a 2D array by a specific row, preserving column structure.
    
    Parameters
    ----------
    array : list, numpy.ndarray, or pandas.DataFrame
        2D array to sort.
    nrow : int
        Row index to sort by.
    sort_order : {"ascending", "descending"}
        Sort order. Default is "ascending".
    
    Returns
    -------
    sorted_array : numpy.ndarray or pandas.DataFrame
        Array sorted by the specified row.
    """
    if isinstance(array, DataFrame):
        return array.T.sort_values(by=array.T.columns[nrow], ascending=(sort_order == "ascending")).T
    
    array = np.array(array).T
    sorted_array = sort_rows_by_column(array, nrow, sort_order).T
    return sorted_array


# Inserting, Extending, and Removing Data #
#-----------------------------------------#

def insert_values(x, index, values, axis=None):    
    """
    Insert values into a list, numpy array, or pandas Series at a specific index.
    
    Parameters
    ----------
    x : list, numpy.ndarray, or pandas.Series
        Object to insert values into.
    index : int
        Position to insert values.
    values : list, numpy.array, pandas.Series
        Values to insert.
    axis : int, optional
        Axis along which to insert values for numpy arrays.
    
    Returns
    -------
    appended_array : numpy.ndarray or list
        Updated array with inserted values.
    """
    if isinstance(x, (list, np.ndarray, Series)):
        if isinstance(x, list):
            x.insert(index, values)
        elif isinstance(x, np.ndarray):
            x = np.insert(x, index, values, axis=axis)
        elif isinstance(x, Series):
            x = x.append(Series(values)).sort_index()
        return x
    raise TypeError(f"Unsupported type '{type(x)}' for insertion.")


def extend_array(obj, obj2extend, np_axis=None):
    """
    Extend a list or concatenate a NumPy array with another list or array.
    """
    if isinstance(obj, list):
        obj.extend(obj2extend)
    elif isinstance(obj, np.ndarray):
        obj = np.concatenate((obj, obj2extend), axis=np_axis)
    elif isinstance(obj, Series):
        obj = obj.append(Series(obj2extend)).sort_index()
    return obj


def remove_elements(array, idx2access, axis=None):    
    """
    Remove elements from a list or numpy array using indices.
    """
    if isinstance(array, list):
        array.pop(idx2access)
    elif isinstance(array, np.ndarray):
        array = np.delete(array, idx2access, axis=axis)
    elif isinstance(array, Series):
        array = array.drop(idx2access)
    return array


# Time-Series Manipulations #
#---------------------------#

def decompose_24h_cumulative_data(array, zeros_dtype='d'):    
    """
    Decompose cumulative 24-hour data into 1-hour intervals.
    
    Parameters
    ----------
    array : numpy.ndarray
        24-hour time step data.
    zeros_dtype : str or numpy dtype
        Data type for arrays of zeros.
    
    Returns
    -------
    hour_timestep_array : numpy.ndarray
        Array with 1-hour time step cumulative data.
    """
    hour_timestep_array = np.diff(array, axis=0, prepend=np.zeros_like(array[:1]))
    hour_timestep_array[hour_timestep_array < 0] = 0
    return hour_timestep_array


#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported options #
#-------------------#

# Sorting options #
sort_order_ops = ["ascending", "descending"]
