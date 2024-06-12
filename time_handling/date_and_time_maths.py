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

from strings import information_output_formatters, string_handler
from time_handling.time_formatters import time2seconds, time_format_tweaker

# Create aliases #
#----------------#

find_substring_index = string_handler.find_substring_index

format_string = information_output_formatters.format_string
get_obj_type_str = information_output_formatters.get_obj_type_str
print_format_string = information_output_formatters.print_format_string

#------------------#
# Define functions #
#------------------#

#%%

# Times #
#-------#

# Sum and subtract operations #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# Main method #
def clock_time_sum(clock_obj_list, operation="sum", 
                   subtract_start_idx=1,
                   time_fmt_str="%H:%M:%S"):
    
    # Proper date and/or time list format control #
    arg_names = clock_time_sum.__co_varnames__
    obj_list_pos = find_substring_index(arg_names, "clock_obj_list")
    
    if isinstance(clock_obj_list, str):
        raise TypeError(f"Argument '{arg_names[obj_list_pos]}' "
                        f"(position {obj_list_pos}) must either be a "
                        "list, tuple or numpy.ndarray.")
    elif (isinstance(clock_obj_list, (list, tuple, np.ndarray)) and len(clock_obj_list) < 2):
        raise ValueError("At least two date and/or time objects are required "
                         "to perform the addition.")
    
    # Proper operation argument control #
    if operation not in basic_math_opt_list:
        raise ValueError("Unsupported mathematical operation. "
                         f"Supported ones are sum and subtractions: {basic_math_opt_list}")
    
    # Time delta object conversions #
    timedelta_list = []
    for clock_obj in clock_obj_list:
        time_obj = convert_to_time(clock_obj, time_fmt_str=time_fmt_str)
        timedelta_obj = time_to_timedelta(time_obj)
        timedelta_list.append(timedelta_obj)
        
        
    # Only for subtractions: time delta list index in range control #
    len_td_list_idx = len(timedelta_list)-1
    if (subtract_start_idx < 0 or subtract_start_idx > len_td_list_idx):
        raise IndexError("List index out of range, it must be between "
                         f"0 and {len_td_list_idx}.")
        
    # Perform the sum or subtract operation # TODO: switch dictionary ???
    if operation == "sum":
        total_timedelta = np.sum(timedelta_list)
    elif operation == "subtract":
        total_timedelta = \
        timedelta_list[0] - np.sum(timedelta_list[subtract_start_idx:])        
    return total_timedelta


# Auxiliary methods #
def convert_to_time(clock_obj, time_fmt_str):
    if isinstance(clock_obj, str):
        datetime_obj = time_format_tweaker(clock_obj, time_fmt_str=time_fmt_str)
        time_obj = datetime_obj.time()
        return time_obj
    elif isinstance(clock_obj, np.datetime64):
        datetime_obj = time_format_tweaker(clock_obj, method="datetime_tolist")
        time_obj = datetime_obj.time()
        return time_obj
    elif isinstance(clock_obj, _time.struct_time):
        time_obj = datetime.time(clock_obj.tm_hour, clock_obj.tm_min, clock_obj.tm_sec)
        return time_obj
    elif isinstance(clock_obj, datetime.datetime):
        time_obj = clock_obj.time()
        return time_obj
    elif isinstance(clock_obj, datetime.time):
        time_obj = clock_obj
        return time_obj
    elif isinstance(clock_obj, pd.Timestamp):
        time_obj = clock_obj.time()
        return time_obj
    else:
        raise TypeError("Unsupported type")
        

def time_to_timedelta(t):
    timedelta_obj = pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return timedelta_obj


time_list = [
    '2024-03-12 12:30:45',
    np.datetime64('2024-03-12T08:45:30'),
    _time.localtime(_time.mktime((2024, 3, 12, 15, 30, 0, 0, 0, -1))),
    datetime.datetime(2024, 3, 12, 14, 45, 15),
    datetime.time(9, 30, 0),
    pd.Timestamp('2024-03-12 07:20:30')
]

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

def sum_date_objects(date_list):
    # if len(date_list) < 2:
    #     raise ValueError("At least two dates are required to perform the addition.")
    
    # Proper date and/or time list format control #
    arg_names = sum_date_objects.__co_varnames__
    date_list_pos = find_substring_index(arg_names, "date_list")

    if isinstance(date_list, str):
        raise TypeError(f"Argument '{arg_names[date_list_pos]}' "
                        f"(position {date_list_pos}) must either be a "
                        "list, tuple or numpy.ndarray.")
    elif (isinstance(date_list, (list, tuple, np.ndarray)) and len(date_list) < 2):
        raise ValueError("At least two date and/or time objects are required "
                         "to perform the addition.")

    # Proper operation argument control #
    # if operation not in basic_math_opt_list:
    #     raise ValueError("Unsupported mathematical operation. "
    #                      f"Supported ones are sum and subtractions: {basic_math_opt_list}")
    
    # Date or datetime object conversions to date only #
    total_date = convert_to_date(date_list[0])
    for obj in date_list[1:]:
        date_obj = convert_to_date(obj)
        total_date = add_dates_with_year_gap(total_date, date_obj)
    
    return total_date


def convert_to_date(obj, time_fmt_str="%Y-%m-%d"):
    if isinstance(obj, str):
        datetime_obj = datetime.datetime.strptime(obj, time_fmt_str)
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
        raise TypeError("Unsupported type")

def add_dates_with_year_gap(date1, date2):
    # Extract year, month, and day from both dates
    year1, month1, day1 = date1.year, date1.month, date1.day
    year2, month2, day2 = date2.year, date2.month, date2.day

    # Calculate the gap in years
    year_gap = abs(year2 - year1)
    
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

    return result_date


# Example usage
date_list = [
    '2024-03-12',
    np.datetime64('2025-12-12'),
    datetime.datetime(2026, 5, 10),
    datetime.date(2027, 7, 8),
    pd.Timestamp('2028-09-15')
]

result = sum_date_objects(date_list)
print("Resulting date:", result)

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
type_error_str = """Argument '{}' at position {} must be of type '{}'."""