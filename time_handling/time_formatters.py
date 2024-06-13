#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import datetime
import time

import inspect

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from strings import information_output_formatters, string_handler

# Create aliases #
#----------------#

format_string = information_output_formatters.format_string
find_substring_index = string_handler.find_substring_index
get_obj_type_str = information_output_formatters.get_obj_type_str
substring_replacer = string_handler.substring_replacer

#------------------#
# Define functions #
#------------------#

# TODO: proiektuaren atal nahikoa handia
#       ONDO BERRAZTERTU ETA AURREIKUSI (gehien gauzatzen ditudan eragiketen arabera) BERE NEURRIAN:
#       1. Zein sarrera mota nahi ditudan
#       2. Horietako bakoitza zer motatara bihurtu nahi ditudan
#       3. Kontsideratu, hala badagokio, data- edo denbora-zatiak erakustea
#       4. Erakuste formatoa zehaztu <-> 'output_format' aldagaia
#       5. Galdetu ChatGPT-ri, ONGI ATERAKO DA
#       6. Docstring-a
        
def time_format_tweaker(t,
                        time_fmt_str=None,
                        return_str=False,
                        return_days=False,
                        method="datetime",
                        standardize_hour_range=False):
    
    """
    Parameters
    ----------
    t: int, float, str or tuple, 
        time.struct_time or datetime.[datetime, date, time],
        array-like, pandas.Series or xarray.DataArray 
    In either case, the object containg the dates and times.
    
    method : {"numpy_generic", "numpy_dt64",
              "pandas", 
              "datetime", "model_datetime"}
    
        Method to use in order to give to the time (t) object.
    
        If "pandas" is selected, then the dates are treated as strings,
        so the function gives the date time format using 
        pd.to_datetime formatter.
    
        If "datetime", then the format is given using
        the built-in "datetime" module's datetime.strptime attribute.
    
        Lastly, the option "model_datetime" is designed in order
        to use again "datetime" module, 
        but creating a model (or generic) date and time where the year
        is 1, for example in model or calendar year calculations
        in climate change; that is to say the year is unimportant.         

    Returns
    -------
    t_res : str, tuple, datetime.datetime,
        array-like or pandas.[DatetimeIndex, DataFrame, Series]
    
    Array containg the reformatted date times.
    If the type of calendar used in the original time array
    is different of Gregorian, it converts to that one.
    Otherwise the calendar type remains as Gregorian, unchanged.
    """
    
    method_name = inspect.currentframe().f_code.co_name
    arg_names = time_format_tweaker.__code__.co_varnames
    
    print_arg_pos = find_substring_index(arg_names, "return_str")
    t_arg_pos = find_substring_index(arg_names, "t")
    method_arg_pos = find_substring_index(arg_names, "method")
    
    return_str_options = [False, "basic", "extended"]
    
    
    if return_str not in return_str_options:
        arg_tuple_tweaker1 = (arg_names[print_arg_pos], return_str_options)
        raise ValueError(format_string(value_error_str, arg_tuple_tweaker1))
        
    if method not in method_options:
        arg_tuple_tweaker2 = (arg_names[method_arg_pos], method_options)
        raise ValueError(format_string(value_error_str, arg_tuple_tweaker2))

    if isinstance(t, (float, int)):
        
        # This part assumes that the input 't' time is expressed in seconds #
        if t < 0:
            # If the seconds match the next day's midnight,
            # set the hour to zero instead of 24.
            hours = (t // 3600) % 24
        else:
            hours = t // 3600
            
        minutes = (t % 3600) // 60
        seconds = t % 60
        
        t_res = hours, minutes, seconds
    
        if return_days:
            days = hours // 24
            hours %= 24
            t_res = days, hours, minutes, seconds
            
        # Time printing cases #
        #---------------------#
            
        if return_str == "basic" and not return_days:
            
            if isinstance(t, float):
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)
                
            t_res_timetuple = datetime.time(hours, minutes, seconds)
            t_res = str(t_res_timetuple)
            
        elif return_str == "basic" and return_days:
            time_str_format_specCase\
            = f"{days:d}:{hours:.0f}:{minutes:.0f}:{seconds:.0f}"
            t_res = time_str_format_specCase
            
        elif return_str == "extended" and return_days:
            t_res = f"{days:.0f} days "\
                    f"{hours:.0f} hours "\
                    f"{minutes:.0f} minutes "\
                    f"{seconds:6.3f} seconds"
                    
        elif return_str == "extended" and not return_days:
            if hours != 0:
                t_res = f"{hours:.0f} hours "\
                        f"{minutes:.0f} minutes "\
                        f"{seconds:6.3f} seconds"
                
            else:
                if minutes != 0:
                    t_res = f"{minutes:.0f} minutes "\
                            f"{seconds:6.3f} seconds"
                  
                else:
                    t_res = f"{seconds:6.3f} seconds"
                    
                    
        return t_res
                    
    
    elif isinstance(t, str):

        if time_fmt_str is None:
            arg_tuple_tweaker3 = (arg_names[0], t_arg_pos, get_obj_type_str(t), method_name)
            raise ValueError(format_string(no_str_format_error_str, arg_tuple_tweaker3))

        particular_allowed_methods = ["pandas", "datetime", "model_datetime"]
        if method not in particular_allowed_methods:
            arg_tuple_tweaker4 = (arg_names[method_arg_pos],
                                  method,
                                  arg_names[t_arg_pos],
                                  get_obj_type_str(eval(arg_names[t_arg_pos])),
                                  particular_allowed_methods)
            
            raise ValueError(format_string(value_error_for_type_str, arg_tuple_tweaker4))
        
    
        if method == "model_datetime":
            t_res = frequent_time_format_converter(t,
                                                method="datetime",
                                                time_fmt_str=time_fmt_str)
            
            if ("%Y" not in time_fmt_str or "%y" not in time_fmt_str)\
                and "%m" not in time_fmt_str\
                and "%d" not in time_fmt_str:
                    
                t_res_aux = datetime.datetime(1, 1, 1,
                                              t_res.hour, t_res.minute, t_res.second)
                t_res = t_res_aux
                
            elif ("%Y" not in time_fmt_str or "%y" not in time_fmt_str)\
                  and "%m" not in time_fmt_str\
                  and "%d" in time_fmt_str:
    
                t_res_aux = datetime.datetime(1, 1, t_res.day, 
                                              t_res.hour, t_res.minute, t_res.second)
                t_res = t_res_aux
                
            elif ("%Y" not in time_fmt_str or "%y" not in time_fmt_str)\
                  and "%m" in time_fmt_str:
            
                t_res_aux = datetime.datetime(1, t_res.month, t_res.day, 
                                              t_res.hour, t_res.minute, t_res.second)
                t_res = t_res_aux
                
            return t_res
        
        else:
            t_res = frequent_time_format_converter(t, method, time_fmt_str)
            return t_res
                  
      
    elif (isinstance(t, tuple)) and\
        not(isinstance(t, tuple) and isinstance(t, time.struct_time)):
        
        if time_fmt_str is None:
            arg_tuple_tweaker5 = (arg_names[0], t_arg_pos, get_obj_type_str(t), method_name)
            raise ValueError(format_string(no_str_format_error_str, arg_tuple_tweaker5))
        else:
            t_res = datetime.datetime(*t).strftime(time_fmt_str) 
            
        if method == "pandas":    
            arg_tuple_tweaker6 = (arg_names[t_arg_pos], get_obj_type_str(t))
            raise Exception(format_string(non_satisfactory_dt_obj_error_str, arg_tuple_tweaker6))
            
        return t_res
        
    
    elif isinstance(t, tuple) and isinstance(t, time.struct_time):
        if time_fmt_str is None:
            arg_tuple_tweaker7 = (arg_names[0], t_arg_pos, get_obj_type_str(t), method_name)
            raise ValueError(format_string(no_str_format_error_str, arg_tuple_tweaker7))
        else:
            t_res = datetime.datetime(*t[:-3]).strftime(time_fmt_str)
            
        if method == "pandas":
            arg_tuple_tweaker8 = (arg_names[t_arg_pos], get_obj_type_str(t))
            raise Exception(format_string(non_satisfactory_dt_obj_error_str, arg_tuple_tweaker8))
            
        return t_res
        
        
    elif (isinstance(t, datetime.datetime)\
        or isinstance(t, datetime.date)\
        or isinstance(t, datetime.time))\
        and not isinstance(t, pd.Timestamp):
            
        if not return_days:
            method = "pandas"
            t_res = frequent_time_format_converter(t, method, time_fmt_str) 
        else:
            t_res = datetime.datetime.strftime(t, time_fmt_str)
        
        return t_res


    elif isinstance(t, pd.Timestamp):
        
        if not return_str:        
            particular_allowed_methods = ["numpy_generic", "numpy_dt64", "datetime_pydt"]
            
            if method not in particular_allowed_methods:  
                arg_tuple_tweaker9 = (arg_names[method_arg_pos],
                                      method,
                                      arg_names[t_arg_pos],
                                      get_obj_type_str(eval(arg_names[t_arg_pos])),
                                      particular_allowed_methods)
                
                raise ValueError(format_string(value_error_for_type_str, arg_tuple_tweaker9))
            
            else:
                t_res = frequent_time_format_converter(t, method)
                return t_res
        
        elif return_str == "extended":
            arg_tuple_tweaker10 = (arg_names[print_arg_pos],
                                   return_days,
                                   arg_names[t_arg_pos],
                                   get_obj_type_str(eval(arg_names[t_arg_pos])),
                                   particular_allowed_methods)

            raise ValueError(format_string(value_error_for_type_str, arg_tuple_tweaker10))
            
        elif return_str == "basic" :
            t_res = t.strftime(time_fmt_str)
            return t_res
        
    elif isinstance(t, np.datetime64):
        
        if method == "datetime_tolist":
            t_res = frequent_time_format_converter(t, method)
        if return_str:
            t_res = str(t)
        return t_res
    

    
    else:                
        if standardize_hour_range:
            try:
                t_res = over_24hour_fixer(t)
            except Exception:        
                arg_tuple_tweaker11 = (arg_names[t_arg_pos], get_obj_type_str(t))
                raise TypeError(format_string(unstandardizable_error_str, arg_tuple_tweaker11))
            else:
                return t_res
                
        else:   
            particular_allowed_methods = ["numpy_dt64_array", "pandas"]
            if method not in particular_allowed_methods:
                arg_tuple_tweaker12 = (arg_names[method_arg_pos],
                                       method,
                                       arg_names[t_arg_pos],
                                       get_obj_type_str(eval(arg_names[t_arg_pos])),
                                       particular_allowed_methods)
                
                raise ValueError(format_string(value_error_for_type_str,
                                               arg_tuple_tweaker12))
            
                t_res = frequent_time_format_converter(t, method, time_fmt_str)
                return t_res
            
            
            else:
                if isinstance(t, (pd.DataFrame, pd.Series)):
                    t_res = t.dt.strftime(time_fmt_str) 
                    if len(t_res) == 1:
                        return t_res[0]
                    else:
                        return t_res
                    
                elif isinstance(t_res, np.ndarray):
                    t_res = t.astype('U')
                    if len(t_res) == 1:
                        return t_res[0]
                    else:
                        return t_res
                else:
                    try:
                        t_res  = t.strftime(time_fmt_str)
                    except:
                        arg_tuple_tweaker13 = (arg_names[t_arg_pos, get_obj_type_str(t_res)])
                        raise Exception(format_string(unconverteable_pandas_dt_obj_error_str,
                                                      arg_tuple_tweaker13))
                    else:
                        return t_res
                            
            
    if return_str:
        if isinstance(t_res, pd.Series):
            t_res = t_res.dt.strftime(time_fmt_str) 
            return t_res
        if isinstance(t_res, pd.DataFrame):
            for col in t_res.columns:
                t_res.loc[:, col] = t_res.loc[:, col].dt.strftime(time_fmt_str)                
            return t_res
        elif isinstance(t_res, np.ndarray):
            t_res = t_res.astype('U')
            return t_res
        else:
            try:
                t_res  = t_res.strftime(time_fmt_str)
            except:
                arg_tuple_tweaker14 = (arg_names[t_arg_pos, get_obj_type_str(t_res)])
                raise Exception(format_string(unconverteable_pandas_dt_obj_error_str,
                                              arg_tuple_tweaker14))
            else:
                return t_res
                    
                
