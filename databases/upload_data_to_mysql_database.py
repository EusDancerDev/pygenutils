#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Note**

This program is an application of the main module 'database_handler.py',
and it uses some of its attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory
and adapt it to your needs.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from databases.database_handler import load_file_to_sql
# from files_and_directories.file_and_directory_paths import find_files_by_globstr

#-------------------#
# Define parameters #
#-------------------#

# Config dictionary containing database credentials #
#---------------------------------------------------#

config_dict = {
    "username": "username",
    "password": "cool-password",
    "host": "host",
    "database_name": "dbname",
}

# Database type #
#---------------#

database_type="mysql"

# Table parameters #
#------------------#

table_param_dict = dict(
    if_exists="replace",
    import_index=False,
    separator="\t", 
    header=0,
    parser_engine=None,
    decimal=","
    )

# Data files #
#------------#

input_file_list = ["/home/jonander/Documents/gordetegiak/pytools/databases/test.csv"]
# input_file_list = find_files_by_globstr("test*",
#                                         path_to_walk_into=".", 
#                                         top_path_only=True)


#------------------#
# Perform the task #
#------------------#

load_file_to_sql(input_file_list,
                 config_dict, 
                 database_type=database_type, 
                 **table_param_dict)