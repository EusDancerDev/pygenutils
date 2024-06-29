#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import common_delim_list
from pyutils.strings.information_output_formatters import format_string
from pyutils.strings.string_handler import find_substring_index
from pyutils.utilities.introspection_utils import get_obj_type_str, \
                                                  retrieve_function_name,\
                                                  get_caller_method_args

#------------------#
# Define functions # 
#------------------#

# Array sorting #
#---------------#

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
        them in a list. Default behaviour is the latter one.
          
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

    sorted_values = array.copy()
    return sorted_values


def sort_1D_arr_rudimentary(obj, reverse=False):
    """
    Function that sorts a 1D array, using simple maths, without any 
    standard or external modules (hence the word 'rudimentary').
    This implies swapping list item positions, for that using a classic external
    function in order to accomplish the task.
    
    Parameters
    ----------
    obj : list or numpy.ndarray of int, float, complex or str
        List or NumPy array containing the above mentioned type of simple data.
        Every data must be of the same type, which is always guaranteed
        if the object is a numpy.ndarray.
    reverse: bool
        If False, then the items are sorted in an ascending order,
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

def sort_array_rows_by_column(array, ncol, sort_order="ascending", order=None):   
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
    array : numpy.ndarray
        Array to be sorted.
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
    
    sort_array_rows_by_column(array, ncol=0)
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
    
    sort_array_rows_by_column(array, ncol=1)
    array([['VID-20221230_162.jpg', '2022-12-30 15:10:28'],
           ['VID-20221230_146.jpg', '2022-12-30 15:10:29'],
           ['VID-20221230_190.jpg', '2022-12-30 15:10:30'],
           ['VID-20221230_305.jpg', '2022-12-30 15:10:32'],
           ['VID-20221230_110.jpg', '2022-12-30 15:10:34'],
           ['VID-20221230_320.jpg', '2022-12-30 15:10:35']], dtype='<U27')
    
    This example could be extended by adding the creation
    and last time access columns, but the mechanism remains exactly the same.
    """
    
    all_arg_names = get_caller_method_args()
    sort_opt_pos = find_substring_index(all_arg_names, "sort_order")
    if sort_order not in sort_order_ops:
        raise ValueError("Invalid sort order option. "
                         f"(argument '{all_arg_names[sort_opt_pos]}'). \n"
                         f"Choose one from {sort_order_ops}.")
    
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


def sort_array_columns_by_row(array, nrow, sort_order="ascending"): 
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
    array : numpy.ndarray
        Array to be sorted.
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
    which is performed by the 'sort_array_rows_by_column' function:
    
    >>> array1_tr=sort_array_rows_by_column(array.T, ncol=0)
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
    
    array_dtype = array.dtype
    
    if hasattr(array, 'T'):
        array_tr = array.T    
        sorted_array_cbr_tr = sort_array_rows_by_column(array_tr, nrow, sort_order)
        sorted_array_cbr = sorted_array_cbr_tr.T
        return sorted_array_cbr 
    else:
        raise TypeError(format_string(incompat_operation_obj_type, array_dtype))
        

# Array value inserting and removing #
#------------------------------------#

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


def remove_elements_from_array(array, idx2access, axis=None):    
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


# Array pattern management #
#--------------------------#

# Advanced methods #
#-#-#-#-#-#-#-#-#-#-