def frequent_time_format_converter(t,
                                   method=None,
                                   time_fmt_str=None):
    
    arg_names = frequent_time_format_converter.__code__.co_varnames
    method_arg_pos = find_substring_index(arg_names, "method")
    
    method_options = list(datetime_obj_dict.keys())
    if method not in method_options:
        arg_tuple_tweaker15 = (arg_names[method_arg_pos], method_options)
        raise ValueError(format_string(value_error_str, arg_tuple_tweaker15))
    
    else:
        if method == "pandas":
            try:
                dtobj = eval(datetime_obj_dict.get(method))                
            except:        
                import cftime as cft
                dtobj\
                = pd.to_datetime([cft.datetime.strftime(time_el, format=time_fmt_str)
                                  for time_el in t],
                                 format=time_fmt_str)
                      
        else:
            dtobj = eval(datetime_obj_dict.get(method))
            
        return dtobj
    
    
def over_24hour_fixer(time_obj):

    """
    Function that checks whether the range of hours
    contained in an object (numpy's or pandas's) is the 24-hour standard 0-23.
    
    For the task, the date and times in the input object 
    must only be of type string, otherwise it is not possible
    to define non standard hour ranges like 1-24
    with Timestamp-like attributes.
    
    Time 24:00 is assumed to mean the next day,
    so it is converted to string 23:00 and then 
    an hour time delta is added to it.
    
    Parameters
    ----------
    time_obj : array-like of strings, pandas.DataFrame or pandas.Series
        Object containing the date and times to be checked.
    
    Returns
    -------
    time_obj_fixed : array-like, pandas.DataFrame or pandas.Series
        Object containing fixed dates and times.
    """
   
    if isinstance(time_obj, np.ndarray):
        twentyFourHourIdx = find_substring_index(time_obj, "24:0")
        time_obj_no24Hour = substring_replacer(time_obj, "24:0", "23:0")
        
        time_obj_fixed = \
        frequent_time_format_converter(time_obj_no24Hour, method="numpy_dt64_array")
        time_obj_fixed[twentyFourHourIdx] += np.timedelta64(1, "s")
        
    elif isinstance(time_obj, (pd.DataFrame, pd.Series)):
        try:
            twentyFourHourIdx = time_obj.str.contains("24:0")
        except:
            twentyFourHourIdx = time_obj.iloc[:,0].str.contains("24:0")
            
        twentyFourHourIdxFilt = twentyFourHourIdx[twentyFourHourIdx]  
        time_obj_no24Hour = substring_replacer(time_obj, "24:0", "23:0")
            
        time_obj_fixed = \
        frequent_time_format_converter(time_obj_no24Hour, method="pandas")
        time_obj_fixed[twentyFourHourIdxFilt] += pd.Timedelta(hours=1)
        
    # TODO: ondokoa garatu
    # else:
    #     import xarray as xr
             
    return time_obj_fixed


