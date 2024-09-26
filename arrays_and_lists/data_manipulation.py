#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: orokorra, atalak bereizten dituzten goiburu-komentarioak testuingurura egokitu

#----------------#
# Import modules #
#----------------#

import numpy as np
from pandas import Series

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings.information_output_formatters import format_string
from pyutils.strings.string_handler import find_substring_index
from pyutils.utilities.introspection_utils import get_obj_type_str, \
                                                  get_caller_method_args

#------------------#
# Define functions # 
#------------------#

# Sorting #
#---------#

# Simple methods #
#-#-#-#-#-#-#-#-#-

def sort_values_standard(array, key=None, reverse=False,
                         axis=-1, order=None,
                         want_numpy_array=False):
    
    """
    Function that sorts the values in an array using the normal procedure,
    using np.sort() or list.sort() methods, depending on the input object type.
    It is intended to use especially in such cases where the usage of sort()
    method returns a generator.
    Of course, this function can be used however simple the case it is.
    
    Parameters
    ----------
    array : list or numpy.ndarray
        Array containing string, integer, float, etc. values,
        but all of the same semantics.
    key : function, optional
        If a key function is given, apply it once to each list item and sort them,
        ascending or descending, according to their function values.
        This parameter is relevant only for lists.
    reverse: bool
        If False, then the items are sorted in an ascending order,
        else in an descending order.
    axis : int, optional
        Axis alength which to sort. If None, the array is flattened before
        sorting. The default is -1, which sorts alength the last axis.
        This parameter is relevant only for type numpy.ndarray.
    order : str or list of str, optional
        When parameter 'array' is that with fields defined, this argument specifies
        which fields to compare first, second, etc.  A single field can
        be specified as a string, and not all fields need be specified,
        but unspecified fields will still be used, in the order in which
        they come up in the dtype, to break ties.
    want_numpy_array : bool
        Determines whether to return the sorted values
        in a NumPy array, otherwise the functions returns
        them in a list. Default behaviour is the latter.
          
    Returns
    -------
    sorted_array : list or numpy.ndarray
        List or array of sorted values.
    """

    if isinstance(array, list):
        # Invoke the method without assigning a new variable #
        array.sort(key=key, reverse=reverse)

    elif isinstance(array, np.ndarray):
        array = np.sort(array, axis=axis, order=order)

    if want_numpy_array:
        array = np.array(array)

    return array


def sort_1D_arr_rudimentary(obj, reverse=False):
    """
    Function that sorts a 1D array, using simple maths, without any 
    standard or external modules (hence the word 'rudimentary').
    This implies swapping list item positions, for that using a classic external
    function in order to accomplish the task.
    
    Parameters
    ----------
    obj : list or numpy.ndarray of int, float, complex or str
        List or NumPy array containing simple data.
        Every object must be of the same type, which is always guaranteed
        if the object is a numpy.ndarray.
    reverse: bool
        If True, then the items are sorted in an ascending order,
        else in an descending order.
    
    Returns
    -------
    obj : list or numpy.ndarray
        Array with its items sorted according to 'reverse' parameter's value.
    """

    for i in range(len(obj)):
        current = i
        for k in range(i+1, len(obj)):
            if not reverse:
                if obj[k] < obj[current]:
                    current = k
            else:
                if obj[k] > obj[current]:
                    current = k
                    
        pos_swapper(obj, current, i)
    return obj


def pos_swapper(A, x, y):
    temp = A[x]
    A[x] = A[y]
    A[y] = temp
    
    
# Advanced methods #
#-#-#-#-#-#-#-#-#-#-