def detect_subarray_in_array(obj, test_obj, 
                             preferent_adapt_method="numpy",
                             reverse_arg_order=False,
                             return_all=False):
    
    """
    Calculates element in 'test_elements', broadcasting over 'obj' only.
    Returns a boolean array of the same shape as 'obj' that is True
    where an element of 'obj' is in 'test_obj' and False otherwise.
    (adapted from help on 'np.isin' attribute).
    
    Parameters
    ----------
    obj : numpy.ndarray or pandas.Series 
        Input object.
    test_obj : numpy.ndarray or pandas.Series
        Object whose values to test against all inside parameter 'obj'.
        It does not need to be of the same type as it,
        but also the other type than thereof.
        
        All available options are
        -------------------------
        type(obj) === 'numpy.ndarray'; type(test_obj) === 'numpy.ndarray'
        type(obj) === 'numpy.ndarray'; type(test_obj) === 'pandas.Series'
        type(obj) === 'pandas.Series'; type(test_obj) === 'numpy.ndarray'
        type(obj) === 'pandas.Series'; type(test_obj) === 'pandas.Series'
                
    preferent_adapt_method : {'numpy', 'pandas'}
        If the input 'obj' argument is neither an array or pandas Series,
        it will be converted accordingly.
        Default method is 'numpy', which means that if this case is satisfied,
        it will be converted to a NumPy array.            
    reverse_arg_order : bool
        Some times is more logical to strictly limit to the size of
        the test element array.
        Then if True, the function actually reverses the comparison
        criterium, testing value of 'obj' agains those in 'test_obj'.            
    return_all : bool
        Controls whether to return the satisfaction of the test
        for all elements of 'test_obj'.
        Default value is False.
            
    Returns
    -------
    is_test_obj_contained : numpy.ndarray or pandas.Series
        Returns a multi-dimension object if 'return_all' is set to True.
    are_all_test_elements_in : bool
        If 'return_all' is set to False, it retuns True if all elements
        of the test array are contained in the original one, else returns False.
    """
    
    all_arg_names = get_caller_method_args()
    adapt_method_opt_pos = find_substring_index(all_arg_names, "preferent_adapt_method")
    
    if preferent_adapt_method not in modules_adaptation:
        raise ValueError("Invalid module for input object adaptations. "
                         f"(argument '{all_arg_names[adapt_method_opt_pos]}'.\n"
                         f"Options are {modules_adaptation}.")
    else:
        obj = obj_conversion_opt_dict.get(preferent_adapt_method)(obj)
      
    
    # Determine the element-wise presence #
    if isinstance(obj, np.ndarray):   
        
        if not reverse_arg_order:
            is_test_obj_contained = np.isin(obj, test_obj)
        else:
            is_test_obj_contained = np.isin(test_obj, obj)
        
        if return_all:
            are_all_test_elements_in = np.all(is_test_obj_contained)
            return are_all_test_elements_in
        else:
            return is_test_obj_contained
            
        
    elif get_obj_type_str(obj) == "Series":        
        if not reverse_arg_order:
            is_test_obj_contained = obj.isin(test_obj)
        else:
            is_test_obj_contained = test_obj.isin(obj)
        
        if return_all:
            are_all_test_elements_in = is_test_obj_contained.all()
            return are_all_test_elements_in
        else:
            return is_test_obj_contained
        
    else:
        raise TypeError("Input argument type must either be of type "
                        "'numpy.ndarray' or 'pandas.Series'.")


# Simple methods #
#-#-#-#-#-#-#-#-#-

def find_item_rudimentary(obj, obj2find):
    """
    Function that finds a given element in an array.
    For that, it always starts searching from its middle position,
    discarding its left or right side, depending on whether the object in the 
    middle position is greater or lower than the element to find.
    
    This function uses only simple maths without using any standard
    or external library.
    In order the latter to be effective, the input object must already be sorted,
    and since the mathematics are simple, that task is also going to be
    accomplished using the simple 'sort_1D_arr_rudimentary' function.
    
    Parameters
    ----------
    obj : list or numpy.ndarray of int, float, complex or str
        List or NumPy array containing the above mentioned type of simple data.
        Every data must be of the same type, which is always guaranteed
        if the object is a numpy.ndarray.
    obj2find: int, float, complex or str
        Simple data to find in the input object.
          
    Returns
    -------
    bool
        Returns True if the element is found, else returns False.
    """
    
    length = len(obj)
    sorted_obj = sort_1D_arr_rudimentary(obj)
    
    i = 0
    start = 0
    end = length - 1
    
    while i < length:
        half = (start + end) // 2
        if sorted_obj[half] == obj2find:
            return True
        elif sorted_obj[half] < obj2find:
            start = half + 1
        else:
            end = half - 1
        i += 1
    return False
    
        

