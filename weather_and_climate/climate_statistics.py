#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import calendar

import numpy as np
import pandas as pd
import scipy.signal as ssig
import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.pandas_data_frames.data_frame_handler import find_date_key
from pyutils.parameters_and_constants import global_parameters
from pyutils.strings import information_output_formatters, string_handler
from pyutils.time_handling.time_formatters import datetime_obj_converter
from pyutils.utilities.introspection_utils import get_obj_type_str
from pyutils.weather_and_climate.netcdf_handler import find_time_dimension

# Create aliases #
#----------------#

basic_time_format_strs = global_parameters.basic_time_format_strs
month_number_dict = global_parameters.month_number_dict
season_time_freq_dict = global_parameters.season_time_freq_dict
time_freqs1 = global_parameters.time_frequencies_complete
time_freqs2 = global_parameters.time_frequencies_short_1

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.format_string

find_substring_index = string_handler.find_substring_index

#------------------#
# Define functions #
#------------------#

def periodic_statistics(obj, statistic, freq,
                        groupby_dates=False,
                        drop_date_idx_col=False,
                        season_months=None):
    
    """
    Calculates basic statistics (not climatologies) for the given data 
    object over a specified time frequency.

    This function supports data analysis on Pandas DataFrames and 
    xarray objects, allowing for grouping by different time frequencies 
    such as yearly, quarterly, monthly, etc. 

    Parameters
    ----------
    obj : pandas.DataFrame or xarray.Dataset or xarray.DataArray
        The data object for which statistics are to be calculated.
    
    statistic : {"max", "min", "mean", "std", "sum"}
        The statistical measure to compute.
    
    freq : str
        The frequency for resampling or grouping the data.
        For example, "D" for daily, "M" for monthly, etc.
        Refer to the Pandas documentation for more details 
        on time frequency aliases.
    
    groupby_dates : bool, optional
        Only applicable for xarray.Dataset or xarray.DataArray.
        If True, the function will group the dates according to 
        the specified frequency.
    
    drop_date_idx_col : bool, optional
        Whether to drop the date index column from the results. 
        Default is False, retaining the dates in the output.
    
    season_months : list of int, optional
        A list of three integers representing the months of a season,
        used if 'freq' is "SEAS". Must contain exactly three months.

    Returns
    -------
    pandas.DataFrame or xarray object
        The computed statistics as a DataFrame or xarray object,
        depending on the type of input data.

    Raises
    ------
    ValueError
        If the specified statistic is unsupported, the frequency is 
        invalid, or if the season_months list does not contain exactly 
        three integers.

    Notes
    -----
    - The function is designed to handle various data structures
      and performs input validation to ensure proper usage.
    - Seasonality can be analyzed by providing a list of months 
      that define a season, which is particularly useful for seasonal
      frequency analysis.
    """
    
    # Constants
    statistics = ["max", "min", "mean", "std", "sum"]
    freq_abbrs1 = ["Y", "SEAS", "M", "D", "H", "min", "S"]

    # Validate statistic
    if statistic not in statistics:
        raise ValueError(format_string(unsupported_option_error_str, ("statistic", statistics)))

    # Determine object type
    obj_type = get_obj_type_str(obj).lower()
    if obj_type not in ["dataframe", "dataset", "dataarray"]:
        raise ValueError("Cannot operate with this data type.")
    
    # GroupBy Logic
    if obj_type == "dataframe":
        date_key = find_date_key(obj)
    else:
        date_key = find_time_dimension(obj)
    
    if obj_type in ["dataset", "dataarray"]:
        groupby_key = f"{date_key}.dt.{freq}"
    else:
        groupby_key = date_key
    
    if groupby_dates and obj_type in ["dataset", "dataarray"]:
        # Validation and Grouping Logic
        if freq not in time_freqs1 or (freq == time_freqs1[1] and season_months is None):
            raise ValueError(season_month_fmt_error_str)
        if season_months and len(season_months) != 3:
            raise ValueError(season_length_warning_str)
        if season_months:
            freq = season_time_freq_dict[season_months[-1]]
        obj_groupby = obj.groupby(groupby_key)
    else:
        # Handle DataFrame Grouping
        if freq not in freq_abbrs1 or (freq == freq_abbrs1[1] and season_months is None):
            raise ValueError(unsupported_option_error_str)
        if season_months and len(season_months) != 3:
            raise ValueError(season_length_warning_str)
        if season_months:
            freq = season_time_freq_dict[season_months[-1]]
            obj_groupby = obj.resample({date_key: freq})
        else:
            obj_groupby = pd.Grouper(key=date_key, freq=freq)


    # Calculate Statistics
    result = getattr(obj_groupby, statistic)()
    if obj_type == "dataframe":
        result.reset_index(drop=drop_date_idx_col)
    else:
        return result
    

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
    
    # Parameter validation #   
    #----------------------#
    
    tf_idx = find_substring_index(time_freqs2, time_freq)     
    if tf_idx == -1:
        arg_tuple_climat_stats = ("time-frequency", time_freqs2)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_climat_stats))
    else:
        freq_abbr = freq_abbrs2[tf_idx]
      
        
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
            
            """Define a dictionary matching the month number 
            with the corresponding names first letter
            """
            
            if season_months is None:
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
            """Follow CDO's climatologic time array pattern,
            it is a model hourly time array.
            """
            
            # Define the hourly climatology pattern #
            obj_climat_nonstd_times = obj['time.hour'] / 24 + obj['time.dayofyear']
            obj_climat = obj.groupby(obj_climat_nonstd_times).statistic(dim=date_key)
            
        elif time_freq == "seasonal":
            if season_months is None:
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


