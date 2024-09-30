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
from pyutils.utilities.introspection_utils import get_caller_method_args, get_obj_type_str
from pyutils.weather_and_climate.netcdf_handler import find_time_dimension

# Create aliases #
#----------------#

count_consecutive = patterns.count_consecutive
decompose_24h_cumulative_data = data_manipulation.decompose_24h_cumulative_data

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
    """
    
    # Input validation block #
    #-#-#-#-#-#-#-#-#-#-#-#-#-
    
    all_arg_names = get_caller_method_args()
    seas_months_arg_pos = find_substring_index(all_arg_names, "season_months")
    
    obj_type = get_obj_type_str(obj).lower()
    seas_mon_arg_type = get_obj_type_str(season_months)
    
    if statistic not in statistics:
        arg_tuple_stat = ("statistic", statistic, statistics)
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
    if obj_type == "dataframe":
        date_key = find_date_key(obj)
    else:
        date_key = find_time_dimension(obj)

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
        The normalized autocorrelation values. If `twosided` is False, 
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
    
    # Normalize the autocorrelation values
    x_autocorr /= np.max(x_autocorr)
    
    # Return two-sided or one-sided autocorrelation
    return x_autocorr if twosided else x_autocorr[len(x_autocorr) // 2:]

    
# Signal analysis #
#-----------------#

# Forcing #
#~~~~~~~~~#

# Noise handling #
#-#-#-#-#-#-#-#-#-
    
def signal_whitening(data, method="classic"):
    """
    Function to perform signal whitening (decorrelation) on the input data.

    Parameters
    ----------
    data : numpy.ndarray
        The input signal data that requires whitening. It should be a 1D or 2D array.
    method : str, optional
        The whitening method to apply. Supported options are:
        - "classic": Uses the covariance matrix method to decorrelate the data.
        - "sklearn": Uses PCA (Principal Component Analysis) for whitening via sklearn.
        - "zca": Uses ZCA whitening which is a form of whitening that retains
          more resemblance to the original data.

    Returns
    -------
    whitened_data : numpy.ndarray
        The whitened version of the input data.
    
    Notes
    -----
    - Classic whitening: It ensures that the data has unit variance, and no correlations between dimensions.
    - sklearn whitening: This uses PCA from the sklearn library to perform decorrelation.
    - ZCA whitening: Zero Component Analysis whitening retains data structure while decorrelating.
    """
    
    from scipy import linalg
    from sklearn.decomposition import PCA
    
    # Classic whitening method using covariance matrix
    if method == "classic":
        data_mean = data - np.mean(data, axis=0)
        cov_matrix = np.cov(data_mean, rowvar=False)
        eigvals, eigvecs = linalg.eigh(cov_matrix)
        whitening_matrix = eigvecs @ np.diag(1.0 / np.sqrt(eigvals)) @ eigvecs.T
        whitened_data = data_mean @ whitening_matrix
        return whitened_data
    
    # Whitening using PCA from sklearn
    elif method == "sklearn":
        pca = PCA(whiten=True)
        whitened_data = pca.fit_transform(data)
        return whitened_data
    
    # ZCA whitening
    elif method == "zca":
        data_mean = data - np.mean(data, axis=0)
        cov_matrix = np.cov(data_mean, rowvar=False)
        eigvals, eigvecs = linalg.eigh(cov_matrix)
        whitening_matrix = eigvecs @ np.diag(1.0 / np.sqrt(eigvals)) @ eigvecs.T
        zca_whitening_matrix = eigvecs @ np.diag(np.sqrt(eigvals)) @ eigvecs.T
        whitened_data = data_mean @ zca_whitening_matrix
        return whitened_data
    
    else:
        arg_tuple_white_noise = ("whitening method", method, signal_forcing_methods)
        raise ValueError(format_string(unsupported_option_error_str, arg_tuple_white_noise))
        
# Filtering #
#~~~~~~~~~~~#

def low_pass_filter(data, window_size=3):
    """
    Applies a simple moving average (SMA) low-pass filter to the input data.
    
    This method smooths the input signal by averaging over a sliding window,
    effectively filtering out high-frequency noise.
    
    Parameters
    ----------
    data : array-like
        The input time series data to be filtered.
    window_size : int, optional, default=3
        The size of the moving window over which to average the signal.
        A larger window will provide more smoothing but may reduce important signal details.
        
    Returns
    -------
    filtered_data : np.ndarray
        The filtered time series with reduced high-frequency noise.
    
    Notes
    -----
    The simple moving average filter is a basic low-pass filter
    and is useful for removing short-term fluctuations in data.
    """
    
    if window_size < 1:
        raise ValueError("Window size must be a positive integer.")
    
    window = np.ones(window_size) / window_size
    filtered_data = np.convolve(data, window, mode='valid')
    
    return filtered_data


def high_pass_filter(data):
    """
    Applies a simple high-pass filter by taking the difference between consecutive points in the time series.
    
    This method is useful for extracting high-frequency components and removing slow trends from the data.
    
    Parameters
    ----------
    data : array-like
        The input time series data to be filtered.
    
    Returns
    -------
    filtered_data : np.ndarray
        The high-pass filtered data, emphasizing rapid changes and removing slow trends.
    
    Notes
    -----
    High-pass filtering is used to isolate high-frequency changes in the data,
    which can be useful for detecting sudden events or fluctuations.
    """
    
    filtered_data = np.diff(data, n=1)
    return filtered_data


def band_pass1(original, timestep, low_freq, high_freq):
    """
    Band-pass filter, method 1.

    This filter works in the frequency domain by selecting a desired frequency range
    and zeroing out the Fourier coefficients for frequencies outside that range.

    The signal is then converted back to the time domain.

    Parameters
    ----------
    original : np.ndarray
        The original time series data to be filtered.
    timestep : float
        Time step between successive data points in the time series.
    low_freq : float
        The lower frequency bound for the band-pass filter.
    high_freq : float
        The upper frequency bound for the band-pass filter.

    Returns
    -------
    band_filtered : np.ndarray
        The band-pass filtered signal in the time domain.

    Notes
    -----
    This method processes the data entirely in the frequency domain. 
    Do not work directly with the time-domain signal.
    """

    # Convert original time series to frequency domain
    fourier_orig = np.fft.fft(original)
    n = len(fourier_orig)

    # Get the corresponding frequency values
    freqs_orig = np.fft.fftfreq(n, timestep)

    # Create a mask for the desired frequency range
    freq_mask = (freqs_orig >= low_freq) & (freqs_orig <= high_freq)

    # Zero out Fourier coefficients outside the desired frequency range
    new_fourier = np.zeros_like(fourier_orig)
    new_fourier[freq_mask] = fourier_orig[freq_mask]

    # Convert the filtered signal back to the time domain
    band_filtered = np.real(np.fft.ifft(new_fourier))
    return band_filtered


def band_pass2(original, low_filtered_all_highfreq, low_filtered_all_lowfreq):
    """
    Band-pass filter, method 2.

    This filter creates a band-pass filter by subtracting the results of 
    two low-pass filters: one with a higher cutoff frequency and another
    with a lower cutoff frequency.

    Parameters
    ----------
    original : np.ndarray
        The original time series data to be filtered.
    low_filtered_all_highfreq : np.ndarray
        The result of applying a low-pass filter with a higher cutoff frequency.
    low_filtered_all_lowfreq : np.ndarray
        The result of applying a low-pass filter with a lower cutoff frequency.

    Returns
    -------
    band_filtered : np.ndarray
        The band-pass filtered signal in the time domain.

    Notes
    -----
    This method requires pre-filtered signals using low-pass filters.
    """

    # Convert time series and low-pass filtered signals to frequency domain
    fourier_orig = np.fft.fft(original)
    fourier_low_high = np.fft.fft(low_filtered_all_highfreq)
    fourier_low_low = np.fft.fft(low_filtered_all_lowfreq)

    # Create the band-pass filter in the frequency domain
    RL1 = fourier_low_high / fourier_orig
    RL2 = fourier_low_low / fourier_orig
    RB = RL1 - RL2

    # Convert the band-pass filtered signal back to time domain
    band_filtered = np.real(np.fft.ifft(RB))
    return band_filtered


def band_pass3(original, low_filtered_all, high_filtered_all):
    """
    Band-pass filter, method 3.

    This filter combines a high-pass filter and a low-pass filter to create
    a band-pass filter. The signal is processed in the frequency domain and
    then converted back to the time domain.

    Parameters
    ----------
    original : np.ndarray
        The original time series data to be filtered.
    low_filtered_all : np.ndarray
        The result of applying a low-pass filter.
    high_filtered_all : np.ndarray
        The result of applying a high-pass filter.

    Returns
    -------
    band_filtered : np.ndarray
        The band-pass filtered signal in the time domain.

    Notes
    -----
    The method works entirely in the frequency domain. Do not manipulate
    the time-domain signal directly.
    """

    # Convert time series and filtered signals to frequency domain
    fourier_orig = np.fft.fft(original)
    fourier_low = np.fft.fft(low_filtered_all)
    fourier_high = np.fft.fft(high_filtered_all)

    # Create the band-pass filter by combining the high-pass and low-pass filters
    RL = fourier_low / fourier_orig
    RH = fourier_high / fourier_orig
    RB = RH * RL

    # Convert the band-pass filtered signal back to time domain
    band_filtered = np.real(np.fft.ifft(RB))
    return band_filtered


#--------------------------#
# Parameters and constants #
#--------------------------#

unsupported_option_error_str = "Unsupported {} '{}'. Options are {}."
season_month_fmt_error_str = """Parameter 'season_months' must contain exactly \
3 integers representing months. For example: [12, 1, 2]."""

# Statistics #
statistics = ["max", "min", "sum", "mean", "std"]

# Time frequency abbreviations #
freq_abbrs = ["Y", "SEAS", "M", "D", "H", "min", "S"]

# Signal forcing #
signal_forcing_methods = ["classic", "sklearn", "zca"]