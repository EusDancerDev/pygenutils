#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Note**

This program is an application of the main module 'audio_and_video',
and it uses the 'merge_audio_and_video_files' attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pytools.audio_and_video.audio_and_video_manipulation import merge_audio_and_video_files

#-------------------#
# Define parameters #
#-------------------#

input_video_file_list = [
    ]

input_audio_file_list = [
    ]

# output_file_name_list = None
output_file_name_list = [
    ]

ZERO_PADDING = 1

#------------------#
# Perform the task #
#------------------#

merge_audio_and_video_files(input_video_file_list,
                            input_audio_file_list,
                            output_file_name_list=None,
                            ZERO_PADDING=ZERO_PADDING)
