#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Note**

This program is an application of the main module 'audio_and_video',
and it relies on the method 'merge_audio_or_video_files'.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pygenutils.audio_and_video.audio_and_video_manipulation import merge_audio_or_video_files

#-------------------#
# Define parameters #
#-------------------#

# Simple data #
#-------------#

output_ext = "mp4"

# Input media #
#-------------#

# List #
media_file_list = []

# External file containing file names #
# media_name_containing_file = "media_name_containing_file.txt"

# Output media #
#--------------#

# Merged media file #
output_file_name = "output.{output_ext}"
# output_file_name = None

# Zero-padding and bit rate factor #
"""The factor is multiplied by 32, so that the bit rate is in range [32, 320] kBps"""
zero_padding = 1
quality = 1

#------------#
# Operations #
#------------#

merge_audio_or_video_files(media_file_list,
                           output_file_name=output_file_name,
                           zero_padding=zero_padding,
                           quality=quality)

# merge_audio_or_video_files(media_name_containing_file,
#                            output_file_name=output_file_name,
#                            zero_padding=zero_padding,
#                            quality=quality)
