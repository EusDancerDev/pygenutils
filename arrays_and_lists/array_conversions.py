#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists.array_data_manipulation import extend_array
from pyutils.parameters_and_constants.global_parameters import common_delim_list
from pyutils.utilities.introspection_utils import get_caller_method_args,\
                                                  get_obj_type_str, \
                                                  retrieve_function_name

#------------------#
# Define functions #
#------------------#

# Data types #
#------------#

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
        
        # TODO: gehitu ondoko metodoa egikaritzeko hitz gakoa funtzioaren argumentuen artean
        # array = np.hstack(array_of_lists) (EQUIVALENT for 'np.concatenate')
        
    return array


# TODO: berrizendatu 'flatten_content_to_string'-era
def flatten_content_to_string(obj, delim=None, add_final_space=False):
    method_name = retrieve_function_name()
    
    if get_obj_type_str(obj) not in ["list", "ndarray", "DataFrame", "Series"]:
        raise TypeError(f"'{method_name}' method supports "
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
        
        # If no delimiter is given for data joining, consider the space character
        if delim is None:
            delim = common_delim_list[6]
        allobj_string = delim.join(obj_list)
        
        """
        If other procedures or methods require a final space in the string,
        add it as requested
        """
        if add_final_space:
            allobj_string += delim
        
        return allobj_string
