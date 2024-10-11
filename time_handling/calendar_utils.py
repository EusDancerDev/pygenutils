#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import calendar
import datetime

import numpy as np
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists.data_manipulation import unique_type_objects
from pyutils.pandas_data_frames import data_frame_handler
from pyutils.parameters_and_constants.global_parameters import basic_time_format_strs
from pyutils.strings.string_handler import modify_obj_specs
from pyutils.time_handling.date_and_time_utils import find_time_key, infer_frequency
from pyutils.utilities.introspection_utils import get_obj_type_str

# Create aliases #
#----------------#

insert_row_in_df = data_frame_handler.insert_row_in_df
save2csv = data_frame_handler.save2csv
save2excel = data_frame_handler.save2excel

#------------------#
# Define functions #
#------------------#

# Calendar standardizers #
#------------------------#

def standardize_calendar(obj,
                         file_path,
                         interpolation_method=None,
                         order=None,
                         save_as_new_obj=False, 
                         extension=None, 
                         separator=",",
                         save_index=False,
                         save_header=False):
    
    """
    **Global note** 
    ---------------
    
    Function to standardize the calendar of an object 
    (pandas.DataFrame, xarray.Dataset, or xarray.DataArray)
    to the Gregorian calendar and perform interpolations for missing data along rows (axis=0).
    This need arises when modelled atmospheric or land data is considered,
    when each model has its own calendar.
    This funcion is useful when several model data is handled at once.

    To this day, taking account the structure of the modules
    and practicity and cleanliness of this function,
    module patterns from the subpackage 'xarray_utils' will only be imported here
    together with xarray.    
    
    Parameters
    ----------
    obj : pandas.DataFrame or xarray.Dataset or xarray.DataArray or list of them.
        Object containing data. If it is a pd.DataFrame, the first column must be of type datetime64.
    file_path : str or list of str
        String referring to the file name from which the data object has been extracted.
    interpolation_method : str, optional
        Interpolation method to use for filling missing data. Examples: 'linear', 'polynomial'.
    order : int, optional
        Order of the interpolation if a polynomial or spline method is chosen.
    save_as_new_obj : bool, optional
        If True, saves the standardized object as a CSV, Excel, or NetCDF file.
    extension : str, optional
        Extension of the file to save the standardized object. Options are "csv", "xlsx", and "nc".
    separator : str, optional
        Separator used for CSV files. Default is ','.
    save_index : bool, optional
        Whether to save the index when saving the object. Default is False.
    save_header : bool, optional
        Whether to include headers when saving the object. Default is False.

    Returns
    -------
    obj : pandas.DataFrame or xarray.Dataset or xarray.DataArray
        Object with the standardized calendar and interpolated missing data.
    
    Note
    ----
    There is no programatic way to store multiple sheets on a CSV file,
    as can be done with Excel files, because CSV is rough, old format
    but mainly for data transport.
    """

    obj_type = get_obj_type_str(obj).lower()
    
    # Handling pandas dataframes #
    #----------------------------#    
    
    if (obj_type == "pandas" \
        or (obj_type == "list" \
        and all(get_obj_type_str(element) == "dataframe") for element in obj)):

        if not isinstance(obj, list) and not isinstance(obj, np.ndarray):
            obj = [obj]
            
        if not isinstance(file_path, list) and not isinstance(file_path, np.ndarray):
            file_path = [file_path]
            
        obj_std_calendar = []
        len_objects = len(obj)
            
        # Check whether all objects passed in a list are of the same type #
        len_unique_type_list = unique_type_objects(obj)[-1]
        
        if len_unique_type_list > 1:
            raise ValueError("Not every object in the list is of the same type.")
            
        else:
            """It is supposed that every component is of the same type"""
            if isinstance(obj[0], pd.DataFrame):
                
                for (obj_num, obj), fp in zip(enumerate(obj), file_path):
                    
                    # Get the date key and time frequency #
                    time_col = find_time_key(obj)
                    time_freq = infer_frequency(obj.loc[:10,time_col])
                    
                    # Get the time array with possible missing datetimes #
                    time_shorter = obj.loc[:,time_col]
                    time_shorter_arr = np.array(time_shorter)
                    ltm = len(time_shorter)
                   
                    # Construct full time array to compare with the previous array #
                    first_datetime = obj.iloc[0, 0]
                    last_datetime = obj.iloc[-1, 0]
                    
                    full_times = pd.date_range(first_datetime,
                                               last_datetime, 
                                               freq=time_freq)
                    lft = len(full_times)
                    
                    data_frames_remaining = len_objects - (obj_num+1) 
                    print(f"Data frames remaining: {data_frames_remaining}")
                    
                    # Compare both time arrays, even if they have the same length #
                    if ltm != lft:
                        for ft in full_times:
                            if ft not in time_shorter_arr:
                                
                                """Previous day of the missing date-time (indexing)"""
                                missing_date_yesterday\
                                = ft - datetime.timedelta(days=1)
                                index_yesterday\
                                = obj[obj[time_col]==missing_date_yesterday].index
                                
                                """Actual missing time"""
                                index_missing_time = int((index_yesterday + 1).to_numpy())
                                
                                missing_datetime\
                                = missing_date_yesterday + datetime.timedelta(days=1)
                                
                                """Define values to insert"""
                                values = np.append(missing_datetime,
                                                   np.repeat(np.nan, len(obj.columns[1:])))
                                
                                insert_row_in_df(obj, index_missing_time, values=values)
                    
                        # Reorder the data frame indices #
                        obj = obj.sort_index().t_reset_index(drop=True)
                        obj.iloc[:, 1:] = obj.iloc[:, 1:].astype('d')
                                        
                        # Perform the interpolation, if requested #
                        if interpolation_method is not None:
                            
                            if (interpolation_method in supported_interpolation_methods)\
                            and order is None:
                                raise ValueError("Please specify and order for the "
                                                  "interpolation method "
                                                  f"{interpolation_method}")
                        
                            # Fill the missing data as a   #
                            # consequence of missing dates #
                            print("Filling the missing data "
                                  "as a consequence of missing dates...")
                            
                            obj.iloc[:, 1:]\
                            = obj.iloc[:, 1:].interpolate(method=interpolation_method,
                                                          order=order)
                            
                    obj_std_calendar.append(obj)
        
                    # Save the object either as Excel or CSV document #
                    if save_as_new_obj:
                        
                        obj2change = "name_noext"
                        str2add = "_std_calendar"
                        
                        saving_file_name = modify_obj_specs(fp,
                                                            obj2change,
                                                            new_obj=None,
                                                            str2add=str2add)
                        
                        if extension == "csv":        
                            
                            print("Saving data into a CSV document...")
                            save2csv(saving_file_name,
                                     obj,
                                     separator,
                                     save_index,
                                     save_header,
                                     date_format=basic_time_format_strs[time_freq])
                            
                        elif extension == "xlsx":
                            
                            frame_dict = {}
                            obj_cols = obj.columns
                            
                            for grid_col in obj_cols[1:]:
                                
                                excel_sheet_name = grid_col
                                frame_dict[excel_sheet_name]\
                                = obj.loc[:, [time_col, grid_col]]
                                
                                print("Writing and storing data "
                                      "into an excel document...")
                                save2excel(saving_file_name,
                                           frame_dict,
                                           save_index,
                                           save_header)
            
                        else:
                            raise ValueError("Unsupported file extension . "
                                             "Options for a Pandas data frame "
                                             f"are {supported_file_exts_pandas}.")
                            
        return obj_std_calendar
    
    # Handling xarray datasets or data arrays #
    #-----------------------------------------#
    
    # !!! Created by ChatGPT following pandas.DataFrame logic
    
    elif (obj_type in ["dataarray", "dataset"]\
          or (obj_type == "list" and all(get_obj_type_str(element) in ["dataarray", "dataset"]
                                         for element in obj))):
        
        # Import module and custom modules here by convenience #
        #------------------------------------------------------#
        
        import xarray as xr
        from pyutils.utilities.xarray_utils.patterns import find_time_dimension
        
        if isinstance(obj, list):
            obj = obj[0]  # assuming only one object passed

        time_dim = find_time_dimension(obj)
        full_times = xr.cftime_range(start=obj[time_dim][0].values,
                                     end=obj[time_dim][-1].values,
                                     freq=infer_frequency(obj[time_dim]))

        obj_std_calendar = obj.reindex({time_dim: full_times}, method=None)  # aligning with the full time range
        
        if interpolation_method:
            obj_std_calendar = obj_std_calendar.interpolate_na(dim=time_dim, method=interpolation_method)
            if interpolation_method in supported_interpolation_methods and order is not None:
                obj_std_calendar = obj_std_calendar.polyfit(dim=time_dim, deg=order)

        # Saving object if required
        if save_as_new_obj:
            obj2change = "name_noext"
            str2add = "_std_calendar"
            saving_file_name = modify_obj_specs(file_path, obj2change, new_obj=None, str2add=str2add)

            if extension == "nc":
                print("Saving data into a NetCDF document...")
                obj_std_calendar.to_netcdf(saving_file_name)
            else:
                raise ValueError(f"Unsupported file extension {extension} for xarray objects.")

    else:
        raise TypeError("Unsupported object type. "
                        "Please provide a pandas DataFrame, xarray Dataset, or xarray DataArray.")
    
    return obj_std_calendar


