#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from datetime import datetime, timedelta, timezone
import time

import os

from numpy import float128
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from filewise.general.introspection_utils import get_caller_args, get_type_str
from filewise.xarray_utils import file_utils, patterns
from pygenutils.strings import text_formatters, string_handler
from pygenutils.time_handling.time_formatters import datetime_obj_converter, floated_time_parsing_dict


# Try to import `pytz` and set a flag for availability
try:
    import pytz
    pytz_installed = True
except ImportError:
    pytz_installed = False

# Create aliases #
#----------------#

check_ncfile_integrity = file_utils.check_ncfile_integrity

format_string = text_formatters.format_string
print_format_string = text_formatters.print_format_string
find_substring_index = string_handler.find_substring_index

get_file_dimensions = patterns.get_file_dimensions
get_file_variables = patterns.get_file_variables

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
    param_keys = get_caller_args()
    err_clas_arg_pos = find_substring_index(param_keys, "error_class")
    
    if error_class not in error_class_list :
        raise KeyError(f"Unsupported error class '{param_keys[err_clas_arg_pos]}'. "
                       f"Choose one from {error_class_list}.")
    
    option = arg_iterable[0]
    allowed_options = arg_iterable[1]
    
    if option not in allowed_options:
        raise error_class(format_string(error_str, arg_iterable))
            
# %%

# Display and Conversion Utilities #
#----------------------------------#

def display_user_timestamp(user_timestamp, user_timezone_str):
    """
    Converts a UTC timestamp to the user's local timezone and formats it for display.
    
    Parameters
    ----------
    user_timestamp : datetime.datetime or str
        The timestamp to be converted. If a string, it should be in ISO format (e.g., "2023-01-01T12:00:00Z").
        The function assumes `user_timestamp` is in UTC if naive (no timezone).
        
    user_timezone_str : str
        The IANA timezone name (e.g., "America/New_York", "Europe/London") for the target timezone.

    Returns
    -------
    datetime.datetime or str
        The timestamp converted to the specified timezone.
        Returns as a `datetime` object if conversion is successful; otherwise, as a string with error details.

    Notes
    -----
    - If the `pytz` library is available, it is used for timezone conversion, providing extensive IANA timezone support.
    - If `pytz` is unavailable, the function defaults to using `datetime`'s built-in `astimezone()` mechanism, but limited to standard UTC offset conversions.
    
    Example
    -------
    >>> display_user_timestamp(datetime.now(timezone.utc), "America/New_York")
    datetime.datetime(2023, 1, 1, 7, 0, tzinfo=<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)
    
    >>> display_user_timestamp("2023-01-01T12:00:00Z", "Europe/London")
    datetime.datetime(2023, 1, 1, 12, 0, tzinfo=<DstTzInfo 'Europe/London' GMT0:00:00 STD>)
    """
    # Ensure user_timestamp is a datetime object in UTC
    if isinstance(user_timestamp, str):
        try:
            user_timestamp = datetime.fromisoformat(user_timestamp.replace("Z", "+00:00"))
        except ValueError:
            return "Invalid timestamp format. Expected ISO format (e.g., '2023-01-01T12:00:00Z')."
    elif not isinstance(user_timestamp, datetime):
        return "Invalid timestamp type. Expected `datetime` or ISO format string."
    
    if user_timestamp.tzinfo is None:
        user_timestamp = user_timestamp.replace(tzinfo=timezone.utc)

    # Convert timestamp using pytz if available, or fallback otherwise
    try:
        if pytz_installed:
            try:
                user_timezone = pytz.timezone(user_timezone_str)
            except pytz.UnknownTimeZoneError:
                raise ValueError(f"Invalid timezone: {user_timezone_str}")
            localized_timestamp = user_timestamp.astimezone(user_timezone)
        else:
            offset_hours = int(user_timezone_str.split("UTC")[-1].split(":")[0])
            offset_minutes = int(user_timezone_str.split(":")[1]) if ":" in user_timezone_str else 0
            offset = timedelta(hours=offset_hours, minutes=offset_minutes)
            localized_timestamp = user_timestamp.astimezone(timezone(offset))
            
    except Exception as e:
        raise RuntimeError(f"Error converting timestamp: {e}")

    return localized_timestamp


