#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import datetime
import time

import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings.string_handler import substring_replacer
from pyutils.time_handling.time_formatters import time_format_tweaker

#------------------#
# Define functions #
#------------------#

# TODO: 'time_format_tweaker' optimizatutakoan, berrikusi hura deitzeko sintaxia

def countdown(t, time_fmt_str=None, print_str=False):
    
    if isinstance(t, str):
        time_dt = time_format_tweaker(t, time_fmt_str=time_fmt_str)
      
        if "%Y" not in time_fmt_str:
            time_dt = time_format_tweaker(t, method="model_datetime",
                                          time_fmt_str=time_fmt_str)
        
        for s2find_1, s2replace_1 in zip(string_arr1[:,0], string_arr1[:,1]):
            time_fmt_str = substring_replacer(time_fmt_str, 
                                              s2find_1, 
                                              s2replace_1)
                    
            zero_pad_ans = input("Would you like to include zero padding? [y/n] ")
            while (zero_pad_ans != "y" and zero_pad_ans != "n"):
                zero_pad_ans = input("Please write 'y' for 'yes' or 'n' for 'no' ")
            
            else:
                if zero_pad_ans == "n":
                    for s2find_2, s2replace_2 in zip(string_arr2[:,0], 
                                                     string_arr2[:,1]):
                        
                        time_fmt_str = substring_replacer(time_fmt_str, 
                                                          s2find_2,
                                                          s2replace_2)
                        
                
                while (t):
                    try:
                        time_str = time_dt.strftime(time_fmt_str)  
                        time_dt -= datetime.timedelta(seconds=1)  
                    except OverflowError:
                        raise OverflowError(  )
                    else:
                        print(time_str, end="\r")
                        time.sleep(1)
                        
              
    elif isinstance(t, int):
        t_secs = time_format_tweaker(t)
        
        while (t_secs):
            time_str = time_format_tweaker(t_secs, print_str=True)
            print(time_str, end="\r")
            
            time.sleep(1)
            t_secs -= 1
	
        else:
            print("Time up!")

#--------------------------#
# Parameters and constants #
#--------------------------#

string_arr1 = np.array([["%d", "%d-1"],
                        ["%m", "%m-1"],
                        ["%Y", "%Y-1"],
                        ["%y", "%y-1"]])

string_arr2 = np.array([["%d", "%-d"],
                        ["%m", "%-m"],
                        ["%Y", "%-Y"],
                        ["%y", "%-y"]])

#---------------#
# Function gear #
#---------------#

t = input("Introduce any time: ")

if t.isdigit():
    print_str = input("Convertible time format detected. "
                      "Would you like to print the time in string format? [y/n] ")
    
    while (print_str != "y" and print_str != "n"):
        print_str = input("Please write 'y' for 'yes' or 'n' for 'no' ")
    else: 
        try:            
            countdown(t, print_str=print_str)    
        except KeyboardInterrupt:
            print("\nCountdown stopped.")
            
else:
    time_fmt_str = input("String format detected. "
                         "Introduce the formatting string without quotes: ")
    try:
        countdown(t, time_fmt_str=time_fmt_str)
    except OverflowError:
        print("Time up!")
    except KeyboardInterrupt:
        print("\nCountdown stopped.")