def time2seconds(t, time_fmt_str=None):
    
    # TODO: proiektuaren atal nahikoa handia
    #       ONDO BERRAZTERTU ETA AURREIKUSI (gehien gauzatzen ditudan eragiketen arabera) BERE NEURRIAN:
    #       1. Allowed types: string, datetime.datetime, datetime.date, datetime.time
    #                         np.datetime64, pd.Timestamp and time.struct_time
    #       2. Horietako bakoitza, AHAL DELA 'time_format_tweaker' erabiliz,
    #          beti bihurtu 'timedelta' batera --> lehenetsi datetime.timedelta
    #          zeren azkarragoa eta memoria-erabilera txikiagokoa baita, 
    #          pd.Timedelta baino (izatez, ondoko hau datetime-ren gainean dago eraikita).
    #       3. Irteera-formatoa: BETI FLOAT, '.total_seconds()' ezaugarria 
    #          deituko baita, non emaitza segundoak besterik ez diren.
    #       4. Galdetu ChatGPT-ri, ONGI ATERAKO DA
    #       5. Docstring-a

    
    # TODO: Convert the input object to datetime.timedelta object #

    
    method_name = inspect.currentframe().f_code.co_name
    
    if isinstance(t, str):
        t_datetime_tuple = time_format_tweaker(t, time_fmt_str)
        
        days = t_datetime_tuple.day
        hours = t_datetime_tuple.hour
        minutes = t_datetime_tuple.minute
        seconds = t_datetime_tuple.second        
        t_secs = days*86400 + hours*3600 + minutes*60 + seconds
        return(t_secs)
        
    elif isinstance(t, tuple):
        
        lt = len(t)        
        if lt == 4:
            days = t[0]
            hours = t[1]
            minutes = t[2]
            seconds = t[3]            
            t_secs = days*86400 + hours*3600 + minutes*60 + seconds
            
        elif lt == 3:
            hours = t[0]
            minutes = t[1]
            seconds = t[2]            
            t_secs = hours*3600 + minutes*60 + seconds
            
        else:
            raise ValueError(f"Method '{method_name}' does neither accept "
                              "years nor months. "
                              "Time tuple structure must be the following:\n"
                              "([days,] hours, minutes, seconds)")
            
        return(t_secs)
    

