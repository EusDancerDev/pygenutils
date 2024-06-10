#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'file_format_tweaker.py',
and it uses the 'pdf_file_compressor' attributes and/or functions.
PLEASE DO NOT REDISTRIBUTE this program along any other directory,
as the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from files_and_directories.file_format_tweaker import pdf_file_compressor

#-------------------#
# Define parameters #
#-------------------#

# 1st case usage #
#----------------#

in_path_str  = "/home/jonander/Documents/apunteak.pdf"
out_path_str = "/home/jonander/Documents/tweaked.pdf"

# 2nd case usage #
#----------------#

in_path_list = ["/home/jonander/Documents/sample_1.pdf",
                "/home/jonander/Documents/sample_2.pdf",
                "/home/jonander/Documents/sample_3.pdf",
                "/home/jonander/Documents/sample_4.pdf"]

out_path_list = ["/home/jonander/Documents/compressed_sample1.pdf",
                 "/home/jonander/Documents/compressed_sample2.pdf",
                 "/home/jonander/Documents/compressed_sample3.pdf",
                 "/home/jonander/Documents/compressed_sample4.pdf",]

#-----------------------------#
# Compress the provided files #
#-----------------------------#

# pdf_file_compressor(in_path_str, out_path_str)
pdf_file_compressor(in_path_list, out_path_list)