# Dates and times #
#-----------------#

def get_current_datetime(dtype="datetime", time_fmt_str=None, tz_arg=None):    
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
        Default is 'datetime'.

    time_fmt_str : str, optional
        Optional format string for datetime formatting using .strftime().
        Default is None.

    tz_arg : timezone or str, optional
        Optional timezone object or string for specifying the timezone.
        If a string is provided, it will be converted to a timezone using pytz.

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
    format_args_current_time = (dtype, dt_dtype_options)
    _validate_option(format_args_current_time, ValueError, unsupported_option_template)
    
    # Handle timezone argument
    if tz_arg is None:
        tz = None
    
    elif isinstance(tz_arg, str):
        if pytz_installed:
            try:
                tz_arg = pytz.timezone(tz_arg)
            except pytz.UnknownTimeZoneError:
                raise ValueError(f"Invalid timezone: {tz_arg}")
        else:
            raise ValueError("'pytz' library is required for string timezone arguments.")
    elif isinstance(tz_arg, int):
        tz = timezone(timedelta(hours=tz_arg))
    elif isinstance(tz_arg, timezone):
        tz = tz_arg
    else:
        raise TypeError("'tz_arg' must be a timezone object, string, or integer for UTC offset.")

    # Get the current date and time #
    current_time = current_datetime_dict.get(dtype)(tz)
    
    # A string does not have .strftime attribute, warn accordingly #
    param_keys = get_caller_args()
    fmt_str_arg_pos = find_substring_index(param_keys, "time_fmt_str")
    if (isinstance(current_time, str) and time_fmt_str is not None):
        raise ValueError("Current time is already a string. "
                         f"Choose another data type or "
                         f"set '{param_keys[fmt_str_arg_pos]}' to None.")
    
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
    format_args_float_time_to_dt = (module, list(floated_time_parsing_dict.keys()))
    _validate_option(format_args_float_time_to_dt, ValueError, unsupported_option_template)
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

# %%

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
    obj_type = get_type_str(dt_obj)
    
    if hasattr(dt_obj, "dtype"):
        dtype_str = str(dt_obj.dtype)
        if ("[" in dtype_str and "]" in dtype_str):
            return dtype_str.split("[", 1)[1].split("]", 1)[0]
        else:
            raise ValueError(f"Could not determine unit from dtype: '{dtype_str}'")
    else:
        raise AttributeError(f"Object of type '{obj_type}' has no attribute 'dtype'.")
        
        
