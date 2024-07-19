#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os
import numpy as np

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings import information_output_formatters, string_handler
from pyutils.utilities.introspection_utils import get_caller_method_args

# Create aliases #
#----------------#

find_substring_index = string_handler.find_substring_index
format_string = information_output_formatters.format_string

#------------------#
# Define functions #
#------------------#

def merge_audio_and_video_files(input_video_file_list,
                                input_audio_file_list,
                                output_file_name_list=None,
                                ZERO_PADDING=1):
    
    # Quality control of the zero-padding #
    all_arg_names = get_caller_method_args()
    zp_arg_pos = find_substring_index(all_arg_names, "ZERO_PADDING")
    
    if ((ZERO_PADDING is not None and not isinstance(ZERO_PADDING, int))\
        or (ZERO_PADDING is not None
            and isinstance(ZERO_PADDING, int) 
            and ZERO_PADDING < 1)):
        raise TypeError(f"Argument '{all_arg_names[zp_arg_pos]}' "
                        f"at position {zp_arg_pos} must either be "
                        "an integer equal or greater than 1.\n"
                        "Set to `None` if no zero padding is desired.")
        
        
    # Check whether the compulsory lists are of the same length #
    livfl = len(input_video_file_list)
    liafl = len(input_audio_file_list)
    
    if livfl != liafl:
        raise ValueError("Input audio and video files have to be of the same length.")
    else:
        # If output file name list is not provided, create a default one #
        if output_file_name_list is None:
            if ZERO_PADDING is None:
                output_file_name_list_default = [f"merged_video_{i:d}"
                                                 for i in range(1, livfl+1)]
            else:
                output_file_name_list_default = [f"merged_video_{i:0{ZERO_PADDING+1}d}"
                                                 for i in range(1, livfl+1)]
            lofnl = len(output_file_name_list_default)
        else:
            lofnl = len(output_file_name_list)
            
        length_lists = [livfl, liafl, lofnl]
        unique_lengths = np.unique(length_lists)
        lul = len(unique_lengths)
        
        if lul > 1:
            raise ValueError("All lists have to be of the same length.")
            
        # Perform the operations #
        else:
            for in_audio_fn, in_video_fn, out_video_fn in zip(input_audio_file_list,
                                                              input_video_file_list,
                                                              output_file_name_list):
                
                arg_tuple = (in_audio_fn, in_video_fn, out_video_fn)
                merge_command = format_string(ffmpeg_aud_vid_merge_syntax, arg_tuple)
                os.system(merge_command)
                
                
# TODO: bi bideo artxibo alkartzeko metodoa eraiki

#--------------------------#
# Parameters and constants #
#--------------------------#

# Preformatted strings #
#----------------------#

# FFMPEG merge syntaxes #
ffmpeg_aud_vid_merge_syntax = "ffmpeg -i {} -i {} -c:v copy -c:a aac {}"
ffmpeg_vid_merge_syntax = "ffmpeg -i 'concat:{}|{}' -c copy {}"


