#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
simple_bias_correction.py
-------------------------

This module provides a set of functions to perform simple bias correction techniques,
particularly designed for climatology data. These methods focus on calculating and 
applying deltas between observed data series and reanalysis or model output series, 
which are useful for correcting systematic biases in climate simulations or historical 
reanalysis datasets.

The methods in this module support bias correction using both absolute and relative deltas,
across various time frequencies such as seasonal, monthly, daily, or hourly resolutions.
They can handle common data structures used in climatology like Pandas DataFrames or 
xarray Datasets.
"""

#----------------#
# Import modules #
#----------------#

import numpy as np
import pandas as pd
import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.pandas_data_frames.data_frame_handler import find_date_key
from pyutils.parameters_and_constants import global_parameters
from pyutils.strings.information_output_formatters import format_string, print_format_string
from pyutils.statistics.fields.climatology.periodic_climatology_stats import climat_periodic_statistics
from pyutils.utilities.general.introspection_utils import get_obj_type_str
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
    
# Climatologic statistics #
#-------------------------#



# Bias correction methods #
#-------------------------#

# Deltas #
#-#-#-#-#-

def calculate_and_apply_deltas(observed_series,
                               reanalysis_series,
                               time_freq,
                               delta_type="absolute",
                               statistic="mean",
                               preference="observed",
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
    preference : {"observed", "reanalysis"}
        If "observed", then the observed series will be treated as the 'truth'
        and the reanalysis will be delta-corrected.
        Otherwise, though it is not common, the reanalysis will be treated
        as the truth and observations will be delta-corrected.
        Defaults to give preference over the observed series.
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
    
    # Input validations #
    #-------------------#
    
    if delta_type not in delta_types:
        arg_tuple_delta1 = ("delta type", delta_type, delta_types)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_delta1))
    
    if preference not in supported_time_series:
        arg_tuple_delta2 = ("preferent time series name", preference, supported_time_series)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_delta2))
    
    # Operations #
    #------------#
    
    # Determine object type #
    #-#-#-#-#-#-#-#-#-#-#-#-#
    
    obj_type_observed = get_obj_type_str(observed_series).lower()
    obj_type_reanalysis = get_obj_type_str(reanalysis_series).lower()
    
    # Identify the time dimension #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    
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
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        
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
        #-#-#-#-#-#-#-#-#-#-
    
        if ((obj_type_observed, obj_type_reanalysis) == ("dataframe", "dataframe")):
            
            if preference == "observed":
                delta_cols = observed_series.columns[1:]
                
                if delta_type == "absolute":
                    delta_arr = rean_climat.iloc[:, 1:].values - obs_climat.iloc[:, 1:].values
                else:
                    delta_arr = rean_climat.iloc[:, 1:].values / obs_climat.iloc[:, 1:].values
                
            elif preference == "reanalysis":
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
                
            if preference == "observed":
                
                if delta_type == "absolute":
                    delta_obj = rean_climat - obs_climat
                else:
                    delta_obj = rean_climat / obs_climat
                
            elif preference == "reanalysis":            
                if delta_type == "absolute":
                    delta_obj = obs_climat - rean_climat
                else:
                    delta_obj = obs_climat / rean_climat
                
        # Apply the deltas over the chosen series # 
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        
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
        
        obj_aux = reanalysis_series.copy() if preference == "observed" else observed_series.copy()
        
        """
        Acronyms used in the following lines
        ------------------------------------            
        obj2correct : object 
            Can either be a Pandas DataFrame or a xarray data set to be corrected.
        obj_delta : delta object
        """
    
        # Seasonal time-frequency #
        ###########################
        
        if time_freq == "seasonal":
            obj2correct = obj_aux[obj_aux[date_key].dt.month.isin(season_months)]
            
            # Delta application #
            arg_tuple_delta5 = (
                f"Applying deltas over the {preference} series...",
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
                    f"Applying deltas over the {preference} series...",
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
                            f"Applying deltas over the {preference} series...",
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
                                f"Applying deltas over the {preference} series...",
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

    
#--------------------------#
# Parameters and constants #
#--------------------------#

unsupported_option_error_str = "Unsupported {} '{}'. Options are {}."

# Delta application function #
delta_types = ["absolute", "relative"]
supported_time_series = ["observed", "reanalysis"]

# Statistics #
statistics = ["max", "min", "sum", "mean", "std"]

# Preformatted strings #
#----------------------#

# Delta application options #
delta_application_info_str = """{}
Time frequency : {}
Month = {}
Day = {}
Hour = {}
"""