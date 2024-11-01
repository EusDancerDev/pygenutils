#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Note**

This program is an application of the main module 'audio_and_video',
and it relies on the method 'merge_audio_and_video_files'.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pygenutils.audio_and_video.audio_and_video_manipulation import merge_audio_and_video_files

#-------------------#
# Define parameters #
#-------------------#

# Input media #
#-------------#

# Lists #
video_file_list = []
audio_file_list = []

# External file containing file names #
# video_name_containing_file = "video_name_containing_file.txt"
# audio_name_containing_file = "audio_name_containing_file.txt"

# Output media #
#--------------#

# List #
output_file_list = []
# output_file_list = None

# Zero-padding and bit rate factor #
"""The factor is multiplied by 32, so that the bit rate is in range [32, 320] kBps"""
zero_padding = 1
quality = 1

#------------#
# Operations #
#------------#

merge_audio_and_video_files(video_file_list,
                            audio_file_list,
                            output_file_list=output_file_list,
                            zero_padding=zero_padding,
                            quality=quality)

# merge_audio_and_video_files(video_name_containing_file,
#                             audio_name_containing_file,
#                             zero_padding=zero_padding,
#                             quality=quality)
