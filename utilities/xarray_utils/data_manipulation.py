#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import xarray as xr
import os

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.string_handler import information_output_formatters

from pyutils.utilities.file_operations import file_and_directory_handler
from pyutils.utilities.xarray_utils import file_utils, patterns

# Create aliases #
#----------------#

move_files_by_globstr_from_exec_code = \
file_and_directory_handler.move_files_by_globstr_from_exec_code

get_netcdf_file_dir_list = file_utils.get_netcdf_file_dir_list
get_netcdf_file_list = file_utils.get_netcdf_file_list
ncfile_integrity_status = file_utils.ncfile_integrity_status

format_string = information_output_formatters.format_string

find_coordinate_variables = patterns.find_coordinate_variables
find_time_dimension = patterns.find_time_dimension
get_latlon_bounds = patterns.get_latlon_bounds
get_latlon_deltas = patterns.get_latlon_deltas
get_times = patterns.get_times

#-------------------------#
# Define custom functions #
#-------------------------#

def extract_and_store_latlon_bounds(delta_roundoff, value_roundoff):

    #------------------------------------------------------------------------#
    # Open each file, extract coordinate dimension data and save to txt file #
    #------------------------------------------------------------------------#
    
    netcdf_files_dirs = get_netcdf_file_dir_list(code_call_dir)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir_num, ncf_dir_name in enumerate(netcdf_files_dirs, start=1):
        nc_files = get_netcdf_file_list(ncf_dir_name)
        lncfs = len(nc_files)
        
        out_file_obj = open(latlon_bound_out_file_obj_name, "w")
    
        if lncfs > 0:
            for ncf_num, ncf_name in enumerate(nc_files, start=1):
                print("Extracting coordinate values "
                      f"from file {ncf_num} out of {lncfs} "
                      f"at directory {ncf_dir_num} out of {lncfd}...")
                
                faulty_file_trial = ncfile_integrity_status(ncf_name)
                
                if faulty_file_trial == 0:                    
                    coord_varlist = find_coordinate_variables(ncf_name, raise_exception=False)
                            
                    if coord_varlist == -1:
                        out_file_obj.write(f"No 'latitude' or 'longitude' coordinates "
                                    f"found in file {ncf_name}\n")
                        
                    else:        
                        latlons = get_latlon_bounds(ncf_name,
                                                    coord_varlist[0],
                                                    coord_varlist[1],
                                                    value_roundoff)
                        
                        lats = latlons[0]
                        lons = latlons[1]
                        
                        try:
                            llats = len(lats)
                        except:
                            llats = 1
                            llons = 1
                            
                            lat_delta = 0
                            lon_delta = 0
                        
                            arg_tuple_latlons2 = (ncf_name,
                                                  lats, 
                                                  lons,
                                                  llats,
                                                  llons,
                                                  lat_delta,
                                                  lon_delta)
                            out_file_obj.write(format_string(latlon_info_str,
                                                      arg_tuple_latlons2))
                            
                        else:
                            llons = len(lons)
                            
                            deltas = get_latlon_deltas(lats, lons, delta_roundoff)
                            
                            arg_tuple_latlons1 = (
                                ncf_name,
                                lats, 
                                lons,
                                llats,
                                llons,
                                deltas[0],
                                deltas[1]
                                )
                            out_file_obj.write(format_string(latlon_info_str, 
                                                      arg_tuple_latlons1))
                                                
                else: 
                    out_file_obj.write(f"FAULTY FILE {ncf_name}\n")
                            
                            
            out_file_obj.close()
            move_files_by_globstr_from_exec_code(latlon_bound_out_file_obj_name, ncf_dir_name)
                
        else:
            out_file_obj.write(f"No netCDF files in directory {ncf_dir_name}\n")
            out_file_obj.close()
            
            move_files_by_globstr_from_exec_code(latlon_bound_out_file_obj_name, ncf_dir_name)
        

def extract_and_store_period_bounds():
    
    #---------------------------------------------------#
    # Open each file and extract time array format data #
    #---------------------------------------------------#
 
    netcdf_files_dirs = get_netcdf_file_dir_list(code_call_dir)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir_num, ncf_dir_name in enumerate(netcdf_files_dirs, start=1):
        nc_files = get_netcdf_file_list(ncf_dir_name)
        lncfs = len(nc_files)
        
        out_file_obj = open(period_bound_out_file_obj_name, "w")
    
        if lncfs > 0:
            for ncf_num, ncf_name in enumerate(nc_files, start=1):    
                print("Extracting time bounds "
                      f"from file {ncf_num} out of {lncfs} "
                      f"at directory {ncf_dir_num} out of {lncfd}...")
                                
                faulty_file_trial = ncfile_integrity_status(ncf_name)
                
                if faulty_file_trial == 0:
                    time_var = find_time_dimension(ncf_name, raise_exception=False)
                    
                    if not time_var:
                        out_file_obj.write("No 'time' dimension or variable "
                                           f"found in file {ncf_name}.\n")
                    
                    else:    
                        times = get_times(ncf_name, time_var)
                        records = len(times)
                                        
                        arg_tuple_bounds1 = (
                            ncf_name,
                            times[0].values,
                            times[-1].values,
                            records
                            )
                        out_file_obj.write(format_string(period_info_str, arg_tuple_bounds1))
                else: 
                    out_file_obj.write(f"FAULTY FILE {ncf_name}\n")
                
            out_file_obj.close()
            move_files_by_globstr_from_exec_code(period_bound_out_file_obj_name, ncf_dir_name)
                
        else:
            out_file_obj.write(f"No netCDF files in directory {ncf_dir_name}\n")    
            out_file_obj.close()
            move_files_by_globstr_from_exec_code(period_bound_out_file_obj_name, ncf_dir_name)


