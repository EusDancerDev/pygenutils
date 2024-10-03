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
from pyutils.string_handler import information_output_formatters

# Create aliases #
#----------------#

find_file_containing_dirs_by_ext = file_and_directory_paths.find_file_containing_dirs_by_ext
find_files_by_ext = file_and_directory_paths.find_files_by_ext

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

#-------------------------#
# Define custom functions #
#-------------------------#

# netCDF file searching #
#-----------------------#

# Main method #
#-#-#-#-#-#-#-#

def scan_ncfiles(path_to_walk_into, 
                 return_files=True, 
                 return_dirs=False,
                 check_integrity=False,
                 create_report=False,
                 top_path_only=False,
                 verbose=False,
                 extra_verbose=False):
    """
    Scans directories for netCDF (.nc) files, optionally checks file integrity, 
    and can generate a report for faulty files. Returns netCDF file paths, 
    directories containing netCDF files, or both, depending on user configuration.

    Parameters
    ----------
    path_to_walk_into : str or list
        The directory or list of directories to scan for .nc files.
    
    return_files : bool, optional (default=True)
        If True, returns a list of netCDF file paths found within the specified directories.
    
    return_dirs : bool, optional (default=False)
        If True, returns a list of directories containing netCDF files.
    
    check_integrity : bool, optional (default=False)
        If True, checks the integrity of each .nc file using xarray. Faulty files are flagged and can be reported.
    
    create_report : bool, optional (default=False)
        If True, generates a report listing all faulty netCDF files (requires `check_integrity=True`).
    
    top_path_only : bool, optional (default=False)
        If True, only scans the top-level directory without traversing subdirectories.
    
    verbose : bool, optional (default=False)
        If True, prints progress information (file number and directory) during the scan.
    
    extra_verbose : bool, optional (default=False)
        If True, prints detailed progress information (file name, number, and directory) during the scan.
        Note: `verbose` and `extra_verbose` cannot be True at the same time.

    Returns
    -------
    result : dict
        A dictionary containing the requested data based on the input parameters:
        - 'files': List of netCDF file paths (if `return_files=True`).
        - 'dirs': List of directories containing netCDF files (if `return_dirs=True`).
        - 'faulty_files': List of faulty netCDF file paths (if `check_integrity=True`).
        - 'faulty_count': Total number of faulty netCDF files (if `check_integrity=True`).

    Example
    -------
    # Example 1: Return a list of netCDF files found in the directory
    result = scan_netCDF_files("/path/to/scan", return_files=True)
    print(result['files'])

    # Example 2: Scan and check file integrity, generate a report for faulty files
    result = scan_netCDF_files("/path/to/scan", check_integrity=True, create_report=True)
    print(f"Faulty files: {result['faulty_files']}, Count: {result['faulty_count']}")

    # Example 3: Return both file paths and directories containing netCDF files
    result = scan_netCDF_files("/path/to/scan", return_files=True, return_dirs=True)
    print(result['files'], result['dirs'])
    """

    if not isinstance(path_to_walk_into, list):
        path_to_walk_into = [path_to_walk_into]

    all_nc_files = []
    all_nc_dirs = []
    faulty_files = []
    total_files = 0
    total_faulty = 0

    # Loop over each provided path
    for path in path_to_walk_into:
        nc_files = find_files_by_ext(extensions[0], path, top_path_only=top_path_only)
        nc_dirs = find_file_containing_dirs_by_ext(extensions[0], path)
        
        if return_files:
            all_nc_files.extend(nc_files)
        
        if return_dirs:
            all_nc_dirs.extend(nc_dirs)

        total_files += len(nc_files)

        # File integrity check if enabled
        if check_integrity:
            for idx, file_name in enumerate(nc_files, start=1):
                if verbose:
                    print_format_string(scan_progress_info_str, (idx, len(nc_files), path), end="\r")
                elif extra_verbose:
                    print_format_string(scan_progress_str_evb, (file_name, idx, len(nc_files), path), end="\r")

                integrity_status = ncfile_integrity_status(file_name)
                if integrity_status == -1:
                    faulty_files.append(file_name)
                    total_faulty += 1
        
        # Optionally create a report if there are faulty files
        if check_integrity and create_report and total_faulty > 0:
            with open(f"{code_call_dir}/{report_fn_noext}.txt", "w") as report:
                report.write(format_string(report_info_str, (path, total_files, total_faulty)))
                for faulty_file in faulty_files:
                    report.write(f" {faulty_file}\n")
            print("Faulty netCDF file report created.")
    
    # Return requested results
    result = {}
    if return_files:
        result['files'] = all_nc_files
    if return_dirs:
        result['dirs'] = all_nc_dirs
    if check_integrity:
        result['faulty_files'] = faulty_files
        result['faulty_count'] = total_faulty

    return result


# Helpers #
#-#-#-#-#-#

def ncfile_integrity_status(ncfile_name):    
    try:
        ds = xr.open_dataset(ncfile_name)
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