#--------------------------#
# Parameters and constants #
#--------------------------#

# Global method options #
method_options = ["datetime", "datetime_tolist", "datetime_pydt", "model_datetime",
                  "pandas", 
                  "numpy_dt64", "numpy_dt64_array", "numpy_generic"]

# Extension list #
extensions = ["csv", "xlsx", "nc"]

# Preformatted strings #
#----------------------#

# Error strings #
no_str_format_error_str = \
"""For argument '{}' (position {}) of type '{}', 
'{}' method is designed to output a time string.
Please provide a time string format identifier.
"""

value_error_str = """Unsupported '{}' option. Options are {}."""
value_error_for_type_str = """'{}'=='{}' not allowed for argument '{}' of type '{}'.
Options are {}."""

non_satisfactory_dt_obj_error_str = \
"""Argument '{}' of type '{}' will not give a satisfactory \
pandas's timestamp containing object."""

unstandardizable_error_str = \
"""Cannot handle hour range standardization with Argument '{}' of type '{}'."""

unconverteable_pandas_dt_obj_error_str = \
"""Cannot convert Argument '{}' of type '{}' to pandas's timestamp containing object."""

# Switch dictionaries #
#---------------------#

datetime_obj_dict = {
    "datetime" : "datetime.datetime.strptime(t, time_fmt_str)",
    "datetime_tolist" : "t.tolist()",
    "datetime_pydt" : "t.to_pydatetime()",
    "numpy_dt64" : "t.to_datetime64()",
    "numpy_dt64_array" : "np.array(t, dtype=np.datetime64)",
    "numpy_generic" : "t.to_numpy()",
    "pandas" : "pd.to_datetime(t, format=time_fmt_str)"
    }