def sort_rows_by_column(array, ncol, sort_order="ascending", order=None): 
    # TODO: ondoko azalpenei lista bat sartzen denerako kasua gehitu
    """
    Function that sorts the values in a 2D dimension array
    against a specific column.
    
    The result is an array sorted along the first axis (index=0), i.e. the rows,
    where only the value of the selected column is sorted, while the rest
    of the values of the corresponding row remain the same.
    
    This tool is useful when the array contains parameters with
    different semantics and only one column is needed to sort.
    
    Parameters
    ----------
    array : list or numpy.ndarray
        Array to be sorted. It can contain both types of objects.
    ncol : int
        Number of the column whose values are going to be sorted against to.
    sort_order : {"ascending", "descending"}
        Default order is "ascending".
    order : str or list of str, optional
        When parameter 'array' is that with fields defined, this argument specifies
        which fields to compare first, second, etc.  A single field can
        be specified as a string, and not all fields need be specified,
        but unspecified fields will still be used, in the order in which
        they come up in the dtype, to break ties.
  
    Returns
    -------
    sorted_array : numpy.ndarray
        Array containing the sorted values as explained.
    
    Examples
    --------    
    >>> array=np.random.randint(1,10,size=(3,4))
    >>> array
    array([[6, 4, 2, 3],
           [3, 9, 7, 1],
           [4, 6, 4, 5]])
    
    Suppose that we want to sort the values of the first column (ncol=0)
    in an ascending order.
    Then we only want to sort the values of that column, 
    preserving the structure of each row, instead of sorting every column,
    which would be the standard np.sort() procedure.
    
    That is to say, the lowest value of the mentioned column is 3,
    where the values of the corresponding row are 9, 7 and 1, respectively.
    
    If we were about to sort using the standard procedure, the result would be:
        
    >>> array
    array([[6, 4, 2, 3],
           [3, 9, 7, 1],
           [4, 6, 4, 5]])
    >>> np.sort(array, axis=0)
    array([[3, 4, 2, 1],
           [4, 6, 4, 3],
           [6, 9, 7, 5]])
       
    - The values of the first column are sorted, but so are the rest of
      the columns.
    - The row that corresponds to the lowest value of the 
      first column, which is 3, is [3, 9, 7, 1].
    - But because numbers in every row (remember that axis=0) are sorted
      independently, now it is [3, 4, 2, 1], altering the original structure 
      of the rows. 
    
    We want instead to preserve the original row structure: [3, 9, 7, 1].
    Extending this mechanism to the rest of the rows,
    the result is the following:
    
    sort_rows_by_column(array, ncol=0)
    array([[3, 9, 7, 1],
           [4, 6, 4, 5],
           [6, 4, 2, 3]])
    
    Another example, more intuitive,
    where several files are needed to be sorted
    with respect to the modification time, i.e. the second column:
    
    array([['VID-20221230_110.jpg', '2022-12-30 15:10:34'],
           ['VID-20221230_146.jpg', '2022-12-30 15:10:29'],
           ['VID-20221230_162.jpg', '2022-12-30 15:10:28'],
           ['VID-20221230_190.jpg', '2022-12-30 15:10:30'],
           ['VID-20221230_305.jpg', '2022-12-30 15:10:32'],
           ['VID-20221230_320.jpg', '2022-12-30 15:10:35']], dtype='<U27')
    
    sort_rows_by_column(array, ncol=1)
    array([['VID-20221230_162.jpg', '2022-12-30 15:10:28'],
           ['VID-20221230_146.jpg', '2022-12-30 15:10:29'],
           ['VID-20221230_190.jpg', '2022-12-30 15:10:30'],
           ['VID-20221230_305.jpg', '2022-12-30 15:10:32'],
           ['VID-20221230_110.jpg', '2022-12-30 15:10:34'],
           ['VID-20221230_320.jpg', '2022-12-30 15:10:35']], dtype='<U27')
    
    This example could be extended by adding the creation
    and last time access columns, but the mechanism remains exactly the same.
    """
    
    # Input validation #
    ####################
    
    # Sort method #
    all_arg_names = get_caller_method_args()
    sort_opt_pos = find_substring_index(all_arg_names, "sort_order")
    if sort_order not in sort_order_ops:
        raise ValueError("Invalid sort order option. "
                         f"(argument '{all_arg_names[sort_opt_pos]}'). \n"
                         f"Choose one from {sort_order_ops}.")
        
    # NumPy array conversion if the data is not of that type #
    if isinstance(array, list):
        # Check if the list contains sub-lists, all of the same length
        array_like = (
            all([get_obj_type_str(sub_obj) in ["list", "ndarray"] for sub_obj in array])
            and 
            len({len(sub_obj) for sub_obj in array if get_obj_type_str(sub_obj) in ["list", "ndarray"]}) == 1
            )
        if not array_like:
            raise ValueError("The given list will not be convertible to a "
                             "Numpy array since it has inhomogeneous parts. "
                             "Check the following:\n"
                             "1. Every object inside the list is either a "
                             "list or Numpy array (there can be mixed types).\n"
                             "2. All of them are of the same length.")
        else:
            array = np.array(array)    
    
    # Operations #    
    ##############
    
    if sort_order == "ascending":
        try:
            sorted_array_rbc = array[np.argsort(array[:,ncol])]
        except IndexError:
            sorted_array_rbc = np.sort(array, order=order)
            
    else:
        try:    
            sorted_array_rbc = array[np.fliplr([np.argsort(array[:,ncol])])[0]]
        except IndexError:
            sorted_array_rbc = np.sort(array, axis=-1, order=order)
        
    return sorted_array_rbc


