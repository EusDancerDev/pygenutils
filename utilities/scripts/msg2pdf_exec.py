#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.files_and_directories.file_format_tweaker import msg2pdf

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Documents"

delete_msg_files = False
delete_eml_files = False

#------------------------------------------#
# Convert every Microsoft Outlook message  #
#------------------------------------------#

msg2pdf(path, delete_msg_files, delete_eml_files)
