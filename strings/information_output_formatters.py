#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
String formatting filewise module.

This module provides functions to handle different types of string formatting:
- F-strings using Python's format method
- %-strings (percent-strings) using old-style string formatting

Additionally, it contains simple tools to beautify the output format of strings

Functions
---------
- format_string(string2format, arg_obj):
    Formats a given string using Python's format method based on the type of arg_obj.
    
- print_format_string(string2format, arg_obj, end="\n"):
    Formats and prints a given string using Python's format method, optionally specifying an end character.
    
- print_percent_string(string2format, arg_obj):
    Formats and prints a string using old-style percent formatting (%-strings).
    
- string_underliner(string, underline_char):
    Underlines a single- or multiple-line string, using the given character.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.strings.string_handler import find_substring_index
from pyutils.filewise.introspection_utils import get_obj_type_str

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

def string_underliner(string, underline_char="-"):
    """
    Underlines a given string with the specified character.
    
    If the string contains multiple lines, each line will be underlined
    individually with the same character, keeping the length of the underline
    consistent with each line's length.
    
    Parameters
    ----------
    string : str
        The string to be underlined. It can be single or multiline.
        
    underline_char : str, optional
        The character used to underline the string.
        Defaults to a dash ("-").
    
    Returns
    -------
    str_underlined : str
        The original string with an underline applied to each line. 
        For multiline strings, each line is individually underlined.
    
    Example
    -------
    For a single-line string:
    
    >>> string_underliner("Hello", "*")
    'Hello\n*****'
    
    For a multiline string:
    
    >>> string_underliner("Hello\nWorld", "*")
    'Hello\n*****\nWorld\n*****'
    """
    
    # Check if the string contains newlines, indicating a multiline string
    newline_char = "\n"
    multiline = newline_char in string
    
    if multiline:
        # Split the string into individual lines
        word_list = string.split(newline_char)
        
        # Build the underlined string by iterating over each line
        str_underlined = ""
        for word in word_list:
            len_word = len(word)
            # Underline each word with the specified character repeated to match the word's length
            str_underlined += f"{word}\n{underline_char * len_word}\n"
        
        # Remove the last newline character to avoid an extra empty line
        str_underlined = str_underlined.rstrip(newline_char)
        
    else:
        # For a single-line string, simply apply the underline
        len_string = len(string)
        str_underlined = f"{string}\n{underline_char * len_string}"

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