def calculate_and_apply_deltas(observed_series,
                               reanalysis_series,
                               time_freq,
                               delta_type="absolute",
                               statistic="mean",
                               preference_over="observed",
                               keep_std_dates=True, 
                               drop_date_idx_col=False,
                               season_months=None):

    """
    Function that calculates simple deltas between two objects
    and then applies to any of them.
    
    For that, it firstly calculates the given time-frequency climatologies
    for both objects using 'climat_periodic_statistics' function,
    and then performs the delta calculation, 
    depending on the math operator chosen:
      1. Absolute delta: subtraction between both objects
      2. Relative delta: division between both objects
    
    Once calculated, delta values are climatologically applied to the chosen
    object, by addition if the deltas are absolute or multiplication if they
    are relative.
    
    Parameters
    ----------
    observed_series : pandas.DataFrame, xarray.Dataset or xarray.DataArray.
    reanalysis_series : pandas.DataFrame, xarray.Dataset or xarray.DataArray.
        This object can be that extracted from a reanalysis,
        CORDEX projections or similar ones.
    time_freq : str
        Time frequency to which data will be filtered.
    delta_type : {"absolute", "relative"}
    statistic : {"max", "min", "mean", "std", "sum"}
        The statistic to calculate.
        Default is "mean" so that climatologic mean is calculated.
    preference_over : {"observed", "reanalysis"}
        If "observed", then the observed series will be treated as the 'truth'
        and the reanalysis will be delta-corrected.
        Otherwise, though it is not common, the reanalysis will be treated
        as the truth and observations will be delta-corrected.
        Defaults to give preference to the observed series.
    keep_std_dates : bool
        If True, standard YMD (HMS) date format is kept for all climatologics
        except for yearly climatologics.
        Otherwise dates are shown as hour, day, or month indices,
        and season achronyms if "seasonal" is selected as the time frequency.
        Default value is False.
    drop_date_idx_col : bool
        Affects only if the passed object is a Pandas DataFrame.
        Boolean used to whether drop the date columns in the new data frame.
        If it is False, then the columns of the dates will be kept.
        Otherwise, the dates themselves will be kept, but they will be
        treated as indexers, and not as a column.
        Defaults to True in order to return date-time incorporated series.
    season_months : list of integers
        List containing the month numbers to later refer to the time array,
        whatever the object is among the mentioned three types.
        Defaults to None.
    
    Returns
    -------
    obj_climat : pandas.DataFrame, xarray.Dataset or xarray.DataArray.
        Climatological average of the data.
    
    Notes
    -----
    For Pandas DataFrames, since it is an 2D object,
    it is interpreted that data holds for a specific geographical point.
    """
    
    # Quality control of parameters #     
    if delta_type not in delta_types:
        arg_tuple_delta1 = ("delta type", delta_types)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_delta1))
    
    if preference_over not in preferences_over:
        arg_tuple_delta2 = ("preference type", preferences_over)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_delta2))
    
    # Determine object type #
    #-----------------------#
    
    obj_type_observed = get_obj_type_str(observed_series).lower()
    obj_type_reanalysis = get_obj_type_str(reanalysis_series).lower()
    
    # Identify the time dimension #
    #-----------------------------#
    
    if (obj_type_observed, obj_type_reanalysis ) == ("dataframe", "dataframe"):      
        date_key = find_date_key(observed_series)
        date_key_rean = find_date_key(observed_series)

        if date_key != date_key_rean:
            reanalysis_series.columns = [date_key] + reanalysis_series.columns[1:]

    elif ((obj_type_observed, obj_type_reanalysis) == ("dataset", "dataset"))\
        or ((obj_type_observed, obj_type_reanalysis) == ("dataarray", "dataarray")):
        
        date_key = find_time_dimension(observed_series)
        date_key_rean = find_time_dimension(observed_series)
        
        if date_key != date_key_rean:
            
            try:
                
                # Rename the analogous dimension of 'time' on dimension list #
                reanalysis_series\
                = reanalysis_series.rename_dims({date_key_rean : date_key})
                   
                # Rename the analogous dimension name of 'time' to standard #
                reanalysis_series\
                = reanalysis_series.rename({date_key_rean : date_key})
                
            except:
                
                # Rename the analogous dimension of 'time' on dimension list #
                reanalysis_series\
                = reanalysis_series.swap_dims({date_key_rean : date_key})
                   
                # Rename the analogous dimension name of 'time' to standard #
                reanalysis_series\
                = reanalysis_series.swap_dims({date_key_rean : date_key})
                
    else:
        
        # Calculate statistical climatologies #
        #-------------------------------------#
        
        arg_tuple_delta3 = (
            "Calculating observed climatologies...",
            time_freq,
            "N/P",
            "N/P",
            "N/P"
            )
        print_format_string(delta_application_info_str, arg_tuple_delta3)
        
        obs_climat = climat_periodic_statistics(observed_series, 
                                                statistic, 
                                                time_freq,
                                                keep_std_dates,
                                                drop_date_idx_col,
                                                season_months)
        arg_tuple_delta4 = (
            "Calculating reanalysis climatologies...",
            time_freq,
            "N/P",
            "N/P",
            "N/P"
            )
        print_format_string(delta_application_info_str, arg_tuple_delta4)
        
        rean_climat = climat_periodic_statistics(reanalysis_series, 
                                                 statistic, 
                                                 time_freq,
                                                 keep_std_dates,
                                                 drop_date_idx_col,
                                                 season_months)
        
        # Calculate deltas #
        #------------------#
    
        if ((obj_type_observed, obj_type_reanalysis) == ("dataframe", "dataframe")):
            
            if preference_over == "observed":
                delta_cols = observed_series.columns[1:]
                
                if delta_type == "absolute":
                    delta_arr = rean_climat.iloc[:, 1:].values - obs_climat.iloc[:, 1:].values
                else:
                    delta_arr = rean_climat.iloc[:, 1:].values / obs_climat.iloc[:, 1:].values
                
            elif preference_over == "reanalysis":
                delta_cols = reanalysis_series.columns[1:]
                
                if delta_type == "absolute":
                    delta_arr = obs_climat.iloc[:, 1:].values - rean_climat.iloc[:, 1:].values
                else:
                    delta_arr = obs_climat.iloc[:, 1:].values / rean_climat.iloc[:, 1:].values
                
            delta_obj = pd.concat([obs_climat[date_key],
                                   pd.DataFrame(delta_arr, columns=delta_cols)],
                                  axis=1)
            
        
        elif ((obj_type_observed, obj_type_reanalysis) == ("dataset", "dataset"))\
            or ((obj_type_observed, obj_type_reanalysis) == ("dataarray", "dataarray")):
                
            if preference_over == "observed":
                
                if delta_type == "absolute":
                    delta_obj = rean_climat - obs_climat
                else:
                    delta_obj = rean_climat / obs_climat
                
            elif preference_over == "reanalysis":            
                if delta_type == "absolute":
                    delta_obj = obs_climat - rean_climat
                else:
                    delta_obj = obs_climat / rean_climat
                
        # Apply the deltas over the chosen series # 
        #-----------------------------------------#
        
        months_delta = np.unique(delta_obj[date_key].dt.month)
        days_delta = np.unique(delta_obj[date_key].dt.day)
        hours_delta = np.unique(delta_obj[date_key].dt.hour)
        
        if time_freq == "seasonal":
            freq_abbr = time_freq
            
        else:
            
            if ((obj_type_observed, obj_type_reanalysis) == ("DataFrame", "DataFrame")): 
                freq_abbr = pd.infer_freq(obs_climat[date_key])
                
            elif ((obj_type_observed, obj_type_reanalysis) == ("dataset", "dataset"))\
                or ((obj_type_observed, obj_type_reanalysis) == ("dataarray", "dataarray")):
                freq_abbr = xr.infer_freq(obs_climat[date_key])
        
        if preference_over == "observed":
            obj_aux = reanalysis_series.copy()
        else:
            obj_aux = observed_series.copy()
        
        """Acronyms used in the following lines:
            
        obj2correct === object (can either be a Pandas DataFrame or a xarray data set)
                  to be corrected
        obj_delta === delta object
        """
    
        # Seasonal time-frequency #
        ###########################
        
        if time_freq == "seasonal":
            obj2correct = obj_aux[obj_aux[date_key].dt.month.isin(season_months)]
            
            # Delta application #
            arg_tuple_delta5 = (
                f"Applying deltas over the {preference_over} series...",
                freq_abbr,season_months,"all","all"
                )
            print_format_string(delta_application_info_str, arg_tuple_delta5)
            
            if ((obj_type_observed, obj_type_reanalysis) == ("DataFrame", "DataFrame")):    
                if delta_type == "absolute":    
                    obj_aux.loc[obj2correct.index, delta_cols]\
                    += delta_obj.loc[:, delta_cols].values
                else:
                    obj_aux.loc[obj2correct.index, delta_cols]\
                    *= delta_obj.loc[:, delta_cols].values
                    
            elif ((obj_type_observed, obj_type_reanalysis) == ("dataset", "dataset"))\
                or ((obj_type_observed, obj_type_reanalysis) == ("dataarray", "dataarray")):
                if delta_type == "absolute":
                    obj_aux.loc[obj2correct.time] += delta_obj.values
                else:
                    obj_aux.loc[obj2correct.time] *= delta_obj.values
                 
        
        # Monthly time-frequency #
        ##########################
        
        elif time_freq == "monthly":
            
            for m in months_delta:            
                obj2correct = obj_aux[obj_aux[date_key].dt.month==m]
                obj_delta = delta_obj[delta_obj[date_key].dt.month==m]
                
                # Delta application #
                arg_tuple_delta6 = (
                    f"Applying deltas over the {preference_over} series...",
                    freq_abbr,m,"all","all"
                    )
                print_format_string(delta_application_info_str, arg_tuple_delta6)
                
                if ((obj_type_observed, obj_type_reanalysis) == ("DataFrame", "DataFrame")):
                    if delta_type == "absolute":
                        obj_aux.loc[obj2correct.index, delta_cols]\
                        += obj_delta.loc[:, delta_cols].values
                    else:
                        obj_aux.loc[obj2correct.index, delta_cols]\
                        *= obj_delta.loc[:, delta_cols].values
                        
                elif ((obj_type_observed, obj_type_reanalysis) == ("dataset", "dataset"))\
                    or ((obj_type_observed, obj_type_reanalysis) == ("dataarray", "dataarray")):

                    if delta_type == "absolute":
                        obj_aux.loc[obj2correct.time] += obj_delta.values
                    else:
                        obj_aux.loc[obj2correct.time] *= obj_delta.values
                    
                
        # Daily time-frequency #
        ########################
            
        elif time_freq == "daily":
            
            for m in months_delta: 
                for d in days_delta:
                        
                    obj2correct = obj_aux[(obj_aux[date_key].dt.month==m)&
                                    (obj_aux[date_key].dt.day==d)]
                    
                    obj_delta = delta_obj[(delta_obj[date_key].dt.month==m)&
                                     (delta_obj[date_key].dt.day==d)]
                    
                    # Delta application #
                    if len(obj2correct) > 0 and len(obj_delta) > 0:
                        arg_tuple_delta7 = (
                            f"Applying deltas over the {preference_over} series...",
                            freq_abbr,m,d,"all"
                            )
                        print_format_string(delta_application_info_str, arg_tuple_delta7)
                        
                        if ((obj_type_observed, obj_type_reanalysis) == ("DataFrame", "DataFrame")):
                            if delta_type == "absolute":
                                obj_aux.loc[obj2correct.index, delta_cols] \
                                += obj_delta.loc[:, delta_cols].values
                            
                            else:
                                obj_aux.loc[obj2correct.index, delta_cols] \
                                *= obj_delta.loc[:, delta_cols].values
                                
                        elif ((obj_type_observed, obj_type_reanalysis) == ("dataset", "dataset"))\
                            or ((obj_type_observed, obj_type_reanalysis) == ("dataarray", "dataarray")):
                                
                            if delta_type == "absolute":
                                obj_aux.loc[obj2correct.time] += obj_delta.values
                            else:
                                obj_aux.loc[obj2correct.time] *= obj_delta.values
                        
                    else:
                        pass
                           
        # Hourly time-frequency #
        #########################
        
        elif time_freq == "hourly":
                
            for m in months_delta:
                for d in days_delta:
                    for h in hours_delta:
                        
                        obj2correct = obj_aux[(obj_aux[date_key].dt.month==m)&
                                        (obj_aux[date_key].dt.day==d)&
                                        (obj_aux[date_key].dt.hour==h)]
                       
                        obj_delta = delta_obj[(delta_obj[date_key].dt.month==m)&
                                         (delta_obj[date_key].dt.day==d)&
                                         (delta_obj[date_key].dt.hour==h)]
                       
                        # Delta application #
                        if len(obj2correct) > 0 and len(obj_delta) > 0:
                            arg_tuple_delta8 = (
                                f"Applying deltas over the {preference_over} series...",
                                freq_abbr,m,d,h
                                )
                            print_format_string(delta_application_info_str, arg_tuple_delta8)
                            
                            if ((obj_type_observed, obj_type_reanalysis) == ("DataFrame", "DataFrame")):
                                if delta_type == "absolute":
                                    obj_aux.loc[obj2correct.index, delta_cols] \
                                    += obj_delta.loc[:, delta_cols].values
                                else:
                                    obj_aux.loc[obj2correct.index, delta_cols] \
                                    *= obj_delta.loc[:, delta_cols].values
                                    
                            elif ((obj_type_observed, obj_type_reanalysis) == ("dataset", "dataset"))\
                                or ((obj_type_observed, obj_type_reanalysis) == ("dataarray", "dataarray")):
                                if delta_type == "absolute":
                                    obj_aux.loc[obj2correct.time] += obj_delta.values
                                else:
                                    obj_aux.loc[obj2correct.time] *= obj_delta.values
                       
                        else:
                            pass
                       
        delta_corrected_obj = obj_aux.copy()    
        return delta_corrected_obj


