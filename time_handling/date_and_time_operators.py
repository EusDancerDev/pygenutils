#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import datetime
import time

import os

import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.pandas_data_frames.data_frame_handler import find_date_key
from pyutils.strings import information_output_formatters, string_handler
from pyutils.time_handling.time_formatters import time_format_tweaker
from pyutils.utilities.introspection_utils import get_caller_method_args

# Create aliases #
#----------------#

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

find_substring_index = string_handler.find_substring_index

#------------------#
# Define functions #
#------------------#

# TODO: 'time_format_tweaker' optimizatutakoan, berrikusi hura deitzeko sintaxia

#%%

# Dates and times #
#-----------------#

def get_current_datetime(dtype, time_fmt_str=None):   
    
    """
    Returns the current date and time based on the specified data type.

    Parameters
    ----------
    dtype : str
        Type of current time to retrieve. 
        Available options:
        - 'datetime'  : Returns datetime object using datetime.datetime.now()
        - 'str'       : Returns string representation of current time using time.ctime()
        - 'timestamp' : Returns timestamp object using pd.Timestamp.now()

    time_fmt_str : str, optional
        Optional format string for datetime formatting using .strftime().
        Default is None.

    Raises
    ------
    ValueError
    - If dtype is not one of the valid options ('datetime', 'str', 'timestamp').
    - If 'time_fmt_str' is provided and dtype is 'str' (which returns a string),
      as strings do not have .strftime() attribute.

    Returns
    -------
    current_time : str or datetime.datetime or pd.Timestamp
        Current date and time object based on the dtype.
        If 'time_fmt_str' is provided, returns a formatted string representation.
    """
    
    # Valid data type selection control #
    all_arg_names = get_caller_method_args()
    if dtype not in current_time_type_options:
        arg_tuple_current_time = (dtype, current_time_type_options)
        raise ValueError(format_string(unsupported_option_str, arg_tuple_current_time))
    
    # Get the current date and time #
    current_time = current_datetime_dict.get(dtype)
    
    # A string does not have .strftime attribute, warn accordingly #
    fmt_str_arg_pos = find_substring_index(all_arg_names, "time_fmt_str")
    if (isinstance(current_time, str) and time_fmt_str is not None):
        raise ValueError("Current time is already a string. "
                         f"Choose another data type or "
                         f"set {all_arg_names[fmt_str_arg_pos]} to None.")
    
    # Format the object based on 'time_fmt_str' variable, if provided #
    if time_fmt_str is not None:
        current_time = current_time.strftime(time_fmt_str)
    
    return current_time

#%%

# File manipulation time attributes #
#-----------------------------------#

def get_obj_operation_datetime(obj_list,
                               attr="modification",
                               time_fmt_str="%Y-%m-%d %H:%M:%S",
                               want_numpy_array=True):
    """
    Returns a 2D numpy array where each row contains an object (file path)
    from obj_list and its corresponding time attribute (creation, modification,
    or access time).

    Parameters
    ----------
    obj_list : list or str
        List of file paths or a single file path string.
    attr : {'creation', 'modification', or 'access'}, optional
        Type of time attribute to retrieve. Defaults to 'modification'.
    time_fmt_str : str, optional
        Format string for formatting the time attribute using .strftime(). 
        Defaults to '%Y-%m-%d %H:%M:%S'.
    want_numpy_array : bool
        Determines whether to convert the final object to a 2D Numpy array.
        If True, a 2D Numpy array is returned, else a list composed of lists.
        Defaults to True.
        
    Returns
    -------
    obj_timestamp_container : list of lists or numpy.ndarray
        If 'want_numpy_array' is False, a list of lists, where each of the latter
        contains the [file path, formatted time attribute], else a 2D Numpy array.

    Raises
    ------
    AttributeError
        If attr is not one of the valid options ('creation', 'modification', 'access').
        
    Note
    ----
    By default, 'want_numpy_array' is set to True, because
    it is expected to perform high-level operations with arrays frequently.
    However, this is a large library an since it's used only minimally in this module,
    lazy and selective import will be made.
    """
    # Validate the type of time attribute #
    all_arg_names = get_caller_method_args()
    attr_arg_pos = find_substring_index(all_arg_names, "attr")
    
    if attr not in attr_options:
        arg_tuple_operation_datetime = (attr_arg_pos, attr_options)
        raise AttributeError(format_string(attribute_error_str, 
                                           arg_tuple_operation_datetime))
    
    # Convert the input file object to a list if it is a string #
    if isinstance(obj_list, str):
        obj_list = [obj_list]
    
    # Retrieve operation times #
    obj_timestamp_container = []
    
    for obj in obj_list:
        struct_time_attr_obj = struct_time_attr_dict.get(attr)(obj)
        timestamp_str_attr_obj = time.strftime(time_fmt_str, struct_time_attr_obj)
        info_list = [obj, timestamp_str_attr_obj]
        obj_timestamp_container.append(info_list)
        
    # Format the result into a Numpy array if desired #
    if want_numpy_array:
        from numpy import array
        return array(obj_timestamp_container)
    else:
        return obj_timestamp_container    