# Array indexing #
#----------------#

def select_array_elements(array, idx2access):
    """
    Function to select elements from an array, list, or dict.
    Supports multidimensional NumPy arrays with dimensions up to 3.
    
    Parameters
    ----------
    array : list, dict, or numpy.ndarray
        Container holding the values. If a NumPy array, it can have up to 3 dimensions.
    idx2access : int, list, or numpy.ndarray
        Indices to select multiple values. If a single value is provided,
        it will be converted to a list.
    
    Returns
    -------
    selected : int, list, dict, or numpy.ndarray
        Single value or a slice of the input container.
    
    Raises
    ------
    ValueError
        If the input NumPy array has more than 3 dimensions.
    TypeError
        If the input array is not a list, dict, or numpy.ndarray.
    
    Examples
    --------
    # Selecting from a 1D list
    >>> select_array_elements([10, 20, 30, 40, 50], [1, 3])
    [20, 40]
    
    # Selecting from a 1D NumPy array
    >>> select_array_elements(np.array([10, 20, 30, 40, 50]), [1, 3])
    array([20, 40])
    
    # Selecting from a 2D NumPy array
    >>> select_array_elements(np.array([[10, 20, 30], [40, 50, 60], 
                                        [70, 80, 90]]), [[0, 1], [2, 2]])
    array([20, 90])
    
    # Selecting from a 3D NumPy array
    >>> select_array_elements(np.array([[[10, 20], [30, 40]],
                                        [[50, 60], [70, 80]]]),
                              [[0, 1, 0], [1, 0, 1]])
    array([30, 60])
    
    # Selecting from a dictionary
    >>> select_array_elements({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
    {'a': 1, 'c': 3}
    """
    
    # Ensure idx2access is a list or numpy.ndarray 
    # if it is a single integer or also numpy.ndarray, respectively
    if isinstance(idx2access, int):
        idx2access = [idx2access]
    elif isinstance(idx2access, list):
        idx2access = np.array(idx2access)
    
    # Access elements in a list
    if isinstance(array, list):
        accessed_mapping = map(array.__getitem__, idx2access)
        accessed_list = list(accessed_mapping)
        
        if len(accessed_list) == 1:
            accessed_list = accessed_list[0]
        return accessed_list
    
    # Access elements in a dictionary
    elif isinstance(array, dict):
        accessed_dict = {idx: array[idx] for idx in idx2access}
        return accessed_dict
    
    # Access elements in a NumPy array        
    elif isinstance(array, np.ndarray):
        if array.ndim > 3:
            raise ValueError("The input array has more than 3 dimensions, "
                             "which is not supported.")
        
        accessed_array = array[tuple(idx2access.T)] if idx2access.ndim > 1 else array[idx2access]
        
        if accessed_array.size == 1:
            accessed_array = accessed_array.item()
        return accessed_array
    
    else:
        raise TypeError("Unsupported array type. "
                        "Only lists, dicts, and numpy.ndarrays are supported.")


# Array uniqueness-related operations #
#-------------------------------------#

def find_duplicated_elements(array_like):    
    """
    Finds duplicated or N-folded elements in an array-like object,
    and returns the indices in which the element is present, 
    together with the element itself.
    
    Parameters
    ----------
    array_like : list, tuple or numpy.ndarray
        Array containing data.
        
    Returns
    -------
    duplicated_element_indices_dict : dict
        Dictionary composed with N-folded elements as keys 
        and indices, contained in tuples, as the values.    
    """
    
    if isinstance(array_like, (list, np.ndarray)):
        if isinstance(array_like, list):
            array_like = np.array(array_like).copy()
        flattened_array = array_like.flatten()
        
    elif isinstance(array_like, tuple):
        flattened_array = array_like

    # Use a dictionary to track the indices of each element
    index_dict = {}
    for idx, value in enumerate(flattened_array):
        if value in index_dict:
            index_dict[value].append(idx)
        else:
            index_dict[value] = [idx]
    
    # Identify duplicated elements and their indices
    duplicated_indices_dict = \
    {key: value for key, value in index_dict.items() if len(value) > 1}
    
    # Convert the flattened indices back to N-dim indices 
    # and store them in the dictionary
    duplicated_element_indices_dict = {}
    for element, indices in duplicated_indices_dict.items():
        duplicated_element_indices_dict[element] = \
        [tuple(np.unravel_index(idx, array_like.shape))
         # if isinstance(array_like, numpy.ndarray)
         if len(tuple(np.unravel_index(idx, array_like.shape))) > 1
         else idx 
         for idx in indices]
    
    return(duplicated_element_indices_dict)