def extract_and_store_time_formats():
    
    #---------------------------------------------------#
    # Open each file and extract time array format data #
    #---------------------------------------------------#
    
    out_file_obj_name = "time_formats.txt"

    netcdf_files_dirs = get_netcdf_file_dir_list(code_call_dir)
    lncfd = len(netcdf_files_dirs)
    
    for ncf_dir_num, ncf_dir_name in enumerate(netcdf_files_dirs, start=1):
        nc_files = get_netcdf_file_list(ncf_dir_name)
        lncfs = len(nc_files)
        
        out_file_obj = open(out_file_obj_name, "w")

        if lncfs > 0:                
            for ncf_num, ncf_name in enumerate(nc_files, start=1):
                print("Extracting time formats "
                      f"from file {ncf_num} out of {lncfs} "
                      f"at directory {ncf_dir_num} out of {lncfd}...")
                
                faulty_file_trial = ncfile_integrity_status(ncf_name)
                
                if faulty_file_trial == 0:
                    time_var = find_time_dimension(ncf_name, raise_exception=False)
                    
                    if not time_var:
                        out_file_obj.write("No 'time' dimension or variable "
                                           f"found in file {ncf_name}\n")
                    
                    else:
                        times = get_times(ncf_name, time_var)
                        records = len(times)
                            
                        arg_tuple_bounds2 = (
                            ncf_name,
                            times.values,
                            records
                            )
                        out_file_obj.write(format_string(time_format_info_str, arg_tuple_bounds2))
                        
                else:
                    out_file_obj.write(f"FAULTY FILE {ncf_name}\n")
                    
            out_file_obj.close()
            move_files_by_globstr_from_exec_code(out_file_obj_name, ncf_dir_name)
            
        else:
            out_file_obj.write(f"No netCDF files in directory {ncf_dir_name}\n")
            out_file_obj.close()
            move_files_by_globstr_from_exec_code(out_file_obj_name, ncf_dir_name)
            
            
def netcdf_regridder(ds_in, ds_image, regrid_method="bilinear"):    
    
    import xesmf as xe
    
    """
    Function that regrids a xarray Dataset to that of the desired Dataset. 
    It is similar to CDO but more intuitive and
    easier to understand, supported by Python.
    
    Parameters
    ----------
    ds_in : xarray.Dataset
        Input xarray data set
    ds_image : xarray.Dataset
        Xarray data set with grid specifications to which apply on ds_in.
    regrid_method : {'bilinear', 'conservative', 'nearest_s2d', 'nearest_d2s', 'patch'}
        Regridding method. Defaults 'bilinear'.
    
    Returns
    -------
    ds_out : xarray.Dataset
        Output data set regridded according to the grid specs of ds_in.
    """
    
    if regrid_method not in regrid_method_list:
        raise ValueError("Invalid regridding method.\n"
                         f"Choose one from {regrid_method_list}.")
        
    else:
        regridder = xe.Regridder(ds_in, ds_image, regrid_method)
        ds_out = regridder(ds_in)
        return ds_out
    


def create_ds_component(var_name,
                        data_array,
                        dimlist,
                        dim_dict,
                        attrs_dict):
    
    data_array_dict = {
        var_name : xr.DataArray(
            data=data_array,
            dims=dimlist,
            coords=dim_dict,
            attrs=attrs_dict,
            )
        }
    
    return data_array_dict

#--------------------------#
# Parameters and constants #
#--------------------------#

# Directory from where this code is being called #
code_call_dir = os.getcwd()

# File extensions #
extensions = ["nc", "csv"]

# Main file names #
latlon_bound_out_file_obj_name = "latlon_bounds.txt"
period_bound_out_file_obj_name = "period_bounds.txt"

# Regridding method options #
regrid_method_list = [
    "bilinear",
    "conservative",
    "conservative_normed",
    "nearest_s2d",
    "nearest_d2s",
    "patch"
    ]

# Preformatted strings #
#----------------------#

# Main parameter scanning info strings #
latlon_info_str = \
"""=========================================================
·File: {}

·Latitudes:
 {}

·Longitudes:
 {}

-Latitude-longitude array dimensions = {} x {}
-Latitude-longitude array delta = ({}, {})
    
"""

period_info_str = \
"""=========================================================
·File: {}
·Time range: {} -- {}
-Range length = {}

"""
    
time_format_info_str = \
"""=========================================================
·File: {}
    
·Time array:
 {}

-Array length = {}
"""
