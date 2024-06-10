#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 21:52:48 2024

@author: jonander
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import json

#-----------------------#
# Import custom modules #
#-----------------------#

from files_and_directories.file_and_directory_paths import find_files_by_globstr
from strings.string_handler import aux_ext_adder, get_obj_specs

#-------------------------#
# Define custom functions #
#-------------------------#

# Conversions to JSON files and importations from them #
#------------------------------------------------------#

def dict2json(dictionary, json_indent=4, out_file_path=None):
    """
    Convert a dictionary to a JSON string and write it to a file.

    Parameters
    ----------
    dictionary : dict
        The dictionary to be converted to JSON format.
    json_indent : int, optional
        The number of spaces to use as indentation in the JSON file. Default is 4.
    out_file_path : str, optional
        The output file path. If not provided, a default name 'dict2json.json' will be used.

    Returns
    -------
    str
        The output file path where the JSON data is written.

    Raises
    ------
    IOError
        If the file cannot be written to the specified path.
    """
    
    # Convert dictionary to JSON string #
    dict_str = json.dumps(dictionary, indent=json_indent)
    
    # Determine the output file path #
    if out_file_path is None:
        out_file_path = f"dict2json.{extension}"
    else:
        contains_path_extension = len(get_obj_specs(out_file_path, 'ext')) > 0
        if not contains_path_extension:
            out_file_path = aux_ext_adder(out_file_path, extension)

    try:
        with open(out_file_path, 'w') as out_file_obj:
            out_file_obj.write(dict_str)
        
        # Get file specs #
        out_file_parent = get_obj_specs(out_file_path, obj_spec_key="parent")
        out_file_no_rel_path = get_obj_specs(out_file_path, obj_spec_key="name")
        
        # Check for existing file #
        file_already_exists = (len(find_files_by_globstr(f"*{out_file_path}*", ".")) > 0)
        
        if file_already_exists:
            overwrite_stdin = input(
                f"Warning: file '{out_file_no_rel_path}' "
                f"at directory '{out_file_parent}' already exists.\n"
                "Do you want to overwrite it? (y/n) "
            )
            while overwrite_stdin not in ["y", "n"]:
                overwrite_stdin = input("\nPlease select 'y' for 'yes' or 'n' for 'no': ")
            if overwrite_stdin == "y":
                pass
            else:
                raise IOError("File not overwritten as per user input.")
                
        return out_file_path
                
    except IOError as e:
        raise IOError(f"Could not write to file '{out_file_path}', invalid path.") from e

def json2dict(in_file_path):
    """
    Convert a JSON file to a dictionary.

    Parameters 
    ----------
    in_file_path : str
        The input file path, which could be absolute or relative.

    Returns
    -------
    dict
        The content of the JSON file as a dictionary.

    Raises
    ------
    FileNotFoundError
        If the input file is not found.
    TypeError
        If the content of the file cannot be decoded as JSON.
    """
    
    # Open and read the JSON file #
    try:
        with open(in_file_path, 'r') as in_file_obj:
            content_str = in_file_obj.read()
    
        # Convert content to a dictionary #
        try:
            content_dict = json.loads(content_str)
            return content_dict
        except json.JSONDecodeError as e:
            raise TypeError(f"Could not decode content from file '{in_file_path}'.") from e

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{in_file_path}' not found.") from e

# Merge and sort operations #
#---------------------------#

def sort_dictionary_by_keys(dic):
    """
    Sort a dictionary by its keys.

    Parameters
    ----------
    dic : dict
        The dictionary to be sorted.

    Returns
    -------
    dict
        The dictionary sorted by keys.
    """
    keys_sorted_list = sorted(dic)
    dic_sorted_by_keys = {key: dic[key] for key in keys_sorted_list}
    return dic_sorted_by_keys

def merge_dictionaries(dict_list):
    """
    Merge a list of dictionaries into a single dictionary.

    Parameters
    ----------
    dict_list : list
        The list of dictionaries to be merged.

    Returns
    -------
    dict
        The merged dictionary.

    Raises
    ------
    ValueError
        If the list contains less than two dictionaries.
    """
    if len(dict_list) < 2:
        raise ValueError("At least 2 dictionaries must be passed.")
    
    merged_dict = {}
    for d in dict_list:
        merged_dict.update(d)
    return merged_dict

#--------------------------#
# Parameters and constants #
#--------------------------#

# File extension #
extension = "json"