# Leap years #
#------------#

def leap_year_detector(start_year, end_year, return_days=False):
    """
    Detects leap years in a given range or returns the number of days in each year of the range.

    This function can return a dictionary indicating whether each year in the range is a leap year, or 
    return the number of days in each year, depending on the 'return_days' flag.

    Parameters
    ----------
    start_year : int or str
        The start year of the range (inclusive). Can be a string representing the year.
    end_year : int or str
        The end year of the range (inclusive). Can be a string representing the year.
    return_days : bool, optional
        If True, return the number of days in each year. Otherwise, return a dictionary
        with leap year status for each year in the range (default is False).

    Returns
    -------
    dict or list
        - If return_days is False: A dictionary where the keys are years from start_year to end_year, 
          and the values are booleans (True if the year is a leap year, otherwise False).
        - If return_days is True: A list of the number of days for each year in the range.
    """
    
    # Ensure input years are integers
    start_year = int(start_year)
    end_year = int(end_year)
    
    # Return number of days in each year if requested
    if return_days:
        days_per_year = [len(pd.date_range(f'{year}', f'{year+1}', inclusive="left"))
                         for year in range(start_year, end_year+1)]
        return days_per_year
    
    # Otherwise, return a dictionary with leap year status
    leap_years = {year: calendar.isleap(year) for year in range(start_year, end_year+1)}
    return leap_years

        
        
