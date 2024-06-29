#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

# TODO: eraiki txantiloia, databases/upload_data_to_mysql_database.py moduluan bezalatsu

from pyutils.time_handling.program_snippet_exec_timers import program_exec_timer
from pyutils.weather_and_climate.netcdf_handler import netcdf_file_scanner

#-------------------#
# Define parameters #
#-------------------#

# Path containing string or list of strings #
path_obj = "/media/jonander/My_Basic/Dokumentuak"

# path_obj = ["/media/jonander/My_Basic/Dokumentuak"
#             "/home/jonander/Documents/03-Ikasketak]

# Switch for scanning files only at the top level of the given path(s) #
top_path_only = True

# Switch to print every file being scanned #
extra_verbose = True

#------------------------#
# Initialise the program #
#------------------------#

program_exec_timer('start')
netcdf_file_scanner(path_obj, 
                    top_path_only=top_path_only,
                    extra_verbose=extra_verbose)
    
#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

program_exec_timer('stop')
