#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# FIXME: artxibo honen izena, inportatzen den moduluaren ANTZEKOA da!
# TODO: egokitu eta optimizatu alkartzeko pasatzen diren artxiboak zerrenda edo fitxategi moduan pasatzen direlako mekanismoak


"""
**Note**

This program is an application of the main module 'audio_and_video_manipulation',
and it relies on the method 'merge_individual_media_files'.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pygenutils.audio_and_video.audio_and_video_manipulation import merge_individual_media_files

#-------------------#
# Define parameters #
#-------------------#

# Simple data #
#-------------#

output_ext = "mp4"

# Input media #
#-------------#

# Media input can be a list of files or a single file containing file names
media_input = []
# media_input = "media_name_containing_file.txt"

# Output media #
#--------------#

# Merged media file #
output_file_name = f"merged_media_file.{output_ext}"
# output_file_name = None

# Zero-padding and bit rate factor #
"""The factor is multiplied by 32, so that the bit rate is in range [32, 320] kBps"""
ZERO_PADDING = 1
quality = 4

#------------#
# Operations #
#------------#

merge_individual_media_files(media_input,
                             output_file_name=output_file_name,
                             ZERO_PADDING=ZERO_PADDING,
                             quality=quality)