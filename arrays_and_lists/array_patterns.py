#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import itertools as it
import more_itertools as mit

import numpy as np
from pandas import Series

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists.array_data_manipulation import sort_1D_arr_rudimentary
from pyutils.strings.string_handler import find_substring_index
from pyutils.utilities.introspection_utils import get_obj_type_str, \
                                                  get_caller_method_args

#------------------#
# Define functions # 
#------------------#

# Pattern searching #
#-------------------#

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


# Advanced methods #
#-#-#-#-#-#-#-#-#-#-

def detect_subarray_in_array(obj, test_obj, 
                             preferent_adapt_method="numpy",
                             reverse_arg_order=False,
                             return_all=False):
    
    """
    Calculates element in 'test_obj', broadcasting over 'obj' only.
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
        
        **Available options**
        
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
    
    # Input validation and reconversion of 'obj' object if necessary #
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
        

def find_duplicated_elements(array_like, remove_duplicated=False):    
    """
    Finds duplicated or N-folded elements in an array-like object,
    and returns the indices in which the element is present, 
    together with the element itself.
    
    Parameters
    ----------
    array_like : list, tuple or numpy.ndarray
        Array containing data.
    remove_duplicated : bool
        Whether to remove duplicated elements
        If True, it uses dictionaries to do so, as dictionaries cannot have
        duplicated keys.
        
    Returns
    -------
    duplicated_element_indices_dict : dict
        If 'remove_duplicated' is False,
        Dictionary composed with N-folded elements as keys 
        and indices, contained in tuples, as the values.   
    unique_key_list : list
        List of unique keys if 'remove_duplicated' is True
    
    """
    
    # Irrespective of whether the input argument is a NumPy array or a list,
    # flatten it and create a copy only if necessary
    flattened_array = np.asarray(array_like).flatten()
 
    # Use a dictionary to track the indices of each element
    duplicated_indices_dict = {}
    for idx, value in enumerate(flattened_array):
        duplicated_indices_dict.setdefault(value, []).append(idx)
    
    # Identify duplicated elements and their indices
    duplicated_element_indices_dict = {
        key: value for key, value in duplicated_indices_dict.items() if len(value) > 1
    }
    
    # Convert the flattened indices back to N-dim indices 
    for element, indices in duplicated_indices_dict.items():
        duplicated_element_indices_dict[element] = [
            tuple(np.unravel_index(idx, array_like.shape))
            if len(array_like.shape) > 1 else idx
            for idx in indices
        ]
        
    if remove_duplicated:
        return list(dict.fromkeys(array_like))
    else:
        return duplicated_element_indices_dict
    

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


# Sequence analysis #
#-------------------#

def count_consecutive(array, calculate_max_consec=False):    
    """
    Function that counts:
        1 : consecutive numbers in an array or pandas series,
            also distinguishing them by blocks.
        2 : maximum consecutive number subset length
            starting from an array that already satisfies certain condition,
            i.e. boolean array.
    
    Example 1
    ---------
    random_list = [45, 46, 47, 48, 80, 81, 83, 87]
    
    As can be seen, the first four numbers are consecutive,
    it stops there and another two consecutive number sequence begins.
    
    The result is then the following array:
    consec_times_array = [4, 2]
    
    Example 2
    ---------
    bool_array = [False, False, True, True, True, True, True, False, True, True]
    consec_times_array = [5, 2]
    max_consec_num = 5
    """
    
    if not calculate_max_consec:
        
        consec_times_array_byGroups_lengths\
        = [len(list(group)) for group in mit.consecutive_groups(array)]
        
        if len(consec_times_array_byGroups_lengths) > 1:
            consec_times_array_byGroups_lengths_gt1\
            = [lng for lng in consec_times_array_byGroups_lengths if lng >1]
            return consec_times_array_byGroups_lengths_gt1
            
        elif len(consec_times_array_byGroups_lengths) == 1:
            return consec_times_array_byGroups_lengths
        
        else:
            return None
    
    else:
    
        bool_groups = [list(group) for _, group in it.groupby(array)]
        
        consec_times_array_byGroups_lengths_gt1\
        = [len(group) for group in bool_groups if group[0] and len(group)>1]
        
        if len(consec_times_array_byGroups_lengths_gt1) > 0:
            max_consec_num = np.max(consec_times_array_byGroups_lengths_gt1)
            return max_consec_num
        else:
            return None
        

def count_unique_type_objects(list_of_objects):
    """
    Detects the type of the element inside a list as a whole,
    without diving individually into them (depth=1).
    It then counts the unique number of each object types.
    
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

        

# Pattern comparisons #
#---------------------#

def approach_value_in_array(array, given_value):    
    """
    Finds the index of the nearest numerical value
    compared to the original one in the given array.
    
    Parameters
    ----------
    array : list, numpy.ndarray or pandas.DataFrame
        or pandas.Series
        Array or Pandas DataFrame or series containing the values.
    
    given_value : float
        Value which to compare with those contained in the 'array' parameter.
    
    Returns
    -------
    value_approach : int or float
        Closest value in array to the given value.
    value_approach_idx : int or float or tuple
        Index of the closest value.
        If the array or pandas series is of 1D, it returns a float
        number where the closest value is located.
        If the array or pandas series is of 2D, it returns a tuple
        containing the rows and columns where the closest value is located.
    """
    
    if not isinstance(array, list):
        shape = array.shape
        lsh = len(shape)
        
        if "pandas" in str(type(array)):
            array = array.values
        
        diff_array = abs(array - given_value)
        
        value_approach_idx = np.where(array==np.min(diff_array))     
        if lsh == 1:        
            value_approach_idx = value_approach_idx[0][0]
            
        value_approach = array[value_approach_idx]
            
    else:
        shape = len(array)        
        diff_array = [abs(array[i] - given_value)
                      for i in range(shape)]
        value_approach_idx = [j
                              for j in range(shape) 
                              if diff_array[j]==min(diff_array)]
        
        if isinstance(value_approach_idx, list):
            value_approach_idx = value_approach_idx[0]
            
        value_approach = select_array_elements(array, value_approach_idx)
            
    return (value_approach, value_approach_idx)


#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported options #
#-------------------#

# Modules used in input object adaptations #
modules_adaptation = ["numpy", "pandas"]

# Switch case dictionaries #
#--------------------------#

# Data type main conversions #
obj_conversion_opt_dict = {
    modules_adaptation[0] : lambda obj: np.array(obj),
    modules_adaptation[1] : lambda obj: Series(obj)
    }