#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Time-related utilities that are independent of other packages.
"""

#----------------#
# Import modules #
#----------------#

import xarray as xr

#------------------------#
# Import project modules #
#------------------------#

from filewise.general.introspection_utils import get_type_str

#------------------#
# Define functions #
#------------------#

def find_time_key(data):
    """
    Function that searches for the date/time key in various data structures.
    Supports both exact matches and partial matches with common time-related terms.

    Parameters
    ----------
    data : pandas.DataFrame, xarray.Dataset, xarray.DataArray, or str
        The input data structure to search for time-related keys:
        - For pandas DataFrame: searches column names
        - For xarray Dataset/DataArray: searches dimensions and variables
        - For str: assumes it's a file path and opens it as xarray Dataset

    Returns
    -------
    str
        The identified time-related key name.

    Raises
    ------
    TypeError
        If the input data type is not supported.
    ValueError
        If no time-related key is found.
    """
    # Common time-related keywords - both full words and prefixes
    time_keywords = {
        'exact': ['time', 'Time', 'TIME', 't', 'T', 'date', 'Date', 'DATE'],
        'prefix': ['da', 'fe', 'tim', 'yy', 't_', 'ti']
    }
    
    def check_exact_match(name):
        """Helper to check for exact matches"""
        return name.lower() in [k.lower() for k in time_keywords['exact']]
    
    def check_prefix_match(name):
        """Helper to check for prefix matches"""
        name_lower = name.lower()
        return any(name_lower.startswith(prefix.lower()) for prefix in time_keywords['prefix'])
    
    # Handle pandas DataFrame
    obj_type = get_type_str(data, lowercase=True)
    if obj_type == "dataframe":
        # Try exact matches first
        df_cols = data.columns.tolist()
        for col in df_cols:
            if check_exact_match(col):
                return col
        
        # Try prefix matches if no exact match found
        for col in df_cols:
            if check_prefix_match(col):
                return col
                
        raise ValueError("No time-related column found in the pandas DataFrame.")
    
    # Handle xarray objects
    elif isinstance(data, (xr.Dataset, xr.DataArray)):
        # First check dimensions
        for dim in data.dims:
            if check_exact_match(dim):
                return dim
            if check_prefix_match(dim):
                return dim
        
        # Then check variables
        for var in data.variables:
            if check_exact_match(var):
                return var
            if check_prefix_match(var):
                return var
                
        raise ValueError("No time-related dimension or variable found in the xarray object.")
    
    # Handle string (assumed to be file path)
    elif isinstance(data, str):
        try:
            ds = xr.open_dataset(data)
            try:
                time_key = find_time_key(ds)
                return time_key
            finally:
                ds.close()
        except Exception as e:
            raise ValueError(f"Could not find time dimension in file {data}: {e}")
    
    else:
        raise TypeError("Unsupported data type. Must be pandas DataFrame, "
                       "xarray Dataset/DataArray, or file path string.")