def sort_columns_by_row(array, nrow, sort_order="ascending"): 
    # TODO: ondoko azalpenei lista bat sartzen denerako kasua gehitu
    """
    Function that sorts the values in a 2D dimension array
    against a specific row.
    
    The result is an array sorted along the second axis (index=1), i.e. the columns,
    where only the value of the selected row is sorted, while the rest
    of the values of the corresponding column remain the same.
    
    This tool is useful when the array contains parameters with
    different semantics and only one row is needed to be sorted.
    
    Parameters
    ----------
    array : list or numpy.ndarray
        Array to be sorted. It can contain both types of objects.
    nrow : int
        Number of the row whose values are going to be sorted against to.
    sort_order : {"ascending", "descending"}
        Default order is "ascending".
    
    Returns
    -------
    sorted_array : numpy.ndarray
        Array containing the sorted values as explained.
        
    Raises
    ------
    TypeError: if the array is not actually a NumPy array, because
                every operation relies on that type of arrays.
    
    Examples
    --------
    
    >>> array=np.random.randint(1,10,size=(3,4))
    >>> array
    array([[6, 4, 2, 3],
            [3, 9, 7, 1],
            [4, 6, 4, 5]])
    
    Suppose that we want to sort the values of the first row (nrow=0)
    in an ascending order.
    Then we only want to sort the values of that row, 
    preserving the structure of each column, instead of sorting every row,
    which would be the standard np.sort() procedure.
    
    That is to say, the lowest value of the mentioned row is 2,
    where the values of the corresponding column are 7 and 4, respectively.
    
    If we were about to sort using the standard procedure, the result would be:
        
    >>> array
    array([[6, 4, 2, 3],
           [3, 9, 7, 1],
           [4, 6, 4, 5]])
    >>> np.sort(array,axis=1)
    array([[2, 3, 4, 6],
           [1, 3, 7, 9],
           [4, 4, 5, 6]])
       
    - The values of the first row are sorted, but so are the rest of
      the rows.     
    - The column that corresponds to the lowest value of the 
      first row, which is 2, is [2, 7, 4].    
    - But because numbers in every column (remember that axis=1) are sorted
      independently, now it is [2, 1, 4], altering the original structure 
      of the columns. 
    
    We want instead to preserve the original column structure: [2, 7, 4].
    However, due to the matrix structure definition, it is not straightforward 
    to extending this mechanism to the rest of the columns.
    Nevertheless, the matrix definition does allow to work with 
    consecutive transposes!
    
    >>> array1=array.T
    >>> array1
    array([[6, 3, 4],
           [4, 9, 6],
           [2, 7, 4],
           [3, 1, 5]])
    
    And now we apply the same method as sorting ROWS AGAINST a specified
    COLUMN, where now array === array.T, and ncol=nrow=0
    which is performed by the 'sort_rows_by_column' function:
    
    >>> array1_tr=sort_rows_by_column(array.T, ncol=0)
    >>> array1_tr
    array([[2, 7, 4],
           [3, 1, 5],
           [4, 9, 6],
           [6, 3, 4]])
    
    And now we calculate its transpose.
    >>> array2 = array1_tr.T
    >>> array2
    array([[2, 3, 4, 6],
           [7, 1, 9, 3],
           [4, 5, 6, 4]])
    """
    
    # Input validation #
    ####################
    
    # Sort method #
    all_arg_names = get_caller_method_args()
    sort_opt_pos = find_substring_index(all_arg_names, "sort_order")
    if sort_order not in sort_order_ops:
        raise ValueError("Invalid sort order option. "
                         f"(argument '{all_arg_names[sort_opt_pos]}'). \n"
                         f"Choose one from {sort_order_ops}.")
        
    # NumPy array conversion if the data is not of that type #
    if isinstance(array, list):
        # Check if the list contains sub-lists, all of the same length
        array_like = (
            all([get_obj_type_str(sub_obj) in ["list", "ndarray"] for sub_obj in array])
            and 
            len({len(sub_obj) for sub_obj in array if get_obj_type_str(sub_obj) in ["list", "ndarray"]}) == 1
            )
        if not array_like:
            raise ValueError("The given list will not be convertible to a "
                             "Numpy array since it has inhomogeneous parts. "
                             "Check the following:\n"
                             "1. Every object inside the list is either a "
                             "list or Numpy array (there can be mixed types).\n"
                             "2. All of them are of the same length.")
        else:
            array = np.array(array)
            
    # Operations #
    ##############
    
    array_dtype = array.dtype
    
    if hasattr(array, 'T'):
        array_tr = array.T    
        sorted_array_cbr_tr = sort_rows_by_column(array_tr, nrow, sort_order)
        sorted_array_cbr = sorted_array_cbr_tr.T
        return sorted_array_cbr 
    else:
        raise TypeError(format_string(incompat_operation_obj_type, array_dtype))
        

