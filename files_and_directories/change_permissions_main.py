#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import grp
import pwd

import os
from pathlib import Path
import shutil

#-----------------------#
# Import custom modules #
#-----------------------#

import pytools.file_and_directory_paths as pyt_paths
from pytools.parameters_and_constants.global_parameters import basic_object_types
from pytools.strings import information_output_formatters, string_handler
from pytools.utilities.introspection_utils import get_caller_method_args

# Create aliases #
#----------------#

find_all_file_extensions = pyt_paths.find_all_file_extensions
find_all_directories = pyt_paths.find_all_directories
find_files_by_ext = pyt_paths.find_files_by_ext

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

find_substring_index = string_handler.find_substring_index

#-----------------------------#
# Get this laptop user's name #
#-----------------------------#

home_posix_path = Path.home()
whoami = home_posix_path.parts[-1]

#-------------------------#
# Define custom functions #
#-------------------------#

def modify_obj_permissions(path, 
                           obj_type="file",
                           extensions2skip="",
                           attr_id=664):
    
    """
    Default permission ID configuration (as when touching files
    or creating directories) is as follows:
    
    Files: attr_id = 664
    Directories: attr_id = 775
    """    
    all_arg_names = get_caller_method_args()
    ot_arg_pos = find_substring_index(all_arg_names, "obj_type")
    attr_arg_pos = find_substring_index(all_arg_names, "attr_id")
    
    if isinstance(attr_id, str):
        raise TypeError(format_string(type_error_str, all_arg_names[attr_arg_pos]))
        
    le2s = len(extensions2skip)
    
    if obj_type not in basic_object_types:
        arg_tuple_mod_perms1 = (all_arg_names[ot_arg_pos], basic_object_types)
        raise ValueError(format_string(value_error_str, arg_tuple_mod_perms1))
  
    if obj_type == basic_object_types[0]:
        
        if le2s > 0:
            arg_tuple_mod_perms2 = ("permissions", path, extensions2skip)
            print_format_string(perm_mod_excepts_progress_info, arg_tuple_mod_perms2)
        else:
            arg_tuple_mod_perms3 = ("permissions", "files", path)
            print_format_string(perm_mod_progress_info_str, arg_tuple_mod_perms3)
            
        file_extension_list = find_all_file_extensions(extensions2skip, 
                                                      path, 
                                                      top_path_only=True)
        obj_path_list = find_files_by_ext(file_extension_list,
                                            path, 
                                            top_path_only=True)
            
    elif obj_type == basic_object_types[1]:
        arg_tuple_mod_perms4 = ("permissions", "directories", path)
        print_format_string(perm_mod_progress_info_str, arg_tuple_mod_perms4)
        obj_path_list = find_all_directories(path)
        

    for obj_path in obj_path_list:
        try:
            os.chmod(obj_path, attr_id)
        except PermissionError:
            raise PermissionError(permission_error_str)
                
 
def modify_obj_owner(path,
                     module="shutil",
                     obj_type="file",
                     extensions2skip="",
                     new_owner=None,
                     new_group=None):    
    """
    Note
    ----
    In order to modify file and/or directory owner and/or group names,
    both os.chown and shutil.chown need the user to be rooted.
    """
    
    all_arg_names = get_caller_method_args()
    mod_arg_pos = find_substring_index(all_arg_names, "module")
    ot_arg_pos = find_substring_index(all_arg_names, "obj_type")
    
    le2s = len(extensions2skip)
    
    if obj_type not in basic_object_types:
        arg_tuple_mod_perms2 = (all_arg_names[ot_arg_pos], basic_object_types)
        raise ValueError(format_string(value_error_str, arg_tuple_mod_perms2))
        
    if module not in modules:
        arg_tuple_mod_perms3 = (all_arg_names[mod_arg_pos], modules)
        raise ValueError(format_string(value_error_str, arg_tuple_mod_perms3))
        
    if obj_type == basic_object_types[0]:
        
        if le2s > 0:
            arg_tuple_mod_perms5 = ("owner", "files", path, extensions2skip)
            print_format_string(perm_mod_excepts_progress_info, arg_tuple_mod_perms5)
        else:
            arg_tuple_mod_perms6 = ("owner", "files", path)
            print_format_string(perm_mod_progress_info_str, arg_tuple_mod_perms6)
            
        file_extension_list = find_all_file_extensions(extensions2skip, 
                                                      path, 
                                                      top_path_only=True)
        obj_path_list = find_files_by_ext(file_extension_list,
                                            path, 
                                            top_path_only=True)
        
    elif obj_type == basic_object_types[1]:
        arg_tuple_mod_perms7 = ("permissions", "directories", path)
        print_format_string(perm_mod_progress_info_str, arg_tuple_mod_perms7)
        obj_path_list = find_all_directories(path)
    
    for obj_path in obj_path_list:
        if module == "os":
            
            # Owner modification #
            if new_owner is None or new_owner == "unchanged":
                uid = -1
            else:
                uid = pwd.getpwnam(new_owner).pw_uid
                
            # Group modification #
            if new_group is None or new_group == "unchanged":
                gid = -1
            else:
                gid = grp.getgrnam(new_group).gr_gid
                
            try:
                os.chown(obj_path, uid, gid)
            except PermissionError:
                raise PermissionError(permission_error_str)
            
        elif module == "shutil":
            try:
                shutil.chown(obj_path, user=new_owner, group=new_group)
            except PermissionError:
                raise PermissionError(permission_error_str)
    
#--------------------------#
# Parameters and constants #
#--------------------------#

# OS-related #
#------------#

modules = ["os", "shutil"]

# Preformatted strings #
#----------------------#

# Error indicators #
type_error_str = """Argument '{}' "must be of type 'int'."""
permission_error_str = "Please execute the program as sudo."
value_error_str = """Unsupported '{}' option. Choose one from {}."""

# Progress information #
perm_mod_excepts_progress_info = """Modifying {} of all {} in {}\
except the following extensioned ones...\n{}"""

perm_mod_progress_info_str = """Modifying {} of all {} in {}..."""