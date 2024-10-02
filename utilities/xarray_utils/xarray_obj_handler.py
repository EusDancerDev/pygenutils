#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import xarray as xr

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists.data_manipulation import flatten_content_to_string
from pyutils.pandas_data_frames.data_frame_handler import save2csv
from pyutils.operative_systems.os_operations import run_system_command, exit_info
from pyutils.string_handler.string_handler import find_substring_index, get_obj_specs, modify_obj_specs
from pyutils.utilities.xarray_utils.data_manipulation import create_ds_component
from pyutils.utilities.xarray_utils.patterns import find_coordinate_variables, find_time_dimension

#-------------------------#
# Define custom functions #
#-------------------------#

def save_data_as_netcdf_std(file_name,
                            vardim_names_for_ds,
                            data_arrays,
                            dimlists,
                            dim_dictlist,
                            attrs_dictlist,
                            global_attrs_dict):

    ds = xr.Dataset()
    
    for vardim, data_array, dimlist, dim_dict, attrs_dict in zip(vardim_names_for_ds,
                                                                 data_arrays,
                                                                 dimlists,
                                                                 dim_dictlist,
                                                                 attrs_dictlist):
        
        data_array_dict = create_ds_component(vardim,
                                             data_array,
                                             dimlist,
                                             dim_dict,
                                             attrs_dict)
        ds = ds.merge(data_array_dict)
        
    ds.attrs = global_attrs_dict
    
    file_name += ".{extensions[0]}"
    
    ds.to_netcdf(file_name, "w", format="NETCDF4")
    print(f"{file_name} file successfully created")
    
    
def save_xarray_dataset_as_netcdf(xarray_ds, file_name, attrs_dict=None):
    
    """
    Function that writes a xarray data set directly into a netCDF,
    with the option of updating attributes.
    
    Parameters
    ----------
    xarray_ds : xarray.Dataset
        OPENED xarray data set.
    file_name : str
        String for the resulting netCDF file name.
    attrs_dict : dict
        Dictionary containing attributes, such as source,
        version, date of creation, etc.
        If not given, attributes will remain the same as the input file.
  
    Returns
    -------
    netCDF file
    """
    
    file_name += ".nc"
    
    if attrs_dict:
        xarray_ds.attrs = attrs_dict
    
    xarray_ds.to_netcdf(file_name, "w", format="NETCDF4")

    print(f"{file_name} has been successfully created")
    
    
