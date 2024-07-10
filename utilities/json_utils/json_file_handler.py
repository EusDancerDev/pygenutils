#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import json
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.files_and_directories.file_and_directory_paths import find_files_by_globstr
from pyutils.strings.string_handler import aux_ext_adder, get_obj_specs

#------------------#
# Define functions #
#------------------#

# Read from and write to JSON files #
#-----------------------------------#

# Dictionaries #
#-#-#-#-#-#-#-#-

def dict2json(dictionary, 
              out_file_path=None,
              indent=4,
              ensure_ascii=False,
              sort_keys=False,
              allow_nan=False):
    """
    Convert a dictionary to a JSON string and write it to a file.

    Parameters
    ----------
    dictionary : dict
        The dictionary to be converted to JSON format.
    out_file_path : str, optional
        The output file path. If not provided, a default name 'dict2json.json' will be used.
    indent : int, optional
        The number of spaces to use as indentation in the JSON file. Default is 4.

    Returns
    -------
    str
        The output file path where the JSON data is written.

    Raises
    ------
    IOError
        If the file cannot be written to the specified path.
    """
    
    # Determine the output file path #
    if out_file_path is None:
        out_file_path = f"dict2json.{extensions[0]}"
    else:
        contains_path_extension = len(get_obj_specs(out_file_path, 'ext')) > 0
        if not contains_path_extension:
            out_file_path = aux_ext_adder(out_file_path, extensions[0])

    try:
        with open(out_file_path, 'w') as out_file_obj:
            
            # Convert dictionary to JSON string #
            json.dump(dictionary, 
                      out_file_obj,
                      indent=indent,
                      ensure_ascii=ensure_ascii, 
                      sort_keys=sort_keys,
                      allow_nan=allow_nan)
        
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
            else:
                if overwrite_stdin == "y":
                    with open(out_file_path, 'w') as out_file_obj:
                        
                        # Convert dictionary to JSON string #
                        json.dump(dictionary, 
                                  out_file_obj,
                                  indent=indent,
                                  ensure_ascii=ensure_ascii, 
                                  sort_keys=sort_keys,
                                  allow_nan=allow_nan)
                elif overwrite_stdin == "n":
                    print("File not overwritten as per user input.")
                
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
        
        
# Pandas Dataframe #
#------------------#

def json2df(json_file_list, encoding="utf-8"):
    
    if isinstance(json_file_list, str):
        json_file_list = [json_file_list]
    
    df = pd.DataFrame()

    for json_file in json_file_list:        
        with open(json_file, "r", encoding=encoding) as jsf:
            data = json.load(jsf)
            next_df = pd.json_normalize(data)
            df = pd.concat([df, next_df],ignore_index=True)
 
    return df


#--------------------------#
# Parameters and constants #
#--------------------------#

# File extension list #
extensions = ["json"]