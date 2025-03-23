#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
**Note**

This program is an application of the main module 'audio_and_video_manipulation',
and it relies on the method 'merge_media_files'.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from filewise.utilities.file_operations.path_utils import find_files
from pygenutils.audio_and_video.audio_and_video_manipulation import merge_media_files

#-------------------#
# Define parameters #
#-------------------#

# Simple data #
#-------------#

# File type delimiters #
audio_delimiter = "audio"
video_delimiter = "video"

# File extensions and globstrings #
audio_extension = "mp3"
audio_file_globstr = f"*_{audio_delimiter}.{audio_extension}"

video_extension = "mp4"
video_file_globstr = f"*_{video_delimiter}.{video_extension}"

# Path to walk into for file searching #
search_path = "../Curso_superior_ML/"

# Input media #
#-------------#

# Find target audio and video files #
input_audio_file_list = find_files(audio_file_globstr, search_path)
input_video_file_list = find_files(video_file_globstr, search_path)

# Output media #
#--------------#

# Name output file names manually #
"""Taking into account the names of the files, the simplest way to rename them is by removing the item type"""

output_file_name_list = [
    f"{input_audio_file.split(audio_delimiter)[0][:-1]}.{video_extension}"
    for input_audio_file in input_audio_file_list
]
# output_file_name_list = None

# Zero-padding and bit rate factor #
"""The factor is multiplied by 32, so that the bit rate is in range [32, 320] kBps"""
ZERO_PADDING = None
quality = 4

#-------------------#
# Program operation #
#-------------------#

merge_media_files(input_video_file_list,
                  input_audio_file_list,
                  output_file_name_list=output_file_name_list,
                  ZERO_PADDING=ZERO_PADDING,
                  quality=quality)