# Date/time detection and handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def infer_frequency(data):
    """
    Infer the most likely frequency from the input, which can be either 
    a pandas DataFrame, Series, DatetimeIndex, TimedeltaIndex, 
    a NetCDF file path (as a string), or an xarray Dataset/DataArray.

    Parameters
    ----------
    data : pandas.DataFrame, pandas.Series, pandas.DatetimeIndex, pandas.TimedeltaIndex, 
           str (NetCDF file path), or xarray.Dataset/xarray.DataArray
        The input data for which to infer the frequency. 
        - For pandas objects, the method will try to infer the time frequency using 
          the 'find_time_key' helper to locate the date column or index.
        - For NetCDF files (string or xarray object), the method will infer the time frequency 
          using the 'find_time_key' helper to locate the time dimension.

    Returns
    -------
    str
        The inferred time frequency. If the frequency cannot be determined, a ValueError is raised.

    Raises
    ------
    ValueError
        If the frequency cannot be inferred from the input data.

    Notes
    -----
    - For pandas Series, the method will infer the frequency based on the series values, 
      not the index.
    - For NetCDF files, the method can handle either file paths (strings) or already-opened 
      xarray.Dataset/xarray.DataArray objects.
    """
    # Check input data type #
    #########################
    obj_type = get_type_str(data, lowercase=True)
    
    # Section 1: Handling Pandas DataFrame, Series, DatetimeIndex, or TimedeltaIndex #
    ##################################################################################
    if obj_type in ["dataframe", "series", "datetimeindex","timedeltaindex"]:
        try:
            # Attempt to find date column and infer frequency
            date_key = find_time_key(data)
            time_freq = pd.infer_freq(data[date_key])
        except (TypeError, ValueError):
            # If no date key is found, assume the input is an index
            time_freq = pd.infer_freq(data)
            
        if not time_freq:
            raise ValueError("Could not determine the time frequency from the pandas object.")
        return time_freq

    # Section 2: Handling NetCDF Files (string or xarray objects) #
    ###############################################################

    elif obj_type == "str":
        ds = check_ncfile_integrity(data)
    elif obj_type in ["dataset", "dataarray"]:
        ds = data.copy()
    else:
        raise TypeError("Unsupported data type. Must be pandas DataFrame, "
                        "Series, DatetimeIndex, TimedeltaIndex, "
                        "NetCDF file path (string), or xarray.Dataset/DataArray.")
        
    # Lazy import of xarray (if not already imported)
    if 'xr' not in globals():
        import xarray as xr
     
    # Infer time frequency for NetCDF data
    date_key = find_time_key(ds)
    time_freq = xr.infer_freq(ds[date_key])

    if not time_freq:
        raise ValueError("Could not determine the time frequency from the NetCDF data.")
    return time_freq


def infer_dt_range(data):
    """
    Infer the date and time range (first and last timestamps) from the input data,
    which can be either a pandas DataFrame, Series, or a NetCDF file path (as a string),
    or an xarray Dataset/DataArray.

    Parameters
    ----------
    data : pandas.DataFrame, pandas.Series, str (NetCDF file path), or xarray.Dataset/xarray.DataArray
        The input data from which to infer the date range.
        - For pandas objects, the method will use the 'find_time_key' to locate the date column.
        - For NetCDF files (string or xarray object), the method will infer the time range
          using the 'find_time_key' to locate the time dimension.

    Returns
    -------
    str
        A string representing the full time period in the format 'start_year-end_year'.

    Raises
    ------
    TypeError
        If the input data type is not supported.

    Notes
    -----
    - For pandas Series, the method will infer the date range based on the series values, 
      not the index.
    - For NetCDF files, the method will attempt a lazy import of xarray to avoid unnecessary 
      installation for non-climate-related tasks.
    """
    # Check input data type #
    obj_type = get_type_str(data, lowercase=True)
    
    # Section 1: Handling Pandas DataFrame or Series
    if obj_type in ["dataframe", "series"]:
        date_key = find_time_key(data)
        years = pd.unique(data[date_key].dt.year)
        full_period = f"{years[0]}-{years[-1]}"
        return full_period

    # Section 2: Handling NetCDF Files (string or xarray objects)
    elif obj_type == "str":
        ds = check_ncfile_integrity(data)
    elif obj_type in ["dataset", "dataarray"]:
        ds = data.copy()
    else:
        raise TypeError("Unsupported data type. Must be pandas DataFrame, Series, "
                        "NetCDF file path (string), or xarray.Dataset/DataArray.")
    
    # Infer time range for NetCDF data
    date_key = find_time_key(ds)
    years = pd.unique(ds[date_key].dt.year)
    full_period = f"{years[0]}-{years[-1]}"
    
    return full_period