#%%

# Pandas DataFrames of dates and times #
#--------------------------------------#

def merge_datetime_dataframes(df1, df2,
                              operator,
                              time_fmt_str=None,
                              return_str=False):
    """
    Merges two datetime objects (either pandas.DataFrames or named/unnamed pandas.Series) 
    based on a specified operator, and optionally formats the datetime columns.

    Parameters
    ----------
    df1 : pandas.DataFrame or pandas.Series
        The first datetime object.
    df2 : pandas.DataFrame or pandas.Series
        The second datetime object.
    operator : {'inner', 'outer', 'left', 'right'}
        The type of merge to be performed.
    time_fmt_str : str, optional
        Format string for formatting the datetime columns using .strftime(). 
        Defaults to None.
    return_str : bool, optional
        If True, convert datetime to string using the format specified in time_fmt_str. 
        Defaults to False.

    Returns
    -------
    pandas.DataFrame
        The merged datetime DataFrame.

    Raises
    ------
    ValueError
        If the operator is not one of the valid options:
        ('inner', 'outer', 'left', 'right').
    TypeError
        If df1 or df2 are not pandas.DataFrame or pandas.Series.
    AttributeError
        If df2 is a pandas.Series and does not have a name attribute.
    """
    
    # Parameter validations #
    #-#-#-#-#-#-#-#-#-#-#-#-#
    
    # Get the main argument names and their position on the function's arg list #    
    all_arg_names = get_caller_method_args()
    df1_arg_pos = find_substring_index(all_arg_names, "df1")
    df2_arg_pos = find_substring_index(all_arg_names, "df2")
    
    # Convert Series to DataFrame if necessary and standardize the column name #
    if isinstance(df1, pd.Series):
        df1 = df1.to_frame(name=df1.name if df1.name else "Date")
        
    if isinstance(df2, pd.Series):
        df2 = df2.to_frame(name=df2.name if df2.name else "Date")
        
    # If objects are DataFrames, ensure first datetime column name is standardized #
    std_date_colname = "Date"
    
    # First object
    try:
        dt_colname = find_date_key(df1)
    except:
        print_format_string(date_colname_not_found_err, all_arg_names[df1_arg_pos])
        
        df1_cols = list(df1.columns)
        df1_cols[0] = std_date_colname
        df1.columns = df1_cols
    
    # Second object
    try:
        dt_colname = find_date_key(df2)
    except:
        print_format_string(date_colname_not_found_err, all_arg_names[df2_arg_pos])
        
        df2_cols = list(df2.columns)
        df2_cols[0] = std_date_colname
        df2.columns = df2_cols
        
        
    # Operator argument choice #    
    if operator not in dt_range_operators:
        arg_tuple_dt_range_op1 = (operator, dt_range_operators)
        raise ValueError(format_string(unsupported_option_str, arg_tuple_dt_range_op1))
        
    # Operations #
    #-#-#-#-#-#-#-
    
    # Perform merge operation #
    res_dts = pd.merge(df1, df2, how=operator)
    
    # Sort values by datetime column #
    try:
        res_dts = res_dts.sort_values(by=dt_colname)
    except:
        res_dts = res_dts.sort_values(by=std_date_colname)
    
    # Optionally format datetime values #
    if time_fmt_str is not None:
        res_dts = time_format_tweaker(res_dts, time_fmt_str, return_str=return_str)
        
    return res_dts

  
#%%

#--------------------------#
# Parameters and constants #
#--------------------------#

# Option lists #
dt_range_operators = ["inner", "outer", "cross", "left", "right"]
current_time_type_options = ["datetime", "str", "timestamp"]
attr_options = ["creation", "modification", "access"]

# Preformatted strings #
#----------------------#

# Error strings #
unsupported_option_str = """Unsupported option '{}'. Options are {}."""
attribute_error_str = "Wrong attribute option at position {}. Options are {}. "
date_colname_not_found_err = """Standard time column name not found at object \
f"'{all_arg_names[df1_arg_pos]}.\nSetting default name 'Date' to column number 0."""

# Switch dictionaries #
#---------------------#

# Dictionary mapping attribute names to corresponding methods #
struct_time_attr_dict = {
    attr_options[0]: lambda obj: time.gmtime(os.path.getctime(obj)),
    attr_options[1]: lambda obj: time.gmtime(os.path.getmtime(obj)),
    attr_options[2]: lambda obj: time.gmtime(os.path.getatime(obj))
}

# Dictionary mapping current time provider methods to the corresponding methods #
current_datetime_dict = {
    current_time_type_options[0] : datetime.datetime.now(),
    current_time_type_options[1] : time.ctime(),
    current_time_type_options[2] : pd.Timestamp.now()
    }
