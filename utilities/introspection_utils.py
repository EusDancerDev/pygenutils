#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import inspect
import sys

#------------------#
# Define functions #
#------------------#

# Methods #
#---------#

def retrieve_function_name(library="inspect"):
    """Returns the name of the method defined in situ."""

    if library not in method_name_retrieval_libraries:
        raise ValueError("Unsupported library, choose one from "
                          f"{method_name_retrieval_libraries}.")
    else:
        if library == "inspect":
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back  # Get the caller's frame
            frame_info = inspect.getframeinfo(caller_frame)
            return frame_info.function
        elif library == "sys":
            method_name = sys._getframe(1).f_code.co_name  # Get the caller's frame (1 level up)
        return method_name
    
    
def get_obj_type_str(obj):
    """Returns the type of an object as a string"""
    obj_type_class = type(obj)
    obj_type_str = obj_type_class.__name__
    return obj_type_str

# Attributes #
#------------#

def get_attribute_names(obj):
    """Returns the names of all attributes of an object."""
    attr_list = [attr 
                 for attr in dir(obj)
                 if not callable(getattr(obj, attr))]
    
    return attr_list


# More functions related to introspection or utility as needed #
#--------------------------------------------------------------#

# Example of potential future expansion
def inspect_memory_usage(obj):
    """Inspects memory usage of an object."""
    # Implementation details
    
#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported library list for method name retrievals #
method_name_retrieval_libraries = ["inspect", "sys"]