#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import datetime
import time

import os

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pandas_data_frames.data_frame_handler import find_date_key
from strings import information_output_formatters, string_handler
from time_handling.time_formatters import time_format_tweaker

# Create aliases #
#----------------#

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

find_substring_index = string_handler.find_substring_index

#%%

#------------------#
# Define functions #
#------------------#

def get_current_time(dtype="datetime", time_fmt_str=None):
    arg_names = get_current_time.__code__.co_varnames
        
    type_arg_pos = find_substring_index("dtype", 
                                        arg_names,
                                        advanced_search=False)
    
    if dtype not in current_time_type_options:
        arg_tuple_current_time = (arg_names[type_arg_pos], current_time_type_options)
        raise ValueError(format_string(choice_error_str, arg_tuple_current_time))
    
    else:
        current_datetime = current_datetime_dict.get(dtype)
    
    if dtype == "str" and time_fmt_str is not None:
        raise TypeError("Current time is already a string type.")
        
        current_datetime_str\
        = time_format_tweaker(current_datetime, time_fmt_str)
        return current_datetime_str    
    
    elif dtype == "str" and time_fmt_str is None:
        return current_datetime
    

def get_obj_operation_datetime(obj_list,
                               attr="modification", 
                               time_fmt_str=None):
    
    attr_options = list(struct_time_attr_dict.keys())
    arg_names = get_obj_operation_datetime.__code__.co_varnames
    
    attr_arg_pos = find_substring_index(arg_names,
                                        "attr", 
                                        advanced_search=False)
    
    if attr not in attr_options:
        arg_tuple_operation_datetime = (attr_arg_pos, attr_options)
        raise AttributeError(format_string(attribute_error_str, 
                                           arg_tuple_operation_datetime))
        
    if isinstance(obj_list, str):
        obj_list = [obj_list]
    
    obj_timestamp_arr = []
    
    for obj in obj_list:    
        structTime_attr_obj = struct_time_attr_dict.get(attr) 
        
        timestamp_str_attr_obj\
        = time_format_tweaker(structTime_attr_obj, time_fmt_str)
        
        info_list = [obj, timestamp_str_attr_obj]
        obj_timestamp_arr.append(info_list)
        
    obj_timestamp_arr = np.array(obj_timestamp_arr)
    return obj_timestamp_arr


def datetime_range_operator(df1, df2,
                            operator,
                            time_fmt_str=None,
                            return_str=False):
    
    # Quality control #
    #-----------------#
    
    # Main argument names and their position on the function's definition #    
    arg_names = datetime_range_operator.__code__.co_varnames
    
    df1_arg_pos\
    = find_substring_index(arg_names,
                           "df1",
                           advanced_search=False)
    
    df2_arg_pos\
    = find_substring_index(arg_names,
                           "df2",
                           advanced_search=False)
    
    operator_arg_pos\
    = find_substring_index(arg_names,
                           "operator", 
                           advanced_search=False)
    
    # Operator argument choice #    
    if operator not in dt_range_operators:
        arg_tuple_dt_range_op1 = (arg_names[operator_arg_pos], dt_range_operators)
        raise ValueError(format_string(choice_error_str, arg_tuple_dt_range_op1))
        
    # Right input argument types #
    if not isinstance(df1, pd.DataFrame):
        arg_tuple_dt_range_op2 = (arg_names[df1_arg_pos], df1_arg_pos,
                                  'pandas.DataFrame', 'pandas.Series')
        raise TypeError(format_string(type_error_str2, arg_tuple_dt_range_op2))
        
    if not isinstance(df2, pd.DataFrame)\
    and not isinstance(df2, pd.Series):
        arg_tuple_dt_range_op3 = (arg_names[df2_arg_pos], df2_arg_pos,
                                  'pandas.DataFrame', 'pandas.Series')
        raise TypeError(format_string(type_error_str2, arg_tuple_dt_range_op3))
        
        
    elif isinstance(df2, pd.Series):
        if not hasattr(df2, "name"):
            arg_tuple_dt_range_op4 = (arg_names[df2_arg_pos],
                                      'pandas.Series',
                                      arg_names[df2_arg_pos])
            raise AttributeError(format_string(non_existent_attr_error_str,
                                               arg_tuple_dt_range_op4))
            
    # Operations #
    #------------#
    
    std_date_colname = "Date"
    
    # Check whether both objects have a standard date and time (column) name #
    try:
        dt_colname = find_date_key(df1)
    except:
        print("Standard time column name not found on object "
              f"'{arg_names[df1_arg_pos]}. "
              "Setting default name 'Date' to column number 0.")
        
        df1_cols = list(df1.columns)
        df1_cols[0] = std_date_colname
        df1.columns = df1_cols
        
    try:
        dt_colname = find_date_key(df2)
    except:
        print("Standard time column name not found on object "
              f"'{arg_names[df2_arg_pos]}. "
              "Setting default name 'Date' to column number 0.")
        
        df2_cols = list(df2.columns)
        df2_cols[0] = std_date_colname
        df2.columns = df2_cols
        
    # Perform the merge #
    res_dts = pd.merge(df1, df2, how=operator)
    
    # Sort values by the time-column #
    try:
        res_dts = res_dts.sort_values(by=dt_colname)
    except:
        res_dts = res_dts.sort_values(by=std_date_colname)
    
    # Choose whether to customize times' format #
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

# Preformatted strings #
#----------------------#

# Error strings #
choice_error_str = """Wrong '{}' option. Options are {}."""
type_error_str1 = """Argument '{}' at position {} must be of type '{}'."""
type_error_str2 = """Argument '{}' at position {} must be of type '{}' or ´{}´."""

non_existent_attr_error_str = \
"""Argument '{}' is of type '{}' but it is unnamed. 
Please set a name using {}.name attribute."""

attribute_error_str = "Wrong attribute option at position {}. Options are {}. "

# Switch dictionaries #
#---------------------#

struct_time_attr_dict = {
    "creation"     : "time.gmtime(os.path.getctime(obj))",
    "modification" : "time.gmtime(os.path.getmtime(obj))",
    "access"       : "time.gmtime(os.path.getatime(obj))"
    }

current_datetime_dict = {
    "datetime"  : "datetime.datetime.now()",
    "str"       : "time.ctime()",
    "timestamp" : "pd.Timestamp.now()"
    }
