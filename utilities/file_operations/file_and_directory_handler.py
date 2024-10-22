#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path
import shutil

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.operative_systems.os_operations import exit_info, run_system_command

#------------------#
# Helper Functions #
#------------------#

def select_files(patterns, base_directory, match_type="ext"):
    """
    Helper function to select files based on file extensions or glob patterns.
    
    Parameters
    ----------
    patterns : str or list
        String or list of patterns to match files (extension or glob pattern).
    base_directory : Path
        The directory from which to search for files.
    match_type : str, optional
        Type of matching to perform. Options are "ext" (for extensions)
        or "glob" (for glob patterns). Defaults to "ext".
    
    Returns
    -------
    list of Path objects
        A list of matching file paths.
    """
    if isinstance(patterns, str):
        patterns = [patterns]

    all_files = []
    
    for pattern in patterns:
        if match_type == "ext":
            selected_files = base_directory.glob(f"*.{pattern}")
        elif match_type == "glob":
            selected_files = base_directory.glob(pattern)
        else:
            raise ValueError(f"Invalid match_type: {match_type}")
        
        all_files.extend([file for file in selected_files if file.is_file()])
    
    return all_files

#----------------------#
# Refactored Functions #
#----------------------#

# Operations involving files #
#----------------------------#

def move_files(patterns, input_directories, destination_directories, match_type="ext"):
    """
    Function to move files based on extensions or glob patterns from specified input directories
    to one or more destination directories.
    
    Parameters
    ----------
    patterns : str or list
        String or list of file extensions (without dot) or glob patterns.
    input_directories : str or list
        Directory or list of directories from which to select the files.
    destination_directories : str or list
        String or list of destination directories.
    match_type : str, optional
        Type of pattern matching to use: "ext" for extensions or "glob" for glob patterns. Defaults to "ext".
    
    """
    if isinstance(input_directories, str):
        input_directories = [input_directories]

    if isinstance(destination_directories, str):
        destination_directories = [destination_directories]

    for input_directory in input_directories:
        input_directory_path = Path(input_directory)
        selected_files = select_files(patterns, input_directory_path, match_type=match_type)
        
        for file in selected_files:
            file_name_nopath = file.name
            for destination_directory in destination_directories:
                shutil.move(file, os.path.join(destination_directory, file_name_nopath))


def copy_files(patterns, input_directories, destination_directories, match_type="ext"):
    """
    Function to copy files based on extensions or glob patterns from specified input directories
    to one or more destination directories.
    
    Parameters
    ----------
    patterns : str or list
        String or list of file extensions (without dot) or glob patterns.
    input_directories : str or list
        Directory or list of directories from which to select the files.
    destination_directories : str or list
        String or list of destination directories.
    match_type : str, optional
        Type of pattern matching to use: "ext" for extensions or "glob" for glob patterns. Defaults to "ext".
    
    """
    if isinstance(input_directories, str):
        input_directories = [input_directories]
    
    if isinstance(destination_directories, str):
        destination_directories = [destination_directories]

    for input_directory in input_directories:
        input_directory_path = Path(input_directory)
        selected_files = select_files(patterns, input_directory_path, match_type=match_type)
        
        for file in selected_files:
            file_name_nopath = file.name
            for destination_directory in destination_directories:
                shutil.copy(file, os.path.joindestination_directory, file_name_nopath)


def remove_files(patterns, input_directories, match_type="ext"):
    """
    Function to remove files based on extensions or glob patterns from specified input directories.
    
    Parameters
    ----------
    patterns : str or list
        String or list of file extensions (without dot) or glob patterns.
    input_directories : str or list
        Directory or list of directories from which to select the files.
    match_type : str, optional
        Type of pattern matching to use: "ext" for extensions or "glob" for glob patterns. Defaults to "ext".
    
    """
    if isinstance(input_directories, str):
        input_directories = [input_directories]

    for input_directory in input_directories:
        input_directory_path = Path(input_directory)
        selected_files = select_files(patterns, input_directory_path, match_type=match_type)
        
        for file in selected_files:
            os.remove(file)

# Operations involving directories #
#----------------------------------#

def make_directories(directory_list):
    """
    Creates the specified parent directories if they do not already exist using os.makedirs.
    
    Parameters
    ----------
    directory_list : str or list
        A string or list of directory paths to create.
    """
    if isinstance(directory_list, str):
        directory_list = [directory_list]

    for directory in directory_list:
        os.makedirs(directory, exist_ok=True)