def window_sum(x, N):

    """
    Function that computes the sum of the elements
    of a (time, lat, lon) array, in a sliding window, i.e. the moving sum.
    
    Parameters
    ----------
    x : numpy.ndarray
        Array containing data.
    N : int
        Window size.
    
    Returns
    -------
    sum_window : numpy.ndarray
        The sum of the elements.
    
    Notes
    -----
    Numpy's 'convolve' function does not work for n > 1 dimensional arrays.
    In such cases, scipy's 'convolve' function does the trick.
    """
    
    shape = x.shape
    dims = len(shape)
    
    if dims == 1:
        try:
            sum_window = np.convolve(x, np.ones(N, np.int64), mode="valid")
        except:
            sum_window = np.convolve(x, np.ones(N, np.float64), mode="valid")

    elif dims > 1:   
        number_of_ones = np.append(N, np.repeat(1, dims-1))
        ones_size_tuple = tuple(number_of_ones)
             
        try:
            sum_window = ssig.convolve(x,
                                       np.ones(ones_size_tuple, np.int64),
                                       mode="same"
                                       )[1:]
        except:
            sum_window = ssig.convolve(x,
                                       np.ones(ones_size_tuple, np.float64),
                                       mode="same"
                                       )[1:]
            
    else:
        raise ValueError("Given array is an empty one!")
        
    return sum_window


