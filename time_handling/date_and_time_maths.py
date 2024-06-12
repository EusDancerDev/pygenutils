#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Goal**

This module aims to perform basic mathematical operations regarding
Pandas, Numpy date and time clock_objects.
"""

#----------------#
# Import modules #
#----------------#

import datetime
import time as _time
import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from strings.string_handler import find_substring_index
from strings.information_output_formatters import format_string, print_format_string
from time_handling.time_formatters import time2seconds, time_format_tweaker

#------------------#
# Define functions #
#------------------#

#%%

# Times #
#-------#

# Sum and subtract operations #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# Main method #
def clock_time_sum(clock_obj_list, operation="sum", str_obj_fmt="%H:%M:%S", output_format="standard"):
    """
    Calculate the sum or difference of a list of clock times.

    Parameters
    ----------
    clock_obj_list : list, tuple, or numpy.ndarray
        A list, tuple, or numpy.ndarray containing time objects as strings 
        that follow the format specified in 'str_obj_fmt'.
    operation : str, optional
        The operation to perform on the clock times. Supported operations 
        are "sum" (default) and "subtr" for subtraction.
    str_obj_fmt : str, optional
        The format string that specifies the format of the time objects. 
        Default is "%H:%M:%S".
    output_format : {'standard', 'class_object', 'raw'}, optional
        The output format for the result.
        Options are "standard" (default) for pandas.Timedelta, 
        "class_object" for datetime.time objects,
        and "raw" for a list containing [days, hours, minutes, seconds].

    Returns
    -------
    object
        The total time represented in the specified output format.

    Raises
    ------
    TypeError
        If 'clock_obj_list' is not a list, tuple, or numpy.ndarray, 
        or if 'output_format' is not a valid option.
    ValueError
        If 'clock_obj_list' contains fewer than 2 elements or if an unsupported 
        operation is specified.
    """

    # Proper date and/or time list format control #
    arg_names = clock_time_sum.__code__.co_varnames
    obj_list_pos = arg_names.index("clock_obj_list")
    
    if isinstance(clock_obj_list, str):
        raise TypeError(f"Argument '{arg_names[obj_list_pos]}' "
                        f"(position {obj_list_pos}) must either be a "
                        "list, tuple or numpy.ndarray.")
    elif (isinstance(clock_obj_list, (list, tuple, np.ndarray)) and len(clock_obj_list) < 2):
        raise ValueError(f"Argument '{arg_names[obj_list_pos]}' "
                         "must contain at least two objects.")
    
    # Proper operation argument control #
    basic_math_opt_list = ["sum", "subtr"]
    if operation not in basic_math_opt_list:
        raise ValueError("Unsupported mathematical operation. "
                         f"Supported ones are: {basic_math_opt_list}")
    
    # Time delta object conversions #
    timedelta_list = []
    for clock_obj in clock_obj_list:
        time_obj = convert_to_time(clock_obj, str_obj_fmt=str_obj_fmt)
        timedelta_obj = time_to_timedelta(time_obj)
        timedelta_list.append(timedelta_obj)
        
    # Perform the arithmetical operations #
    total_timedelta = operation_dict.get(operation)(timedelta_list)    
    
    # Return the result in the specified output format #
    if output_format == "standard":
        return total_timedelta
    elif output_format == "class_object":
        total_timedelta_time_part = total_timedelta.time()
        return total_timedelta_time_part
    elif output_format == "raw":
        total_timedelta_comp_list = [total_timedelta.days,
                                     total_timedelta.hour,
                                     total_timedelta.minute,
                                     total_timedelta.second]
        
        return total_timedelta_comp_list
   

# Auxiliary methods #
def convert_to_time(clock_obj, str_obj_fmt):
    """
    Convert various representations of time objects to datetime.time.

    Parameters
    ----------
    clock_obj : str, numpy.datetime64, time.struct_time, 
                datetime.datetime, datetime.time, or pandas.Timestamp
        The input time object to be converted.
    str_obj_fmt : str
        The format string that specifies the format of the time objects.

    Returns
    -------
    datetime.time
        The converted time object.
        
    Raises
    ------
    TypeError
        If the input object type is not supported.
    """
    if isinstance(clock_obj, str):
        datetime_obj = time_format_tweaker(clock_obj, str_obj_fmt=str_obj_fmt)
        time_obj = return_time_part(datetime_obj)
        return time_obj
    elif isinstance(clock_obj, np.datetime64):
        datetime_obj = time_format_tweaker(clock_obj, method="datetime_tolist")
        time_obj = return_time_part(datetime_obj)
        return time_obj
    elif isinstance(clock_obj, _time.struct_time):
        datetime_obj = clock_obj
        dt_parts_list = [clock_obj.tm_hour, clock_obj.tm_min, clock_obj.tm_sec]
        time_obj = return_time_part(datetime_obj, dt_parts_list)
        return time_obj
    elif isinstance(clock_obj, datetime.datetime):
        time_obj = return_time_part(clock_obj)
        return time_obj
    elif isinstance(clock_obj, datetime.time):
        return clock_obj
    elif isinstance(clock_obj, pd.Timestamp):
        time_obj = return_time_part(clock_obj)
        return time_obj    
    else:
        time_conv_arg_list = ["time or datetime", "time"]
        raise TypeError(format_string(unsupported_obj_type_str, time_conv_arg_list))
        
        
def return_time_part(datetime_obj, arg_list=None):
    """
    Return the time part of a datetime object.

    Parameters
    ----------
    datetime_obj : datetime.datetime
        The datetime object from which to extract the time part.
    arg_list : list, optional
        List containing specific parts of the datetime object.

    Returns
    -------
    datetime.time
        The time part of the datetime object.
    """
    if arg_list is None:
        time_obj = datetime_obj.time()
    else:
        time_obj = datetime_obj.time(*arg_list)
    return time_obj

def time_to_timedelta(t):
    """
    Convert a time object to a timedelta object.

    Parameters
    ----------
    t : datetime.time
        The time object to be converted.

    Returns
    -------
    pd.Timedelta
        The time represented as a timedelta object.
    """
    timedelta_obj = pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return timedelta_obj



# Time average #
#-#-#-#-#-#-#-#-

# Adapted from https://stackoverflow.com/questions/12033905/using-python-to-create-an-average-out-of-a-list-of-times

# Main method #
###############

def clock_time_average(clock_obj_list):
    # input datetime.datetime array and output datetime.time value
    angles = [time_to_radians(time) for time in clock_obj_list]
    avg_angle = average_angle(angles)    
    return radians_to_time_of_day(avg_angle)

# Auxiliary methods #
#####################

def time_to_radians(x):
    # Radians are calculated using a 24-hour circle, not 12-hour, 
    # starting at north and moving clockwise.
    
    # If the given time is already a datetime.time() clock_object,
    # skip to the next step.
    
    if isinstance(x, datetime.time):
        time_of_day = x
    else:
        time_of_day = x.time()
    
    time_tuple = (time_of_day.hour, time_of_day.minute, time_of_day.second)
    seconds_from_midnight = time2seconds(time_tuple)
    
    radians = seconds_from_midnight / (24 * 60 * 60) * 2 * np.pi
    return radians

def average_angle(angles):
    # Angles are measured in RADIANS
    x_sum = np.sum([np.sin(x) for x in angles])
    y_sum = np.sum([np.cos(x) for x in angles])
    
    x_mean = x_sum / len(angles)
    y_mean = y_sum / len(angles)
    
    return np.arctan2(x_mean, y_mean)   

def radians_to_time_of_day(x):
    # Radians are measured clockwise from north and represent time in a 24-hour circle
    seconds_from_midnight = x / (2 * np.pi) * 24 * 60 * 60
    
    # It cannot be considered the next second
    # until the decimal fraction equals to 1.
    # However in some cases due to the previous calculations using np.pi()
    # and the seconds of a whole day, the decimal fraction can
    # be almost one by an extremely small number.
    # In these cases add one second to the integer part.
    tol = 1.0e-9
    
    second_fraction_to_one\
    = abs(abs(seconds_from_midnight - int(seconds_from_midnight)) - 1)
    
    if second_fraction_to_one < tol:
        seconds_from_midnight_int = int(seconds_from_midnight) + 1
        
    else:
        seconds_from_midnight_int = int(seconds_from_midnight)
    
    # If the seconds match the next day's midnight,
    # set the hour to zero instead of 24.
    # Minutes and seconds are calculated on the 60th basis.
    hour, minute, second = time_format_tweaker(seconds_from_midnight_int)
    
    dt_time = datetime.time(hour, minute, second)
    
    return dt_time

#%%

# Dates #
#-------#

# Sum and subtract operations #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def sum_date_objects(date_list, operation="sum", str_obj_fmt="%Y-%m-%d"):

    """
    Parameters
    ----------
    str_obj_fmt : str
        String that identifies the format of those datetime objects of type string.
    """
    
    # Proper date and/or time list format control #
    arg_names = sum_date_objects.__code__.co_varnames
    date_list_pos = find_substring_index(arg_names, "date_list")
    
    if isinstance(date_list, str):
        raise TypeError(f"Argument '{arg_names[date_list_pos]}' "
                        f"(position {date_list_pos}) must either be a "
                        "list, tuple or numpy.ndarray.")
    elif (isinstance(date_list, (list, tuple, np.ndarray)) and len(date_list) < 2):
        raise ValueError(format_string(too_few_arg_error_str, "time"))
    
    # Proper operation argument control #
    if operation not in basic_math_opt_list:
        raise ValueError("Unsupported mathematical operation. "
                         f"Supported ones are sum and subtractions: {basic_math_opt_list}")
   
    # Perform the aritmethical operations #
    total_date = convert_to_date(date_list[0], str_obj_fmt=str_obj_fmt)
    for obj in date_list[1:]:
        date_obj = convert_to_date(obj, str_obj_fmt=str_obj_fmt)
        total_date = add_dates_with_year_gap(total_date, date_obj, operation=operation)
    return total_date


def convert_to_date(obj, str_obj_fmt):
    if isinstance(obj, str):
        datetime_obj = datetime.datetime.strptime(obj, str_obj_fmt)
        date_obj = datetime_obj.date()
        return date_obj
    elif isinstance(obj, np.datetime64):
        datetime_obj = pd.Timestamp(obj).to_pydatetime()
        date_obj = datetime_obj.date()
        return date_obj
    elif isinstance(obj, datetime.datetime):
        date_obj = obj.date()
        return date_obj
    elif isinstance(obj, datetime.date):
        return obj
    elif isinstance(obj, pd.Timestamp):
        date_obj = obj.date()
        return date_obj
    else:
        date_conv_arg_list = ["date or datetime", "date"]
        raise TypeError(format_string(unsupported_obj_type_str, date_conv_arg_list))
        

def add_dates_with_year_gap(date1, date2, operation):
    
    # Extract year, month, and day from both dates
    year1, month1, day1 = date1.year, date1.month, date1.day
    year2, month2, day2 = date2.year, date2.month, date2.day

    # Calculate the gap in years
    year_gap = abs(year2 - year1)

    # Date additions #
    ##################
    
    if operation == "sum":        
        # Add the months and days
        new_month = month1 + month2
        new_day = day1 + day2
        
        # Adjust the month and day for overflow
        while new_month > 12:
            new_month -= 12
            year_gap += 1
    
        # Create a dummy date to handle day overflow
        while True:
            try:
                result_date = datetime.date(year1 + year_gap, new_month, new_day)
                break
            except ValueError:
                new_day -= 1
                
                
    elif operation == "subtr":
        # Subtract the months and days
        new_month = month1 - month2
        new_day = day1 - day2
        
        # Adjust the month and day for underflow
        while new_month < 1:
            new_month += 12
            year_gap += 1
    
        # Create a dummy date to handle day underflow
        while True:
            try:
                result_date = datetime.date(year1 - year_gap, new_month, new_day)
                break
            except ValueError:
                new_day += 1

    return result_date


# Natural years #
#-#-#-#-#-#-#-#-#

def natural_year(dt_start, dt_end, time_fmt_str=None,
                 months_shift=0,
                 method="pandas",
                 print_str=False):
    
    # Quality control #
    #-#-#-#-#-#-#-#-#-#
    
    # Main argument names and their position on the function's definition #    
    arg_names = natural_year.__code__.co_varnames 
    shift_mon_arg_pos = find_substring_index(arg_names,
                                             "months_shift",
                                             advanced_search=False)
    
    if not isinstance(months_shift, int):
        arg_tuple_natural_year1 = (arg_names[shift_mon_arg_pos], 
                                   shift_mon_arg_pos, 'int')
        raise ValueError(format_string(type_error_str, arg_tuple_natural_year1))
    
    # Case study #
    #-#-#-#-#-#-#-
      
    # String to string format conversion checker #   
    if time_fmt_str is not None:
        dt_start_std = time_format_tweaker(dt_start, 
                                           time_fmt_str=time_fmt_str, 
                                           method=method)                    
        
        dt_end_std = time_format_tweaker(dt_end,
                                         time_fmt_str=time_fmt_str, 
                                         method=method)
        
    else:
        dt_start_std = dt_start
        dt_end_std = dt_end  
        
  
    # Get the final natural time's year and month #
    tf_nat_year = dt_end_std.year
    tf_nat_month = dt_end_std.month
    
    # Shift months by convenience, if necessary #
    tf_nat_month += months_shift
    
    # Get the last day of the resulting final time's day #
    tf_nat_ym0 = f"{tf_nat_year}-{tf_nat_month}"
    tf_nat_ym1 = f"{tf_nat_year}-{tf_nat_month+1}"
    
    tf_month_date_range = pd.date_range(tf_nat_ym0,
                                        tf_nat_ym1,
                                        inclusive="left")
    
    tf_nat_day = tf_month_date_range[-1].day
    
    # Convert the final natural date and time string to datetime clock_object #
    tf_nat_ymd = f"{tf_nat_year}-{tf_nat_month}-{tf_nat_day}"
    dt_end_natural = time_format_tweaker(tf_nat_ymd, method="pandas")
    dt_start_natural = dt_end_natural + pd.Timedelta(days=1)
        
    # Choose between returning the results as strings or datetime clock_objects #     
    if print_str:
        natural_year_range_table = \
        """
        {} -- {}
        
        |
        |
        v
        
        {dt_start_natural} -- {dt_end_natural}
        """
           
        arg_tuple_natural_year2 = (dt_start_std, dt_end_std)
        print_format_string(natural_year_range_table, arg_tuple_natural_year2)
    
    else:
        return (dt_start_natural, dt_end_natural)
    
    
#%%

#--------------------------#
# Parameters and constants #
#--------------------------#

# Option lists #
#--------------#

# Abbreviated mathematical operations #
basic_math_opt_list = ["sum", "subtr"]

# Preformatted strings #
#----------------------#

# Error strings #
type_error_str = "Argument '{}' at position {} must be of type '{}'."
        
unsupported_obj_type_str = """Unsupported {} type. Supported types are:
    - string
    - datetime.datetime
    - datetime.{}
    - numpy.datetime64
    - pandas.Timestamp
"""

too_few_arg_error_str = \
"At least two {} or datetime objects are required to perform the addition."

# Switch case dictionaries #
#--------------------------#

operation_dict = {
    "sum": np.sum,
    "subtr": lambda tds: tds[0] - np.sum(tds[1:])
}