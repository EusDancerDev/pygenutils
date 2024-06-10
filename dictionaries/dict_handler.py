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

# File exportations #
#-------------------#

def dict2json(dictionary, json_indent=4, out_file_path=None):    
    """
    Function that converts a dictionary (not only its content, 
    but as a whole) to a string and writes the latter to a JSON file.
    
    Parameters 
    ----------
    dictionary : dict
        The original dictionary, no matter what structure is composed of.
    json_indent : int
        Determines the space to be used expressing the dictionary 
        as a string. Default value is that used widely, 
        a tab, equivalent to 4 whitespaces.
    out_file_path : str
        Output file path, could be absolute or relative.
        If not passed, default name 'dict2json.json' will be used.
            
    Returns
    -------
    Output file path in which the whole dictionary is written.    
    """
    
    # Convert dictionary  to string #
    dict_str = json.dumps(dictionary, indent=json_indent)
    
    # Write the string directly and at once to the given path #
    #---------------------------------------------------------#
    
    # Check whether a path is given #
    if out_file_path is None:
        out_file_path = f"dict2json.{extension}"
        
    # Check whether the path contains an extension, else add it #
    else:
        containsPathExtension = len(get_obj_specs(out_file_path, 'ext')) > 0
        if not containsPathExtension:
            out_file_path = aux_ext_adder(out_file_path, extension)

    try:
        out_file_obj = open(out_file_path, 'w')        
    except:
        raise IOError("Could not write to file '{out_file_path}',"
                      "invalid path.")
    else:
        out_file_obj.write(dict_str)
        
        # Get the file name's parent and the name without the relative path #        
        out_file_parent = get_obj_specs(out_file_path, obj_spec_key="parent")
        out_file_no_rel_path = get_obj_specs(out_file_path, obj_spec_key="name")
        
        # Find already existing file #
        file_already_exists = (len(find_files_by_globstr(f"*{out_file_path}*", ".")) > 0)
        
        if file_already_exists:
            overwrite_stdin\
            = input(f"Warning: file '{out_file_no_rel_path}' "
                    f"at directory '{out_file_parent}' already exists.\n"
                    "Do you want to overwrite it? (y/n) ")
            
            while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                overwrite_stdin = input("\nPlease select 'y' for 'yes' "
                                       "or 'n' for 'no': ")
            else:    
                if overwrite_stdin == "y":
                    out_file_obj.close()
                else:
                    pass
    

# Merge and sort operations #
#---------------------------#

def sort_dictionary_by_keys(dic):
    keys_sorted_list = sorted(dic)
    dic_sorted_byKeys = {key : dic[key]
                         for key in keys_sorted_list}
    return dic_sorted_byKeys
    

def merge_dictionaries(dict_list):
    ldl = len(dict_list)
    if ldl == 1:
        raise ValueError("2 dictionaries at least must be passed.")
    
    str2eval = "{"
    for d in dict_list:
        str2eval += f"**{d},"
    str2eval += "}"
    
    merged_dict = eval(str2eval)
    return merged_dict

    
#--------------------------#
# Parameters and constants #
#--------------------------#

# File extensions #
extension = "json"
