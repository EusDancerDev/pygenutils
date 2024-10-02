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

from pyutils.files_and_directories import file_and_directory_paths
from pyutils.string_handler import information_output_formatters, string_handler
from pyutils.utilities.introspection_utils import get_caller_method_args

# Create aliases #
#----------------#

find_substring_index = string_handler.find_substring_index

find_file_containing_dirs_by_ext = file_and_directory_paths.find_file_containing_dirs_by_ext
find_files_by_ext = file_and_directory_paths.find_files_by_ext

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

#-------------------------#
# Define custom functions #
#-------------------------#

# netCDF file path searching #
#----------------------------#

def scan_ncfiles(path_to_walk_into, 
                 top_path_only=False,
                 verbose=False,
                 extra_verbose=False,
                 create_report=False):

    # Proper argument selection control #
    arg_names = get_caller_method_args()
    verb_arg_pos = find_substring_index(arg_names, "verbose")
    xverb_arg_pos = find_substring_index(arg_names, "extra_verbose")
    
    # Define the input data directories and files #
    #---------------------------------------------#
    
    if not isinstance(path_to_walk_into, list):        
        path_to_walk_into = [path_to_walk_into]
        
    for ptwi in path_to_walk_into:
        ncgrib_file_list = find_files_by_ext(extensions[0], ptwi, top_path_only=top_path_only)
        lncfl = len(ncgrib_file_list)
    
        # Initialise faulty file counter #
        #--------------------------------#
        
        faulty_ncf_counter = [lncfl, 0]
        faulty_ncf_list = []
        
        # Loop through all path list #
        #----------------------------#
        
        for file_num, file_name in enumerate(ncgrib_file_list, start=1):
            if verbose and extra_verbose:
                raise ValueError(f"Arguments '{arg_names[verb_arg_pos]}' "
                                 f"and '{arg_names[xverb_arg_pos]}' "
                                 "cannot be 'True' at the same time.")
                
            else:
                if verbose:
                    arg_tuple_file_scan1 = (file_num, lncfl, ptwi)
                    print_format_string(scan_progress_info_str,
                                        arg_tuple_file_scan1,
                                        end="\r")
                elif extra_verbose:
                    arg_tuple_file_scan2 = (file_name, file_num, lncfl, ptwi)
                    print_format_string(scan_progress_str_evb,
                                        arg_tuple_file_scan2,
                                        end="\r")
        
            integrity_status = ncfile_integrity_status(file_name)
            
            if integrity_status == -1:
                faulty_ncf_counter[-1] += 1
                faulty_ncf_list.append(file_name)
                
        if create_report:
        
            # Create faulty netCDF file report #
            #----------------------------------#
            
            out_file_obj_name = f"{code_call_dir}/{report_fn_noext}.txt"
            out_file_obj = open(out_file_obj_name, "w")
            
            arg_tuple_file_scan3 = (ptwi, faulty_ncf_counter[0], faulty_ncf_counter[-1])
            out_file_obj.write(format_string(report_info_str, arg_tuple_file_scan3))
            
            for faulty_ncf in faulty_ncf_list:
                out_file_obj.write(f" {faulty_ncf}\n")
            
            print("Faulty netCDF file report created at the current directory.")
            out_file_obj.close()
            
        else:
            return faulty_ncf_counter[-1]


def get_netcdf_file_list(path_to_walk_into):    
    netcdf_files = find_files_by_ext(extensions[0], path_to_walk_into, top_path_only=True)
    return netcdf_files


def get_netcdf_file_dir_list(path_to_walk_into):    
    netcdf_files_dirs = find_file_containing_dirs_by_ext(extensions[0], path_to_walk_into)
    return netcdf_files_dirs


# Faulty netCDF file detecting #
#------------------------------#

def ncfile_integrity_status(ncfile_name):    
    try:
        ds=xr.open_dataset(ncfile_name)
    except:
        return -1
    else:
        ds.close()
        return 0


#--------------------------#
# Parameters and constants #
#--------------------------#

# Directory from where this code is being called #
code_call_dir = os.getcwd()

# File extensions #
extensions = ["nc", "csv"]

# Preformatted strings #
#----------------------#

# File scanning progress information strings #
report_fn_noext = "faulty_netcdf_file_report"

scan_progress_info_str =\
"""
File number: {} out of {}
Directory: {}
"""

scan_progress_str_evb =\
"""
File: {}
File number: {} out of {}
Directory: {}
"""

# Faulty file report's header string #
report_info_str =\
"""Faulty NETCDF format file report
--------------------------------

·Directory: {}
·Total scanned files scanned: {}
·Faulty file number: {}

·Faulty files:
"""
