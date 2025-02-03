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

# Sorting algorithms #
#--------------------#

# Basic #
#-#-#-#-#

# Helpers #
def _pos_swapper(A, x, y):
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
    >>> _pos_swapper(A, 0, 2)
    >>> A
    [3, 2, 1, 4]
    
    >>> A = np.array([10, 20, 30, 40])
    >>> _pos_swapper(A, 1, 3)
    >>> A
    array([10, 40, 30, 20])
    """
    A[x], A[y] = A[y], A[x]

# Main #
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

    Examples
    --------
    >>> sort_values_standard([3, 1, 2])
    [1, 2, 3]

    >>> sort_values_standard(np.array([10, 5, 7]), reverse=True)
    array([10, 7, 5])

    >>> sort_values_standard(pd.Series([4, 2, 8]), reverse=True)
    2    8
    0    4
    1    2
    dtype: int64
    """
    # Check input type (allow pandas Series as well)
    if isinstance(array, (list, np.ndarray, Series)):
        if isinstance(array, list):
            array.sort(key=key, reverse=reverse)
        elif isinstance(array, np.ndarray):
            array = np.sort(array, axis=axis, order=order)[::-1] if reverse else np.sort(array, axis=axis, order=order)
        elif isinstance(array, Series):
            array = array.sort_values(ascending=not reverse)
        return np.array(array) if want_numpy_array else array
    else:
        raise TypeError(f"Unsupported type '{type(array)}' for sorting.")

def sort_1d_basic(arr, reverse=False):
    """
    Sort a 1D array or list without external libraries (basic function).
    
    Parameters
    ----------
    arr : list or numpy.ndarray of int, float, complex, or str
        1D array or list with values to sort.
    reverse : bool
        Sort in ascending (False) or descending (True) order. Default is False.
    
    Returns
    -------
    arr : list or numpy.ndarray
        Sorted array.
    """
    for i in range(len(arr)):
        current = i
        for k in range(i+1, len(arr)):
            if not reverse and arr[k] < arr[current]:
                current = k
            elif reverse and arr[k] > arr[current]:
                current = k
        _pos_swapper(arr, current, i)
    return arr


# Advanced #
#-#-#-#-#-#-

def sort_rows_by_column(array, ncol, reverse=False, order=None): 
    """*
    Sort a 2D array by a specific column, preserving row structure.    
    The mechanism preserves the original structure of each row, 
    only sorting based on the specified column. 
    This is especially useful when the user needs to sort an array by a single column,
    without altering the rows.
    
    Parameters
    ----------
    array : list, numpy.ndarray, or pandas.DataFrame
        2D array to sort.
    ncol : int
        Column index to sort by.
    reverse : bool
        If True, sort in descending order. Default is False (ascending).
    order : str or list of str, optional
        Field order for structured arrays. Default is None.
    
    Returns
    -------
    sorted_array : numpy.ndarray or pandas.DataFrame
        Sorted array by column.

    Examples
    --------
    >>> array = np.array([[6, 4, 2, 3],
                          [3, 9, 7, 1],
                          [4, 6, 4, 5]])
    >>> sort_rows_by_column(array, ncol=0)
    array([[3, 9, 7, 1],
           [4, 6, 4, 5],
           [6, 4, 2, 3]])

    >>> sort_rows_by_column(array, ncol=0, reverse=True)
    array([[6, 4, 2, 3],
           [4, 6, 4, 5],
           [3, 9, 7, 1]])
    """
    if isinstance(array, DataFrame):
        return array.sort_values(by=array.columns[ncol], ascending=not reverse)
    
    if isinstance(array, (list, np.ndarray)):
        array = np.array(array) if isinstance(array, list) else array
        sorted_indices = np.argsort(array[:, ncol])[::-1] if reverse else np.argsort(array[:, ncol])
        return array[sorted_indices]
    raise TypeError(f"Unsupported type '{type(array)}' for sorting.")


