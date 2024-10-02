#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.files_and_directories import file_and_directory_paths
from pyutils.parameters_and_constants.global_parameters import common_delim_list

# Create aliases #
#----------------#

find_file_containing_dirs_by_ext = file_and_directory_paths.find_file_containing_dirs_by_ext
find_files_by_ext = file_and_directory_paths.find_files_by_ext

#-------------------------#
# Define custom functions #
#-------------------------#            

# Dimension handlers #
#--------------------#

def find_time_dimension(nc_file_name):
    
    """
    Function that searches for time dimension names.
    It should always be located among dimensions,
    but it can happen that it either located only among variables
    or be duplicated among those.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
        String of the data file or the data set itself.
    
    Returns
    -------
    time_varlist : list
        List containing the strings that identify the time dimension.
    time_varlist_retry : list
        List containing the strings that identify the time variable.
        It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)
        
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    time_varlist = [key
                    for key in dimlist
                    if key.lower().startswith("t")
                    or key.lower().startswith("ti")
                    or key.lower().startswith("da")]
    time_varlist.sort()
    
    if len(time_varlist) > 0:       
        return time_varlist[0]
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        
        time_varlist_retry = [key
                              for key in varlist
                              if key.lower().startswith("t")
                              or key.lower().startswith("ti")
                              or key.lower().startswith("da")]
        time_varlist_retry.sort()
        
        if len(time_varlist_retry) > 0:
            return time_varlist_retry[0]
        
        else:
            raise ValueError("No 'time' dimension found in file {nc_file_name}.")
            
    ds.close()
            
            
def find_time_dimension_raise_none(nc_file_name):
    
    """
    Function that searches for time dimension names.
    It should always be located among dimensions,
    but it can happen that it either located only among variables
    or be duplicated among those.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
        String of the data file or the data set itself.
    
    Returns
    -------
    time_varlist : list
        List containing the strings that identify the time dimension.
    time_varlist_retry : list
        List containing the strings that identify the time variable.
        It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)
        
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    time_varlist = [key
                    for key in dimlist
                    if key.lower().startswith("t")
                    or key.lower().startswith("ti")
                    or key.lower().startswith("da")]
    time_varlist.sort()
    
    if len(time_varlist) > 0:       
        return time_varlist[0]
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        
        time_varlist_retry = [key
                              for key in varlist
                              if key.lower().startswith("t")
                              or key.lower().startswith("ti")
                              or key.lower().startswith("da")]
        time_varlist_retry.sort()
        
        if len(time_varlist_retry) > 0:
            return time_varlist_retry[0]
        
        else:
            return None
        
    ds.close()
            
            