def save_nc_data_as_csv(nc_file, 
                        columns_to_drop,
                        separator,
                        save_index,
                        save_header,
                        csv_file_name="default",
                        date_format=None,
                        approximate_coords=False,
                        latitude_point=None,
                        longitude_point=None):
    
    """
    Function that saves netCDF data into a CSV file AS IT IS, where data variables
    may originally be 3D, usually dependent on (time, latitude, longitude).
    It is intended to speed up further data processes,
    especially when opening very large netCDF files with xarray,
    which can take a long time.
    Saving data into a CSV, it can then be read very rapidly so as to
    load data for post-processing.
    
    For that, it seeks for essential variables,
    together with 'time' dimension, if present.
    It then concatenates whole data into a data frame and then
    saves it into a CSV file.
    
    Parameters
    ----------
    nc_file : str or xarray.Dataset or xarray.DataArray
        String of the xarray data set containing file or
        the already opened data array or set.
    columns_to_drop : str or list of str
        Names of the columns to drop, if desired, from the
        resultant data frame of xarray.to_pandas() method.
        If None, then the function will not drop any column.
        To drop only coordinate labels, select "coords".
        Else, the function will drop the custom labels passed.
    separator : str
        String used to separate data columns.
    save_index : bool
        Boolean to choose whether to include a column into the excel document
        that identifies row numbers. Default value is False.
    save_header : bool
        Boolean to choose whether to include a row into the excel document
        that identifies column numbers. Default value is False.
    csv_file_name : str, optional
        If nc_file is a string and "default" option is chosen,
        then the function will attempt to extract a location name.
        If nc_file is a xarray object, a custom name must be provided.    #       
    date_format : str
        In case the data frame contains a time column,
        use to give format thereof when storing the data frame.
    approximate_coords : str
        If both latitude and longitude arrays are length higher than 1,
        determines whether to select a coordinate point and then
        perform the saving. If true and both lengths are 1,
        throws and error telling that data is already located at a point.
    latitude_point : float
        Valid only if approximate_coords is True.
    longitude_point : float
        Valid only if approximate_coords is True.
    
    Returns
    -------
    CSV file containing data as arranged on the data frame.
    
    Notes
    -----
    Remember that this function serves as a direct copy of netCDF4 data,
    if data modifications are required, then it cannot be used.
    Data frames are only 2D, so that those
    can only reflect a specific point multi-variable netCDF data along time
    or several grid points' data for a specific time position.
    Data frame column names will be the same as those on netCDF data file.
    """
    
    # Open netCDF data file if passed a string #
    if isinstance(nc_file, str):
        print(f"Opening {nc_file}...")
        ds = xr.open_dataset(nc_file)
        
    else:
        ds = nc_file.copy()
        
    if latitude_point is not None or longitude_point is not None:
        
        coord_varlist = find_coordinate_variables(ds)
        lats = ds[coord_varlist[0]]
        lons = ds[coord_varlist[1]]
        
        llats, llons = len(lats), len(lons)
        
        if llats == llons == 1:
            raise ValueError("Object is already located at a point data")
        else:
            if latitude_point is None:
                raise ValueError("Latitude point coordinate not given")
            
            elif longitude_point is None:
                raise ValueError("Longitude point coordinate not given")
            
            elif latitude_point is None and longitude_point is None:
                raise ValueError("Both latitude and longitude "
                                 "point coordinates not given.")
                
            else:
                
                if approximate_coords:
                    
                    lat_idx = abs(lats - latitude_point).argmin()
                    lon_idx = abs(lons - longitude_point).argmin()
                    
                    coord_idx_kw = {
                        coord_varlist[0] : lat_idx,
                        coord_varlist[1] : lon_idx
                        }
                    
                    ds = ds.isel(**coord_idx_kw)
                    
                else:
                    
                    coord_idx_kw = {
                        coord_varlist[0] : latitude_point,
                        coord_varlist[1] : longitude_point
                        }
                    
                    ds = ds.sel(**coord_idx_kw)
                    
    elif latitude_point is not None\
    and isinstance(approximate_coords, str):
                
        print(f"Coordinate label is {approximate_coords}")
        
        coord_idx_kw = {
            approximate_coords : latitude_point,
            }
        
        ds = ds.isel(**coord_idx_kw)
        
    elif latitude_point is None\
    and isinstance(approximate_coords, str):
        
        raise ValueError("You must provide a coordinate or ID")

    # Drop columns if desired #
    if columns_to_drop is None:
        data_frame\
        = ds.to_pandas().reset_index(drop=False)
    
    elif columns_to_drop == "coords": 
        columns_to_drop = coord_varlist.copy()
        data_frame\
        = ds.to_pandas().reset_index(drop=False).drop(columns=columns_to_drop)
        
    else:
        data_frame\
        = ds.to_pandas().reset_index(drop=False).drop(columns=columns_to_drop)
       
    # Create the saving file's name or maintain the user-defined name #
    #-----------------------------------------------------------------#
    
    if (isinstance(nc_file, str) and csv_file_name == "default"):
        obj2change = "ext"
        csv_file_name = get_obj_specs(nc_file, obj2change, extensions[1])
    
    elif (not isinstance(nc_file, str) and csv_file_name == "default"):
        raise ValueError("You must provide a CSV file name.")
        
    else:
        # Save data as desired format file #   
        #----------------------------------#
        
        save2csv(csv_file_name,
                 data_frame,
                 separator,
                 save_index,
                 save_header,
                 date_format)
    
    
