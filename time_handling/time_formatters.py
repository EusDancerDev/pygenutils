#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import datetime
import time

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pytools.arrays_and_lists.array_data_manipulation import select_array_elements,\
                                                             remove_elements_from_array
from pytools.strings.information_output_formatters import format_string
from pytools.strings.string_handler import find_substring_index
from pytools.utilities.introspection_utils import get_obj_type_str,\
                                                  get_caller_method_args, \
                                                  retrieve_function_name

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
                        module="datetime",
                        standardize_hour_range=False):
    
    """
    Parameters
    ----------
    t: int, float, str or tuple, 
        time.struct_time or datetime.[datetime, date, time],
        array-like, pandas.Series or xarray.DataArray 
    In either case, the object containg the dates and times.
    
    module : {"numpy_generic", "numpy_dt64",
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
    
    module_name = retrieve_function_name()
    all_arg_names = get_caller_method_args()
    
    print_arg_pos = find_substring_index(all_arg_names, "return_str")
    t_arg_pos = find_substring_index(all_arg_names, "t")
    module_arg_pos = find_substring_index(all_arg_names, "module")
    
    return_str_options = [False, "basic", "extended"]
    
    
    if return_str not in return_str_options:
        arg_tuple_tweaker1 = (all_arg_names[print_arg_pos], return_str_options)
        raise ValueError(format_string(value_error_str, arg_tuple_tweaker1))
        
    if module not in supported_modules:
        arg_tuple_tweaker2 = (all_arg_names[module_arg_pos], supported_modules)
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
            arg_tuple_tweaker3 = (all_arg_names[0], t_arg_pos, get_obj_type_str(t), module_name)
            raise ValueError(format_string(no_str_format_error_str, arg_tuple_tweaker3))

        particular_allowed_modules = select_array_elements(supported_modules, [0,3,4])
        if module not in particular_allowed_modules:
            arg_tuple_tweaker4 = (all_arg_names[module_arg_pos],
                                  module,
                                  all_arg_names[t_arg_pos],
                                  get_obj_type_str(all_arg_names[t_arg_pos]),
                                  particular_allowed_modules)
            
            raise ValueError(format_string(value_error_for_type_str, arg_tuple_tweaker4))
        
    
        if module == "model_datetime":
            t_res = datetime_object_type_converter(t,
                                                   module="datetime",
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
            t_res = datetime_object_type_converter(t, module, time_fmt_str)
            return t_res
                  
      
    elif (isinstance(t, tuple)) and\
        not(isinstance(t, tuple) and isinstance(t, time.struct_time)):
        
        if time_fmt_str is None:
            arg_tuple_tweaker5 = (all_arg_names[0], t_arg_pos, get_obj_type_str(t), module_name)
            raise ValueError(format_string(no_str_format_error_str, arg_tuple_tweaker5))
        else:
            t_res = datetime.datetime(*t).strftime(time_fmt_str) 
            
        if module == "pandas":    
            arg_tuple_tweaker6 = (all_arg_names[t_arg_pos], get_obj_type_str(t))
            raise Exception(format_string(non_satisfactory_dt_obj_error_str, arg_tuple_tweaker6))
            
        return t_res
        
    
    elif isinstance(t, tuple) and isinstance(t, time.struct_time):
        if time_fmt_str is None:
            arg_tuple_tweaker7 = (all_arg_names[0], t_arg_pos, get_obj_type_str(t), module_name)
            raise ValueError(format_string(no_str_format_error_str, arg_tuple_tweaker7))
        else:
            t_res = datetime.datetime(*t[:-3]).strftime(time_fmt_str)
            
        if module == "pandas":
            arg_tuple_tweaker8 = (all_arg_names[t_arg_pos], get_obj_type_str(t))
            raise Exception(format_string(non_satisfactory_dt_obj_error_str, arg_tuple_tweaker8))
            
        return t_res
        
        
    elif (isinstance(t, datetime.datetime)\
        or isinstance(t, datetime.date)\
        or isinstance(t, datetime.time))\
        and not isinstance(t, pd.Timestamp):
            
        if not return_days:
            module = "pandas"
            t_res = datetime_object_type_converter(t, module, time_fmt_str) 
        else:
            t_res = datetime.datetime.strftime(t, time_fmt_str)
        
        return t_res


    elif isinstance(t, pd.Timestamp):
        
        if not return_str:        
            particular_allowed_modules = select_array_elements(supported_modules, [2, -3, -1])
            if module not in particular_allowed_modules:  
                arg_tuple_tweaker9 = (all_arg_names[module_arg_pos],
                                      module,
                                      all_arg_names[t_arg_pos],
                                      get_obj_type_str(all_arg_names[t_arg_pos]),
                                      particular_allowed_modules)
                
                raise ValueError(format_string(value_error_for_type_str, arg_tuple_tweaker9))
            
            else:
                t_res = datetime_object_type_converter(t, module)
                return t_res
        
        elif return_str == "extended":
            arg_tuple_tweaker10 = (all_arg_names[print_arg_pos],
                                   return_days,
                                   all_arg_names[t_arg_pos],
                                   get_obj_type_str(all_arg_names[t_arg_pos]),
                                   particular_allowed_modules)

            raise ValueError(format_string(value_error_for_type_str, arg_tuple_tweaker10))
            
        elif return_str == "basic" :
            t_res = t.strftime(time_fmt_str)
            return t_res
        
    elif isinstance(t, np.datetime64):
        
        if module == "datetime_tolist":
            t_res = datetime_object_type_converter(t, module)
        if return_str:
            t_res = str(t)
        return t_res
    

    
    else:                
        if standardize_hour_range:
            try:
                t_res = hour_range_standardizer(t)
            except Exception:        
                arg_tuple_tweaker11 = (all_arg_names[t_arg_pos], get_obj_type_str(t))
                raise TypeError(format_string(unstandardizable_error_str, arg_tuple_tweaker11))
            else:
                return t_res
                
        else:   
            particular_allowed_modules = select_array_elements(supported_modules, [4, -2])
            if module not in particular_allowed_modules:
                arg_tuple_tweaker12 = (all_arg_names[module_arg_pos],
                                       module,
                                       all_arg_names[t_arg_pos],
                                       get_obj_type_str(all_arg_names[t_arg_pos]),
                                       particular_allowed_modules)
                
                raise ValueError(format_string(value_error_for_type_str,
                                               arg_tuple_tweaker12))
            
                t_res = datetime_object_type_converter(t, module, time_fmt_str)
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
                        arg_tuple_tweaker13 = (all_arg_names[t_arg_pos, get_obj_type_str(t_res)])
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
                arg_tuple_tweaker14 = (all_arg_names[t_arg_pos, get_obj_type_str(t_res)])
                raise Exception(format_string(unconverteable_pandas_dt_obj_error_str,
                                              arg_tuple_tweaker14))
            else:
                return t_res
                    
                
def datetime_object_type_converter(time_obj, module=None, time_fmt_str=None):
    """
    Convert datetime objects between different types using specified modules.
    
    Parameters
    ----------
    time_obj : datetime.datetime or list-like
        The datetime object(s) or list of datetime objects to convert.
    module : {'datetime', 'datetime_tolist', 'datetime_pydt', 'pandas',
              'numpy_dt64', 'numpy_dt64_array', 'numpy_generic'}, optional
        Module name specifying the type of conversion.
    time_fmt_str : str, optional
        Format string specifying the format of datetime objects. Required
        only for certain conversions.
        
    Returns
    -------
    converted_obj : object
        Converted datetime object or array based on the specified module.
        
    Raises
    ------
    ValueError
        If an unsupported module option is provided.
    """
    
    # Get all argument names of the caller method
    all_arg_names = get_caller_method_args()
    module_arg_pos = find_substring_index(all_arg_names, "module")
    arg_tuple_tweaker15 = (all_arg_names[module_arg_pos], supported_modules_switch_case)
    
    # Validate 'module' argument
    if module not in supported_modules_switch_case:
        raise ValueError(format_string(value_error_str, arg_tuple_tweaker15))
    
    # Get the function or lambda from the dictionary using getattr
    func_or_lambda = datetime_obj_dict.get(module)
    
    if func_or_lambda is None:
        raise ValueError(format_string(value_error_str, arg_tuple_tweaker15))
    
    # Perform conversion based on the selected module
    if callable(func_or_lambda):
        # Handle callable lambdas directly
        if module == "datetime":
            dtobj = func_or_lambda(time_obj, time_fmt_str)
        else:
            dtobj = func_or_lambda(time_obj)
    elif isinstance(func_or_lambda, str):
        # Handle string functions (e.g., for pandas)
        dtobj = eval(func_or_lambda)
    else:
        # Handle unsupported options (though ideally this should not occur)
        raise ValueError(format_string(value_error_str, arg_tuple_tweaker15))
    
    return dtobj
    


def hour_range_standardizer(time_obj):
    """
    Function that checks whether the range of hours contained in an object 
    (numpy, pandas, or xarray) is the 24-hour standard 0-23. Converts hours in 
    the range 1-24 to 0-23.

    For the task, the date and times in the input object must only be of type 
    string, otherwise it is not possible to define non-standard hour ranges 
    like 1-24 with Timestamp-like attributes.

    Time 24:00 is assumed to mean the next day, so it is converted to string 
    23:00 and then an hour time delta is added to it.

    Parameters
    ----------
    time_obj : array-like of strings, pandas.DataFrame, pandas.Series,
               xarray.Dataset, or xarray.DataArray
        Object containing the date and times to be checked.

    Returns
    -------
    time_obj_fixed : array-like of strings, pandas.DataFrame, pandas.Series,
                     xarray.Dataset, or xarray.DataArray
        Object containing fixed dates and times.
    """
    
    # Define anidated functions for easier manipulations #
    #----------------------------------------------------#
    
    def fix_24_hour_format(time_series):
        twenty_four_hour_idx = time_series.str.contains("24:0")
        time_series_no24hour = time_series.str.replace("24:0", "23:0", regex=False)
        time_series_fixed = pd.to_datetime(time_series_no24hour, format="%H:%M")
        time_series_fixed[twenty_four_hour_idx] += pd.Timedelta(hours=1)
        return time_series_fixed

    # Operations depending on the type of the input object #
    #------------------------------------------------------#

    if isinstance(time_obj, np.ndarray):
        time_series = pd.Series(time_obj)
        time_obj_fixed = fix_24_hour_format(time_series).to_numpy()

    elif isinstance(time_obj, pd.DataFrame):
        time_obj_fixed = time_obj.apply(lambda col: fix_24_hour_format(col) if col.dtype == 'O' else col)

    elif isinstance(time_obj, pd.Series):
        time_obj_fixed = fix_24_hour_format(time_obj)

    elif (get_obj_type_str(time_obj) == "Dataset"
          or get_obj_type_str(time_obj) == "DataArray"):
        
        time_obj_fixed = time_obj.copy()
        time_series = time_obj_fixed.to_series().reset_index(drop=True)
        time_series_fixed = fix_24_hour_format(time_series)
        time_obj_fixed.values = time_series_fixed.values.reshape(time_obj_fixed.shape)
    
    else:
        raise TypeError("Unsupported object type. Supported types are "
                        "array-like of strings, pandas.DataFrame, pandas.Series, "
                        "xarray.Dataset, or xarray.DataArray.")
    
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
   
    method_name = retrieve_function_name()
    
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

# Supported module options #
supported_modules = ["datetime", "datetime_tolist", "datetime_pydt", "model_datetime",
                     "pandas", 
                     "numpy_dt64", "numpy_dt64_array", "numpy_generic"]

supported_modules_switch_case = remove_elements_from_array(supported_modules, 3)

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
    supported_modules_switch_case[0] : lambda t, time_fmt_str: datetime.datetime.strptime(t, time_fmt_str),
    supported_modules_switch_case[1] : lambda t: t.tolist(),
    supported_modules_switch_case[2] : lambda t: t.to_pydatetime(),
    supported_modules_switch_case[3] : "pd.to_datetime(time_obj, format=time_fmt_str)",
    supported_modules_switch_case[4] : np.datetime64,
    supported_modules_switch_case[5] : lambda t: np.array(t, dtype=np.datetime64),
    supported_modules_switch_case[6] : np.asarray,
}