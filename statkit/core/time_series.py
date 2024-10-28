#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for time series operations in statistical analysis.
"""

#----------------#
# Import modules #
#----------------#

import numpy as np
from pandas import Grouper

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists import patterns, data_manipulation

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.pandas_data_frames.data_frame_handler import find_date_key
from pyutils.strings.information_output_formatters import format_string
from pyutils.strings.string_handler import find_substring_index
from pyutils.filewise.introspection_utils import get_caller_args, get_type_str
from pyutils.filewise.xarray_utils.patterns import find_time_dimension

# Create aliases #
#----------------#

count_consecutive = patterns.count_consecutive
decompose_24h_cumulative_data = data_manipulation.decompose_24h_cumulative_data

#------------------#
# Define functions #
#------------------#

# Statistical Processing #
#------------------------#

def periodic_statkit(obj, statistic, freq,
                        groupby_dates=False,
                        drop_date_idx_col=False,
                        season_months=None):
    """
    Calculates basic statkit (not climatologies) for the given data 
    object over a specified time frequency.

    This function supports data analysis on Pandas DataFrames and 
    xarray objects, allowing for grouping by different time frequencies 
    such as yearly, quarterly, monthly, etc.

    Parameters
    ----------
    obj : pandas.DataFrame or xarray.Dataset or xarray.DataArray
        The data object for which statkit are to be calculated.
    
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
        The computed statkit as a DataFrame or xarray object,
        depending on the type of input data.

    Raises
    ------
    ValueError
        If the specified statistic is unsupported, the frequency is 
        invalid, or if the season_months list does not contain exactly 
        three integers.
    """
    
    # Input validation block #
    #-#-#-#-#-#-#-#-#-#-#-#-#-
    
    param_keys = get_caller_args()
    seas_months_arg_pos = find_substring_index(param_keys, "season_months")
    
    obj_type = get_type_str(obj, lowercase=True)
    seas_mon_arg_type = get_type_str(season_months)
    
    if statistic not in statkit:
        arg_tuple_stat = ("statistic", statistic, statkit)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_stat))
        
    
    if obj_type not in ["dataframe", "dataset", "dataarray"]:
        arg_tuple_obj_type = ("data type",
                              obj_type, 
                              "{pandas.DataFrame, xarray.Dataset, xarray.DataArray}")
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_obj_type))

    if freq not in freq_abbrs:
        arg_tuple_freq = ("frequency", freq, freq_abbrs)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_freq))
    
    if seas_mon_arg_type != "list":
        raise TypeError("Expected a list for parameter 'season_months' "
                        f"(number {seas_months_arg_pos}) got '{seas_mon_arg_type}'.")
    
    if freq == "SEAS" and not season_months:
        raise ValueError("Seasonal frequency requires parameter 'season_months'.")
    
    if season_months and len(season_months) != 3:
        raise ValueError(season_month_fmt_error_str)

    # Operations #
    #-#-#-#-#-#-#-

    # GroupBy Logic
    date_key = find_date_key(obj) if obj_type == "dataframe" else find_time_dimension(obj)

    if obj_type in ["dataset", "dataarray"]:
        groupby_key = f"{date_key}.dt.{freq}"
    else:
        groupby_key = date_key

    # Handling grouping logic
    if groupby_dates and obj_type in ["dataset", "dataarray"]:
        obj_groupby = obj.groupby(groupby_key)
    else:
        obj_groupby = Grouper(key=date_key, freq=freq)

    # Calculate Statistics
    result = getattr(obj_groupby, statistic)()
    if obj_type == "dataframe":
        result.reset_index(drop=drop_date_idx_col)
    
    return result


def hourly_ts_cumul(array, zero_threshold, zeros_dtype='d'):    
    """
    Obtain the 1-hour time step cumulative data by subtracting the 
    previous cumulative value from the next.

    Parameters
    ----------
    array : numpy.ndarray
        Time-series array (first index corresponds to time).
    zero_threshold : float
        Values below this threshold are considered unrealistic and set to zero.
    zeros_dtype : str or numpy type, optional
        Data type of the resulting zero array, by default 'd' (double-precision float).

    Returns
    -------
    hour_ts_cumul : numpy.ndarray
        Array of 1-hour time step cumulative data with unrealistic edges set to zero.
    """
    
    
    hour_ts_data = decompose_24h_cumulative_data(array)  # Apply your decomposition logic
    unmet_case_values = np.zeros_like(array, dtype=zeros_dtype)

    hour_ts_cumul = np.where(np.all(hour_ts_data >= zero_threshold, axis=1),
                                 hour_ts_data, unmet_case_values)
    
    return hour_ts_cumul


def consec_occurrences_maxdata(array,
                               max_threshold,
                               min_consec=None,
                               calc_max_consec=False):
    
    """
    Count the occurrences where values exceed a threshold,
    with an option to calculate the longest consecutive occurrences.

    Parameters
    ----------
    array : numpy.ndarray or pandas.Series
        Input array with maximum value data.
    max_threshold : float
        Threshold for counting occurrences.
    min_consec : int, optional
        Minimum number of consecutive occurrences.
    calc_max_consec : bool, optional
        If True, returns the maximum length of consecutive occurrences.
        Defaults to False.

    Returns
    -------
    int
        Number of occurrences or max length of consecutive occurrences 
        based on input parameters.
    """
    
    above_idx = array > max_threshold
    
    if min_consec is None:
        if calc_max_consec:
            return count_consecutive(above_idx, True) or 0
        return np.count_nonzero(above_idx)

    # Handle cases with a minimum number of consecutive occurrences
    block_idx = \
    np.flatnonzero(np.convolve(above_idx, np.ones(min_consec, dtype=int), mode='valid') >= min_consec)
    consec_nums = count_consecutive(block_idx)

    if consec_nums:
        return len(consec_nums) * min_consec + sum(consec_nums)
    return 0
    
    
def consec_occurrences_mindata(array, min_thres, 
                               threshold_mode="below", 
                               min_consec=None, 
                               calc_min_consec=False):
    """
    Count the occurrences where values are below or above a threshold,
    with an option to calculate the longest consecutive occurrences.

    Parameters
    ----------
    array : numpy.ndarray or pandas.Series
        Input array with minimum value data.
    min_thres : float
        Threshold for counting occurrences.
    threshold_mode : {"below", "above"}, optional
        Whether to count values below or above the threshold. Defaults to "below".
    min_consec : int, optional
        Minimum number of consecutive occurrences.
    calc_min_consec : bool, optional
        If True, returns the maximum length of consecutive occurrences.
        Defaults to False.

    Returns
    -------
    int
        Number of occurrences or max length of consecutive occurrences based on input parameters.
    """
    
    if threshold_mode not in {"below", "above"}:
        raise ValueError("Invalid threshold mode. Choose one from {'below', 'above'}.")

    above_idx = array < min_thres if threshold_mode == "below" else array > min_thres

    if min_consec is None:
        if calc_min_consec:
            return count_consecutive(above_idx, True) or 0
        return np.count_nonzero(above_idx)

    block_idx = \
    np.flatnonzero(np.convolve(above_idx, np.ones(min_consec, dtype=int), mode='valid') >= min_consec)
    consec_nums = count_consecutive(block_idx)

    if consec_nums:
        return len(consec_nums) * min_consec + sum(consec_nums)
    return 0


# Correlations #
#--------------#

def autocorrelate(x, twosided=False):
    """
    Computes the autocorrelation of a time series.

    Autocorrelation measures the similarity between a time series and a 
    lagged version of itself. This is useful for identifying repeating 
    patterns or trends in data, such as the likelihood of future values 
    based on current trends.

    Parameters
    ----------
    x : list or numpy.ndarray
        The time series data to autocorrelate.
    twosided : bool, optional, default: False
        If True, returns autocorrelation for both positive and negative 
        lags (two-sided). If False, returns only non-negative lags 
        (one-sided).

    Returns
    -------
    numpy.ndarray
        The normalised autocorrelation values. If `twosided` is False, 
        returns only the non-negative lags.

    Notes
    -----
    - This function uses `numpy.correlate` for smaller datasets and 
      `scipy.signal.correlate` for larger ones.
    - Be aware that NaN values in the input data must be removed before 
      computing autocorrelation.
    - For large arrays (> ~75000 elements), `scipy.signal.correlate` is 
      recommended due to better performance with Fourier transforms.
    """
    from scipy.signal import correlate

    # Remove NaN values and demean the data
    x_nonan = x[~np.isnan(x)]
    x_demean = x_nonan - np.mean(x_nonan)
    
    if len(x_demean) <= int(5e4):
        x_autocorr = np.correlate(x_demean, x_demean, mode="full")
    else:
        x_autocorr = correlate(x_demean, x_demean)
    
    # Normalise the autocorrelation values
    x_autocorr /= np.max(x_autocorr)
    
    # Return two-sided or one-sided autocorrelation
    return x_autocorr if twosided else x_autocorr[len(x_autocorr) // 2:]


#--------------------------#
# Parameters and constants #
#--------------------------#

# Statistics #
statkit = ["max", "min", "sum", "mean", "std"]

# Time frequency abbreviations #
freq_abbrs = ["Y", "SEAS", "M", "D", "H", "min", "S"]

# Preformatted strings #
#----------------------#

unsupported_option_error_str = "Unsupported {} '{}'. Options are {}."
season_month_fmt_error_str = """Parameter 'season_months' must contain exactly \
3 integers representing months. For example: [12, 1, 2]."""
