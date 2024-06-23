#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**

This program is an application of the main module 'change_permissions_main',
and it uses the 'modify_obj_permissions' and 'modify_obj_owner' 
attributes and/or functions.
YOU MAY REDISTRIBUTE this program along any other directory,
but keep in mind that the module is designed to work with absolute paths.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from files_and_directories import change_permissions_main

# Create aliases #
#----------------#

modify_obj_owner = change_permissions_main.modify_obj_owner
modify_obj_permissions = change_permissions_main.modify_obj_permissions

#-------------------#
# Define parameters #
#-------------------#

path = "/home/jonander/Documents"

# Main task control switches #
#----------------------------#

make_obj_perm_mods = False
make_obj_owner_mods = False

# General parameters #
obj_type = "file"
extensions2skip = ""

# Specific parameter oriented to object permission modification #
attr_id = 644

# Specific parameters oriented to object owner modification #
module = "shutil"

"""
**Note**

If there is no need to change the user and/or group name,
please set one or both of the following to None or 'unchanged'.
"""

new_owner = None
new_group = None

#-------------------------------------------------------------#
# Perform the tasks according to the values of the parameters #
#-------------------------------------------------------------#
    
if make_obj_perm_mods:
    modify_obj_permissions(path,
                           obj_type,
                           extensions2skip,
                           attr_id)

if make_obj_owner_mods:
    modify_obj_owner(path,
                     module,
                     obj_type,
                     extensions2skip,
                     new_owner,
                     new_group)
