#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from strings.string_handler import find_substring_index

#-------------------------#
# Define custom functions #
#-------------------------#

# String format management #
#--------------------------#

# F-strings #
def format_string(string2format, arg_obj):    
    bracket_index_list = find_substring_index(string2format, "{}",
                                              advanced_search=True,
                                              all_matches=True)
    
    num_brackets = len(bracket_index_list)
    
    try:
        if isinstance(arg_obj, (list, tuple)):
            if num_brackets >= 2:
                formatted_string = string2format.format(*arg_obj)
            else:
                formatted_string = string2format.format(arg_obj)
        
        elif isinstance(arg_obj, dict):
            formatted_string = string2format.format(**arg_obj)
            
        return formatted_string
    
        
    except TypeError:
        raise TypeError(type_error_str1)
    
    except IndexError:
        raise IndexError(index_error_str)
    
    except SyntaxError:
        raise SyntaxError(syntax_error_str)
        
        
def print_format_string(string2format, arg_obj, end="\n"):
    try:
        formatted_string = format_string(string2format, arg_obj)
        print(formatted_string, end=end)
    except TypeError:
        raise TypeError(type_error_str1)
    except IndexError:
        raise IndexError(index_error_str)
    except SyntaxError:
        raise SyntaxError(syntax_error_str)

    
# %-strings (percent-strings) #
def print_percent_string(string2format, arg_obj):
    try:
        if isinstance(arg_obj, str):
            print(string2format %(arg_obj))
        else:
            raise TypeError(type_error_str2)
            
    except TypeError:
       raise TypeError(type_error_str1)
                
    except IndexError:
        raise IndexError(index_error_str)
        
    except SyntaxError:
        raise SyntaxError(syntax_error_str)
        
        
# Object information gatherers #
#------------------------------#

# Object type's class to string conversions #
def get_obj_type_str(obj):
    obj_type_class = type(obj)
    obj_type_str = obj_type_class.__name__
    return obj_type_str

# Retrieve a function's name to use for visualization purposes #
def retrieve_function_name(library="inspect"):
    """Returns the name of the method that called this function."""

    if library not in method_name_retrieval_libraries:
        raise ValueError("Unsupported library, choose one from "
                         f"{method_name_retrieval_libraries}.")
    else:
        if library == "inspect":
            import inspect
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back  # Get the caller's frame
            frame_info = inspect.getframeinfo(caller_frame)
            return frame_info.function
        elif library == "sys":
            import sys
            """Returns the name of the method that called this function using sys._getframe()."""
            method_name = sys._getframe(1).f_code.co_name  # Get the caller's frame (1 level up)
        return method_name


#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported library list for method name retrievals #
method_name_retrieval_libraries = ["inspect", "sys"]

# Error strings #
type_error_str1 = "Check the iterable type passed to the instance."
type_error_str2 = "Argument must be of type 'str' only."

index_error_str = "Not all indices were referenced in the string to format."

syntax_error_str = "One or more arguments in the formatting object "\
                   "has strings with unclosed quotes."