# Array data type manipulations #
#-------------------------------#

def list_array_to_std_array(array_of_lists):
    """
    Convert a list of NumPy arrays into a single standard NumPy array.

    This function takes a list of NumPy arrays and combines them into a single
    NumPy array. It supports arrays with dimensions up to 3.

    Parameters
    ----------
    array_of_lists : list
        A list of NumPy arrays to be combined.

    Returns
    -------
    array : numpy.ndarray
        A single NumPy array formed by combining the input arrays.

    Raises
    ------
    Exception: If the arrays in the list have more than 3 dimensions.

    Example:
    >>> import numpy as np
    >>> array1 = np.array([[1, 2], [3, 4]])
    >>> array2 = np.array([[5, 6], [7, 8]])
    >>> array_of_lists = [array1, array2]
    >>> result = list_array_to_std_array(array_of_lists)
    >>> print(result)
    [[1 2]
     [3 4]
     [5 6]
     [7 8]]

    Note
    ----
    This function assumes that the input is a list of NumPy arrays. If the 
    arrays have different dimensions, it attempts to extend the array using
    the `extend_array` function.
    """
    
    dim_list = np.unique([len(arr.shape) for arr in array_of_lists])
    ld = len(dim_list)
    
    # If all lists in the object are of the same dimension #
    if ld == 1:
        dims = dim_list[0]
        
        if dims == 2:
            array = np.vstack(array_of_lists)
        elif dims == 3:
            array = np.stack(array_of_lists)
        else:
            raise Exception("Cannot handle lists containing N > 3 arrays.")
            
    # If the lists are multi-dimensional #
    else:
        array = extend_array(array, array_of_lists)
        # array = np.hstack(array_of_lists) (EQUIVALENT for 'np.concatenate')
        
    return array


def count_unique_type_objects(list_of_objects):
    """
    Checks whether all objects contained in a given list are the same,
    for that iterating over the list, getting the type,
    make the list of types unique and checking its length.
    
    Parameters
    ----------
    list_of_objects : list
        List of whatever objects.
    
    Returns
    -------
    unique_type_list : list of types
        List containing the unique types of the objects in the list.
    lutl : int
        Length of the unique object type list.
    """
    
    unique_type_list = np.unique([str(type(element)) for element in list_of_objects])
    lutl = len(unique_type_list)
    
    return (unique_type_list, lutl)


