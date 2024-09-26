#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import pandas as pd
import scipy.stats as ss

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists import data_manipulation, array_numerical_operations
from pyutils.global_parameters import common_delim_list
from pyutils.meteorological_variables import meteorological_wind_direction
from pyutils.string_handler import find_substring_index
from pyutils.weather_and_climate import climate_statistics, \
                                        climatic_signal_modulators, \
                                        consecutive_idx_statistics

# Create aliases #
#----------------#

select_array_elements = data_manipulation.select_array_elements
sort_array_rows_by_column = data_manipulation.sort_array_rows_by_column
remove_elements = data_manipulation.remove_elements

count_consecutive = array_numerical_operations.count_consecutive

periodic_statistics = climate_statistics.periodic_statistics
window_sum = climate_statistics.window_sum

evaluate_polynomial = climatic_signal_modulators.evaluate_polynomial
polynomial_fitting_coefficients = \
climatic_signal_modulators.polynomial_fitting_coefficients


count_consecutive_days_maxdata\
= consecutive_idx_statistics.count_consecutive_days_maxdata
count_consecutive_days_mindata\
= consecutive_idx_statistics.count_consecutive_days_mindata

#-------------------------#
# Define custom functions #
#-------------------------#

def calculate_biovars(tmax_monthly_climat, 
                      tmin_monthly_climat, 
                      prec_monthly_climat):
    
    """
    Function that calculates 19 bioclimatic variables
    based on already monthly climatologic data, for every horizontal grid point.
    
    Parameters
    ----------
    tmax_monthly_climat : numpy.ndarray
          Array containing the monthly climatologic maximum temperature data.
    tmin_monthly_climat : numpy.ndarray
          Array containing the monthly climatologic minimum temperature data.
    precip_dataset : numpy.ndarray
          Array containing the monthly climatologic precipitation data.
    
    Returns
    -------
    p : numpy.ndarray
          Array containing the bioclimatic data for the considered period.
          structured as (biovariable, lat, lon).
    """

    dimensions = tmax_monthly_climat.shape
    bioclim_var_array = np.zeros((19, dimensions[1], dimensions[2]))
     
    # tavg = (tmin_monthly_climat + tmax_monthly_climat) / 2
    tavg = np.mean((tmax_monthly_climat, tmin_monthly_climat), axis=0)
    range_temp = tmax_monthly_climat - tmin_monthly_climat
      
    # P1. Annual Mean Temperature
    bioclim_var_array[0] = np.mean(tavg, axis=0)
      
    # P2. Mean Diurnal Range(Mean(period max-min))
    bioclim_var_array[1] = np.mean(range_temp, axis=0)
      
    # P4. Temperature Seasonality (standard deviation)
    bioclim_var_array[3] = np.std(tavg, axis=0) # * 100
      
    # P5. Max Temperature of Warmest Period 
    bioclim_var_array[4] = np.max(tmax_monthly_climat, axis=0)
     
    # P6. Min Temperature of Coldest Period
    bioclim_var_array[5] = np.min(tmin_monthly_climat, axis=0)
      
    # P7. Temperature Annual Range (P5 - P6)
    bioclim_var_array[6] = bioclim_var_array[4] - bioclim_var_array[5]
      
    # P3. Isothermality ((P2 / P7) * 100)
    bioclim_var_array[2] = bioclim_var_array[1] / bioclim_var_array[6] * 100
      
    # P12. Annual Precipitation
    bioclim_var_array[11] = np.sum(prec_monthly_climat, axis=0)
      
    # P13. Precipitation of Wettest Period
    bioclim_var_array[12] = np.max(prec_monthly_climat, axis=0)
      
    # P14. Precipitation of Driest Period
    bioclim_var_array[13] = np.min(prec_monthly_climat, axis=0)
    
    # P15. Precipitation Seasonality(Coefficient of Variation) 
    # the "+1" is to avoid strange CVs for areas where the mean rainfall is < 1 mm)
    bioclim_var_array[14] = ss.variation(prec_monthly_climat+1, axis=0) * 100
    
    # precipitation by quarters (window of 3 months)
    wet = window_sum(prec_monthly_climat, N=3)
    
    # P16. Precipitation of Wettest Quarter
    bioclim_var_array[15] = np.max(wet, axis=0)
      
    # P17. Precipitation of Driest Quarter 
    bioclim_var_array[16] = np.min(wet, axis=0)
      
    # temperature by quarters (window of 3 months)
    tmp_qrt = window_sum(tavg, N=3) / 3
      
    # P8. Mean Temperature of Wettest Quarter
    wet_qrt = np.argmax(wet, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[7,i,j] = tmp_qrt[wet_qrt[i,j],i,j]
      
    # P9. Mean Temperature of Driest Quarter
    dry_qrt = np.argmin(wet, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[8,i,j] = tmp_qrt[dry_qrt[i,j],i,j]
    
    # P10 Mean Temperature of Warmest Quarter 
    bioclim_var_array[9] = np.max(tmp_qrt, axis=0)
      
    # P11 Mean Temperature of Coldest Quarter
    bioclim_var_array[10] = np.min(tmp_qrt, axis=0)
          
    # P18. Precipitation of Warmest Quarter 
    hot_qrt = np.argmax(tmp_qrt, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[17,i,j] = wet[hot_qrt[i,j],i,j]
     
    # P19. Precipitation of Coldest Quarter 
    cold_qrt = np.argmin(tmp_qrt, axis=0)
    for i in range(dimensions[1]):
        for j in range(dimensions[2]):
            bioclim_var_array[18,i,j] = wet[cold_qrt[i,j],i,j]
    
    print("Biovariables have been successfully computed")
    return bioclim_var_array


def calculate_WSDI(season_daily_tmax, tmax_threshold, min_consec_days):
    
    """
    Function that calculates the WSDI (Warm Spell Duration Index),
    
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
    WSDI : int
          Number of total days where at least a specified number of
          consecutive days exceeds certain percentile as a threshold.
    """

    WSDI = count_consecutive_days_maxdata(season_daily_tmax,
                                          tmax_threshold,
                                          min_consec_days)

    return WSDI


def calculate_SU(season_daily_tmax, tmax_threshold):
    
    """
    Function that calculates the SU (Summer Days).
    
    Parameters
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
        Daily maximum temperature data of the corresponding season in units ºC.
    
    tmax_threshold : float
        Upper limit of the maximum temperature, preferably 25ºC.
    
    Returns
    -------
    SU : int
        Number of days in which the
        maximum temperature has risen above the threshold.
    """
    
    SU = count_consecutive_days_maxdata(season_daily_tmax, tmax_threshold)

    return SU


def calculate_CSU(season_daily_tmax, tmax_threshold):
    
    """
    Function that calculates the CSU (Consecutive Summer Days).
    
    Parameters
    ----------
    season_daily_tmax : numpy.ndarray or pandas.Series
        Daily maximum temperature data of the season in units ºC.
    
    tmax_threshold : float
        Upper limit of the maximum temperature, preferably 25ºC.
    
    Returns
    -------
    CSU : int
        Number of maximum consecutive days in which
        the temperature has risen above the threshold.
    """
    
    CSU = count_consecutive_days_maxdata(season_daily_tmax,
                                         tmax_threshold,
                                         min_consec_days=None,
                                         calculate_max_consecutive_days=True)

    return CSU


def calculate_FD(season_daily_tmin, tmin_threshold):
    
    """
    Function that calculates the FD (Frost Days).
    
    Parameters
    ----------
    season_daily_tmin : numpy.ndarray or pandas.Series
        Daily minimum temperature data of the corresponding season in units ºC.
    
    tmin_threshold : float
        Upper limit of the minimum temperature, preferably 0ºC.
    
    Returns
    -------
    FD : int
        Number of days in which the
        minimum temperature has fallen below the threshold.
    """
    
    FD = count_consecutive_days_mindata(season_daily_tmin, tmin_threshold)

    return FD


def calculate_TN(season_daily_tmin, tmin_threshold):
    
    """
    Function that calculates the TN (Tropical Night Days).
    
    Parameters
    ----------
    season_daily_tmin : numpy.ndarray or pandas.Series
        Daily minimum temperature data of the corresponding season in units ºC.
    
    tmin_threshold : float
        Lower limit of the minimum temperature, preferably 20ºC.
    
    Returns
    -------
    TN : int
        Number of nights in which the
        minimum temperature has risen above the threshold.
    """
    
    TN = count_consecutive_days_mindata(season_daily_tmin,
                                        tmin_threshold,
                                        threshold_mode="above")
    return TN


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
    RR : int
        Number of days in which the
        precipitation has risen above the threshold.   
    """
    
    RR = count_consecutive_days_maxdata(season_daily_precip, precip_threshold)
    return RR


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
    CWD : int
        Number of maximum consecutive days in which
        the precipitation has risen above the threshold.
    """
    
    CWD = count_consecutive_days_maxdata(season_daily_precip,
                                         precip_threshold,
                                         min_consec_days=None,
                                         calculate_max_consecutive_days=True)

    return CWD


def calculate_HWD(tmax_array, tmin_array,
                  max_threshold, min_threshold,
                  date_array, min_consec_days):
    
    """
    Function that returns the total number of heat waves, based on daily data.
    A heat wave is defined such that at least in N consecutive days
    the maximum temperature exceeds its 95th percentile
    and the minimum temperature exceeds it 90th percentile.
    
    Each heat wave is assocciated with the following:
    
    -Heat wave intensity : maximum temperature registered during the heat wave,
                           i.e. that event satisfying the conditions aforementioned.
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
    HWD_characteristics : numpy.ndarray composed of tuples
        All heat wave events,
        each with its characteristics englobed in a tuple.
    HWD : int 
        Total number of heat wave events.
    """

    N = min_consec_days
    satisfied_thres_bool_arr = (tmax_array > max_threshold) * (tmin_array > min_threshold)
           
    HWD_characteristics = []
    HWD = 0 

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
            
            HWD_characteristics.append(hw_event_characteristics)
            HWD += hw_event_characteristics[0]
            idx_to_delete = [idx[0] for idx in enumerate(hw_event_partial)]
    
            block_consecutive_idx = np.delete(block_consecutive_idx,
                                              idx_to_delete)

        return (HWD_characteristics, HWD)
        
    else:
        HWD_characteristics = (0, None, None, None)
        return (HWD_characteristics, 0)


def calculate_HDY(hourly_df: pd.DataFrame, 
                  varlist: list, 
                  varlist_primary: list, 
                  drop_new_idx_col: bool = False) -> tuple:
    """
    Calculate the Hourly Design Year (HDY) using ISO 15927-4:2005 (E) standard.
    
    Parameters
    ----------
    hourly_df : pd.DataFrame
        DataFrame containing hourly climatological data.
    varlist : list
        List of all variables (column names) to be considered in HDY DataFrame.
    varlist_primary :list
        Primary variables to be used for ranking calculations.
    drop_new_idx_col : bool
        Whether to drop the reset index column.
        
    Returns
    -------
    tuple: HDY DataFrame and the list of selected years for each month.
    """
    # Initialize the HDY DataFrame to store results
    hdy_df = pd.DataFrame(columns=varlist)

    # Extract unique years and months
    hist_years = pd.unique(hourly_df.date.dt.year)
    months = pd.unique(hourly_df.date.dt.month)

    # List to store selected years for each month
    hdy_years = []

    for m in months:
        try:
            # Filter data for the current month and calculate monthly statistics
            hdata_MONTH = hourly_df[hourly_df.date.dt.month == m].filter(items=varlist_primary).reset_index(drop=drop_new_idx_col)
            hdata_MONTH_rank_phi = hdata_MONTH.copy()
            
            # Step a: Calculate daily means for the primary variables
            hdata_MONTH_dm_bymonth = periodic_statistics(hourly_df[hourly_df.date.dt.month == m], varlist_primary, 'day', 'mean')

        except ValueError as e:
            print(f"Error in periodic_statistics for month {m}: {e}")
            continue  # Skip the current month if there’s an error

        # Get unique days for the current month
        no_of_days = len(pd.unique(hdata_MONTH_rank_phi.date.dt.day))

        # Step a: Calculate rankings for each day by each primary variable
        dict_rank = {}
        dict_phi = {}
        
        for var in varlist_primary[1:]:
            var_orig = hdata_MONTH_dm_bymonth[var].to_numpy()
            var_rank = np.argsort(np.argsort(var_orig)) + 1
            dict_rank[var] = var_rank

            # Step b: Calculate cumulative probabilities (phi)
            phi = (var_rank - 0.5) / no_of_days
            dict_phi[var] = phi

            # Store calculated phi values
            hdata_MONTH_rank_phi[var] = phi
        
        # Step c: Group data by year and calculate year-specific ranks
        dict_rank_per_year = {}
        for year in hist_years:
            year_data = hdata_MONTH_rank_phi[hdata_MONTH_rank_phi.date.dt.year == year]
            dict_rank_per_year[year] = {
                var: np.sum(np.abs(year_data[var] - dict_phi[var]))
                for var in varlist_primary[1:]
            }

        # Step d: Calculate total sum of deviations (Fs_sum) for each year
        Fs_sum = {}
        for year, ranks in dict_rank_per_year.items():
            Fs_sum[year] = sum(ranks.values())

        # Step e: Rank the years based on the Fs_sum and choose the best year for the current month
        selected_year = min(Fs_sum, key=Fs_sum.get)
        hdy_years.append(selected_year)

        # Extract the hourly data for the selected year and append it to the HDY DataFrame
        hourly_data_sel = \
        hourly_df[(hourly_df.date.dt.year == selected_year) 
                  & (hourly_df.date.dt.month == m)].filter(items=varlist)\
                 .reset_index(drop=drop_new_idx_col)
        hdy_df = pd.concat([hdy_df, hourly_data_sel], axis=0)

    return hdy_df, hdy_years


# %%

# !!! !!! Behekoa ez da behin betikoa, aldagai bakoitzeko interpolaketa-metodoen iradokizun asko baitago
def hdy_interpolation(hdy_df,
                      hdy_years,
                      previous_month_last_time_range,
                      next_month_first_time_range,
                      varlist_to_interpolate,
                      polynomial_order,
                      drop_date_idx_col=False):
    
    """
    Interpolates along a selected time array between two months
    of and HDY constructed following the standard ISO 15927-4 2005 (E).
    
    Since the HDY is composed of 'fragments' of completely different months
    there are unavoidable vertical jumps on the tendencies for every variable.         
    Interpolation will help to smoothen those jumps.
    
    The problem is that the slice to be interpolated
    in most of the cases presents vertical jumps,
    so when interpolating that slice those jumps won't be completely removed.
    
    In this case, the polynomial fitting technique will be applied.
    This function performs a determined order polynomial interpolation,
    passed as an argument.
    
    Do not consider the whole previous and next month
    of the slice to be interpolated, but only some days more earlier and later.
    The reason for that is because data is hourly so there are
    obviously a lot of oscillations.
    
    Also do not consider all month indices,
    because the last interpolation involving pairs of months
    is that of October and November.
    
    For practicality and uniqueness purposes, it is strongly reccommended,
    to the extent of present elements in the variable list
    to interpolate against, to follow these standard short names.
    The order of the variables is not strict:
    
    2 metre temperature : t2m
    2 metre dew point temperature : d2m
    Relative humidity : rh
    10 metre U wind component : u10
    10 metre V wind component : v10
    10 metre wind speed modulus : ws10
    Surface solar radiation downwards : ssrd
    Surface thermal radiation downwards : strd
    Surface solar radiation downwards : ssrd
    Direct solar radiation at the surface : fdir
    Diffuse solar radiation at the surface : fdif
    Surface pressure : sp
    
    
    Notes
    -----
    Both wind direction and speed modulus will be calculated
    after the interpolation of u10 and v10 arrays.
    """
    
    hdy_interp = hdy_df.copy()
    
    hdy_months = pd.unique(hdy_interp.date.dt.month)
    lhdy_m = len(hdy_months) # == len(hdy_years), by definition
    
    # Remove 'ws10' variable from the list of variables to be interpolated #
    ws10_idx = find_substring_index(varlist_to_interpolate, "ws10")
    varlist_to_interpolate = remove_elements(varlist_to_interpolate, 
                                                        ws10_idx)

    for i in range(lhdy_m-1):
    
        days_slice_prev\
        = pd.unique(hdy_interp[(hdy_interp.date.dt.year == hdy_years[i])
                        &(hdy_interp.date.dt.month == hdy_months[i])].date.dt.day)
        
        days_slice_next\
        = pd.unique(hdy_interp[(hdy_interp.date.dt.year == hdy_years[i+1])
                        &(hdy_interp.date.dt.month == hdy_months[i+1])].date.dt.day)
        
        pml1, pml2 = np.array(previous_month_last_time_range.split(splitdelim), "i")
        nmf1, nmf2 = np.array(next_month_first_time_range.split(splitdelim), "i")
    
        ymdh_first1\
        = f"{hdy_years[i]:04d}-{hdy_months[i]:02d}-{days_slice_prev[-1]:02d} "\
          f"T{pml1:02d}"
          
        ymdh_last1\
        = f"{hdy_years[i]:04d}-{hdy_months[i]:02d}-{days_slice_prev[-1]:02d} "\
          f"T{pml2:02d}"
          
        ymdh_first2\
        = f"{hdy_years[i+1]:04d}-{hdy_months[i+1]:02d}-{days_slice_next[0]:02d} "\
          f"T{nmf1:02d}"
          
        ymdh_last2\
        = f"{hdy_years[i+1]:04d}-{hdy_months[i+1]:02d}-{days_slice_next[0]:02d} "\
          f"T{nmf2:02d}"
        
        df_slice1 = hdy_interp[(hdy_interp.date >= ymdh_first1)&
                               (hdy_interp.date <= ymdh_last1)]
        df_slice2 = hdy_interp[(hdy_interp.date >= ymdh_first2)&
                               (hdy_interp.date <= ymdh_last2)]
    
        df_slice_to_fit_reidx\
        = pd.concat([df_slice1, df_slice2],axis=0).reset_index(drop=drop_date_idx_col)
        
        # Polynomial fitting parameters #
        poly_ord = polynomial_order
        x = np.arange(len(df_slice_to_fit_reidx))
        df_slice_fit_indices = np.array(df_slice_to_fit_reidx.index)
        
        for var in varlist_to_interpolate:
            y_var = df_slice_to_fit_reidx[var]
            var_poly_coeffs = polynomial_fitting_coefficients(x, y_var, poly_ord)    
            
            for ix in range(len(x)):
                var_eval = evaluate_polynomial(var_poly_coeffs, x[ix])
                df_slice_to_fit_reidx.loc[df_slice_fit_indices[ix],var] = var_eval
                
                idx_for_hdy = df_slice_to_fit_reidx.loc[df_slice_fit_indices[ix],"index"]
                df_slice_to_fit_reidx.loc[df_slice_to_fit_reidx["index"] == idx_for_hdy,var]\
                = var_eval            
                hdy_interp.loc[idx_for_hdy,var] = var_eval
                    
                
    # Calculate the 10m wind speed direction and modulus #
    """
    On the wind direction calculus
    ------------------------------
    
    ·The sign of both components follow the standard convention:
        * u is positive when the wind is westerly,
          i.e wind blows from the west and is eastwards.
        * v is positive when the wind is northwards,
          i.e wind blows from the south.
          
    ·From the meteorological point of view,
     the direction of the wind speed vector is taken as
     the antiparallel image vector.
     The zero-degree angle is set 90º further than the
     default unit cyrcle, so that 0º means wind blowing from the North. 
    """    
    hdy_interp.loc[:,"ws10"]\
    = np.sqrt(hdy_interp.u10 ** 2 + hdy_interp.v10 ** 2)
    
    print("\nCalculating the wind direction from the meteorological point of view...")
    
    wind_dir_meteo_interp = meteorological_wind_direction(hdy_interp.u10.values,  
                                                          hdy_interp.v10.values)

    return (hdy_interp, wind_dir_meteo_interp)
    
#--------------------------#
# Parameters and constants #
#--------------------------#

splitdelim = common_delim_list[1]
