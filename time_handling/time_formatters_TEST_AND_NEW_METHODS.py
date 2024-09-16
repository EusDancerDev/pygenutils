#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import arrow
from datetime import datetime
from dateutil import parser
import time

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.parameters_and_constants import global_parameters
# from pyutils.parameters_and_constants.global_parameters import numpy_unit_list, \
#                                                                pandas_unit_list, \
#                                                                unit_factor_dict
from pyutils.strings.information_output_formatters import format_string
from pyutils.time_handling.date_and_time_operators import parse_floated_nanotime
from pyutils.utilities.general.introspection_utils import get_obj_type_str, retrieve_function_name

#----------------#
# Define aliases #
#----------------#

numpy_unit_list = global_parameters.numpy_unit_list
pandas_unit_list = global_parameters.pandas_unit_list
unit_factor_dict = global_parameters.unit_factor_dict

#------------------#
# Define functions #
#------------------#

# %% INPUT VALIDATION STREAMLINERS

def _validate_option(explanation, option, allowed_options):
    """
    Validate if the given option is within the list of allowed options.

    Parameters
    ----------
    explanation : str
        A brief description or context of the validation.
    option : object
        The option to be validated.
    allowed_options : list/iterable
        A list or iterable of valid options.

    Raises
    ------
    ValueError: 
        If the option is not in the list of allowed options, with a detailed explanation.
    """
    if option not in allowed_options:
        raise ValueError(f"{explanation} '{option}' not supported for this operation. "
                         f"Choose one from {allowed_options}.")

def _validate_precision(frac_precision, option, min_prec=0, max_prec=9):
    """
    Validate the precision level for a floating-point number and ensure it is within a valid range.
    
    Parameters
    ----------
    frac_precision : int or None
        The desired fractional precision to validate.
    option : str
        Specifies the type of object or library (e.g., "pandas") that supports higher precision.
    min_prec : int, optional
        The minimum allowed precision. Default is 0.
    max_prec : int, optional
        The maximum allowed precision. Default is 9.
    
    Raises
    ------
    ValueError
        If `frac_precision` is outside the range [min_prec, max_prec] or
        `frac_precision` is greater than or equal to 7 but `option` is not "pandas".
    """
    if ((frac_precision is not None) and not (min_prec <= frac_precision <= max_prec)):
        raise ValueError(f"Fractional precision must be between {min_prec} and {max_prec}.")
    if ((7 <= frac_precision <= max_prec) and option != "pandas"):
        raise ValueError(f"Only option 'pandas' supports precision={frac_precision}.")
        
def _validate_unit(unit, module):
    """
    Validates the date unit based on the module.

    Parameters
    ----------
    unit : str
        Time unit for the floated time. 
        Only applicable if the module is 'numpy' or 'pandas'.
    module : {"numpy", "pandas"}
        The module used for parsing the floated time.

    Raises
    ------
    ValueError
        If `unit` is not supported for the specified `module`.
    """
    
    # Define allowed date units for each module    
    if module == "numpy" and unit not in numpy_unit_list:
        raise ValueError(f"Unsupported date unit for numpy.datetime64 objects. Choose one from {numpy_unit_list}.")
        
    if module == "pandas" and unit not in pandas_unit_list:
        raise ValueError(f"Unsupported date unit for pandas.Timestamp objects. Choose one from {pandas_unit_list}.")



# %% SIMPLE DATA PARSING

# Input format: str #
#-------------------#