# Insert and remove values #
#--------------------------#

def insert_values(x, index, values, axis=None):    
    """
    Inserts values at the specified index either on a list or NumPy array.
    
    Parameters
    ----------
    x : list or numpy.ndarray
        Object containing whatever type of data
    index : int
        Position where to introduce new data.
        Same behaviour as introducing a blank space at the left
        and then filling it with new data.
    values : list, numpy.array or pandas.Series
        If values are part of a DataFrame, they equally can be introduced
        into a list, to then call its data in the appropriate manner.
    axis : int, optional
        Axis alength which to insert 'values'.  If 'axis' is None then 'x'
        is flattened first.
    
    Returns
    -------
    appended_array : numpy.ndarray
        Only if 'x' is a numpy.ndarray. Array with new data appended.
    """
    
    lx = len(x)
    
    if isinstance(x, list):        
        if index >= lx:
            print(f"Index {index} beyond list length, "
                  "will be appended at the end of it.")
            
        x.insert(index, values)
        return x
        
    elif isinstance(x, np.ndarray):
        x_appended = np.insert(x, index, values, axis=axis)
        return x_appended
        
    else:
        input_obj_type = get_obj_type_str(x)
        raise TypeError(f"Expected a list or NumPy array, got {input_obj_type}.")
        
        
