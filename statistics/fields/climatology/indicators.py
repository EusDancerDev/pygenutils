#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists import data_manipulation, patterns
from pyutils.statistics.core.time_series import consec_occurrences_mindata, consec_occurrences_maxdata

# Create aliases #
#----------------#

select_elements = data_manipulation.select_elements
count_consecutive = patterns.count_consecutive

#------------------#
# Define functions #
#------------------#

# Atmospheric variables #
#-----------------------#

def calculate_WSDI(season_daily_tmax, tmax_threshold, min_consec_days):
    """
    Function that calculates the WSDI (Warm Spell Duration Index).
    
    Input data
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
          Daily maximum temperature data of the corresponding season in units ºC.
    tmax_threshold : float
          Upper limit of the maximum temperature.
    min_consec_days : int
          Minimum consecutive days number.
    
    Returns
    -------
    int
        Number of total days where at least a specified number of
        consecutive days exceeds certain percentile as a threshold.
    """
    return consec_occurrences_maxdata(season_daily_tmax, tmax_threshold, min_consec_days)


def calculate_SU(season_daily_tmax, tmax_threshold=25):
    """
    Function that calculates the SU (Summer Days).
    
    Parameters
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
        Daily maximum temperature data of the corresponding season in units ºC.
    
    tmax_threshold : float
        Upper limit of the maximum temperature in units ºC. Default is 25ºC.
    
    Returns
    -------
    int
        Number of days in which the
        maximum temperature has risen above the threshold.
    """
    return consec_occurrences_maxdata(season_daily_tmax, tmax_threshold)


def calculate_CSU(season_daily_tmax, tmax_threshold=25):
    """
    Function that calculates the CSU (Consecutive Summer Days).
    
    Parameters
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
        Daily maximum temperature data of the season in units ºC.
    
    tmax_threshold : float
        Upper limit of the maximum temperature in units ºC. Default is 25ºC.
    
    Returns
    -------
    int
        Number of maximum consecutive days in which
        the temperature has risen above the threshold.
    """
    return consec_occurrences_maxdata(season_daily_tmax,
                                          tmax_threshold,
                                          min_consec_days=None,
                                          max_consecutive_days=True)


def calculate_FD(season_daily_tmin, tmin_threshold=0):
    """
    Function that calculates the FD (Frost Days).
    
    Parameters
    ----------
    season_daily_tmin : numpy.ndarray or pandas.Series
        Daily minimum temperature data of the corresponding season in units ºC.
    
    tmin_threshold : float
        Upper limit of the minimum temperature in units ºC. Defaults to 0ºC.
    
    Returns
    -------
    int
        Number of days in which the
        minimum temperature has fallen below the threshold.
    """
    return consec_occurrences_mindata(season_daily_tmin, tmin_threshold)


def calculate_TN(season_daily_tmin, tmin_threshold=20):
    """
    Function that calculates the TN (Tropical Night Days).
    
    Parameters
    ----------
    season_daily_tmin : numpy.ndarray or pandas.Series
        Daily minimum temperature data of the corresponding season in units ºC.
    
    tmin_threshold : float
        Lower limit of the minimum temperature in units ºC. Default is 20ºC.
    
    Returns
    -------
    int
        Number of nights in which the
        minimum temperature has risen above the threshold.
    """
    return consec_occurrences_mindata(season_daily_tmin,
                                          tmin_threshold,
                                          threshold_mode="above")


def calculate_RR(season_daily_precip, precip_threshold):
    """
    Function that calculates the RR parameter (Wet Days).
    It is defined as the number of days in which the precipitation
    amount exceeds 1 mm.
    
    Parameters
    ----------
    season_daily_precip : numpy.ndarray or pandas.Series
        Daily precipitation data of the corresponding season in units mm.
    
    precip_threshold : float
        Upper limit of the daily precipitation, 1 mm in this case.
    
    Returns
    -------
    int
        Number of days in which the
        precipitation has risen above the threshold.   
    """
    return consec_occurrences_maxdata(season_daily_precip, precip_threshold)