def nearest_leap_year(year):
    """
    Finds the nearest leap year to a given year.

    If the given year is not a leap year, this function will search for the closest leap year 
    within a range of four years before or after the input year. If there are two equally 
    distant leap years, both are returned.

    Parameters
    ----------
    year : int
        The year for which to find the nearest leap year.

    Returns
    -------
    int or str
        The nearest leap year. If two leap years are equally close, a string with both years is returned.
    """
    
    if leap_year_detector(year, year)[year]:
        return year

    # Search range of years within 4 years before and after the given year
    for offset in range(1, 5):
        if calendar.isleap(year - offset):
            return year - offset
        elif calendar.isleap(year + offset):
            return year + offset

    return f"No nearby leap year found in the given range for year {year}"  # This case should be rare


# Date/time ranges #
#------------------#

def week_range(date):
    """
    Finds the first and last date of the week for a given date.
    
    This function calculates the range of the week (Monday to Sunday) 
    where the given date falls, based on ISO calendar conventions.
    
    In this convention, the day of the week ('dow' === 'day of week') 
    is 'Mon' = 1, ... , 'Sat' = 6, 'Sun' = 7.
    
    Parameters
    ----------
    date : datetime.date, datetime.datetime, np.datetime64, pd.Timestamp.
         The date for which the week range is calculated. Supports standard Python 
         date/datetime objects, pandas Timestamps, and numpy datetime64 types.

    Returns
    -------
    tuple
        A tuple containing two pd.Timestamp objects:
        - start_date: The first day of the week (Monday).
        - end_date: The last day of the week (Sunday).

    Raises
    ------
    ValueError
        If the provided date is not a pandas Timestamp object.
    """
    
    if isinstance(date, (datetime.date, datetime.datetime, np.datetime64, pd.Timestamp)):
        dow = date.isocalendar().weekday
        
        # Calculate the start of the week (Monday)
        start_date = date - pd.Timedelta(days=dow - 1)
        
        # Calculate the end of the week (Sunday)
        end_date = start_date + pd.Timedelta(days=6)
        
        return (start_date, end_date)
    else:
        raise TypeError("Unsupported data type",
                        "The date provided must be a datetime.date, datetime.datetime, "
                        "np.datetime64 or pd.Timestamp object.")


#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported file extensions for calendar standardizations #
supported_file_exts_pandas = ['csv', 'xlsx']

# Supported interpolation methods #
supported_interpolation_methods = ["polynomial", "spline"]