#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: eraiki txantiloia, databases/upload_data_to_mysql_database.py moduluan bezalatsu

"""
This program is an application of the main module 'xarray_utils'
Simply copy this script to the desired directory.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.time_handling.program_snippet_exec_timers import program_exec_timer
from pyutils.utilities import xarray_utils

# Create aliases #
#----------------#

extract_latlon_bounds = xarray_utils.extract_latlon_bounds 
extract_time_bounds = xarray_utils.extract_time_bounds
extract_time_formats = xarray_utils.extract_time_formats

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

extract_latlon_bounds(DELTA_ROUNDOFF, VALUE_ROUNDOFF)
extract_time_bounds()
extract_time_formats()

#-----------------------------------------------#
# Calculate the elapsed time for full execution #
#-----------------------------------------------#

program_exec_timer("stop")