def find_coordinate_variables(nc_file_name):
    
    """
    Function that searches for coordinate variable names.
    Usually those are located inside the dimension list,
    but it can happen that in some cases are among variables.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
        String of the data file or the data set itself.
    
    Returns
    -------
    coord_varlist : list
        List containing the strings that identify
        the 'latitude' and 'longitude' dimensions.
    coord_varlist_retry : list
        List containing the strings that identify
        the 'latitude' and 'longitude' variables.
        It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    coord_varlist = [key
                     for key in dimlist
                     if key.lower().startswith("lat")
                     or key.lower().startswith("y")
                     or key.lower().startswith("lon")
                     or key.lower().startswith("x")]                             
    
    if len(coord_varlist) == 2: 
        coord_varlist.sort()
        return coord_varlist
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        coord_varlist_retry = [key
                               for key in varlist
                               if key.lower().startswith("lat")
                               or key.lower().startswith("y")
                               or key.lower().startswith("lon")
                               or key.lower().startswith("x")]
        
        if len(coord_varlist_retry) == 2:
            coord_varlist_retry.sort()
            return coord_varlist_retry
        
        else:
            raise ValueError("No 'latitude' or 'longitude' coordinates found "
                             f"in file '{nc_file_name}'")
            
    ds.close()
    
            
def find_coordinate_variables_raise_none(nc_file_name):
    
    """
    Function that searches for coordinate variable names.
    Usually those are located inside the dimension list,
    but it can happen that in some cases are among variables.
    This function is designed to try both cases.
    
    Parameters
    ----------
    nc_file_name : str or xarray.Dataset
        String of the data file or the data set itself.
    
    Returns
    -------
    coord_varlist : list
        List containing the strings that identify
        the 'latitude' and 'longitude' dimensions.
    coord_varlist_retry : list
        List containing the strings that identify
        the 'latitude' and 'longitude' variables.
        It is returned only if the previous case is not satisfied.
    """
    
    # Open the netCDF file if necessary #
    if isinstance(nc_file_name, str):
        ds = xr.open_dataset(nc_file_name)        
    else:
        ds = nc_file_name.copy()
    
    # Search inside the dimension list #    
    dimlist = list(ds.dims)
    
    coord_varlist = [key
                     for key in dimlist
                     if key.lower().startswith("lat")
                     or key.lower().startswith("y")
                     or key.lower().startswith("lon")
                     or key.lower().startswith("x")]
    
    if len(coord_varlist) == 2:       
        return coord_varlist
        
    else:
        
        # Search inside the variable list #    
        varlist = list(ds.variables)
        coord_varlist_retry = [key
                               for key in varlist
                               if key.lower().startswith("lat")
                               or key.lower().startswith("y")
                               or key.lower().startswith("lon")
                               or key.lower().startswith("x")]                             
        
        if len(coord_varlist_retry) == 2:
            return coord_varlist_retry
        
        else:
            return None
        
    ds.close()

        
def get_model_list(path_list, split_pos):

    """
    Function that searches for model names present
    in the given relative file path list.
    Paths can either be absolute, relative or only file names,
    but they should, as a matter of unification, contain low bars.
    If paths are relative or absolute, i.e. contain forward slashes,
    the function selects only the file name.
    Then it splits the file name and select the position, defined by the user
    taking the low bar as the separator.
    
    Parameters
    ----------
    path_list : list
        List of relative/absolute paths or file names.
    split_pos : int
        Integer that defines which position 
    
    Returns
    -------
    unique_model_list : list
        Unique list containing model names found in the path list.
    """
    
    fwd_slash_containing_files = [path
                                  for path in path_list
                                  if "/" in path]
    
    grib_file_list = [path.name
                      if len(fwd_slash_containing_files) > 0
                      and splitdelim in path
                      else path
                      for path in path_list]
        
    unique_model_list = np.unique([f.split(splitdelim)[split_pos]
                                   for f in grib_file_list
                                   if len(grib_file_list) > 0])
    
    return unique_model_list


def get_file_dimensions(nc_file):
    
    """
    Function that extracts dimensions names from a netCDF file.
    There are some cases in which variables are also among dimensions,
    so it is convenient to eliminate those.
    
    Parameters
    ----------
    nc_file : str or xarray.Dataset, throws an error otherwise.
        String or already opened file
        that identifies the netCDF file to work with.
    
    Returns
    -------
    dimension_names = list
        List containing the names of the dimensions.
    """
    
    if isinstance(nc_file, str):
        
        ds = xr.open_dataset(nc_file)
            
        varlist = list(ds.variables)
        dimlist = list(ds.dims)
        
        # Remove variables from the dimension list if present #
        dimlist_nodim = [dim
                         for dim in varlist
                         if dim in dimlist]
        
        ldn = len(dimlist_nodim)
        if ldn == 1:
            return dimlist_nodim[0]
        else:
            return dimlist_nodim
        
        ds.close()
        
    elif isinstance(nc_file, xr.Dataset):
        
        varlist = list(nc_file.variables)
        dimlist = list(nc_file.dims)
        
        # Remove variables from the dimension list if present #
        dimlist_nodim = [dim
                         for dim in varlist
                         if dim in dimlist]
        
        ldn = len(dimlist_nodim)
        if ldn == 1:
            return dimlist_nodim[0]
        else:
            return dimlist_nodim
    
    else:
        return TypeError("Unsupported data file type.")


def get_file_variables(nc_file):
    
    """
    Function that extracts variable names from a netCDF file.
    Usually some dimensions are also inside the variable list,
    so it is convenient to eliminate those.
    
    Parameters
    ----------
    nc_file : str or xarray.Dataset, throws an error otherwise.
        String or already opened file
        that identifies the netCDF file to work with.
    
    Returns
    -------
    variable_names = list
        List containing the names of the variables.
    """
    
    if isinstance(nc_file, str):
        
        ds = xr.open_dataset(nc_file)
        varlist = list(ds.variables)
        dimlist = list(ds.dims)
        
        # Remove dimensions from the variable list if present #
        varlist_nodim = [var
                         for var in varlist
                         if var not in dimlist]
        
        lvn = len(varlist_nodim)
        if lvn == 1:
            return varlist_nodim[0]
        else:
            return varlist_nodim
        
        ds.close()
        
    elif isinstance(nc_file, xr.Dataset):
        
        varlist = list(nc_file.variables)
        dimlist = list(nc_file.dims)
        
        # Remove dimensions from the variable list if present #
        varlist_nodim = [var
                         for var in varlist
                         if var not in dimlist]
        
        lvn = len(varlist_nodim)
        if lvn == 1:
            return varlist_nodim[0]
        else:
            return varlist_nodim
    
    else:
        return TypeError("Unsupported data file type.")


def get_latlon_bounds(netcdf_file, lat_dimension_name, lon_dimension_name, value_roundoff):
    ds = xr.open_dataset(netcdf_file)
    
    lat_values = ds[lat_dimension_name].values.round(value_roundoff)
    lon_values = ds[lon_dimension_name].values.round(value_roundoff)
    
    ds.close()
        
    return (lat_values, lon_values)


def get_latlon_deltas(lat_values, lon_values, delta_roundoff):
    lat_delta = f"{abs(lat_values[0]-lat_values[1]):.{delta_roundoff}f}"
    lon_delta = f"{abs(lon_values[0]-lon_values[1]):.{delta_roundoff}f}"
    return (lat_delta, lon_delta)
        
    
def get_times(netcdf_file, time_dimension_name):    
    ds = xr.open_dataset(netcdf_file)        
    time_values = ds[time_dimension_name]
    ds.close()
    return time_values


def find_nearest_coordinates(nc_file_name, lats_obs, lons_obs):
    
    coord_varlist = find_coordinate_variables(nc_file_name)
    
    ds = xr.open_dataset(nc_file_name)    
    lats_ds = np.array(ds[coord_varlist[0]], 'd')
    lons_ds = np.array(ds[coord_varlist[1]], 'd')
    
    lats_obs = np.array(lats_obs, 'd')
    lons_obs = np.array(lons_obs, 'd')
        
    nearest_lats = []
    nearest_lons = []
        
    for lat_obs, lon_obs in zip(lats_obs, lons_obs):
        nearest_lat_idx = (abs(lat_obs-lats_ds)).argmin()
        nearest_lon_idx = (abs(lon_obs-lons_ds)).argmin()
        
        nearest_lat = lats_ds[nearest_lat_idx]
        nearest_lon = lons_ds[nearest_lon_idx]
        
        nearest_lats.append(nearest_lat)
        nearest_lons.append(nearest_lon)
        
    ds.close()
    
    nearest_lats = np.round(nearest_lats, 3)
    nearest_lons = np.round(nearest_lons, 3)
        
    return (nearest_lats, nearest_lons)


#--------------------------#
# Parameters and constants #
#--------------------------#

# File extensions #
extensions = ["nc", "csv"]

# String splitting character #
splitdelim = common_delim_list[0]