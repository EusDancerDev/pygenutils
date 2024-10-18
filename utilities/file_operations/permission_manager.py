#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import grp
import pwd

import os
import shutil

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.utilities.file_operations import file_and_directory_paths as pyt_paths
from pyutils.strings import information_output_formatters, string_handler
from pyutils.utilities.introspection_utils import get_caller_method_args

# Create aliases #
#----------------#

find_all_file_extensions = pyt_paths.find_all_file_extensions
find_all_directories = pyt_paths.find_all_directories
find_files_by_ext = pyt_paths.find_files_by_ext

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

find_substring_index = string_handler.find_substring_index

#-------------------------#
# Define custom functions #
#-------------------------#

def modify_obj_permissions(path, extensions2skip="", attr_id=-1):
    """
    Modifies permissions for files or directories at the given path. 
    Automatically detects if the object is a file or directory.
    
    Parameters
    ----------
    path : str or Path
        The path to the file or directory whose permissions will be modified.
    extensions2skip : str or list, optional
        File extensions to skip during permission changes (only applies to files).
    attr_id : int, optional, default=-1
        Permission ID in Python format (octal or decimal).
        If -1, no changes are made to the permissions.

    Raises
    ------
    TypeError:
        If attr_id is not an integer.
    RuntimeError:
        If permission modification fails.

    Note
    ----

    Permission Comparison Table (Python ID to ZSH/BASH ID):
    +----------------+-------------+----------------------------+
    |   Python ID    | ZSH/BASH ID | File Permissions (ls -ltr) |
    +----------------+-------------+----------------------------+
    | 0o664 / 436    | 664         | -rw-rw-r--                 |
    | 0o775 / 509    | 775         | drwxrwxr-x                 |
    | 0o755 / 493    | 755         | -rwxr-xr-x                 |
    | 0o644 / 420    | 644         | -rw-r--r--                 |
    | -1 (no change) | N/A         | No change to permissions   |
    +----------------+-------------+----------------------------+
    """
    # Validate attr_id
    if not isinstance(attr_id, int):
        all_arg_names = get_caller_method_args()
        attr_id_arg_pos = all_arg_names.index("attr_id")
        raise TypeError(f"'{all_arg_names[attr_id_arg_pos]}' "
                        f"(position {attr_id_arg_pos}) must be an integer, "
                        f"got '{type(attr_id)}' instead.")
    
    # Handle file-specific logic (skip certain extensions)
    if os.path.isfile(path):
        if extensions2skip:
            print_format_string("Skipping the following extensions:", extensions2skip)
            file_extension_list = find_all_file_extensions(extensions2skip, path, top_path_only=True)
            obj_path_list = find_files_by_ext(file_extension_list, path, top_path_only=True)
        else:
            obj_path_list = [path]
    elif os.path.isdir():
        obj_path_list = find_all_directories(path)
    else:
        raise ValueError(f"The specified path is neither a file nor a directory: '{path}'")
    
    # Apply permissions
    for obj_path in obj_path_list:
        try:
            os.chmod(obj_path, attr_id)
            print(f"Successfully modified permissions for '{obj_path}'")
        except PermissionError as perr:
            raise RuntimeError(f"Could not modify permissions for {obj_path}: {perr}")

                
