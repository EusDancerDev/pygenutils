#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from osgeo import gdal
import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import common_delim_list
from pyutils.strings.string_handler import modify_obj_specs, obj_path_specs

#-------------------------#
# Define custom functions #
#-------------------------#

def netcdf2raster(nc_file_list,
                  output_file_format,
                  raster_extension,
                  raster_resolution,
                  nodata_value=None,
                  crs="EPSG:4326"):
    """
    Converts a list of netCDF files to raster format using GDAL.

    Parameters
    ----------
    nc_file_list : list or str
        List of netCDF files to be converted or a single netCDF file.
    output_file_format : str
        Output file format (e.g., "GTiff", "JPEG").
    raster_extension : str
        Extension for the output raster files.
    raster_resolution : int
        Resolution for the output raster files.
    nodata_value : float, optional
        NoData value for the raster files. Default is None.
    crs : str
        Coordinate reference system for the output raster files.
        Default is "EPSG:4326".

    Returns:
    None
    """
    
    # Convert the input netCDF file to list if this is an only file #
    if not isinstance(nc_file_list, list):
        nc_file_list = [nc_file_list]
    lncfl = len(nc_file_list)
    
    # Define the parameter to perform file attribute changes #
    obj2change = "ext"

    for ncf_num, ncf_name in enumerate(nc_file_list, start=1):
        print(f"Converting netCDF file to raster...\n"
              f"{ncf_num} out of {lncfl}...")
        
        raster_file_name = modify_obj_specs(ncf_name, obj2change, raster_extension)
        
        # Open the netCDF file
        dataset = gdal.Open(ncf_name)
        if dataset is None:
            raise RuntimeError(f"Failed to open netCDF file {ncf_name}")

        # Get the output driver
        driver = gdal.GetDriverByName(output_file_format)
        if driver is None:
            raise RuntimeError(f"Driver for format {output_file_format} is not available.")
        
        # Create the output raster file
        options = []
        if nodata_value is not None:
            options.append(f'-a_nodata {nodata_value}')
        options.append(f'-a_srs {crs}')
        options.append(f'--config GDAL_PDF_DPI {raster_resolution}')
        
        out_dataset = driver.CreateCopy(raster_file_name, dataset, options=options)
        if out_dataset is None:
            raise RuntimeError(f"Failed to create raster file {raster_file_name}")
        
        # Properly close the datasets
        dataset = None
        out_dataset = None

        print(f"File {raster_file_name} created successfully.")



def merge_independent_rasters(raster_files_dict,
                              output_file_format,
                              joint_region_name,
                              output_file_name_ext,
                              nodata_value=None):
    
    """
    Merges independent raster files into a single raster file using GDAL.
    
    Parameters
    ----------
    raster_files_dict : dict
        Dictionary where keys are region names and values are 
        lists of raster file paths.
    output_file_format : str
        Output file format (e.g., "GTiff", "JPEG").
    joint_region_name : str
        Name for the joint region to be used in the output file name.
    output_file_name_ext : str
        Extension for the output file name.
    nodata_value : float, optional
        NoData value for the raster files. Default is None.
    
    Returns
    -------
    None
    """
   
    # Ensure all lists in the dictionary have the same length #
    keys = list(raster_files_dict)
    lkeys = len(keys)
    
    list_lengths_set = set([len(raster_files_dict[key]) for key in keys])
    lls_length = len(list_lengths_set)

    if lls_length > 1:
        raise ValueError("Not every key list is of the same length!")
    
    # Merge the rasters #
    else:
        lls_num = list(list_lengths_set)[0]        
        # Define the parameter to perform file attribute changes
        obj2change = "name_noext_parts"
        
        for i in range(1, lls_num):
            print(f"Processing the files no. {i} out of {lls_num} "
                  f"of the {lkeys} regions...")
            
            raster_file_list = [raster_files_dict[key][i] for key in keys]            
            file_path_name_parts = obj_path_specs(raster_file_list[0],
                                                  file_spec_key=obj2change,
                                                  splitdelim="_")
            
            fpnp_changes_tuple = (file_path_name_parts[-2], joint_region_name)
            output_file_name = modify_obj_specs(raster_file_list[0],
                                                obj2change,
                                                fpnp_changes_tuple)
            output_file_name += f".{output_file_name_ext}"
            
            # Open all the input files
            datasets = [gdal.Open(raster_file) for raster_file in raster_file_list]
            
            # Get the metadata of the first file
            geo_transform = datasets[0].GetGeoTransform()
            projection = datasets[0].GetProjection()
            x_size = datasets[0].RasterXSize
            y_size = datasets[0].RasterYSize
    
            # Create the output file
            driver = gdal.GetDriverByName(output_file_format)
            out_dataset = driver.Create(output_file_name, x_size, y_size, len(datasets), gdal.GDT_Float32)
            out_dataset.SetGeoTransform(geo_transform)
            out_dataset.SetProjection(projection)
    
            # Merge the files
            for band_idx in range(len(datasets)):
                in_band = datasets[band_idx].GetRasterBand(1)
                out_band = out_dataset.GetRasterBand(band_idx + 1)
                data = in_band.ReadAsArray()
                
                if nodata_value is not None:
                    data[data == nodata_value] = np.nan
                    out_band.SetNoDataValue(nodata_value)
                
                out_band.WriteArray(data)
    
            # Properly close the datasets
            datasets = None
            out_dataset = None
    
            print(f"File {output_file_name} created successfully.")


#--------------------------#
# Parameters and constants #
#--------------------------#
    
splitdelim = common_delim_list[0]
