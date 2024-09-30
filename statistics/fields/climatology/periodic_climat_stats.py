#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
periodic_climat_stats.py
------------------------

This module provides functionality to compute periodic climatology statistics 
over specified time frequencies. These methods are particularly useful for 
climatological and atmospheric sciences, where it's common to analyze data 
on seasonal, monthly, daily, or even hourly time scales.

The primary function calculates summary statistics (mean, median, etc.) 
for an observed or modeled data series across these time intervals, allowing for 
the detection and comparison of climate patterns and trends.

Notes
-----

- This module supports various time frequencies common in climatological studies, 
  allowing flexibility in analyzing and summarizing periodic trends.
- It works with standard data structures used in climatology, including both Pandas 
  and xarray, making it adaptable for various data sources (e.g., observations, 
  reanalysis, or climate model outputs).
- The function is optimized for efficiency with large datasets and supports 
  both absolute and relative time-based statistics.
"""


#----------------#
# Import modules #
#----------------#

import calendar

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.pandas_data_frames.data_frame_handler import find_date_key
from pyutils.parameters_and_constants import global_parameters
from pyutils.strings.information_output_formatters import format_string
from pyutils.strings.string_handler import find_substring_index
from pyutils.utilities.introspection_utils import get_caller_method_args, get_obj_type_str
from pyutils.statistics.core.time_series import periodic_statistics
from pyutils.time_handling.time_formatters import datetime_obj_converter
from pyutils.weather_and_climate.netcdf_handler import find_time_dimension

# Create aliases #
#----------------#

basic_time_format_strs = global_parameters.basic_time_format_strs
month_number_dict = global_parameters.month_number_dict
time_freqs1 = global_parameters.time_frequencies_complete
time_freqs2 = global_parameters.time_frequencies_short_1


#------------------#
# Define functions #
#------------------#

def climat_periodic_statistics(obj,
                               statistic,
                               time_freq,
                               keep_std_dates=False, 
                               drop_date_idx_col=False,
                               season_months=None):

    """
    Function that calculates climatologic statistics for a time-frequency.
    
    Parameters
    ----------
    obj : pandas.DataFrame, xarray.Dataset or xarray.DataArray.
    statistic : {"max", "min", "mean", "std", "sum"}
        The statistic to calculate.
    time_freq : str
        Time frequency to which data will be filtered.
    keep_std_dates : bool
        If True, standard YMD (HMS) date format is kept for all climatologics
        except for yearly climatologics.
        Otherwise dates are shown as hour, day, or month indices,
        and season achronyms if "seasonal" is selected as the time frequency.
        Default value is False.
    drop_date_idx_col : bool
        Whether to drop the date index column. Default is False.
        If True, the dates will be kept, but the corresponding array
        will be an index, instead of a column.
        Defaults to False
    season_months : list of integers
        List containing the month numbers to later refer to the time array,
        whatever the object is among the mentioned three types.
        Defaults to None.
    
    Returns
    -------
    obj_climat : pandas.DataFrame, xarray.Dataset or xarray.DataArray.
        Calculated climatological average.
    
    Notes
    -----
    For Pandas DataFrames, since it is a 2D object,
    it is interpreted as data holds for a specific geographical point.
    """
    
    # Input validation #   
    #----------------------#
    
    all_arg_names = get_caller_method_args()
    seas_months_arg_pos = find_substring_index(all_arg_names, "season_months")
    
    seas_mon_arg_type = get_obj_type_str(season_months)
    
    tf_idx = time_freqs2.index(time_freq)
    if tf_idx == -1:
        arg_tuple_climat_stats = ("time-frequency", time_freq, time_freqs2)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_climat_stats))
    else:
        freq_abbr = freq_abbrs[tf_idx]
      
        
    # Operations #
    #------------#    
    
    # Determine object type #
    #-#-#-#-#-#-#-#-#-#-#-#-#
    
    obj_type = get_obj_type_str(obj).lower()
    
    # Identify the time dimension #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    
    if obj_type == "dataframe":
        date_key = find_date_key(obj)
        
    elif obj_type in ["dataset", "dataarray"]:
        date_key = find_time_dimension(obj)               
    
    # Calculate statistical climatologies #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

    # Get date array and parts of it #
    dates = obj[date_key]
    
    years = np.unique(dates.dt.year)        
    days = np.unique(dates.dt.day)
    months = np.unique(dates.dt.month)
    hours = np.unique(dates.dt.hour)
    
    # Check for the number of leap years #
    leapyear_bool_arr = [calendar.isleap(year) for year in years]
    llba = len(leapyear_bool_arr)
    
    if llba > 0:
        latest_year = years[leapyear_bool_arr][-1]
    else:
        latest_year = years[-1]

    if obj_type == "dataframe":
        
        # Define the climatologic statistical data frame #
        climat_obj_cols = \
        [date_key] + [obj.columns[i]+"_climat" for i in range(1, len(obj.columns))]
                
        if time_freq == "hourly":  
            climat_vals = []
            for m in months:
                for d in days:
                    for h in hours:
                        subset = obj[(obj[date_key].dt.month == m) & 
                                     (obj[date_key].dt.day == d) & 
                                     (obj[date_key].dt.hour == h)].iloc[:, 1:]
                        if len(subset) > 0:
                            climat_vals.append(subset[statistic]())
                
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
            else:    
                climat_dates = np.arange(len(climat_vals))
                climat_obj_cols[0] = "hour_of_year"
            
            
        elif time_freq == "daily":   
            climat_vals = []
            for m in months:
                for d in days:
                    subset = obj[(obj[date_key].dt.month == m) & 
                                 (obj[date_key].dt.day == d)].iloc[:, 1:]
                    if len(subset) > 0:
                        climat_vals.append(subset[statistic]())
                
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
            else:    
                climat_dates = np.arange(1, len(climat_vals) + 1)
                climat_obj_cols[0] = "day_of_year"
                
                
        elif time_freq == "monthly": 
            climat_vals = []
            for m in months:
                subset = obj[obj[date_key].dt.month == m].iloc[:, 1:]
                if len(subset) > 0:
                    climat_vals.append(subset[statistic]())
                    
            if keep_std_dates:
                climat_dates = pd.date_range(f"{latest_year}-01-01 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
                
            else:
                climat_dates = np.arange(1, 13)
                climat_obj_cols[0] = "month_of_year"
            
            
        elif time_freq == "seasonal":
            
            """
            Define a dictionary matching the month number 
            with the corresponding names first letter
            """
            
            if seas_mon_arg_type != "list":
                raise TypeError("Expected a list for parameter "
                                f"'{all_arg_names[seas_months_arg_pos]}', "
                                f"got '{seas_mon_arg_type}'.")
            
            if (season_months and len(season_months) != 3):
                raise ValueError(season_month_fmt_error_str)

            climat_vals = [obj[obj[date_key].dt.month.isin(season_months)].iloc[:, 1:][statistic]()]
        
            if keep_std_dates:                
                climat_dates = [obj[obj[date_key].dt.month==season_months[-1]].
                                iloc[-1][date_key].strftime(daytime_fmt_str)]
            else:
                climat_dates = [month_number_dict[m] for m in season_months]
                climat_obj_cols[0] = "season"
                    

            
        elif time_freq == "yearly":
            climat_df = periodic_statistics(obj, statistic, freq_abbr, drop_date_idx_col)
            climat_vals = [climat_df.iloc[:, 1:][statistic]()]
            climat_dates = [climat_df.iloc[-1,0]]
              
        # Check climatological value array's shape to later fit into the df #
        climat_vals = np.array(climat_vals)
        climat_vals_shape = climat_vals.shape
         
        if len(climat_vals_shape) == 1:
            climat_vals = climat_vals[:, np.newaxis]    
        
        climat_dates = np.array(climat_dates, 'O')[:, np.newaxis]
        
        # Store climatological data into the data frame #
        climat_arr = np.append(climat_dates, climat_vals, axis=1)
        obj_climat = pd.DataFrame(climat_arr, columns=climat_obj_cols)
        obj_climat.iloc[:, 0] = datetime_obj_converter(obj_climat.iloc[:, 0], "pandas")        
        
    elif obj_type in ["dataset", "dataarray"]:
        if time_freq == "hourly":
            
            # Define the time array #
            """
            Follow CDO's climatologic time array pattern,
            it is a model hourly time array.
            """
            
            # Define the hourly climatology pattern #
            obj_climat_nonstd_times = obj['time.hour'] / 24 + obj['time.dayofyear']
            obj_climat = obj.groupby(obj_climat_nonstd_times).statistic(dim=date_key)
            
        elif time_freq == "seasonal":
            if seas_mon_arg_type != "list":
                raise TypeError("Expected a list for parameter "
                                f"'{all_arg_names[seas_months_arg_pos]}', "
                                f"got '{seas_mon_arg_type}'.")
                
            if (season_months and len(season_months) != 3):
                raise ValueError(season_month_fmt_error_str)
            else:
                obj_seas_sel = obj.sel({date_key: obj[date_key].dt.month.isin(season_months)})
                obj_climat = obj_seas_sel[statistic](dim=date_key)
                      
                 
        # Choose the climatological time format #
        #---------------------------------------#
        
        if time_freq in time_freqs1[2:]:
            
            # Get the analogous dimension of 'time', usually label 'group' #
            occ_time_name_temp = find_time_dimension(obj_climat)

            if keep_std_dates:                          
                climat_dates = pd.date_range(f"{latest_year}-1-1 0:00",
                                             f"{latest_year}-12-31 23:00",
                                             freq=freq_abbr)
                occ_time_name = date_key 
              
            else:
                climat_dates = obj_climat[occ_time_name_temp].values
                lcd = len(climat_dates)
                
                occ_time_name = occ_time_name_temp
                
                if time_freq in time_freqs1[-2:]:
                    occ_time_name = time_freq[:-2] + "ofyear"    
                    climat_dates = np.arange(lcd) 
                
            # 'time' dimension renaming and its assignment #
            try:
                # Rename the analogous dimension of 'time' on dimension list #
                obj_climat = obj_climat.rename_dims({occ_time_name_temp : occ_time_name})
            except:
                # Rename the analogous dimension name of 'time' to standard #
                obj_climat = obj_climat.rename({occ_time_name_temp : occ_time_name})
                
            try:
                # Rename the analogous dimension of 'time' on dimension list #
                obj_climat = obj_climat.swap_dims({occ_time_name_temp : occ_time_name})
                
            except:
                try:
                    # Rename the analogous dimension name of 'time' to standard #
                    obj_climat = obj_climat.swap_dims({occ_time_name_temp : occ_time_name})
                except:
                    pass   
                    
        elif time_freq == time_freqs1[1]:
            
            if keep_std_dates:
                        
                seas_end_dayofmonth\
                = calendar.monthcalendar(latest_year, season_months[-1])[-1][-1]
                climat_dates\
                = pd.Timestamp(latest_year, season_months[-1], seas_end_dayofmonth)
                
                occ_time_name = date_key
                
            else:
                occ_time_name = time_freq[:-2]
                climat_dates = "".join([month_number_dict[m] for m in season_months])
                    
        # Update the time array #
        obj_climat = obj_climat.assign_coords({occ_time_name : climat_dates})
            
    return obj_climat


#--------------------------#
# Parameters and constants #
#--------------------------#

unsupported_option_error_str = "Unsupported {} '{}'. Options are {}."
season_month_fmt_error_str = """Parameter 'season_months' must contain exactly \
3 integers representing months. For example: [12, 1, 2]."""

# Date and time format strings #
daytime_fmt_str = basic_time_format_strs["D"]

# Statistics #
statistics = ["max", "min", "sum", "mean", "std"]

# Time frequency abbreviations #
freq_abbrs = ["Y", "S", "M", "D", "H"]