def moving_average(x, N):
    
    """
    Returns the moving average of an array, independently of its dimension.
    For that, firstly uses the moving sum function and divides the result
    by the window size, N.
    
    Parameters
    ----------
    x : numpy.ndarray
        Array containing data.
    N : int
        Window size.
    
    Returns
    -------
    moving_average : numpy.ndarray
        The moving average of the array.
    """
    return window_sum(x, N) / N
    
#--------------------------#
# Parameters and constants #
#--------------------------#

unsupported_option_error_str = "Unsupported {}. Options are {}"
season_length_warning_str = "Season length must strictly be of 3 months."
season_month_fmt_error_str = \
"""You must specify the season months in a list. For example: [12, 1, 2]"""

# Delta application function #
delta_types = ["absolute", "relative"]
preferences_over = ["observed", "reanalysis"]

# Date and time format strings #
daytime_fmt_str = basic_time_format_strs["D"]

# Statistics #
statistics = ["max", "min", "sum", "mean", "std"]

# Time frequency abbreviations #
freq_abbrs1 = ["Y", "SEAS", "M", "D", "H", "min", "S"]
freq_abbrs2 = ["Y", "S", "M", "D", "H"]

# Tuples to pass in into preformatted strings #
arg_tuple_stats = ("time-frecuency", freq_abbrs1)

# Preformatted strings #
#----------------------#

delta_application_info_str = """{}
Time frequency : {}
Month = {}
Day = {}
Hour = {}
"""