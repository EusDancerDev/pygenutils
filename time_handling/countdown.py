#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:43:27 2024

@author: jonander
"""

# TODO: optimizatu dena <-> ChatGPT

#----------------#
# Import modules #
#----------------#

from datetime import timedelta as td
import time

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings.string_handler import find_substring_index
from pyutils.strings.information_output_formatters import print_format_string
from pyutils.time_handling.time_formatters import parse_time_string

#------------------#
# Define functions #
#------------------#

def return_time_string_parts(datetime_str, dt_fmt_str):
    
    """
    Returns relevant and mostrly operable parts of a string 
    identifiable with a time (day part may be included).
    """
    
    hour_formatter_index = find_substring_index(dt_fmt_str, "%d", return_match_index="hi")
    if hour_formatter_index != -1:
        try:
            days, time_str, time_fmt_str = (
                datetime_str[:hour_formatter_index],
                datetime_str[hour_formatter_index:].strip(),
                dt_fmt_str[hour_formatter_index:].strip()
                )
        except ValueError:
            raise ValueError("Non-numeric values encountered in the datetime string.")
        else:
            dt_obj = parse_time_string(time_str, time_fmt_str)
            return days, dt_obj
    else:
        days, time_str, time_fmt_str = (0, datetime_str, dt_fmt_str)
        time_obj = parse_time_string(time_str, time_fmt_str)
        return days, time_obj 
    

def _check_digit(datetime_str):
    return datetime_str.isdigit()

        
def __countdown(time_str, time_fmt_str):
    days, time_obj = return_time_string_parts(time_str, time_fmt_str)
    
    hours, minutes, seconds = time_obj.hour, time_obj.minute, time_obj.second
    while ((hours, minutes, seconds, days) != (0,0,0,0)):
        # Recalculate the time components
        hours, minutes, seconds = time_obj.hour, time_obj.minute, time_obj.second
        if days > 0:
            dt_args_day = [days, hours, minutes, seconds]
            print_format_string(time_str_parts_fmts[0], dt_args_day)
        else:            
            dt_args_noday = [hours, minutes, seconds]
            print_format_string(time_str_parts_fmts[1], dt_args_noday)
            
        # Subtract one second to the datetime object while simulating one second pass
        time.sleep(1)
        time_obj -= td(seconds=1)
        if ((hours, minutes, seconds) == (0,0,0)):
            days -= 1
        
    else:
        print("Time up!")

#-------------------------#
# Countdown functionality #
#-------------------------#

# Ask for the datetime input #
datetime_str = input("Introduce any time: ")    
is_str_digit = _check_digit(datetime_str)

if is_str_digit:
    print_str = input("Convertible time format detected. "
                      "Would you like to print the time in string format? [y/n] ")
else: 
    dt_fmt_str = input("String format detected. "
                       "Introduce the formatting string without quotes: ")

# Start the countdown #
try:
    __countdown(datetime_str, dt_fmt_str)
except KeyboardInterrupt:
    print("\nCountdown stopped.")
    
#--------------------------#
# Parameters and constants #
#--------------------------#

time_str_parts_fmts = ["{} days {}:{}:{}", "{}:{}:{}"]