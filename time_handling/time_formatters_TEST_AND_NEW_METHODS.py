#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:46:58 2024

@author: jonander

**Note**

This script is for test purposes as we add and restructure functionalities in
'time_formatters' module.
In this course, new modules may be added in order to maintain the subpackage 'time_handling'
structured of different actions and purposes.
"""

import arrow
from datetime import datetime, timedelta
from dateutil import parser
import time

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import pandas_date_unit_list, numpy_date_unit_list
from pyutils.strings.information_output_formatters import format_string
from pyutils.time_handling.date_and_time_operators import parse_floated_nanotime
from pyutils.utilities.general.introspection_utils import get_obj_type_str

# %% 

# Input validation streamliners #
#-------------------------------# 

def validate_conversion(option, explanation, allowed_modules):
    if option not in allowed_options:
        raise ValueError(f"{Explanation} '{option}' not supported for this operation. "
                         f"Choose one from {allowed_options}.")

def validate_precision(frac_precision, option, min_prec=0, max_prec=9):
    if ((frac_precision is not None) and not (min_prec <= frac_precision <= max_prec)):
        raise ValueError(f"Fractional precision must be between {min_prec} and {max_prec}.")
    if ((7 <= frac_precision <= max_prec) and option != "pandas"):
        raise ValueError(f"Only option 'pandas' supports precision={frac_precision}.")
        
def validate_date_unit(date_unit, module):
    """
    Validates the date unit based on the module.

    Parameters
    ----------
    date_unit : str
        Time unit for the floated time. 
        Only applicable if the module is 'numpy' or 'pandas'.
    module : {"pandas", "numpy"}
        The module used for parsing the floated time.

    Raises
    ------
    ValueError
        If `date_unit` is not supported for the specified `module`.
    """
    
    # Define allowed date units for each module
    if module == "pandas" and date_unit not in pandas_date_unit_list:
        raise ValueError(f"Unsupported date unit for pandas.Timestamp objects. Choose one from {pandas_date_unit_list}.")
        
    if module == "numpy" and date_unit not in numpy_date_unit_list:
        raise ValueError(f"Unsupported date unit for numpy.datetime64 objects. Choose one from {numpy_date_unit_list}.")


# %% FROM SIMPLE DATA TO DATE/TIME OBJECTS

# Simple data to date/time objects #
#----------------------------------#

# Input format: str #
#-#-#-#-#-#-#-#-#-#-#

def parse_time_string(datetime_str, dt_fmt_str, module="datetime", date_unit="ns"):
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
    date_unit : str, optional
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
    validate_conversion(module, "Module", allowed_modules)
    
    # Formatting string #
    if not dt_fmt_str:
        raise ValueError("A datetime format string must be provided.")
        
    # Time string parsing #
    #######################
    
    try:
        parse_func = time_str_parsing_dict.get(module)
        datetime_obj = parse_func(datetime_str, dt_fmt_str, date_unit) \
                       if module == "pandas"\
                       else parse_func(datetime_str, dt_fmt_str)
    except ValueError:
        raise ValueError("The time string does not match the format string provided.")
    else:
        return datetime_obj
    
# %% 

# Input format: int, float #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def parse_float_time(datetime_float, 
                     frac_precision=None,
                     origin="unix", 
                     date_unit="us", 
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
    date_unit : str, optional
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
    validate_conversion(module, "Object type conversion", allowed_modules)
    
    # Time formatting string #
    if module != "str" and not dt_fmt_str:
        raise ValueError("You must provide a formatting string.")

    # Fractional second precision #
    validate_precision(frac_precision, option)

    # Date unit #
    validate_date_unit(date_unit, module)

    # Floated time parsing #
    ########################

    if module == "str":
        return parse_float_to_string(datetime_seconds,
                                     frac_precision, 
                                     origin,
                                     dt_fmt_str,
                                     date_unit,
                                     module)
    else:
        return float_time_parser(datetime_float, module, date_unit)
    
    
# Auxiliary methods #
def parse_float_to_string(floated_time, 
                          frac_precision, 
                          origin, 
                          dt_fmt_str, 
                          date_unit,
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
    date_unit : str, optional
        Time unit for `floated_time` if `origin='unix'` and `module` in {'numpy', 'pandas'}.
    module : {"datetime", "time", "pandas", "numpy", "arrow"}
        Module used for parsing.

    Returns
    -------
    str
        The formatted string representation of the floated time.
    """
    
    if origin == "arbitrary":
        return format_arbitrary_time(floated_time)
       
    elif origin == "unix":
        # Accommodation of the fractional second #
        if frac_precision is not None:
            if frac_precision <= 6:
                dt_seconds = round(floated_time)
                dt_obj = float_time_parser(dt_seconds, module, date_unit)
                dt_str = datetime.strftime(dt_fmt_str)
            elif 7 <= frac_precision <= max_prec:
                return parse_floated_nanotime(floated_time, module)
        # Keep the original precision #
        else:
            dt_str = float_time_parser(floated_time, module, date_unit).strftime(dt_fmt_str)
    
        return dt_str  

    
