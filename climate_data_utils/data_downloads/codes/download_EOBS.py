#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 20:57:17 2023

@author: jonander
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.files_and_directories import file_and_directory_handler, file_and_directory_paths
from pyutils.strings.string_handler import find_substring_index, substring_replacer
from pyutils.time_handling.program_snippet_exec_timers import program_exec_timer
from pyutils.weather_and_climate import cds_tools, netcdf_handler

# Create aliases #
#----------------#

download_data = cds_tools.download_data

make_parent_directories = file_and_directory_handler.make_parent_directories
move_files_by_ext_from_exec_code = file_and_directory_handler.move_files_by_ext_from_exec_code

find_files_by_globstr = file_and_directory_paths.find_files_by_globstr

scan_ncfiles = netcdf_handler.scan_ncfiles

#-------------------------#
# Define custom functions #
#-------------------------#

def return_file_extension(file_format):

    extension_idx = find_substring_index(available_formats, file_format)
    
    if extension_idx == -1:
        raise ValueError(f"Unsupported file format. Choose from '{available_formats}'.")
    else:
        extension = available_extensions[extension_idx]
        return extension
    
def return_grid_resolution(resolution):
    
    if resolution not in available_resolutions:
        raise ValueError("Invalid grid resolution. "
                         f"Choose form {available_resolutions}")
    else:
        resolution += "deg"
        return resolution
    
def check_correct_product_type(product_type):
    if product_type not in available_products:
        raise ValueError(f"Unsupported product. Choose from '{available_products}'.")

    
#---------------------#
# Variable parameters #
#---------------------#

# Project name #
project_name = "climate-change"

# Product attributes #
product_type = "ensemble_mean"
check_correct_product_type(product_type)

# Periods #
periods = [
    "1950_1964",
    "1965_1979",
    "1980_1994",
    "1995_2010",
    "2011_2022"
    ]

# Variables #
variable_list = [
    'maximum_temperature',
    'mean_temperature',
    'minimum_temperature',
    'precipitation_amount'
    ]

# Downloadable formats and extensions #
file_format = "zip"
extension = return_file_extension(file_format)

# Version #
version = "28.0e"

# Grid resolution #
resolution = "0.1"

#------------------#
# Fixed parameters #
#------------------#

# Main directories #
#------------------#

# Document containing directory #
repo_path = "/home/jonander/Documents/gordetegiak/pyutils."

# Project (main) directory #
project_dir = f"{repo_path}/test-base_programs/{project_name}"

# Code-containing directory #
codes_dir = f"{project_dir}/codes"

# Input (downloaded) data main directory #
main_input_data_dir = f"{project_dir}/input_data"

# Dataset #
#---------#

dataset = "E-OBS"
dataset_lower = dataset.lower()

# Product attributes #
#--------------------#

# Product name #
product_name = "insitu-gridded-observations-europe"

# Product types #
product_kw = "product_type"

available_products = [
    "ensemble_mean",
    "ensemble_spread",
    "elevation"
    ]

# Periods #
#---------#

period_kw = "period"

# Variables #
#-----------#

variable_kw = "variable"

# Downloadable formats and extensions #
#-------------------------------------#

format_kw = "format"

available_formats = ["zip", "tgz"]
available_extensions = ["zip", "tar.gz"]

# Version #
#---------#

version_kw = "version"

# Grid resolution #
#-----------------#

resolution_kw = "grid_resolution"

available_resolutions = ["0.1", "0.25"]
resolution_std = return_grid_resolution(resolution)

#--------------------#
# Initialize program #
#--------------------#

program_exec_timer('start')

#-----------------------------------#
# Loop through the different ranges #
#-----------------------------------#

# Create, if necessary, the input data directory specific for the data set #
ds_input_data_dir = f"{main_input_data_dir}/{dataset}"
make_parent_directories(ds_input_data_dir)

"""
It is possible that there will not be data available for certain period(s) of time,
or if it is the case, not every variable will be available.

Analyzing each and every one of the possibilities requires
a great effort, but there is no way to catch the 
exit status of the downloading process, so if there is an error,
the CDS API will specify the type thereof and will lead to a program halt.
"""

for p in periods:
    p_std = substring_replacer(p, "_", "-")
        
    # Set the keyword argument dictionary to pass in later on #
    kwargs = {
        product_kw : product_type,
        variable_kw : variable_list,
        resolution_kw : resolution_std,
        period_kw : p,
        version_kw : version,
        format_kw : file_format,
        }
    
    # Gather every parameter to form the output file name #
    output_file_name = f"{dataset_lower}_{product_type}_{p_std}.{extension}"

    """
    Test whether the file is already downloaded
    (current or downloaded data directory)
    """
    ofn_list = find_files_by_globstr(f"*{output_file_name}*",
                                     path_to_walk_into=project_dir)
    
    lofnl = len(ofn_list)
    
    if lofnl > 0:
        num_faulty_ncfiles\
        = scan_ncfiles(path_to_walk_into=codes_dir)
        
        if num_faulty_ncfiles > 0:   
            # Download the specified data #
            download_data(product_name, output_file_name, **kwargs)
            
    else:
        # Download the specified data #
        download_data(product_name, output_file_name, **kwargs)


# Move the downloaded data from the directory where the code is being called #
move_files_by_ext_from_exec_code(extension, ds_input_data_dir)

#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

program_exec_timer('stop')