def calculate_CWD(season_daily_precip, precip_threshold):
    """
    Function that calculates the CWD (Consecutive Wet Days),
    i.e. the number of maximum consecutive days in which
    the precipitation amount exceeds 1 mm.
    
    Parameters
    ----------
    season_daily_precip : numpy.ndarray or pandas.Series
        Daily precipitation data of the season in units mm.
    
    precip_threshold : float
        Upper limit of the daily precipitation, 1 mm in this case.
    
    Returns
    -------
    int
        Number of maximum consecutive days in which
        the precipitation has risen above the threshold.
    """
    return consec_occurrences_maxdata(season_daily_precip,
                                          precip_threshold,
                                          min_consec_days=None,
                                          max_consecutive_days=True)


# TODO: ChatGPT optimizazioa
def calculate_HWD(tmax_array, tmin_array,
                  max_threshold, min_threshold,
                  date_array, min_consec_days):
    """
    Function that returns the total days of heat waves (HWD === Heat Wave Days),
    based on daily data.
    A heat wave is defined such that at least in N consecutive days
    the maximum temperature exceeds its 95th percentile
    and the minimum temperature exceeds it 90th percentile.
    
    Each heat wave is assocciated with the following:
    
    -Heat wave intensity : maximum temperature registered during the heat wave,
                           i.e. the event satisfying the conditions aforementioned.
    -Heat wave duration : number of consecutive days of the heat wave.
    -Heat wave global intensity : sum of the maximum temperatures registered
                                  during the heat wave,
                                  divided by its duration.
    
    Parameters
    ----------
    tmax_array : numpy.ndarray or pandas.Series
        An array which contains the daily maximum temperature data.
    tmin_array : numpy.ndarray or pandas.Series
        An array which contains the daily minimum temperature data.
    max_threshold : float
        Upper limit.
    min_threshold : float
        Lower limit.
    date_array : pandas.DatetimeIndex
        Array containing dates, in this case of the corresponding season.
    min_consec_days : int
        Minimum consecutive days number.
    
    Returns
    -------
    tuple
        hwd_characteristics : numpy.ndarray composed of tuples
            All heat wave events,
            each with its characteristics englobed in a tuple.
        hwd : int 
            Total number of heat wave events.
    """
    N = min_consec_days
    satisfied_thres_bool_arr = (tmax_array > max_threshold) * (tmin_array > min_threshold)
           
    hwd_characteristics = []
    hwd = 0 

    block_consecutive_idx = np.flatnonzero(
                            np.convolve(satisfied_thres_bool_arr,
                                        np.ones(N, dtype=int),
                                        mode='valid')>=N)
    
    
    consec_nums_on_consecutive_idx = count_consecutive(block_consecutive_idx)
    
    if consec_nums_on_consecutive_idx and len(consec_nums_on_consecutive_idx) >= 1:
        
        hw_events_NdayMultiply = consec_nums_on_consecutive_idx.copy()
                
        for i in range(len(hw_events_NdayMultiply)):
            hw_event_partial = block_consecutive_idx[:hw_events_NdayMultiply[i]]

            hw_event = np.unique(np.append(hw_event_partial,
                                           np.arange(hw_event_partial[-1],
                                                     hw_event_partial[-1]+N)))
            
            hw_event_MaxTemps = tmax_array[hw_event]
    
            hw_event_global_intensity = sum(hw_event_MaxTemps) / len(hw_event)
            hw_event_duration = len(hw_event)
            hw_event_intensity = np.max(hw_event_MaxTemps)
            
            hw_event_characteristics = (hw_event_duration,
                                        hw_event_global_intensity,
                                        hw_event_intensity,
                                        date_array[hw_event[0]])
            
            hwd_characteristics.append(hw_event_characteristics)
            hwd += hw_event_characteristics[0]
            idx_to_delete = [idx[0] for idx in enumerate(hw_event_partial)]
    
            block_consecutive_idx = np.delete(block_consecutive_idx,
                                              idx_to_delete)

        return (hwd_characteristics, hwd)
        
    else:
        hwd_characteristics = (0, None, None, None)
        return (hwd_characteristics, 0)