def parse_time_string(datetime_str, dt_fmt_str, module="datetime", unit="ns"):
    """
    Convert a time string to a date/time object using a specified library.
    
    Parameters
    ----------
    datetime_str : str
        A string representing the date and/or time.    
    dt_fmt_str : str
        A format string that defines the structure of `datetime_str`. 
        Must follow the format required by the chosen module.     
    module : {"datetime", "dateutil", "pandas", "numpy", "arrow"}, default 'datetime'
        Specifies the library used for conversion. 
        If 'numpy', datetime_str must be in ISO 8601 date or datetime format.
    unit : str, optional
        Applies only if ``module`` is either 'numpy' or 'pandas'.
        Denotes which unit ``floated_time`` is expressed in.
        
        For Pandas, allowed units are {'D', 's', 'ms', 'us', 'ns'}.
        For NumPy, allowed units are {'Y', 'M', 'D', 'h', 'm', 's' , 'ms', 'us', 'ns'}.
       
        According the standards, this parameter defaults to 'ns' for Pandas 
        and 'us' for NumPy.
        Then, in order to maintain compatibility, the largest common time unit 'us'
        has been defined as default in this method.
    
    Returns
    -------
    datetime_obj : object
        The converted date/time object, as per the chosen module.
    
    Raises
    ------
    ValueError
        If the module is not supported or if the time string does not match
        the provided format.
    """
    
    # Input validation #
    ####################
    
    # Module #
    allowed_modules = list(time_str_parsing_dict.keys())
    _validate_option("Module", module, allowed_modules)
    
    # Formatting string #
    if not dt_fmt_str:
        raise ValueError("A datetime format string must be provided.")
        
    # Time string parsing #
    #######################
    
    try:
        parse_func = time_str_parsing_dict.get(module)
        datetime_obj = parse_func(datetime_str, dt_fmt_str, unit) \
                       if module == "pandas"\
                       else parse_func(datetime_str, dt_fmt_str)
    except ValueError:
        raise ValueError("The time string does not match the format string provided.")
    else:
        return datetime_obj
    
# %% 

# Input format: int, float #
#--------------------------#

# Main method #
#-#-#-#-#-#-#-#

def parse_float_time(datetime_float, 
                     frac_precision=None,
                     origin="unix", 
                     unit="us", 
                     dt_fmt_str=None, 
                     module="datetime"):
    """
    Converts an integer or float time to a date/time object.
    It also converts to a string representation if requested.
    
    datetime_float : int or float
        Time representing a time unit relative to an origin.
    frac_precision : int [0,9] or None 
        Precision of the fractional part of the seconds.
        If not None, this part is rounded to the desired number of decimals,
        which must be between 0 and 9. For decimals in [7,9], nanoscale
        datetime is generated, supported only by 'pandas'.
        Raises a ValueError if 7 <= frac_precision <= 9 and module is not 'pandas'.        
        Defaults to None, i.e., the original precision is used.
    origin : {"arbitrary", "unix"}, default 'unix'
        Determines whether to compute time relative to an arbitrary origin 
        or to the Unix epoch start (1970-01-01 00:00:00).
        For example, the elapsed time for a program to execute has its origin at 
        the moment of execution, whereas for clock times, seconds are counted 
        from the epoch time.
    unit : str, optional
        Applies only if ``origin='unix'`` and ``convert_to={'numpy', 'pandas'}``.
        Denotes which unit ``datetime_str`` is expressed in. 
        
        For Pandas, allowed units are {'D', 's', 'ms', 'us', 'ns'}.
        For NumPy, allowed units are {'Y', 'M', 'D', 'h', 'm', 's', 'ms', 'us', 'ns'}.
        Defaults to 'ns' for Pandas and 'us' for NumPy.
    dt_fmt_str : str
        Format string to convert the date/time object to a string.
    module : {"datetime", "time", "pandas", "numpy", "arrow", "str"}, default 'datetime'.
         The module or class used to parse the floated time. 
         If 'numpy', datetime_float represents an offset from the Unix epoch start.
      
    Returns
    -------
    object
        The converted date/time object or string representation.
    
    Raises
    ------
    ValueError
        If parameters are invalid or the conversion fails.
    """        
    
    # Input validation #
    ####################
    
    # Module #
    allowed_modules = ["str"] + list(floated_time_parsing_dict.keys())
    _validate_option("Object type conversion", module, allowed_modules)
    
    # Time formatting string #
    if module != "str" and not dt_fmt_str:
        raise ValueError("You must provide a formatting string.")

    # Fractional second precision #
    _validate_precision(frac_precision, module)

    # Date unit #
    _validate_unit(unit, module)

    # Floated time parsing #
    ########################

    if module == "str":
        return _parse_float_to_string(datetime_float,
                                     frac_precision, 
                                     origin,
                                     dt_fmt_str,
                                     unit,
                                     module)
    else:
        return _float_time_parser(datetime_float, module, unit)
    
    
# Auxiliary methods #
#-#-#-#-#-#-#-#-#-#-#

