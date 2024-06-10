#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'bulk_rename_index_main.py',
and it uses some of its attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with relative paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from files_and_directories.bulk_rename_index_main import reorder_objs

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Pictures/2023/Tenerife_test_rename_pytools"
obj_type = "file"

ZERO_PADDING = 3
extensions2skip = ""

starting_number = "default"
index_range = "all"

splitdelim = None

#------------------#
# Perform the task #
#------------------#

reorder_objs(path,
             obj_type,
             extensions2skip,
             index_range,
             starting_number,
             ZERO_PADDING,
             splitdelim=splitdelim)