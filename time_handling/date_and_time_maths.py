#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Goal**

This module aims to perform basic mathematical operations regarding
Pandas, Numpy date and time objects.
"""

#----------------#
# Import modules #
#----------------#

import datetime
import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from strings.information_output_formatters import format_string, print_format_string
from strings.string_handler import find_substring_index
from time_handling.time_formatters import time2seconds, time_format_tweaker

#------------------#
# Define functions #
#------------------#

# Basic mathematical operations #
#-------------------------------#


# Time averaging #
#----------------#

# Adapted from https://stackoverflow.com/questions/12033905/using-python-to-create-an-average-out-of-a-list-of-times

def datetime_to_radians(x):
    # Radians are calculated using a 24-hour circle, not 12-hour, 
    # starting at north and moving clockwise.
    
    # If the given time is already a datetime.time() object,
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

def average_times_of_day(x):
    # input datetime.datetime array and output datetime.time value
    angles = [datetime_to_radians(y) for y in x]
    avg_angle = average_angle(angles)
    
    return radians_to_time_of_day(avg_angle)


# Natural year calculation #
#--------------------------#

def natural_year(dt_start, dt_end, time_fmt_str=None,
                 months_shift=0,
                 method="pandas",
                 print_str=False):
    
    # Quality control #
    #-----------------#
    
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
    #------------#
      
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
    
    # Convert the final natural date and time string to datetime object #
    tf_nat_ymd = f"{tf_nat_year}-{tf_nat_month}-{tf_nat_day}"
    dt_end_natural = time_format_tweaker(tf_nat_ymd, method="pandas")
    dt_start_natural = dt_end_natural + pd.Timedelta(days=1)
        
    # Choose between returning the results as strings or datetime objects #     
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

# Preformatted strings #
#----------------------#

# Error strings #
type_error_str = """Argument '{}' at position {} must be of type '{}'."""