def save_data_array_as_csv(data_array, 
                           separator,
                           save_index,
                           save_header,
                           csv_file_name=None,
                           new_columns="default",
                           date_format=None):
    
    """
    Function that saves a xr.DataArray object into a CSV file AS IT IS,
    where data variables may originally be 3D, 
    usually dependent on (time, latitude, longitude).
    This function works exactly as 'save_nc_data_as_csv' function does,
    so the docstrings also apply.
    Parameters
    ----------
    data_array : xarray.DataArray
    new_columns : str or list of str
        Names of the columns for the data frame created from the object.
        Default ones include 'time' and variable name label.
    separator : str
        String used to separate data columns.
    save_index : bool
        Boolean to choose whether to include a column into the excel document
        that identifies row numbers. Default value is False.
    save_header : bool
        Boolean to choose whether to include a row into the excel document
        that identifies column numbers. Default value is False.
    csv_file_name : str, optional
        If nc_file is a string and "default" option is chosen,
        then the function will attempt to extract a location name.
        If nc_file is a xarray object, a custom name must be provided.    #       
    date_format : str
    
    Returns
    -------
    CSV file containing data as arranged on the data frame.
    """
    
    # Drop information to a data frame #
    data_frame = data_array.to_pandas().reset_index(drop=False)        
        
    # Define the 'time' dimension name #
    date_key = find_time_dimension(data_array)
    
    # Rename the resulting data frame columns #
    if new_columns == "default":
        da_varname = data_array.name
        new_columns = [date_key, da_varname]

    data_frame.columns = new_columns
       
    # Create the saving file's name or maintain the user-defined name #
    if csv_file_name is None:
        raise ValueError("You must provide a CSV file name.")
        
    # Save data as desired format file #     
    else:
        save2csv(csv_file_name,
                 data_frame,
                 separator,
                 save_index,
                 save_header,
                 date_format)
        
        
def grib2netcdf(grib_file_list, on_shell=False, option_str=None):
        
    if on_shell:
        if isinstance(grib_file_list, str):
            nc_file_new = modify_obj_specs(grib_file_list, "ext", extensions[0])
            
        else:
            grib_allfile_info_str = flatten_content_to_string(grib_file_list)
            nc_file_new_noext = input("Please introduce a name "
                                      "for the netCDF file, "
                                      "WITHOUT THE EXTENSION: ")
            
            allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                            regex_grib2nc,
                                                            advanced_search=True)
            
            while (allowed_minimum_char_idx == -1):
                print("Invalid file name.\nIt can contain alphanumeric characters, "
                      "as well as the following non-word characters: {. _ -}")
                
                nc_file_new_noext = input("Please introduce a valid name: ")
                allowed_minimum_char_idx = find_substring_index(nc_file_new_noext,
                                                                regex_grib2nc,
                                                                advanced_search=True)
                
            else:
                nc_file_new_noext = modify_obj_specs(nc_file_new_noext,
                                                     obj2modify="ext",
                                                     new_obj=extensions[0])
                
        grib2netcdf_comm = "grib_to_netcdf"
        if not option_str:
            grib2netcdf_comm += f"{option_str}"
        grib2netcdf_comm += f"-o {nc_file_new} {grib_allfile_info_str}"
            
        process_exit_info = run_system_command(grib2netcdf_comm,
                                               capture_output=True,
                                               encoding="utf-8")
        exit_info(process_exit_info)    
        
    else:   
        if isinstance(grib_file_list, str):
            grib_file_list = [grib_file_list]

        for grib_file in grib_file_list:
            grib_file_noext = get_obj_specs(grib_file, "name_noext", extensions[0])
            ds = xr.open_dataset(grib_file, engine="cfgrib")
            save_xarray_dataset_as_netcdf(ds, grib_file_noext)
            
            
#--------------------------#
# Parameters and constants #
#--------------------------#

# File extensions #
extensions = ["nc", "csv"]

# RegEx control for GRIB-to-netCDF single file name #
regex_grib2nc = r"^[a-zA-Z0-9\._-]$"

# Regridding method options #
regrid_method_list = [
    "bilinear",
    "conservative",
    "conservative_normed",
    "nearest_s2d",
    "nearest_d2s",
    "patch"
    ]