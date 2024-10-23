#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.utilities.format_converters.file_format_tweaker import eml2pdf

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Documents"
delete_eml_files = False

#-----------------------------#
# Convert every email message #
#-----------------------------#

eml2pdf(path, delete_eml_files)