# %%
def find_time_key(data):
    """
    Function that searches for the date key in a pandas DataFrame or the 'time' dimension/variable 
    in a NetCDF file or xarray Dataset.

    Parameters
    ----------
    data : pandas.DataFrame, str (NetCDF file path), or xarray.Dataset/xarray.DataArray
        The input data. If a pandas DataFrame is provided, the method will search for a 
        date-related key in the columns. For NetCDF or xarray objects, it will search 
        for the 'time' dimension or variable.

    Returns
    -------
    str
        The string that identifies the 'time' key (for pandas objects) or the 'time' 
        dimension/variable (for NetCDF/xarray objects).

    Raises
    ------
    TypeError
        If the input data type is not supported.
    ValueError
        If no 'time' key is found in pandas DataFrame or no 'time' dimension/variable is 
        found in NetCDF/xarray data.
    """
    # Check input data type 
    obj_type = get_type_str(data, lowercase=True)
    
    # Section 1: Handling Pandas DataFrame
    if obj_type == "dataframe":
        try:
            df_cols = [col.lower() for col in data.columns.tolist()]  # Lowercase all column names
            date_key_idx = find_substring_index(df_cols, time_kws)
            return data.columns[date_key_idx]  # Return original column name (not lowercased)
        except (AttributeError, KeyError):
            raise ValueError("No 'date' or similar key found in the pandas DataFrame.")
    
    else:
        # Section 2: Handling NetCDF Files or xarray objects
        if obj_type == "str":
            ds = check_ncfile_integrity(data)
        elif obj_type in ["dataset", "dataarray"]:
            ds = data.copy()
        else:
            raise TypeError("Unsupported data type. Must be a pandas DataFrame, "
                            "NetCDF file path (string), or xarray.Dataset/DataArray.")
        
        # Retrieve the dimension and variable lists from the dataset
        dims = get_file_dimensions(ds)
        vars_ = get_file_variables(ds)
    
        # Search for 'time'-related elements in dimensions and variables
        time_keys = [key for key in dims + vars_ if key.lower().startswith(('t', 'ti', 'da'))]
        
        if not time_keys:
            if obj_type == "str":
                raise ValueError(f"No 'time' dimension or variable found in the file '{data}'")
            else:
                raise ValueError("No 'time' dimension or variable found in the dataset.")

    return time_keys[0]  # Return the first unique 'time' key

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
    format_args_operation_datetime = (attr, attr_options)
    _validate_option(format_args_operation_datetime, AttributeError, attribute_error_template)
    
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
    param_keys = get_caller_args()
    df1_arg_pos = find_substring_index(param_keys, "df1")
    df2_arg_pos = find_substring_index(param_keys, "df2")
    
    # Convert Series to DataFrame if necessary and standardize the column name #
    if isinstance(df1, pd.Series):
        df1 = df1.to_frame(name=df1.name if df1.name else "Date")        
    if isinstance(df2, pd.Series):
        df2 = df2.to_frame(name=df2.name if df2.name else "Date")
        
    # If objects are DataFrames, ensure first datetime column name is standardised #
    std_date_colname = "Date"
    
    # First object
    try:
        dt_colname = find_time_key(df1)
    except Exception as err:
        format_args_df1 = (err, param_keys[df1_arg_pos])
        print_format_string(date_colname_not_found_template, format_args_df1)
        
        df1_cols = list(df1.columns)
        df1_cols[0] = std_date_colname
        df1.columns = df1_cols
    
    # Second object
    try:
        dt_colname = find_time_key(df2)
    except Exception as err:
        format_args_df2 = (err, param_keys[df2_arg_pos])
        print_format_string(date_colname_not_found_template, format_args_df2)
        
        df2_cols = list(df2.columns)
        df2_cols[0] = std_date_colname
        df2.columns = df2_cols
                
    # Operator argument choice #    
    format_args_dt_range_op1 = (operator, dt_range_operators)
    _validate_option(format_args_dt_range_op1, ValueError, unsupported_option_template)
        
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

# Time span shortands #
time_kws = ["da", "fe", "tim", "yy"]

# Template strings #
#------------------#

# Error strings #
unsupported_option_template = """Unsupported option '{}'. Options are {}."""
attribute_error_template = "Invalid attribute '{}'. Options are {}. "
date_colname_not_found_template = """{} at object '{}'.
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
    dt_dtype_options[0] : lambda tz_arg: datetime.datetime.now(tz_arg),
    dt_dtype_options[1] : lambda tz_arg: time.ctime(tz_arg),
    dt_dtype_options[2] : lambda tz_arg: pd.Timestamp.now(tz_arg)
    }