def _parse_float_to_string(floated_time, 
                          frac_precision, 
                          origin, 
                          dt_fmt_str, 
                          unit,
                          module):
    """        
    Converts a floated time to its string representation.

    Parameters
    ----------
    floated_time : int or float
        Time representing a time unit relative to an origin.
    frac_precision : int [0,9] or None
        Precision of the fractional seconds.
        Only supported by 'pandas' for high precision.
    origin : {"arbitrary", "unix"}
        Origin of the time measurement.
    dt_fmt_str : str
        Format string for the string representation.
    unit : str, optional
        Time unit for `floated_time` if `origin='unix'` and `module` in {'numpy', 'pandas'}.
    module : {"datetime", "time", "pandas", "numpy", "arrow"}
        Module used for parsing.

    Returns
    -------
    str
        The formatted string representation of the floated time.
    """
    
    if origin == "arbitrary":
        return _format_arbitrary_time(floated_time)
       
    elif origin == "unix":
        # Accommodation of the fractional second #
        if frac_precision is not None:
            if frac_precision <= 6:
                dt_seconds = round(floated_time)
                dt_obj = _float_time_parser(dt_seconds, module, unit)
                dt_str = dt_obj.strftime(dt_fmt_str)
            elif 7 <= frac_precision <= 9:
                return parse_floated_nanotime(floated_time, module)
        # Keep the original precision #
        else:
            dt_str = _float_time_parser(floated_time, module, unit).strftime(dt_fmt_str)
    
        return dt_str  

    
def _float_time_parser(floated_time, module, unit):
    """
    Parses a floated time into a date/time object.
    
    Parameters
    ----------
    floated_time : int or float
        Time representing a time unit relative to an origin.
    module : {"datetime", "time", "pandas", "numpy", "arrow"}
        Module used for parsing.
    unit : str, optional
        Time unit for `floated_time` if `module` in {'numpy', 'pandas'}.
    
    Returns
    -------
    datetime_obj : object
        The parsed date/time object.
    """
    
    # Input validation #
    ####################
    
    # Module #
    allowed_modules = list(floated_time_parsing_dict.keys())
    _validate_option("Object type conversion", module, allowed_modules)

    # Date unit #
    _validate_unit(unit, module)
    
    # Calculate datetime object #
    #############################
    
    datetime_obj = floated_time_parsing_dict.get(module)(floated_time, unit)
    return datetime_obj