def basic_value_data_type_converter(obj_data,
                                    old_type, 
                                    new_type, 
                                    colname=None,
                                    convert_to_list=False):
    """
    Function that converts the original data type of the values contained 
    in an object to the desired one.
    If the data dtype is not the same as the original (old) one
    (e.g, if the original dtype is given mistakenly),
    the function simply returns the object unchanged,
    as well as printing a message showing the latter.
    
    Parameters
    ----------
    obj_data : pandas.DataFrame or numpy.ndarray
        Object containing data.
    old_type : str
        Type of the given object's values.
        Options are {"O": object, "U": string, "d": double}.
    new_type : str
        Type the data has to be converted to.
        Options are the same as for parameter 'old_type'.
    colname : str or None
        Only necessary if pandas.DataFrame cases is passed.
        Column name alength which to perform the conversion.
        Set to None if a numpy.ndarray is passed.
    convert_to_list : bool
        Some times it is desired to pass the result to another method
        which does not support object types that are not lists.
        If True, this method converts the result to a list.
    
    Returns
    -------
    obj_data : pandas.DataFrame or numpy.ndarray
        Object containing floated data, if necessary.

    """  
    
    all_arg_names = get_caller_method_args()    
    type_option_list = ["O", "U", "d"]
    
    if old_type not in type_option_list:
        raise ValueError(f"Invalid option of the original data type "
                         f"(argument '{all_arg_names[1]}').\n"
                         f"Options are {type_option_list}.")
    
    # Pandas DataFrames
    if get_obj_type_str(obj_data) == "DataFrame":
        data_type = obj_data.loc[:,colname].dtype
        
        if colname is None:
            raise ValueError("Please introduce a valid "
                             f"column name (argument '{all_arg_names[3]})"
                             "of the obj_data frame.")

        else:            
            if (data_type == old_type) or (old_type in data_type.str):
                data_floated = obj_data.copy()
                
                try:
                    data_floated.loc[:,colname]\
                    = data_floated.loc[:,colname].astype(new_type)                    
                except:
                    raise TypeError(f"Cannot convert object to type '{new_type}'.")
                else:
                    return data_floated
                    
            else:
                print("Returning object with its values' type unchanged.")
                return obj_data

    # Lists or NumPy arrays
    else:
        try:
            data_type = obj_data.dtype
        except AttributeError:
            obj_data = np.array(obj_data)
            data_type = obj_data.dtype

        if colname is not None:
            raise ValueError(f"Please set the argument '{all_arg_names[3]}' "
                             "to 'None'.")

        else:
            if (data_type == old_type) or (old_type in data_type.str):
                try:
                    data_floated = obj_data.copy().astype(new_type)
                except:
                    raise TypeError(f"Cannot convert object to type '{new_type}'.")
                else:
                    if convert_to_list:
                        data_floated = list(data_floated)
                    return data_floated
                
            else:
                print("Returning object with its values' type unchanged.")
                if convert_to_list:
                    obj_data = list(obj_data)
                return obj_data



# String creators from array-like objects #
#-----------------------------------------#

def condense_array_content_as_string(obj, add_final_space=False):
    method_name = retrieve_function_name()
    
    if get_obj_type_str(obj) not in ["list", "ndarray", "DataFrame", "Series"]:
        raise TypeError(f"'{method_name}' method works only for lists, "
                        "NumPy arrays and pandas DataFrames and series.")
        
    else:        
        if isinstance(obj, list):
            obj_val_array = obj.copy()
            
        elif get_obj_type_str(obj) in ["DataFrame", "Series"]:
            # Get the pandas DataFrame's or Series's value array #
            obj_val_array = obj.values
            
        
        """
        In the case of NumPy arrays and pandas DataFrames and series,
        if the object's dimension is N > 1, i.e. has the attribute 'flatten', 
        precisely flatten it.
        """
        if hasattr(obj, "flatten"):
            obj_val_array = obj_val_array.flatten()
            
            
        """
        In order to join every content in a single string, each element
        inside the object must be a string.
        Then, by default, each element is going to be converted to a string
        """
        
        obj_list = [str(el) for el in obj_val_array]
        
        # Merge the content of the resulting list #
        allobj_string = local_delim.join(obj_list)
        
        """
        If other procedures or methods require a final space in the string,
        add it as requested
        """
        if add_final_space:
            allobj_string += local_delim
        
        return allobj_string


#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported options #
#-------------------#

# Conversions of the data type of an object #
type_option_list = ["O", "U", "d"]

# Modules used to adaptat input objects to detect subarrays in arrays #
modules_adaptation = ["numpy", "pandas"]

# Character delimiter #
local_delim = common_delim_list[6]

# Sorting options #
sort_order_ops = ["ascending", "descending"]

# Switch case dictionaries #
#--------------------------#

obj_conversion_opt_dict = {
    modules_adaptation[0] : lambda obj: np.array(obj),
    modules_adaptation[1] : lambda obj: pd.Series(obj)
    }

# Preformatted strings #
#----------------------#

# Error messages #
incompat_operation_obj_type = \
"Cannot perform operations with objects of data type '{}'."