def sort_columns_by_row(array, nrow, reverse=False): 
    """
    Sort columns of a 2D array by a specific row, preserving column structure.
    Just like `sort_rows_by_column`, this function sorts the columns based on 
    the values in the specified row while maintaining the column structure.
    
    Parameters
    ----------
    array : list, numpy.ndarray, or pandas.DataFrame
        2D array to sort.
    nrow : int
        Row index to sort by.
    reverse : bool
        If True, sort in descending order. Default is False (ascending).
    
    Returns
    -------
    sorted_array : numpy.ndarray or pandas.DataFrame
        Array sorted by the specified row.

    Examples
    --------
    >>> array = np.array([[6, 4, 2, 3],
                          [3, 9, 7, 1],
                          [4, 6, 4, 5]])
    >>> sort_columns_by_row(array, nrow=0)
    array([[2, 3, 4, 6],
           [7, 1, 9, 3],
           [4, 5, 6, 4]])

    >>> sort_columns_by_row(array, nrow=0, reverse=True)
    array([[6, 4, 3, 2],
           [3, 9, 1, 7],
           [5, 4, 6, 4]])
    """
    if isinstance(array, DataFrame):
        return array.T.sort_values(by=array.T.columns[nrow], ascending=not reverse).T
    
    array = np.array(array).T
    sorted_array = sort_rows_by_column(array, ncol=nrow, reverse=reverse).T
    return sorted_array

# Flipping or reversing #
#-----------------------#

# Basic #
#-#-#-#-#

