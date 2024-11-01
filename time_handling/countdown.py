#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from datetime import timedelta as td
from time import sleep

#-----------------------#
# Import custom modules #
#-----------------------#

from pygenutils.strings.information_output_formatters import print_format_string
from pygenutils.time_handling.time_formatters import parse_time_string

#------------------#
# Define functions #
#------------------#

def return_time_string_parts(datetime_str, dt_fmt_str):
    
    """
    Parses a time string and returns the day component (if any) and a datetime object.

    Parameters
    ----------
    datetime_str : str
        The time string that needs to be parsed (e.g., "01:12:38").
        
    dt_fmt_str : str
        The format string that identifies the components in the time string 
        (e.g., '%d %H:%M:%S' for days, hours, minutes, and seconds).

    Returns
    -------
    tuple
        A tuple containing the day part (int) and a datetime object with the time components.
        If no day part is identified, the default value for days is 0.
    
    Raises:
    ------
    ValueError
        If non-numeric values are encountered in the datetime string when days are expected.
    """
    
    day_index = dt_fmt_str.find("%d")
    if day_index != -1:
        try:
            days, time_str, dt_fmt_str = (
                int(datetime_str[:day_index]),
                datetime_str[day_index:].strip(),
                dt_fmt_str[day_index:].strip()
                )
        except ValueError:
            raise ValueError("Non-numeric values encountered in the datetime string.")
        else:
            dt_obj = parse_time_string(time_str, dt_fmt_str, end="\r")
            return days, dt_obj
    else:
        dt_obj = parse_time_string(datetime_str, dt_fmt_str, end="\r")
        return 0, dt_obj # No days component, default to 0.

        
def __countdown(time_str, dt_fmt_str):
    """
    Runs a countdown from the provided time until it reaches zero,
    updating every second.

    Parameters
    ----------
    time_str : str
        The time string to countdown from (e.g., "01:12:38").
    
    time_fmt_str : str
        The format string identifying the time components in the time string 
        (e.g., '%d %H:%M:%S' or '%H:%M:%S').

    Functionality
    -------------
    - Displays the remaining time in the format "D days H hours M mins S secs".
    - Updates every second using `time.sleep(1)`.
    - Decrements the time until it reaches zero, at which point it prints "Time up!".
    
    Raises:
    ------
    KeyboardInterrupt
        If the user manually interrupts the countdown (Ctrl+C).
    """
    days, dt_obj = return_time_string_parts(time_str, dt_fmt_str)
    while days > 0 or (dt_obj.hour, dt_obj.minute, dt_obj.second) != (0, 0, 0):
        # Calculate the time components
        hours, minutes, seconds = dt_obj.hour, dt_obj.minute, dt_obj.second
        if days > 0:
            dt_args_day = [days, hours, minutes, seconds]
            print_format_string(time_str_parts_fmts[0], dt_args_day)
        else:            
            dt_args_noday = [hours, minutes, seconds]
            print_format_string(time_str_parts_fmts[1], dt_args_noday)
            
        # Simulate time passing
        sleep(1)
        
        # Decrement time by one second
        dt_obj -= td(seconds=1)
        
        # Check if time is up, then decrement days if necessary
        if ((hours, minutes, seconds) == (0,0,0) and days > 0):
            days -= 1
        
    print("Time up!")

#-------------------------#
# Countdown functionality #
#-------------------------#

# Ask for the datetime input #
datetime_str = input("Introduce any time: ")
dt_fmt_str = input("Introduce the formatting string without quotes: ")

# Start the countdown #
try:
    __countdown(datetime_str, dt_fmt_str)
except KeyboardInterrupt:
    print("\nCountdown stopped.")
    
#--------------------------#
# Parameters and constants #
#--------------------------#

time_str_parts_fmts = ["{} days {}:{}:{}", "{}:{}:{}"]
