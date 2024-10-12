#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:14:15 2022

@author: jon ander

** DISCLAIMER **
This program serves as a module to store parameters that are used frequently or globally.

*GLOBAL PARAMETERS MODULE STRUCTURE*

1. Time-Related Parameters
2. Mathematical Concepts
3. Programming Concepts
4. Socio-Economical Concepts
"""

#%% 1. TIME-RELATED PARAMETERS

#------#
# Time #
#------#

# Basic time format strings
basic_time_format_strs = {
    "H": "%Y-%m-%d %H:%M:%S",
    "H_NODATESEP": "%Y%m%d %H:%M:%S",
    "D": "%Y-%m-%d",
    "D_NODATESEP": "%Y%m%d",
    "M": "%Y-%m",
    "Y": "%Y"
}

# Non-standard time format strings
non_std_time_format_strs = {
    "CFT_H": "%a %b %d %H:%M:%S %Y",
    "CFT_D": "%a %b %d %Y",
    "CFT_M": "%b %Y"
}

# Custom time format strings
custom_time_format_strs = {
    "CT_EXCEL_SPANISH_H": "%d/%m/%y %H:%M:%S",
    "CT_EXCEL_SPANISH_NOBAR_H": "%d%m%y %H:%M:%S",
    "CT_EXCEL_SPANISH_D": "%d/%m/%y",
    "CT_EXCEL_SPANISH_NOBAR_D": "%d%m%y"
}

# Month number to letter mapping
month_number_dict = {
    1: "J", 2: "F", 3: "M", 4: "A", 5: "M", 6: "J", 7: "J", 
    8: "A", 9: "S", 10: "O", 11: "N", 12: "D"
}

# Seasonal time frequency dictionary
season_time_freq_dict = {
    1: "Q-JAN", 2: "Q-FEB", 3: "Q-MAR", 4: "Q-APR", 
    5: "Q-MAY", 6: "Q-JUN", 7: "Q-JUL", 8: "Q-AUG", 
    9: "Q-SEP", 10: "Q-OCT", 11: "Q-NOV", 12: "Q-DEC"
}

# Mathematical approximation for year length
MATHEMATICAL_YEAR_DAYS = 360


# Time frequencies
time_frequencies_complete = ["year", "season", "month", "day", "hour", "minute", "second"]
time_frequencies_short_1 = ["yearly", "seasonal", "monthly", "daily", "hourly"]
time_frequencies_shorter_1 = ["year", "seas", "mon", "day", "hour"]

# Supported date units
pandas_date_unit_list = ['D', 'ms', 'ns', 's', 'us']
numpy_date_unit_list = ['Y', 'M', 'D', 'h', 'm', 's', 'ms', 'us', 'ns']

unit_factor_dict = {
    "D": 1000,
    "s": 1,
    "ms": 1e-3,
    "us": 1e-6,
    "ns": 1e-9
}

#%% 2. MATHEMATICAL CONCEPTS

# Basic operators
basic_four_rules = ["+", "-", "*", "/"]

# Set algebra
operations_sets_list = [
    "union", "difference", "intersection", 
    "symmetric_difference", "comparison"
]

#%% 3. PROGRAMMING CONCEPTS

# Operative Systems
filesystem_context_modules = ["os", "Path", "shutil", "subprocess"]  # 'Path' from 'pathlib' module
storage_entity_types = ["file", "directory"]

# Regular expressions
regex_passwords = r"^(?=.{8,})(?=.*[a-z\s])(?=.*[A-Z\s])(?=.*\d)(?=.*[_\W]).+$"

# Strings
common_delim_list = ["_", "-", ";", ",", "\n", "\t", " "]

# Databases
data_uploading_error_dict = {
    "1007": "Database already exists",
    "1045": "Wrong username",
    "1049": "Unknown database name",
    "1698": "Wrong password",
    "2003": "Wrong host name"
}

#%% 4. SOCIO-ECONOMICAL CONCEPTS

# Climate change
emission_rcp_scenarios = ["historical", "rcp26", "rcp45", "rcp85"]
climate_file_extensions = ["nc", "grib", "netcdf_zip", "csv"]