def float_time_parser(floated_time, module, date_unit):
    """
    Parses a floated time into a date/time object.
    
    Parameters
    ----------
    floated_time : int or float
        Time representing a time unit relative to an origin.
    module : {"datetime", "time", "pandas", "numpy", "arrow"}
        Module used for parsing.
    date_unit : str, optional
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
    validate_conversion(module, "Object type conversion", allowed_modules)

    # Date unit #
    validate_date_unit(date_unit, module)
    
    # Calculate datetime object #
    #############################
    
    datetime_obj = floated_time_parsing_dict.get(module)(floated_time, date_unit)
    return datetime_obj


def format_arbitrary_time(floated_time):
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
            time_parts_string = format_string(time_str_parts_fmts[0], time_tuple)
        else:
            time_tuple = (hours, minutes, seconds)
            time_parts_string = format_string(time_str_parts_fmts[1], time_tuple)
    except (IndexError, KeyError, ValueError) as e:
        raise ValueError(f"Invalid format string or time components: {e}")
    return time_parts_string 
        

# %% DATU KONPLEXUAK, BERRIRO, KONPLEXUAK: DENBORA-OBJEKTU EZBERDINEN ARTEKO BIHURKETA
#   DATU SINPLEEKIN EGINDA DAGO DENA


# INPUT FORMAT: np.datetime64, pd.Timestamp, pd.Series, pd.DataFrame, datetime.dt, time.struct_time, arrow
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

# !!! !!! !!! Eragiketa nahikotxo funtzioen artean amankomunekoak dira!!!!!!!!!

datetime_obj = "12345678.6789"
obj_convert_to = "pandas"

float_class_set = {np.float16, "f", "d", np.float128} # 'f' and 'd' denote np.float32 and np.float64, respectively
float_class = float_class_set[-1]


def datetime_obj_converter(datetime_obj, module, date_unit="ns"):
    """
    Convert a date/time object to another, float included.
    If float, it is assumed that they represent seconds relative to
    the Unix epoch start.
    """
    pass

# TODO: eragiketa nagusi askok barne-eragiketa bera gauzatzen dute

obj_type = get_obj_type_str(datetime_obj).lower()
if obj_type == "datetime":
    """
    Allowed types to convert to:
    {float, pd.Timestamp, np.datetime64, time.struct_time, arrow}
    ===
    {float, pandas, numpy, time, arrow}
    
    
    Note
    ----
    When converting datetime.dt objects to np.datetime64 ones,
    A DeprecationWarning is triggered because np.datetime64
    doesn't handle time zone-aware datetime objects well,
    and time zone information will be deprecated in future versions. 
    Removing the tzinfo is the way to go:
        
    datetime_obj.replace(tzinfo=None)
    """
    
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "pandas", "numpy", "time", "arrow"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    
    # TODO: aurrena if-elif baldintzazko bloke handiak -> ondoren switch case hiztegia
    # TODO: 'obj_convert_to' EDO 'convert_to'???
    if obj_convert_to == "float":
        result_datetime_obj = datetime_obj.timestamp()
    elif obj_convert_to == "pandas":
        result_datetime_obj = pd.to_datetime(datetime_obj, unit=date_unit)
    elif obj_convert_to == "numpy":
        datetime_obj_no_tzinfo = tzinfo_remover(datetime_obj)
        result_datetime_obj = np.datetime64(datetime_obj_no_tzinfo, unit=date_unit)
    elif obj_convert_to == "time":
        result_datetime_obj = datetime_obj.timetuple()
    elif obj_convert_to == "arrow":
        result_datetime_obj = arrow.get(datetime_obj)
    
elif obj_type == "datetime64":
    """
    Allowed types to convert to:
    {float, datetime.datetime, time.struct_time, pd.Timestamp, arrow}
    ===
    {float, datetime, time, pandas, arrow}
    
    Note
    ----

    """
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "datetime", "time", "pandas", "arrow"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    if obj_convert_to == "float":
        result_datetime_obj = datetime_obj.astype(f"timedelta64[{date_unit}]").astype(float_class)
    elif obj_convert_to == "datetime":
        result_datetime_obj = datetime_obj.astype(datetime) # TODO: GOGORATU from datetime import datetime !!!!!
    elif obj_convert_to == "time":
        result_datetime_obj = datetime_obj.astype(datetime).timetuple()
    elif obj_convert_to == "pandas":
        result_datetime_obj = pd.to_datetime(datetime_obj, unit=date_unit)
    elif obj_convert_to == "arrow":
        result_datetime_obj = arrow.get(datetime_obj.astype(datetime))


elif obj_type == "timestamp":
    """
    Allowed types to convert to:
    {float, datetime.datetime, time.struct_time, np.datetime64, arrow}
    ===
    {float, datetime, time, numpy, arrow}
    
    Note
    ----

    """
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "datetime", "time", "numpy", "arrow"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    if obj_convert_to == "float":
        result_datetime_obj = datetime_obj.to_pydatetime().timestamp()
    elif obj_convert_to == "datetime":
        result_datetime_obj = datetime_obj.to_pydatetime()
    elif obj_convert_to == "time":
        result_datetime_obj = datetime_obj.to_pydatetime().timetuple()
    elif obj_convert_to == "numpy":
        result_datetime_obj = datetime_obj.to_numpy()
    elif obj_convert_to == "arrow":
        result_datetime_obj = arrow.get(datetime_obj.to_pydatetime())

elif obj_type == "arrow":
    """
    Allowed types to convert to:
    {float, datetime.datetime, time.struct_time, pd.Timestamp, np.datetime64}
    ===
    {float, datetime, time, pandas, numpy}
    
    Note
    ----

    """
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "datetime", "time", "pandas", "numpy"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    if obj_convert_to == "float":
        result_datetime_obj = datetime_obj.float_timestamp
    elif obj_convert_to == "datetime":
        result_datetime_obj = datetime.fromtimestamp(datetime_obj.float_timestamp)
    elif obj_convert_to == "time":
        result_datetime_obj =  datetime_obj.timetuple()
    elif obj_convert_to == "pandas":
        pd.Timestamp(*datetime_obj.timetuple()[:6])
    elif obj_convert_to == "numpy":
        datetime_obj_no_tzinfo = tzinfo_remover(datetime_obj)
        result_datetime_obj = np.datetime64(datetime_obj_no_tzinfo, date_unit)

elif obj_type == "struct_time":
    """
    Allowed types to convert to:
    {float, datetime.datetime, pd.Timestamp, np.datetime64, arrow}
    ===
    {float, datetime, pandas, numpy, arrow}
    
    Note
    ----

    """
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "datetime", "pandas", "numpy", "arrow"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    if obj_convert_to == "float":
        result_datetime_obj = dt(*datetime_obj[:6]).timestamp()
    if obj_convert_to == "datetime":
        result_datetime_obj = dt(*datetime_obj[:6])
    if obj_convert_to == "pandas":
        result_datetime_obj = pd.to_datetime(dt(*datetime_obj[:6]), unit=date_unit)
    if obj_convert_to == "numpy":
        result_datetime_obj = np.datetime64(dt(*datetime_obj[:6]), date_unit)
    if obj_convert_to == "arrow":
        result_datetime_obj = arrow.get(datetime_obj)
        
    return result_datetime_obj

def tzinfo_remover(datetime_obj):
    return datetime_obj.replace(tzinfo=None)


int_class_set = {np.int8, np.int16, "int", np.int64} # 'int' denotes np.int32
int_class = int_class_set[-1]


elif obj_type == "dataframe":
    """
    For the sake of practicity and simplicity, the allowed types to convert to are (only):
    {float, pd.Timestamp}
    ===
    {float, pandas}
    
    Then every value inside the object will be converted to that object.
    In any case, the time unit will be governed by the selected one.
    """
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "pandas"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    date_unit_int_dict = {
        "D"  : 1000,
        "s"  : 1,
        "ms" : 1e-3,
        "us" : 1e-6,
        "ns" : 1e-9
    }
    date_unit_int = date_unit_int_dict.get(date_unit)
    
    # ONDOKO GUZTIA 'total_time_unit' metodoak emana!!!!
    if obj_convert_to == "float":
        result_datetime_obj = total_time_unit(datetime_obj, date_unit)
        return result_datetime_obj
    
    # FIXME: 'total_time_unit'-en oso antzeko egitura, alde bakarra total_time_obj[col] = pd.to_datetime(total_time_obj[col], unit=date_unit)
    #       Nola mergeatu, baldin 'total_time_unit' bakarrik bada unix hasieratik igarotako segundoak emateko?? 
    #       Kontzeptualki bariantetxoren bat egin genezake funtzio hartan?
    elif obj_convert_to == "pandas":
        try:
            columns = datetime_obj.columns
            for col in columns:
                try:
                    total_time_obj = datetime_obj.copy()
                    datetimtotal_time_obje_obj[col] = pd.to_datetime(total_time_obj[col], unit=date_unit)
                except ValueError:
                    pass
        # HACK: ERROREAK, probatu dudanera arte. EZ OTE DA OROKORREGIA IZANGO
        except Exception as err:
            raise Exception(err)
        else:
            return datetime_obj
        

elif obj_type == "series":
    """
    Similar case as ``obj_type='dataframe'``.
    """
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "pandas"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    if obj_convert_to == "float":
        result_datetime_obj = total_time_unit(datetime_obj, date_unit)
        return result_datetime_obj
    elif obj_convert_to == "pandas":
        # FIXME: 'total_time_unit'-en oso antzeko egitura, alde bakarra total_time_obj = pd.to_datetime(total_time_obj, unit=date_unit)
        #       Nola mergeatu, baldin 'total_time_unit' bakarrik bada unix hasieratik igarotako segundoak emateko?? 
        #       Kontzeptualki bariantetxoren bat egin genezake funtzio hartan?
        try:
            total_time_obj = datetime_obj.copy()
            total_time_obj = pd.to_datetime(total_time_obj, unit=date_unit)
        # HACK: ERROREAK, probatu dudanera arte. EZ OTE DA OROKORREGIA IZANGO
        except Exception as err:
            raise Exception(err)
            
        else:
            return total_time_obj

elif obj_type == "ndarray":
    """
    Similar case as ``obj_type='dataframe'`` or ``obj_type='series'``.
    """
    # Input validation #
    #------------------#
    
    # Object type to convert to #
    allowed_obj_type_conversions = ["float", "pandas"]
    validate_conversion(module, "Object type conversion", allowed_obj_type_conversions)
    
    try:
        if obj_convert_to == "float":
            result_datetime_obj = total_time_unit(datetime_obj, date_unit)
        elif obj_convert_to == "pandas":
            result_datetime_obj = pd.to_datetime(datetime_obj)
    # HACK: ERROREAK, probatu dudanera arte. EZ OTE DA OROKORREGIA IZANGO
    #       np.datetime64-ren kasuan edo AttributeError (astype ez) edo TypeError (okerreko data-mota)
    #       pd.to_datetime-ri dagokionez, inportatzea lortu ez dudan DataParseError du.
    except Exception as err:
        raise Exception(err)
    

# Datu konplexu horiek float-era, hau da, eskatutako denbora-unitatera pasatzeko funtzioa
# ---------------------------------------------------------------------------------------
def total_time_unit(datetime_obj, date_unit):
    """
    Total seconds or user-defined unit
    """
    # Input validation #
    #------------------#
    
    obj_type = get_obj_type_str(datetime_obj).lower()
    if obj_type == "datetime":
        total_time_obj = datetime_obj.timestamp()
    elif obj_type == "datetime64":
        total_time_obj = datetime_obj.astype(f"timedelta64[{date_unit}]").astype(float)
    elif obj_type == "arrow":
        total_time_obj = datetime_obj.float_timestamp
    elif obj_type == "struct_time":
        total_time_obj = dt(*datetime_obj[:6])
    elif obj_type == "ndarray":
        total_time_obj = datetime_obj.astype(f"datetime64[{date_unit}]").astype(float)  
    elif obj_type == "series":
        try:
            total_time_obj = datetime_obj.copy()
            total_time_obj = total_time_obj.astype(int_class) * date_unit_int
        except (ValueError, Exception) as err:
        # HACK: ERROREAK, probatu dudanera arte. EZ OTE DA OROKORREGIA IZANGO
            raise Exception(err)
            
    elif obj_type == "dataframe":
        try:
            columns = datetime_obj.columns
            for col in columns:
                try:
                    total_time_obj = datetime_obj.copy()
                    total_time_obj[col] = total_time_obj[col].astype(int_class) * date_unit_int
                except ValueError:
                    pass
        # HACK: ERROREAK, probatu dudanera arte. EZ OTE DA OROKORREGIA IZANGO
        except Exception as err:
            raise Exception(err)
        
        return datetime_obj
    
    return total_time_obj
    
# %% 

# TODO: PLASMATU AURREKO DEEEEEEEEEENA HEMEN
# TODO: aurrekoa gauzatu bitartean, IKUS EA APARTEKO ARTXIBOAK SORTZEA MEREZI DUENENTZ, funtzionaltasunen arabera

# MAIN METHOD #
#-------------#

def datetime_obj_converter(): 
    pass


# GAINONTZEKO FUNTZIOAK HEMENDIK AURRERA #


# %% PARAMETERS AND CONSTANTS

# Fractional second precision bounds #
min_prec = 0
max_prec = 9

# Modules (AS OF THESE DAYS, TEST ONLY) #
module = "datetime"

# Test variables # TODO: FUNTZIOA PROBATUTAKOAN ONDOKO BIAK EZABATU
time_str="70 23:00"
dt_fmt_str = "%d %H:%M"

# Switch case dictionaries #
#--------------------------#

# Time parsing #
#--------------#

# String #    
time_str_parsing_dict = {
    "datetime": lambda datetime_str, dt_fmt_str: datetime.strptime(datetime_str, dt_fmt_str),
    "dateutil": lambda datetime_str, dt_fmt_str: parser.parse(datetime_str, dt_fmt_str),
    "pandas": lambda datetime_str, dt_fmt_str, date_unit: pd.to_datetime(datetime_str, 
                                                                         format=dt_fmt_str,
                                                                         unit=date_unit),
    "numpy": lambda datetime_str, dt_fmt_str, date_unit: np.datetime64(datetime_str, date_unit),
    "arrow": lambda datetime_str, dt_fmt_str: arrow.get(datetime_str, dt_fmt_str)
}

# Floated #
floated_time_parsing_dict = {
    "datetime" : lambda floated_time, _ : datetime.fromtimestamp(floated_time),
    "time" : lambda floated_time : dt(*tuple(time.localtime(floated_time))[:6]),
    "pandas" : lambda floated_time, date_unit : pd.to_datetime(floated_time, unit=date_unit),
    "numpy" : lambda floated_time, date_unit : np.datetime64(floated_time, date_unit),
    "arrow" : lambda floated_time, _ : arrow.get(floated_time)
    }


# Parsing among different objects # 
# TODO: highly probable need of IMPLEMENT
parse_among_datetime_objs_dict = {
    "datetime" : "",#lambda datetime_str, dt_fmt_str : datetime.strptime(datetime_str, dt_fmt_str),
    "numpy" : "",#lambda datetime_str, dt_fmt_str : np.datetime64(datetime_str, dt_fmt_str),
    "pandas" : "" #lambda datetime_str, dt_fmt_str, date_unit : pd.to_datetime(datetime_str, format=dt_fmt_str, unit=date_unit),
    }

# Preformatted strings #
#----------------------#

time_str_parts_fmts = [
    "{} days {} hours {} minutes {} seconds",
    "{} hours {} minutes {} seconds",
]