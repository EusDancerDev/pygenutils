#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: eraiki txantiloia, databases/upload_data_to_mysql_database.py moduluan bezalatsu

"""
This program is an application of the main module netcdf_handler.py
Simply copy this script to the desired directory.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from time_handling.program_snippet_exec_timers import program_exec_timer
from weather_and_climate import netcdf_handler

# Create aliases #
#----------------#

extract_and_store_latlon_bounds = netcdf_handler.extract_and_store_latlon_bounds 
extract_and_store_period_bounds = netcdf_handler.extract_and_store_period_bounds
extract_and_store_time_formats = netcdf_handler.extract_and_store_time_formats

#-------------------#
# Start the program #
#-------------------#

program_exec_timer("start")

#------------#
# Parameters #
#------------#

# Delta and value roundoffs for coordinate values #
DELTA_ROUNDOFF = 3
VALUE_ROUNDOFF = 5

#-----------------------------------------------------------------------#
# Extract every netCDF file's basic information present in this project #
#-----------------------------------------------------------------------#

extract_and_store_latlon_bounds(DELTA_ROUNDOFF, VALUE_ROUNDOFF)
extract_and_store_period_bounds()
extract_and_store_time_formats()

#-----------------------------------------------#
# Calculate the elapsed time for full execution #
#-----------------------------------------------#

program_exec_timer("stop")