def modify_obj_owner(path, module="shutil", extensions2skip="", new_owner=-1, new_group=-1):    
    """
    Modifies the owner and/or group of files or directories at the given path.
    Automatically detects if the object is a file or directory.
    
    Parameters
    ----------
    path : str or Path
        The path to the file or directory whose owner/group will be modified.
    module : str, optional, default='shutil'
        The module used to modify ownership. Must be either 'os' or 'shutil'.
    extensions2skip : str or list, optional
        File extensions to skip during ownership changes (for files only).
    new_owner : int or str, optional, default=-1
        The new owner's username or user ID (int). If -1, no change is made to the owner.
    new_group : int or str, optional, default=-1
        The new group's name or group ID (int). If -1, no change is made to the group.
    
    Raises
    ------
    TypeError:
        If new_owner or new_group are not valid integers or strings.
    ValueError:
        If the module is not 'os' or 'shutil'.
    PermissionError:
        If the operation requires root privileges and the user is not a superuser.
    RuntimeError:
        If the ownership modification fails.
    
    Note
    ----
    The following table compares Python IDs (as either integers or strings) with ZSH/BASH shell
    owner strings or IDs, showing how Python resolves these values, including common system users.
    
    +-------------------+---------------------+---------------------+-----------------------------+
    | Python ID         | ZSH/BASH Equivalent |  ZSH/BASH User ID   | Permission Set (ls -ltr)    |
    +-------------------+---------------------+---------------------+-----------------------------+
    | 'username'        | User string         | User ID (resolved)  | User: rwx                   |
    | 'groupname'       | Group string        | Group ID (resolved) | Group: rwx                  |
    | -1 (owner)        | No change to owner  | -1                  | No change to owner          |
    | -1 (group)        | No change to group  | -1                  | No change to group          |
    | 0 (integer)       | root                | 0 (root)            | User: rwx                   |
    | 1 (integer)       | daemon              | 1 (daemon)          | Group: rwx                  |
    | 2 (integer)       | bin                 | 2 (bin)             | Group: rwx                  |
    | 3 (integer)       | sys                 | 3 (sys)             | Group: rwx                  |
    | 4 (integer)       | adm                 | 4 (adm)             | Group: rwx                  |
    | 5 (integer)       | tty                 | 5 (tty)             | Group: rwx                  |
    | 1000 (integer)    | Numeric User ID     | 1000                | User: rwx (resolved by ID)  |
    | 1001 (integer)    | Numeric Group ID    | 1001                | Group: rwx (resolved by ID) |
    +-------------------+---------------------+---------------------+-----------------------------+
    
    Example:
    --------
    modify_obj_owner("/path/to/file_or_dir", module="os", new_owner="username", new_group="groupname")
    """
  
    # Input validations #
    #####################

    all_arg_names = get_caller_method_args()    
    
    # New owner #
    if not (isinstance(new_owner, (int, str)) or new_owner == -1):
        new_owner_arg_pos = find_substring_index(all_arg_names, "new_owner")
        raise TypeError(f"'{all_arg_names[new_owner_arg_pos]}' "
                        f"(position {new_owner_arg_pos}) must be an integer or string, "
                        f"got '{type(new_owner)}' instead.")
        
    # New group
    if not (isinstance(new_group, (int, str)) or new_group == -1):
        new_grp_arg_pos = find_substring_index(all_arg_names, "new_group")
        raise TypeError(f"{all_arg_names[new_grp_arg_pos]} "
                        f"(position {new_grp_arg_pos}) must be an integer or string, "
                        f"got '{type(new_group)}' instead.")
    
    # Module selection
    if module not in modules:
        raise ValueError(f"Unsupported module '{module}'. Choose one from {modules}")

    # Operations #
    ##############

    # Handle file-specific logic (skip certain extensions)
    if os.path.isfile(path):
        if extensions2skip:
            print_format_string("Skipping the following extensions:", extensions2skip)
            file_extension_list = find_all_file_extensions(extensions2skip, path, top_path_only=True)
            obj_path_list = find_files_by_ext(file_extension_list, path, top_path_only=True)
        else:
            print("All extensions will be considered.")
            obj_path_list = [path]
    elif os.path.isdir(path):
        obj_path_list = find_all_directories(path)
    else:
        raise ValueError(f"The specified path is neither a file nor a directory: '{path}'")
    
    # Apply ownership changes
    for obj_path in obj_path_list:
        if module == "os":
            # Owner modification #
            uid = -1 if new_owner in (None, "unchanged") else pwd.getpwnam(new_owner).pw_uid
            
            # Group modification #
            gid = -1 if new_group in (None, "unchanged") else grp.getgrnam(new_group).gr_gid
            
            try:
                os.chown(obj_path, uid, gid)
                print(f"Successfully modified owner/group for '{obj_path}'.")
            except PermissionError as perr:
                raise RuntimeError(f"Could not perform ownership changes: {perr}")
            
        elif module == "shutil":
            try:
                shutil.chown(obj_path, user=new_owner, group=new_group)
                print(f"Successfully modified owner/group for '{obj_path}'.")
            except PermissionError as perr:
                raise RuntimeError(f"Could not perform ownership changes: {perr}")

#--------------------------#
# Parameters and constants #
#--------------------------#

# OS-related #
#------------#

modules = ["os", "shutil"]