def remove_directories(directory_list):
    """
    Removes the specified directories and their contents.
    
    Parameters
    ----------
    directory_list : str or list
        A string or list of directory paths to remove.
    """
    if isinstance(directory_list, str):
        directory_list = [directory_list]

    for directory in directory_list:
        shutil.rmtree(directory, ignore_errors=True)


def move_directories(directories, destination_directories):
    """
    Moves the specified directories to the destination directories.
    
    Parameters
    ----------
    directories : str or list
        A string or list of directories to move.
    destination_directories : str or list
        A string or list of destination directories.
    """
    if isinstance(directories, str):
        directories = [directories]

    if isinstance(destination_directories, str):
        destination_directories = [destination_directories]

    for directory, destination_directory in zip(directories, destination_directories):
        shutil.move(directory, destination_directory)


def copy_directories(directories, destination_directories, recursive_in_depth=True):
    """
    Copies the specified directories to the destination directories. Can be recursive or non-recursive.
    
    Parameters
    ----------
    directories : str or list
        A string or list of directories to copy.
    destination_directories : str or list
        A string or list of destination directories.
    recursive_in_depth : bool, optional
        If True, copies directories recursively. Defaults to True.
    """
    if isinstance(directories, str):
        directories = [directories]

    if isinstance(destination_directories, str):
        destination_directories = [destination_directories]

    for directory, destination_directory in zip(directories, destination_directories):
        if recursive_in_depth:
            shutil.copytree(directory, destination_directory, dirs_exist_ok=True)
        else:
            shutil.copytree(directory, destination_directory)
            

# Operations involving both files and directories #
#-------------------------------------------------#

def rsync(source_paths, 
          destination_paths, 
          mode="avh", 
          delete_at_destination=True,
          source_allfiles_only=False):
    """
    Synchronizes directories using the rsync command with various options.
    
    Parameters
    ----------
    source_paths : str or list
        A string or list of paths to source directories.
    destination_paths : str or list
        A string or list of paths to destination directories.
    mode : str, optional
        The rsync command mode. Defaults to "avh".
    delete_at_destination : bool, optional
        If True, deletes extraneous files from the destination. Defaults to True.
    source_allfiles_only : bool, optional
        If True, syncs only files present in the source directories. Defaults to False.
    
    Raises
    ------
    ValueError
        If the length of the source_paths and destination_paths lists is not equal.
    """
    
    if isinstance(source_paths, str):
        source_paths = [source_paths]
    
    if isinstance(destination_paths, str):
        destination_paths = [destination_paths]

    if len(source_paths) != len(destination_paths):
        raise ValueError("The length of source_paths and destination_paths must be equal.")
    
    for sp, dp in zip(source_paths, destination_paths):
        # Define the rsync command based on the given options
        rsync_command = ["rsync", f"-{mode}"]

        # Add the --delete flag if needed
        if delete_at_destination:
            rsync_command.append("--delete")
        
        # Add source_allfiles_only flag (no trailing slash on source path)
        if not source_allfiles_only:
            sp = sp.rstrip('/') + "/"
        
        # Complete the rsync command
        rsync_command.append(sp)
        rsync_command.append(dp)

        # Run the rsync command
        process_exit_info = run_system_command(" ".join(rsync_command), encoding="utf-8")
        exit_info(process_exit_info)
            

def rename_objects(relative_paths, renaming_relative_paths):
    """
    Renames the specified files or directories.
    
    Parameters
    ----------
    relative_paths : str or list
        A string or list of paths of the files or directories to rename.
    renaming_relative_paths : str or list
        A string or list of the new names for the files or directories.
    
    Raises
    ------
    ValueError
        If the length of the relative_paths list is not equal to the renaming_relative_paths list.
    TypeError
        If the inputs are not both strings or both lists.
    """
    if isinstance(relative_paths, list) and isinstance(renaming_relative_paths, list):
        if len(relative_paths) != len(renaming_relative_paths):
            raise ValueError(not_equal_length_error)
        else:
            for rp, rrp in zip(relative_paths, renaming_relative_paths):
                os.rename(rp, rrp)
    elif isinstance(relative_paths, str) and isinstance(renaming_relative_paths, str):
        os.rename(relative_paths, renaming_relative_paths)
    else:
        raise TypeError(objtype_error)


#--------------------------#
# Parameters and constants #
#--------------------------#

# Errors #
not_equal_length_error = """File and renamed file lists are not of the same length."""
objtype_error = "Both input arguments must either be strings or lists simultaneously."