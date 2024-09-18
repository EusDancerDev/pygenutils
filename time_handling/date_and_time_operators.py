#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from datetime import datetime, timedelta
import time

import os

from numpy import float128
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.pandas_data_frames.data_frame_handler import find_date_key
from pyutils.strings import information_output_formatters, string_handler
from pyutils.time_handling.time_formatters import floated_time_parsing_dict, datetime_obj_converter
from pyutils.utilities.introspection_utils import get_caller_method_args, get_obj_type_str

# Create aliases #
#----------------#

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

find_substring_index = string_handler.find_substring_index

#------------------#
# Define functions #
#------------------#

#%%
        
# Input validation streamliner #
#------------------------------#

def _validate_option(arg_iterable, error_class, error_str):
    """
    Validate if the given option is within the list of allowed options.
    Specific for printing customised error messages.

    Parameters
    ----------
    arg_iterable : str, list or tuple
        Iterable consisting of elements to map into error_str, 
        particularly the option and the iterable of allowed ones.
    error_class : {ValueError, AttributeError}
        Error class to raise if option is not in the list of allowed ones.
    error_str : str
        Single or multiple line string denoting an error.

    Raises
    ------    
    ValueError or AttributeError: 
        If the option is not in the list of allowed options, with a detailed explanation.
    KeyError
        If error_class is not within the possible errors.
        It is preferred to raise this error rather than another ValueError
        to avoid confusion with the above case.
    """
    all_arg_names = get_caller_method_args()
    err_clas_arg_pos = find_substring_index(all_arg_names, "error_class")
    
    if error_class not in error_class_list :
        raise KeyError(f"Unsupported error class '{all_arg_names[err_clas_arg_pos]}'. "
                       f"Choose one from {error_class_list}.")
    
    option = arg_iterable[0]
    allowed_options = arg_iterable[1]
    
    if option not in allowed_options:
        raise error_class(format_string(error_str, arg_iterable))
            

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
    RuntimeError
        Possible only if ``dtype='str'``, if there is an error during the conversion process.

    Returns
    -------
    current_time : str or datetime.datetime or pd.Timestamp
        Current date and time object based on the dtype.
        If 'time_fmt_str' is provided, returns a formatted string representation.
    """
    
    # Validate string representing the data type #
    arg_tuple_current_time = (dtype, dt_dtype_options)
    _validate_option(arg_tuple_current_time, ValueError, unsupported_option_str)
    
    # Get the current date and time #
    current_time = current_datetime_dict.get(dtype)
    
    # A string does not have .strftime attribute, warn accordingly #
    all_arg_names = get_caller_method_args()
    fmt_str_arg_pos = find_substring_index(all_arg_names, "time_fmt_str")
    if (isinstance(current_time, str) and time_fmt_str is not None):
        raise ValueError("Current time is already a string. "
                         f"Choose another data type or "
                         f"set '{all_arg_names[fmt_str_arg_pos]}' to None.")
    
    # Format the object based on 'time_fmt_str' variable, if provided #
    if time_fmt_str is not None:
        try:
            current_time = datetime_obj_converter(current_time, convert_to="str")
        except Exception as err:
            raise RuntimeError(f"Error during conversion to 'str'': {err}")
        else:
            return current_time


# Nanoscale datetimes #
#-#-#-#-#-#-#-#-#-#-#-#

def get_nano_datetime(t=None, module="datetime"):
    """
    Get the current or specified time in nanoseconds, formatted as a datetime string.
    
    Parameters
    ----------
    t : int, float, or None, optional
        Time value in nanoseconds. If None, the current time is used.
    module : {"datetime", "time", "pandas", "numpy", "arrow"}, default "datetime"
        Module used to parse the floated time.

    Returns
    -------
    nano_dt_str : str
        The formatted datetime string with nanoseconds.
    """
    if t is not None and not isinstance(t, (float, int)):
        raise TypeError("Time value must either be integer or float.")
    
    # Use current time if none is provided
    if t is None:
        t = time.time_ns()  # Get current time in nanoseconds
    
    # Ensure we handle floating-point times by converting to int
    if isinstance(t, float):
        t = int(str(t).replace(".", ""))
        
    floated_nanotime_str = _nano_floated_time_str(t)
    nano_dt_str = _convert_floated_time_to_datetime(floated_nanotime_str, module)
    return nano_dt_str


def _convert_floated_time_to_datetime(floated_time, module):
    """
    Convert a floated time value to a datetime object with nanosecond precision.

    Parameters
    ----------
    floated_time : float or int
        The floated time value to be converted.
    module : str
        Module used to parse the floated time.

    Returns
    -------
    nano_dt_str : str
        The formatted datetime string with nanoseconds.
    """
    # Validate the module #
    arg_tuple_float_time_to_dt = (module, list(floated_time_parsing_dict.keys()))
    _validate_option(arg_tuple_float_time_to_dt, ValueError, unsupported_option_str)

    # Convert to float if input is a string
    if isinstance(floated_time, str):
        floated_time = float128(floated_time)
        
    # Split into seconds and nanoseconds
    seconds = int(floated_time)
    nanoseconds = int((floated_time - seconds) * 1_000_000_000)

    # Convert the seconds part into a datetime object
    dt = floated_time_parsing_dict[module](floated_time, date_unit="ns")
    
    # Add the nanoseconds part and return the formatted string
    dt_with_nanos = dt + timedelta(microseconds=nanoseconds / 1_000)
    dt_with_nanos_str = datetime_obj_converter(dt_with_nanos, 
                                               convert_to="str",
                                               dt_fmt_str='%Y-%m-%dT%H:%M:%S')
    nano_dt_str = f"{dt_with_nanos_str}.{nanoseconds:09d}"
    return nano_dt_str


def _nano_floated_time_str(time_ns):
    """
    Convert a time value in nanoseconds to a formatted floating-point time string.

    Parameters
    ----------
    time_ns : int
        Time value in nanoseconds.

    Returns
    -------
    str
        The floating-point time string with nanosecond precision.
    """
    # Convert nanoseconds to seconds and nanoseconds parts
    seconds = time_ns // 1_000_000_000
    nanoseconds = time_ns % 1_000_000_000

    # Format the floating-point time with nanosecond precision
    return f"{seconds}.{nanoseconds:09d}"


# Date/time attributes #
#-#-#-#-#-#-#-#-#-#-#-#-

def get_datetime_object_unit(dt_obj):
    """
    Retrieve the time unit of a numpy.datetime64 or similar datetime object.

    Parameters
    ----------
    dt_obj : object
        The datetime-like object from which the unit is to be retrieved. 
        Must have a 'dtype' attribute, such as numpy.datetime64 or pandas.Timestamp.

    Returns
    -------
    str
        The time unit of the datetime object (e.g., "ns" for nanoseconds).
    
    Raises
    ------
    AttributeError
        If the object does not have a 'dtype' attribute or is not of a supported type.
    ValueError
        If the string parsing fails
    """
    obj_type = get_obj_type_str(dt_obj)
    if hasattr(dt_obj, "dtype"):
        dtype_str = str(dt_obj.dtype)
        if ("[" in dtype_str and "]" in dtype_str):
            return dtype_str.split("[", 1)[1].split("]", 1)[0]
        else:
            raise ValueError(f"Could not determine unit from dtype: '{dtype_str}'")
    else:
        raise AttributeError(f"Object of type '{obj_type}' has no attribute 'dtype'.")

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
    arg_tuple_operation_datetime = (attr, attr_options)
    _validate_option(arg_tuple_operation_datetime, AttributeError, attribute_error_str)
    
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
                              operator="inner",
                              time_fmt_str=None):
    """
    Merges two datetime objects (either pandas.DataFrames or named/unnamed pandas.Series) 
    based on a specified operator, and optionally formats the datetime columns.

    Parameters
    ----------
    df1 : pandas.DataFrame or pandas.Series
        The first datetime object.
    df2 : pandas.DataFrame or pandas.Series
        The second datetime object.
    operator : {'inner', 'outer', 'left', 'right'}, default 'inner'
        The type of merge to be performed.
    time_fmt_str : str, optional
        Format string for formatting the datetime columns using .strftime(). 
        Defaults to None.

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
    
    # Input validations #
    #-#-#-#-#-#-#-#-#-#-#
    
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
    except Exception as err:
        arg_tuple_df1 = (err, all_arg_names[df1_arg_pos])
        print_format_string(date_colname_not_found_warning, arg_tuple_df1)
        
        df1_cols = list(df1.columns)
        df1_cols[0] = std_date_colname
        df1.columns = df1_cols
    
    # Second object
    try:
        dt_colname = find_date_key(df2)
    except Exception as err:
        arg_tuple_df2 = (err, all_arg_names[df2_arg_pos])
        print_format_string(date_colname_not_found_warning, arg_tuple_df2)
        
        df2_cols = list(df2.columns)
        df2_cols[0] = std_date_colname
        df2.columns = df2_cols
                
    # Operator argument choice #    
    arg_tuple_dt_range_op1 = (operator, dt_range_operators)
    _validate_option(arg_tuple_dt_range_op1, ValueError, unsupported_option_str)
        
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
        res_dts = datetime_obj_converter(res_dts, convert_to="str", dt_fmt_str=time_fmt_str)
        
    return res_dts

  
#%%

#--------------------------#
# Parameters and constants #
#--------------------------#

# Option lists #
dt_range_operators = ["inner", "outer", "cross", "left", "right"]
dt_dtype_options = ["datetime", "str", "timestamp"]
attr_options = ["creation", "modification", "access"]
error_class_list = [ValueError, AttributeError]

# Preformatted strings #
#----------------------#

# Error strings #
unsupported_option_str = """Unsupported option '{}'. Options are {}."""
attribute_error_str = "Invalid attribute '{}'. Options are {}. "
date_colname_not_found_warning = """{} at object '{}'.
Setting default name 'Date' to column number 0."""

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
    dt_dtype_options[0] : datetime.datetime.now(),
    dt_dtype_options[1] : time.ctime(),
    dt_dtype_options[2] : pd.Timestamp.now()
    }