def extend_array(obj, obj2extend, np_axis=None):
    """
    Extend a list or concatenate a NumPy array with another list or NumPy array.

    Parameters
    ----------
    obj : list or numpy.ndarray
        The original list or NumPy array to be extended.
    obj2extend : list or numpy.ndarray
        The list or NumPy array to extend `obj` with.
    np_axis : int, optional
        Axis along which to concatenate the NumPy arrays. Default is None.

    Returns
    -------
    list or numpy.ndarray: The extended list or concatenated NumPy array.

    Raises
    ------
    TypeError: If `obj` is neither a list nor a NumPy array.

    Examples
    --------
    >>> extend_array([1, 2, 3], [4, 5])
    [1, 2, 3, 4, 5]

    >>> extend_array(np.array([1, 2, 3]), np.array([4, 5]), np_axis=0)
    array([1, 2, 3, 4, 5])    
    """
    if isinstance(obj, list):
        obj_extended = obj.extend(obj2extend)
    elif isinstance(obj, np.ndarray):
        obj_extended = np.concatenate((obj, obj2extend), axis=np_axis)
    else:
        raise TypeError("Input argument to be extended must either be of type "
                        "'list' or 'np.ndarray'.")
    return obj_extended


def remove_elements(array, idx2access, axis=None):    
    """
    Function that removes certain elements either from a list or NumPy array,
    selected by indices, which can be integers or booleans.
    
    Parameters
    ----------
    array : list or numpy.ndarray
        List or array containing the values.
    idx2access : list or numpy.ndarray of integers or booleans
        Object containing indices used to select elements
        from the previous list or array.
        If 'array' is of type list, then only a number is accepted.
    
    Returns
    -------
    array_filtered : numpy.ndarray
        Numpy array with the selected elements removed.
    """
    
    if isinstance(array, list):
        array_filtered = array.copy()
        
        if not isinstance(idx2access, int):
            raise TypeError("For a list-type input argument, "
                            "only an integer is accepted to index it.")
        else:
            array_filtered.pop(idx2access)
    
    elif isinstance(array, np.ndarray):
        array_filtered = np.delete(array, idx2access, axis=axis)
        
    else:
        raise TypeError("Input argument must either be of type "
                        "'list' or NumPy array.")
       
    return array_filtered

            
# Time-series manipulations #
#---------------------------#
 
def decompose_24h_cumulative_data(array, zeros_dtype='d'):    
    """
    Function that obtains the 1-hour time step cumulative data,
    subtracting to the next cumulative data, the previous cumulative value.
    It is only intended for 24-hour time step hourly data.
    
    The methodology, by its nature, gives negative values every 24 hours.
    Assuming that data follow a cumulative distribution
    and is definite positive, then those negative values
    are considered as spurious and they are substituted by
    arrays of zeroes.
    It suffices to encounter a single negative value
    along the n-1 dimensional array (for a time index) to set it to zero.
    
    Parameters
    ----------
    array : numpy.ndarray
        Multi-dimensional array which contains data,
        being the first index corresponding to 'time' dimension.
    zeros_dtype : str or numpy type (e.g. numpy.int, numpy.float64)
        Sets the precision of the array composed of zeroes.
    
    Returns
    -------
    hour_timestep_array : numpy.ndarray
        Multi dimensional array containing
        1-hour time step cumulative data.
    """
    
    records = len(array)
    array_shape = array.shape
    
    unmet_case_values = np.zeros(array_shape, dtype=zeros_dtype)
    
    hour_timestep_array\
    = np.array([array[t+1] - array[t]
                if np.all((res :=array[t+1] - array[t]) [~np.isnan(res)] >= 0.)
                else unmet_case_values
                for t in range(records-1)])
           
    hour_timestep_array = np.append(hour_timestep_array,
                              np.mean(hour_timestep_array[-2:], axis=0)[np.newaxis,:],
                              axis=0)
    
    return hour_timestep_array

#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported options #
#-------------------#

# Conversions of the data type of an object #
type_option_list = ["O", "U", "d"]

# Modules used to adaptat input objects to detect subarrays in arrays #
modules_adaptation = ["numpy", "pandas"]

# Sorting options #
sort_order_ops = ["ascending", "descending"]

# Switch case dictionaries #
#--------------------------#

obj_conversion_opt_dict = {
    modules_adaptation[0] : lambda obj: np.array(obj),
    modules_adaptation[1] : lambda obj: Series(obj)
    }

# Preformatted strings #
#----------------------#

# Error messages #
incompat_operation_obj_type = \
"Cannot perform operations with objects of data type '{}'."