def revert_1d_basic(arr, procedure="index"):
    """
    Reverses a 1D array in-place.
I
    Parameters
    ----------
    arr : list or numpy.ndarray
        The array to reverse.
    procedure : str
        The procedure to use for reversing the array.
    
    Returns
    -------
    numpy.ndarray
        The reversed array.
    """

    if procedure not in flip_basic_options:
        raise ValueError(f"Invalid procedure '{procedure}' for reversing an array. "
                         f"Choose from: {flip_basic_options}.")
    
    arr_len = len(arr)-1
    if procedure == "iterative":
        for i in range(arr_len//2):
            arr[i], arr[arr_len-i] = arr[arr_len-i], arr[i]
    elif procedure == "index":
        arr = arr[::-1]
    return arr


# Advanced #
#-#-#-#-#-#-

def flip_array(array, procedure="numpy_default", axis=None):
    """
    Flip a numpy array or list along a specified axis.

    Parameters
    ----------
    array : list or numpy.ndarray
        The array to flip.
    procedure : str
        The procedure to use for flipping the array.
        Options:
            - "numpy_default": Use numpy.flip.
            - "numpy_lr": Use numpy.fliplr (equivalent to numpy.flip(array, axis=1)).
            - "numpy_ud": Use numpy.flipud (equivalent to numpy.flip(array, axis=0)).
            - "index_lr": Use left-right list slicing (equivalent to array[:,::-1]).
            - "index_ud": Use up-down list slicing (equivalent to array[::-1,:]).
    axis : int, optional
        The axis to flip the array along. Default is None.
    """
    if procedure not in flip_advanced_options:
        raise ValueError(f"Invalid procedure '{procedure}' for flipping an array. "
                         f"Choose from: {flip_advanced_options}.")
    
    return advanced_flip_dict[procedure](array, axis=axis)


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

    Examples
    --------
    >>> insert_values([1, 2, 3], 1, 100)
    [1, 100, 2, 3]

    >>> insert_values(np.array([1, 2, 3]), 1, 100)
    array([  1, 100,   2,   3])

    >>> insert_values(pd.Series([1, 2, 3]), 1, 100)
    0      1
    1    100
    1      2
    2      3
    dtype: int64
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
    
    Parameters
    ----------
    obj : list, numpy.ndarray, or pandas.Series
        The original list, numpy array, or pandas Series to be extended.
    obj2extend : list, numpy.ndarray, or pandas.Series
        The object to extend `obj` with.
    np_axis : int, optional
        Axis along which to concatenate numpy arrays. Default is None.
    
    Returns
    -------
    Extended list, numpy array, or pandas Series.

    Examples
    --------
    >>> extend_array([1, 2, 3], [4, 5])
    [1, 2, 3, 4, 5]

    >>> extend_array(np.array([1, 2, 3]), np.array([4, 5]), np_axis=0)
    array([1, 2, 3, 4, 5])

    >>> extend_array(pd.Series([1, 2, 3]), pd.Series([4, 5]))
    0    1
    1    2
    2    3
    3    4
    4    5
    dtype: int64
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
    Remove elements from a list, numpy array, or pandas Series using indices.
    
    Parameters
    ----------
    array : list, numpy.ndarray, or pandas.Series
        List, numpy array, or pandas Series from which elements will be removed.
    idx2access : int, list, or numpy.ndarray
        Indices to access the elements that will be removed. For lists, multiple
        indices are now allowed.
    axis : int, optional
        Axis along which to remove elements for numpy arrays. Default is None.
    
    Returns
    -------
    Updated list, numpy array, or pandas Series with specified elements removed.

    Examples
    --------
    >>> remove_elements([1, 2, 3, 4], [1, 3])
    [1, 3]

    >>> remove_elements(np.array([10, 20, 30, 40]), [1, 3])
    array([10, 30])

    >>> remove_elements(pd.Series([10, 20, 30, 40]), [0, 2])
    1    20
    3    40
    dtype: int64
    """
    if isinstance(array, list):
        if isinstance(idx2access, int):  # Handle single index
            array.pop(idx2access)
        elif isinstance(idx2access, (list, np.ndarray)):  # Handle multiple indices
            for index in sorted(idx2access, reverse=True):
                if index < 0 or index >= len(array):
                    raise IndexError(f"Index {index} is out of range for list of size {len(array)}.")
                del array[index]
        else:
            raise TypeError("For list inputs, indices must be an integer or a list/array of integers.")
    elif isinstance(array, np.ndarray):
        array = np.delete(array, idx2access, axis=axis)
    elif isinstance(array, Series):
        array = array.drop(idx2access)
    else:
        raise TypeError(f"Unsupported type '{type(array)}' for removal.")
    return array


# Time-Series Manipulations #
#---------------------------#

def decompose_cumulative_data(cumulative_array, fill_value=None, zeros_dtype='d'):    
    """
    Convert cumulative values into individual values by subtracting consecutive elements,
    with an option to handle negative differences.

    This function takes an array of cumulative values and returns the individual values
    that make up the cumulative sum. Negative differences can either be preserved or replaced 
    with a specified fill value.
    
    Parameters
    ----------
    cumulative_array : numpy.ndarray
        A multi-dimensional array representing cumulative values over time or other axes.
    fill_value : scalar or None, optional
        Value to replace negative differences. If None (default), negative differences are preserved.
    zeros_dtype : str or numpy dtype
        Data type for the array of zeros if `fill_value` is used. Default is 'd' (float).
    
    Returns
    -------
    individual_values_array : numpy.ndarray
        A multi-dimensional array with individual values extracted from the cumulative array.
    
    Examples
    --------
    Example 1: Basic cumulative data decomposition
    >>> cumulative_array = np.array([6, 7, 13, 13, 20, 22, 30, 31, 38, 43, 52, 55])
    >>> decompose_cumulative_data(cumulative_array)
    array([ 6.,  1.,  6.,  0.,  7.,  2.,  8.,  1.,  7.,  5.,  9.,  3.])

    Example 2: Preserving negative differences
    >>> cumulative_array = np.array([6, 7, 13, 12, 20, 22])
    >>> decompose_cumulative_data(cumulative_array)
    array([ 6.,  1.,  6., -1.,  8.,  2.])

    Example 3: Replacing negative differences with zeros
    >>> decompose_cumulative_data(cumulative_array, fill_value=0)
    array([ 6.,  1.,  6.,  0.,  8.,  2.])
    """
    
    records = len(cumulative_array)
    
    # Define the behavior for negative differences
    def handle_negative_difference(diff):
        if fill_value is None:
            return diff
        return np.full_like(diff, fill_value, dtype=zeros_dtype) if np.any(diff < 0) else diff
    
    # Calculate the individual values, applying the fill_value if necessary
    individual_values_array = \
        np.array([handle_negative_difference(cumulative_array[t+1] - cumulative_array[t])
                  for t in range(records-1)])
    
    # Add the average of the last two differences to match the shape of the original array
    individual_values_array = np.append(individual_values_array,
                                        np.mean(individual_values_array[-2:], axis=0)[np.newaxis,:],
                                        axis=0)
    
    return individual_values_array

#--------------------------#
# Parameters and constants #
#--------------------------#

# Procedure options #
#-------------------#

# Array flipping #
flip_basic_options = ["iterative", "index"]

# Switch case dictionaries #
#--------------------------#

# Array flipping #
advanced_flip_dict = {
    "numpy_default": lambda array, axis: np.flip(array, axis=axis),
    "numpy_lr": lambda array: np.fliplr(array),
    "numpy_ud": lambda array: np.flipud(array),
    "index_lr": lambda array: array[:,::-1],
    "index_ud": lambda array: array[::-1,:]
}

flip_advanced_options = advanced_flip_dict.keys()