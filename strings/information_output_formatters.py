#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
String formatting utilities module.

This module provides functions to handle different types of string formatting:
- F-strings using Python's format method
- %-strings (percent-strings) using old-style string formatting

Functions
---------
- format_string(string2format, arg_obj):
    Formats a given string using Python's format method based on the type of arg_obj.
    
- print_format_string(string2format, arg_obj, end="\n"):
    Formats and prints a given string using Python's format method, optionally specifying an end character.
    
- print_percent_string(string2format, arg_obj):
    Formats and prints a string using old-style percent formatting (%-strings).

Constants
---------
- main_input_dtype_list_strfmt
    List of frequent input data types suitable for string formatting.
    
- type_error_str1
    Error string raised for TypeError in format_string and print_format_string.
    
- type_error_str2
    Error string raised for TypeError in print_percent_string.
    
- index_error_str
    Error string raised for IndexError in format_string and print_format_string.
    
- syntax_error_str
    Error string raised for SyntaxError in format_string and print_format_string.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings.string_handler import find_substring_index
from pyutils.utilities.introspection_utils import get_obj_type_str

#-------------------------#
# Define custom functions #
#-------------------------#

# String format management #
#--------------------------#

# F-strings #
def format_string(string2format, arg_obj):
    """
    Format a string using Python's format method.

    Args
    ----
    string2format : str
        The string to be formatted.
    arg_obj : list, tuple or numpy.ndarray
        The object used to fill in the placeholders in 'string2format'.

    Returns
    -------
    str: Formatted string.

    Raises
    ------
    TypeError: If arg_obj is not of the expected type.
    IndexError: If there are not enough indices referenced in the string to format.
    SyntaxError: If there are syntax errors in the formatting object.
    """
    bracket_index_list = find_substring_index(string2format, "{}",
                                              advanced_search=True,
                                              all_matches=True)
    
    num_brackets = len(bracket_index_list)
    
    try:               
        if (get_obj_type_str(arg_obj) in main_input_dtype_list_strfmt\
            and num_brackets >= 2):
            formatted_string = string2format.format(*arg_obj)
            
        elif ((get_obj_type_str(arg_obj) in main_input_dtype_list_strfmt and num_brackets < 2)\
            or (get_obj_type_str(arg_obj) not in main_input_dtype_list_strfmt\
            and not isinstance(arg_obj, dict))):
            formatted_string = string2format.format(arg_obj)
        
        elif isinstance(arg_obj, dict):
            formatted_string = string2format.format(**arg_obj)
           
        return formatted_string
    
    except (TypeError, UnboundLocalError):
        raise TypeError(type_error_str1)
    
    except IndexError:
        raise IndexError(index_error_str)
    
    except SyntaxError:
        raise SyntaxError(syntax_error_str)
        
        
def print_format_string(string2format, arg_obj, end="\n"):
    """
    Format and print a string using Python's format method.

    Args
    ----
    string2format : str
        The string to be formatted and printed.
    arg_obj : list, tuple or numpy.ndarray
        The object used to fill in the placeholders in string2format.
    end : str, optional
        String appended after the last value, default is "\n".

    Raises
    ------
    TypeError: If arg_obj is not of the expected type.
    IndexError: If there are not enough indices referenced in the string to format.
    SyntaxError: If there are syntax errors in the formatting object.
    """
    try:
        formatted_string = format_string(string2format, arg_obj)
    except Exception as e:
        raise Exception(f"An error occurred: {e}") from e
    else:
        print(formatted_string, end=end)

    
# %-strings (percent-strings) #
def print_percent_string(string2format, arg_obj):
    """
    Format and print a string using old-style percent formatting (%-strings).

    Args
    ----
    string2format : str
        The string to be formatted and printed.
    arg_obj : str
        The string object to be formatted using the % operator.

    Raises
    ------
    TypeError: If arg_obj is not of type 'str'.
    IndexError: If there are not enough indices referenced in the string to format.
    """
    try:
        if isinstance(arg_obj, str):
            print(string2format % (arg_obj))
        else:
            raise TypeError(type_error_str2)
            
    except TypeError:
        raise TypeError(type_error_str1)
                
    except IndexError:
        raise IndexError(index_error_str)
        
    except SyntaxError:
        raise SyntaxError(syntax_error_str)
        

# String font effects #
#---------------------#

# TODO: begizta optimizatu
# TODO: docstring-a idatzi

def string_underliner(string, underline_char):
    multiline = "\n" in string
    
    if multiline:
        word_list = string.split("\n")
        str_underlined = ""
        for word in word_list:
            len_word = len(word)
            str_underlined += f"{word}\n{underline_char:{underline_char}^{len_word}}\n"
            
        # Remove the last newline character #
        str_underlined = str_underlined.rstrip('\n')
        
    else:
        len_string = len(string)
        str_underlined = f"{string}\n{underline_char:{underline_char}^{len_string}}"

    return str_underlined

#--------------------------#
# Parameters and constants #
#--------------------------#

# Frequent input data types for string formatting #
main_input_dtype_list_strfmt = ["list", "ndarray", "tuple"]

# Error strings #
type_error_str1 = "Check the iterable type passed to the instance."
type_error_str2 = "Argument must be of type 'str' only."

index_error_str = "Not all indices were referenced in the string to format."

syntax_error_str = "One or more arguments in the formatting object "\
                    "has strings with unclosed quotes."