def _format_arbitrary_time(floated_time):
    """
    Formats an arbitrary time (in seconds) into a string representation based on the provided format.
    
    Parameters
    ----------
    floated_time : int or float
        Time representing a time unit relative to an arbitrary origin.
    dt_fmt_str : str
        Format string that specifies how to format the time.
    
    Returns
    -------
    str
        The formatted time string.
    
    Raises
    ------
    ValueError
        If the format string is invalid or not supported.
        
    Notes
    -----
    Negative times or hours over 24 represent seconds matching 
    the next day's midnight. If so, set the hour to zero instead of 24.
    """

    # Compute time components #
    days, hours = divmod(floated_time // 3600, 24)
    minutes, seconds = divmod(floated_time % 3600, 60)
   
    # Format time parts according to 'dt_fmt_str' #
    try:
        if days > 0:
            time_tuple = (days, hours, minutes, seconds)
            time_parts_string = format_string(_time_str_parts_fmts[0], time_tuple)
        else:
            time_tuple = (hours, minutes, seconds)
            time_parts_string = format_string(_time_str_parts_fmts[1], time_tuple)
    except (KeyError, IndexError, ValueError) as e:
        raise ValueError(f"Invalid format string or time components: {e}")
    return time_parts_string 
        

# %% PARSING AMONG COMPLEX DATA OBJECTS

# Main methods #
#--------------#

# All except 'float' #
#--------------------#

def datetime_obj_converter(datetime_obj,
                           convert_to,
                           unit="ns",
                           float_class="d", 
                           int_class="int"):
    """
    Convert a date/time object to another, including float.
    If float, it represents seconds since the Unix epoch.
    
    Parameters
    ----------
    datetime_obj : object
        The date/time object to be converted. Accepted objects by library are:
            datetime : `datetime.datetime`, 
            numpy : `np.datetime64`, `np.ndarray`,
            pandas : `pd.Timestamp`, `pd.DataFrame`, `pd.Series`
            arrow : `arrow`, 
            time : `time.struct_time`, 
        
    convert_to : str
        The target type to convert `datetime_obj` to.
        Accepted values depend on the input type.
        For example, if `datetime_obj` is a `datetime`, `convert_to` could be
        `datetime64`, `Timestamp`, etc.
    unit : str
        The date unit for conversion, applicable to certain types. Default is `"ns"` (nanoseconds).
    float_class : str or numpy class
        The float precision class. Default is `"d"` (double precision).
    int_class : str or numpy class
        The integer precision class. Default is `"int"` (signed integer type).

    Returns
    -------
    The converted date/time object in the format/type specified by `convert_to`.

    Raises
    ------
    ValueError
        If `convert_to` is not a valid target type for the given `datetime_obj`.
    RuntimeError
        If there is an error during the conversion process.
        
    Conversion Options:   
    +------------------+---------+--------------+---------------+------------+--------------+---------+
    | Input Type       | `float` | `datetime`   | `struct_time` | `Timestamp`| `datetime64` | `arrow` |
    +------------------+---------+--------------+---------------+------------+--------------+---------+
    | `datetime`       | Yes     | Yes          | Yes           | Yes        | Yes          | Yes     |
    | `datetime64`     | Yes     | Yes          | Yes           | Yes        | No           | Yes     |
    | `Timestamp`      | Yes     | Yes          | Yes           | No         | Yes          | Yes     |
    | `arrow`          | Yes     | Yes          | Yes           | Yes        | Yes          | No      |
    | `struct_time`    | Yes     | Yes          | No            | Yes        | Yes          | Yes     |
    | `DataFrame`      | Yes     | Yes          | No            | No         | No           | No      |
    | `Series`         | Yes     | Yes          | No            | No         | No           | No      |
    | `ndarray`        | Yes     | Yes          | No            | No         | No           | No      |
    +------------------+---------+--------------+---------------+------------+--------------+---------+

    Notes
    -----
    - "Yes" in above table indicates that the conversion from the input type
      to the specified type is supported.
    - If the input object is whichever of types [`DataFrame`, `Series`, `ndarray`]
      and ``convert_to='float'``, the resulting object type will also be array-like,
      but an attempt will be made to convert its all values to float.
    """

    # Input validation #
    ####################
    
    # Object type to convert to #
    if not convert_to:
        raise ValueError("Argument 'convert_to' not provided.")
    
    # Helper function to perform conversion and handle exceptions
    def perform_conversion(conversion_dict, obj, *args):
        try:
            return conversion_dict.get(convert_to)(obj, *args)
        except Exception as err:
            raise RuntimeError(f"Error during conversion to {convert_to}: {err}")
              
    # Date unit factor #
    allowed_factors = list(unit_factor_dict.keys())
    _validate_option("Time unit factor", unit, allowed_factors)
            
    # Numpy precision classes #
    _validate_option("Numpy float precision class", float_class, float_class_list)
    _validate_option("Numpy integer precision class", int_class, int_class_list)
    
    # Operations #
    ##############
    
    # Get the object type's name #
    obj_type = get_obj_type_str(datetime_obj).lower()
    
    # Enumerate switch case dictionaries to use, depending on the input object type #
    conversion_opt_dict = {
        "datetime": datetime_obj_conversion_dict,
        "datetime64": datetime64_obj_conversion_dict,
        "timestamp": timestamp_obj_conversion_dict,
        "arrow": arrow_obj_conversion_dict,
        "struct_time": time_stt_obj_conversion_dict,
        "dataframe": _df_obj_conversion_dict,
        "series": _df_obj_conversion_dict, # Same functionalities as in pd.DataFrame
        "ndarray": _np_obj_conversion_dict
    }
    
    # Perform the conversion #
    allowed_general_options = list(conversion_opt_dict.keys())
    if obj_type in allowed_general_options:
        _validate_option("Object type conversion", convert_to, 
                        list(conversion_opt_dict[obj_type].keys()))
        conversion_dict = conversion_opt_dict[obj_type]
        return perform_conversion(conversion_dict, datetime_obj, unit)
    else:
        _validate_option("Object type conversion", convert_to, allowed_general_options)
        raise ValueError(f"Unsupported object type for conversion: {obj_type}.\n"
                         f"Options are {allowed_general_options}")
        
        
# Auxiliary methods #
#-------------------#

# Exclusively to 'float' #
#-#-#-#-#-#-#-#-#-#-#-#-#-

# Scalar complex data #
def _total_time_unit(datetime_obj, unit, float_class, int_class):
    """
    Convert a datetime object into total time based on the specified unit
    (e.g., seconds, microseconds, nanoseconds).
    
    Parameters
    ----------
    datetime_obj: 
        The datetime object to be converted. Can be of various types
        (e.g., `datetime`, `datetime64`, `Timestamp`).
    unit: 
        The time unit for conversion (e.g., "seconds", "microseconds", "nanoseconds"). 
        The actual unit factors are provided by the `unit_factor_dict`.
    float_class: 
        Specifies the precision class to use for floating-point results.
    int_class: 
        Specifies the precision class to use for integer results.
    
    Returns
    -------
    The total time in the specified unit, converted based on the object's type.
    
    Raises
    ------
    ValueError: 
        If the object type is unsupported for conversion.
    RuntimeError: 
        If an error occurs during the conversion process.
    """
    # Input validation #
    #------------------#
    
    # Current method name #
    current_method = retrieve_function_name()
    
    # Operations #
    #------------#
    
    unit_factor = unit_factor_dict.get(unit)
    obj_type = get_obj_type_str(datetime_obj).lower()  
  
    try:
        conversion_func = _total_time_unit_dict.get(obj_type)
        if conversion_func is None:
            raise ValueError(f"Unsupported object type, method '{current_method}': {obj_type}")
        return conversion_func(datetime_obj, unit, float_class, int_class, unit_factor)
    except Exception as err:
        raise RuntimeError(f"Error in conversion process, method '{current_method}': {err}")
        
        
# Array-like complex data #
def _total_time_complex_data(datetime_obj, int_class, unit_factor):
    """
    Calculate total time in a given unit for complex data types,
    such as Series and DataFrames, by converting all values to float.

    Parameters
    ----------
    datetime_obj: 
        The complex data object to be processed. Can be a `pd.Series` or `pd.DataFrame`.
    int_class: 
        Specifies the precision class to use for integer results.
    unit_factor: 
        The factor by which to multiply the converted values to get the
        total time in the specified unit.

    Returns
    -------
    pd.Series or pd.DataFrame
        The input data object with all values converted to total time in the specified unit.

    Raises
    ------
    RuntimeError: 
        If an error occurs during the conversion process for
        `Series` or `DataFrame` type objects.
    """
    # Input validation #
    current_method = retrieve_function_name()
    
    # Operations #
    obj_type = get_obj_type_str(datetime_obj).lower()
    dt_obj_aux = datetime_obj.copy()
    
    if obj_type == "series":
        try:
            return dt_obj_aux.astype(int_class) * unit_factor
        except (ValueError, Exception) as err:
            raise RuntimeError(f"Error in '{current_method}' method "
                               f"for 'Series' type object:\n{err}.")

    elif obj_type == "dataframe":
        try:
            for col in datetime_obj.columns:
                try:
                    dt_obj_aux[col] = dt_obj_aux[col].astype(int_class) * unit_factor
                except ValueError:
                    pass
            return dt_obj_aux
        except Exception as err:
            raise RuntimeError(f"Error in '{current_method}' method "
                               f"for 'DataFrame' type object:\n{err}.")


# Timezone aware information #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def _tzinfo_remover(dt_obj):
    """
    Remove timezone information from a datetime object if present.

    Parameters
    ----------
    dt_obj: datetime-like
        The datetime object from which timezone information should be removed.

    Returns
    -------
    datetime-like
        The datetime object without timezone information.
    """
    if hasattr(dt_obj, "tzinfo"):
        return dt_obj.replace(tzinfo=None)
    else:
        return dt_obj
    

# Conversions among different complex data #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

# Scalar complex data #
def _to_float(dt_obj, unit, float_class):
    """
    Convert a datetime object to a float representing the total time in the specified unit.

    Parameters
    ----------
    dt_obj: datetime-like
        The datetime object to be converted.
    unit: str
        The unit for conversion (e.g., "s" for seconds, "ms" for milliseconds).
    float_class: str, optional
        The precision class for the float result.

    Returns
    -------
    float
        The converted value in the specified unit.
    """
    obj_type = get_obj_type_str(dt_obj).lower()
    if obj_type == "datetime64":
        return dt_obj.astype(f"timedelta64[{unit}]").astype(float_class)
    if hasattr(dt_obj, 'timestamp'):
        return dt_obj.timestamp()  # works for datetime and pandas
    return float(dt_obj.float_timestamp)  # arrow

def _to_datetime(dt_obj):
    """
    Convert a given datetime-like object to a standard Python datetime object.

    Parameters
    ----------
    dt_obj: datetime-like
        The object to be converted to a Python datetime object.

    Returns
    -------
    datetime
        The converted Python datetime object.
    """
    obj_type = get_obj_type_str(dt_obj).lower()
    if obj_type == "datetime64":
        return dt_obj.astype(datetime)
    if obj_type == "timestamp":
        return dt_obj.to_pydatetime()
    if hasattr(dt_obj, 'fromtimestamp'):
        return dt_obj.fromtimestamp(dt_obj.float_timestamp)  # arrow
    return datetime(*dt_obj[:6])  # time.struct_time

def _to_time_struct(dt_obj):
    """
    Convert a datetime-like object to a time.struct_time object.

    Parameters
    ----------
    dt_obj: datetime-like
        The object to be converted to time.struct_time.

    Returns
    -------
    time.struct_time
        The converted time.struct_time object.
    """
    return _to_datetime(dt_obj).timetuple()

def _to_pandas(dt_obj, unit):
    """
    Convert a datetime-like object to a pandas Timestamp object with the specified unit.

    Parameters
    ----------
    dt_obj: datetime-like
        The object to be converted to a pandas Timestamp.
    unit: str, optional
        The unit for conversion.

    Returns
    -------
    pd.Timestamp
        The converted pandas Timestamp object.
    """
    return pd.to_datetime(_to_datetime(dt_obj), unit=unit)

def _to_numpy(dt_obj, unit):
    """
    Convert a datetime-like object to a NumPy datetime64 object with the specified unit.

    Parameters
    ----------
    dt_obj: datetime-like
        The object to be converted to a NumPy datetime64.
    unit: str, optional
        The unit for conversion (default is "ns" for nanoseconds).

    Returns
    -------
    np.datetime64
        The converted NumPy datetime64 object.
    """
    dt_obj = _to_datetime(dt_obj)
    return np.datetime64(_tzinfo_remover(dt_obj), unit)

def _to_arrow(dt_obj):
    """
    Convert a datetime-like object to an Arrow object.

    Parameters
    ----------
    dt_obj: datetime-like
        The object to be converted to an Arrow object.

    Returns
    -------
    arrow.Arrow
        The converted Arrow object.
    """
    dt_obj = _to_datetime(dt_obj)
    return arrow.get(dt_obj)


# Array-like complex data #
def _unify_complex_data(datetime_obj, unit):
    """
    Convert all columns or series in a DataFrame or Series to datetime using 
    the specified unit.

    Parameters
    ----------
    datetime_obj: pd.DataFrame or pd.Series
        The DataFrame or Series to be converted to datetime.
    unit: str
        The unit for conversion (e.g., "ns" for nanoseconds).

    Returns
    -------
    pd.DataFrame or pd.Series
        The input DataFrame or Series with all values converted to datetime 
        in the specified unit.
    """

    dt_obj_aux = datetime_obj.copy()
    obj_type = get_obj_type_str(datetime_obj).lower()
    
    if obj_type == "dataframe":
        for col in datetime_obj.columns:
            try:
                dt_obj_aux[col] = _to_datetime(dt_obj_aux[col], unit=unit)
            except ValueError:
                pass
    elif obj_type == "series":
        try:
            dt_obj_aux = _to_datetime(dt_obj_aux, unit=unit)
        except ValueError:
            pass
    return dt_obj_aux
        


# %% PARAMETERS AND CONSTANTS

# Precision classes for number integer or floating precision #
float_class_list = [np.float16, np.float32, "f", np.float64, "float", "d", np.float128]
int_class_list = [np.int8, np.int16, "i", np.float32, "int", np.int64]

# Switch case dictionaries #
#--------------------------#

# Time parsing #
#--------------#

# String #    
#-#-#-#-#-

time_str_parsing_dict = {
    "datetime" : lambda datetime_str, dt_fmt_str: datetime.strptime(datetime_str, dt_fmt_str),
    "dateutil" : lambda datetime_str, dt_fmt_str: parser.parse(datetime_str, dt_fmt_str),
    "pandas"   : lambda datetime_str, dt_fmt_str, unit: pd.to_datetime(datetime_str, 
                                                                            format=dt_fmt_str,
                                                                            unit=unit),
    "numpy"    : lambda datetime_str, dt_fmt_str, unit: np.datetime64(datetime_str, unit),
    "arrow"    : lambda datetime_str, dt_fmt_str: arrow.get(datetime_str, dt_fmt_str)
}

# Floated #
#-#-#-#-#-#

floated_time_parsing_dict = {
    "datetime" : lambda floated_time, _ : datetime.fromtimestamp(floated_time),
    "time"     : lambda floated_time : datetime(*tuple(time.localtime(floated_time))[:6]),
    "pandas"   : lambda floated_time, unit : pd.to_datetime(floated_time, unit=unit),
    "numpy"    : lambda floated_time, unit : np.datetime64(floated_time, unit),
    "arrow"    : lambda floated_time, _ : arrow.get(floated_time)
}

# Complex data # 
#-#-#-#-#-#-#-#-

# To other objects #
datetime_obj_conversion_dict = {
    "float"  : lambda dt_obj, _: dt_obj.timestamp(),
    "time"   : lambda dt_obj, _: dt_obj.timetuple(),
    "pandas" : lambda dt_obj, unit: pd.to_datetime(_tzinfo_remover(dt_obj), unit=unit),
    "numpy"  : lambda dt_obj, unit: np.datetime64(_tzinfo_remover(dt_obj), unit),
    "arrow"  : lambda dt_obj, _: arrow.get(dt_obj)
}

datetime64_obj_conversion_dict = {
    "float"    : lambda dt_obj, unit, _: _to_float(dt_obj, unit),
    "datetime" : lambda dt_obj, _: _to_datetime(dt_obj),
    "time"     : lambda dt_obj, _: _to_time_struct(dt_obj),
    "pandas"   : lambda dt_obj, unit: _to_pandas(dt_obj, unit),
    "arrow"    : lambda dt_obj, _: _to_arrow(dt_obj)
}

timestamp_obj_conversion_dict = {
    "float"    : lambda dt_obj: _to_float(dt_obj),
    "datetime" : lambda dt_obj: _to_datetime(dt_obj),
    "time"     : lambda dt_obj: _to_time_struct(dt_obj),
    "numpy"    : lambda dt_obj: dt_obj.to_numpy(),
    "arrow"    : lambda dt_obj: _to_arrow(dt_obj)
}

arrow_obj_conversion_dict = {
    "float"    : lambda dt_obj, _: _to_float(dt_obj),
    "datetime" : lambda dt_obj, _: _to_datetime(dt_obj),
    "time"     : lambda dt_obj, _: _to_time_struct(dt_obj),
    "pandas"   : lambda dt_obj, unit: _to_pandas(dt_obj, unit),
    "numpy"    : lambda dt_obj, unit: _to_numpy(dt_obj, unit)
}

time_stt_obj_conversion_dict = {
    "float"    : lambda dt_obj, _: _to_float(dt_obj),
    "datetime" : lambda dt_obj, _: _to_datetime(dt_obj),
    "pandas"   : lambda dt_obj, unit: pd.Timestamp(*dt_obj[:6], unit=unit),
    "numpy"    : lambda dt_obj, unit: np.datetime64(datetime(*dt_obj[:6]), unit),
    "arrow"    : lambda dt_obj, _: _to_arrow(dt_obj)
}

_df_obj_conversion_dict = {
    "float"  : lambda dt_obj, unit : _total_time_unit(dt_obj, unit),
    "pandas" : lambda dt_obj, unit : _unify_complex_data(dt_obj, unit)
}

_np_obj_conversion_dict = {
    "float"  : lambda dt_obj, unit : _total_time_unit(dt_obj, unit),
    "pandas" : lambda dt_obj, unit : pd.to_datetime(dt_obj, unit=unit)
}
        

# Exclusively to floated time #
_total_time_unit_dict = {
    "datetime"    : lambda dt_obj, _ : dt_obj.timestamp(),
    "datetime64"  : lambda dt_obj, unit, float_class: dt_obj.astype(f"timedelta64[{unit}]").astype(float_class),
    "struct_time" : lambda dt_obj, unit : datetime(*dt_obj[:6]),
    "arrow"       : lambda dt_obj, unit : dt_obj.float_timestamp,
    "dataframe"   : lambda dt_obj, _, int_class, unit_factor : _total_time_complex_data(dt_obj, int_class, unit_factor),
    "series"      : lambda dt_obj, _, int_class, unit_factor : _total_time_complex_data(dt_obj, int_class, unit_factor),
    "ndarray"     : lambda dt_obj, unit, float_class, _ : dt_obj.astype(f"datetime64[{unit}]").astype(float_class)  
    }

# Preformatted strings #
#----------------------#

_time_str_parts_fmts = [
    "{} days {} hours {} minutes {} seconds",
    "{} hours {} minutes {} seconds",
]
