#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import os.path
from pathlib import Path
from sys import maxsize

from numpy import array, vectorize, char
from pandas import DataFrame, Series

import re

#-----------------------#
# Import custom modules # 
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import filesystem_context_modules
from pyutils.utilities.general.introspection_utils import get_obj_type_str, get_caller_method_args

#------------------#
# Define functions #
#------------------#

# String pattern management #
#---------------------------#

# Main method #
#-#-#-#-#-#-#-#

def find_substring_index(string,
                         substring, 
                         start=0,
                         end=None,
                         return_match_index="lo",
                         return_match_str=False,
                         advanced_search=False,
                         case_sensitive=False,
                         find_whole_words=False,
                         all_matches=False):
    """
    Finds the index and/or matched string for a specified substring within a given string,
    with support for advanced pattern matching.
    
    Parameters
    ----------
    string : str, list, np.ndarray, or tuple
        The input object to search within.
    substring : str or list-like of str
        The substring or list of substrings to search for. Can be a regex pattern.
    start : int, optional
        Start index for search. Default is 0.
    end : int, optional
        End index for search. If None, it searches to the end of the string or collection. 
    return_match_index :  {"lo", "hi", "both"}, optional
        Defines which match index to return.
    return_match_str : bool, optional
        If True, returns the matched substring instead of the index.
    advanced_search : bool, optional
        If True, uses advanced search with support for regex and special options.
    case_sensitive : bool, optional
        Specifies whether the search should be case-sensitive.
        Defaults to False (case-insensitive).
    find_whole_words : bool, optional
        Ensures that only whole words are matched, avoiding partial word matches.
    all_matches : bool, optional
        If True, finds all occurrences of the substring.
        Otherwise, only the first match is returned.
    
    Returns
    -------
    int, list, or str
        Returns the index or the matching substring depending on the arguments passed
    
    Notes
    -----
    This method relies on the internal `_advanced_pattern_searcher` 
    to perform the pattern search, which itself uses `_return_search_obj_spec` 
    for handling regular expression matching and result extraction.
    """
    # Argument validation #
    #---------------------#
    
    all_arg_names = get_caller_method_args()
    match_index_pos = all_arg_names.index("return_match_index")
    match_index_str_pos = all_arg_names.index("return_match_str")
    
    if return_match_index and return_match_str:
        raise ValueError(f"Arguments '{all_arg_names[match_index_pos]}' "
                         f"and '{all_arg_names[match_index_str_pos]}' "
                         "cannot both be True.")
        
    if return_match_index and not (return_match_index in match_obj_index_option_keys):
        raise ValueError(f"Invalid '{all_arg_names[match_index_pos]}' value. "
                         f"Choose from {match_obj_index_option_keys}.")
        
    if not (isinstance(return_match_str, bool)):
        raise ValueError("Argument '{all_arg_names[match_index_str_pos]}' "
                         "must be a boolean.")
    
    # Case studies #
    #--------------#
    
    if (isinstance(string, str) and isinstance(substring, str)):
        if advanced_search:
            substr_match_obj = _advanced_pattern_searcher(string, substring, 
                                                          return_match_index,
                                                          return_match_str,
                                                          case_sensitive,
                                                          find_whole_words,
                                                          all_matches)
        else:
            return string.find(substring)

    
    elif get_obj_type_str(string) in ["list", "ndarray", "tuple"]:
        if isinstance(substring, str):
    
            # Simple search without advanced features
            if not advanced_search:
                if get_obj_type_str(string) == "ndarray":
                    match_indices = char.find(string, substring, start=start, end=end)
                    return [idx for idx in match_indices if idx != -1]
                
                else:
                    if end is None:
                        end = maxsize # Highest defined index for a tuple
                    substr_match_obj = string.index(substring, start, end)
                    
                
            else:
                match_indices = _advanced_pattern_searcher(string, substring,
                                                           return_match_index,
                                                           return_match_str,
                                                           case_sensitive, 
                                                           find_whole_words,
                                                           all_matches)
      
                return [n for n in match_indices if n != -1]
                
        elif get_obj_type_str(substring) in ["list", "ndarray", "tuple"]:
            if not advanced_search:
                return char.find(string, substring, start=start, end=end)  
            else:   
                match_indices = _advanced_pattern_searcher(string, substring,
                                                           return_match_index,
                                                           return_match_str,
                                                           case_sensitive, 
                                                           find_whole_words,
                                                           all_matches)
      
            return [n for n in match_indices if n != -1]
                
    # Handle case: search in pandas Series #
    #--------------------------------------#
    
    elif get_obj_type_str(string) == "Series":
        try:
            match_series = string.str.contains(substring)
        except AttributeError:
            match_series = string.iloc[:, 0].str.contains(substring)
        else:
            return list(match_series[match_series].index)
       

    # Handle the return based on the result type #
    #--------------------------------------------#
    
    if isinstance(substr_match_obj, list):
        if len(substr_match_obj) == 0:
            return -1
        elif len(substr_match_obj) == 1:
            return substr_match_obj[0]
        else:
            return substr_match_obj
    else:
        return substr_match_obj


# Core method #
#-#-#-#-#-#-#-#

def _advanced_pattern_searcher(string, substring,
                               return_match_index,
                               return_match_str,
                               case_sensitive,
                               find_whole_words,
                               all_matches):
    """
    Performs an advanced pattern search based on specified criteria,
    with options for regex, case-sensitivity, and whole word matching,
    and returns indices and/or match strings.
    
    Parameters
    ----------
    string : str, list, np.ndarray, or tuple
        The input object to search within.
    substring : str or list-like of str
        The substring or list of substrings to search for. Can include regex patterns.
    return_match_index : {"lo", "hi", "both"}
        Defines which match index to return.
    return_match_str : bool
        If True, returns the matched substring instead of the index.
    case_sensitive : bool
        Whether the search is case-sensitive. Defaults to False.
    find_whole_words : bool
        If True, matches whole words only.
    all_matches : bool
        If True, finds all matches; otherwise, only the first is returned.
    
    Returns
    -------
    list or tuple
        A list or tuple of matching indices and/or matched substrings.
        
    Notes
    -----    
    This method serves as an auxiliary to `find_substring_index`, 
    utilizing `_return_search_obj_spec` for detailed pattern matching and result extraction.
    """    
    # Determine if the input string is multi-line
    multiline = '\n' in string \
                if isinstance(string, str) \
                else any('\n' in s for s in string)
    flags = re.MULTILINE if multiline else 0

    # No option selected #
    #--------------------#
    if not case_sensitive and not all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.search(substring, 
                                                         string, 
                                                         re.IGNORECASE | flags)
        iterator_considered = False

    # One option selected #
    #---------------------#
    elif case_sensitive and not all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.search(substring, string, flags)
        iterator_considered = False
        
    elif not case_sensitive and all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.finditer(substring,
                                                           string, 
                                                           re.IGNORECASE | flags)
        iterator_considered = True        
        
    elif not case_sensitive and not all_matches and find_whole_words:
        re_obj_str = lambda substring, string: re.fullmatch(substring,
                                                            string, 
                                                            re.IGNORECASE | flags)
        iterator_considered = False

    # Two options selected #
    #----------------------# 
    elif case_sensitive and all_matches and not find_whole_words:
        re_obj_str = lambda substring, string: re.finditer(substring, string, flags)
        iterator_considered = True        
        
    elif case_sensitive and not all_matches and find_whole_words:
        re_obj_str = lambda substring, string: re.fullmatch(substring, string, flags)
        iterator_considered = False

    # Extract the matching information #
    #----------------------------------#
    arg_list = [
        string, substring, re_obj_str,
        return_match_index, return_match_str,
        iterator_considered,
        case_sensitive,
        find_whole_words,
        all_matches
    ]
    
    if get_obj_type_str(string) in ["list", "ndarray", "tuple"]:        
        match_obj_spec = vectorize(_return_search_obj_spec)(*arg_list)
    else:
        match_obj_spec = _return_search_obj_spec(*arg_list)
        
    return match_obj_spec
       

# Auxiliary functions #
#-#-#-#-#-#-#-#-#-#-#-#

def _return_search_obj_spec(string, substring, re_obj_str,
                            return_match_index, return_match_str,
                            iterator_considered, case_sensitive,
                            find_whole_words, all_matches):
    """
    Handles the regular expression search and result extraction for advanced search.
    
    Parameters
    ----------
    string : str
        The string to search in.
    substring : str
        The pattern or substring to search for.
    re_obj_str : callable
        A callable that performs the actual pattern search using regex or custom logic.
    return_match_index :  {"lo", "hi", "both"}
        Defines which match index to return.
    return_match_str : bool
        If True, returns the matched substrings.
    iterator_considered : bool
        If True, collects all matches in an iterable.
    case_sensitive : bool
        Whether or not to perform a case-sensitive match.
    find_whole_words : bool
        Match whole words only if set to True.
    all_matches : bool
        If True, finds all matches rather than just the first.
    
    Returns
    -------
    tuple
        A tuple of indices and matched substrings. Its components are:
        - indices : list of int
              The start positions of matches.
        - match_strings : list of str
              The matched substrings.
              
    Notes
    -----
    This is a helper function used by `_advanced_pattern_searcher`
    to finalise the search and process the results.
    """
    
    # Create the match object using the provided regex search function
    match_obj = re_obj_str(substring, string)
    
    # If iterator is considered, extract all matches; otherwise, handle single match
    if iterator_considered:
        matches = [m for m in match_obj]
    else:
        matches = [match_obj] if match_obj else []
    
    # Use the appropriate action for returning indices based on return_match_index
    if return_match_index in match_index_action_dict:
        indices = match_index_action_dict[return_match_index](matches)
    else:
        indices = []
    
    if return_match_str:
        match_strings = [m.group() for m in matches] if matches else []
    else:
        match_strings = []
    
    return indices, match_strings
 
# %%
   
# PosixPath string management #
#-----------------------------#

# Main methods #
#-#-#-#-#-#-#-#-

# Specifications of a file or directory path #
##############################################

def obj_path_specs(obj_path, module="os", splitdelim=None):
    """
    Retrieve the specifications of a file or directory path.
    
    This function identifies different parts of the provided path string, such as
    the parent directory, file name, file name without extension, and file extension.
    It works with either the 'os' module or 'pathlib.Path'.

    Parameters
    ----------
    obj_path : str
        The file or directory path string to process.
    module : str, optional
        The module to use for path processing. Options are 'os' (default) and 'Path' (from pathlib).
    splitdelim : str, optional
        Delimiter for splitting the file name (without extension) into parts. If None, no splitting is performed.

    Returns
    -------
    obj_specs_dict : dict
        A dictionary containing the following path components:
        - 'parent': The parent directory of the path.
        - 'name': The full name of the file or directory.
        - 'name_noext': The file or directory name without the extension.
        - 'ext': The file extension (without the dot).
        - 'name_noext_parts' (optional): A list of parts if the file name (without extension) is split by `splitdelim`.

    Raises
    ------
    ValueError
        If an unsupported module is provided.
    """

    # List of supported modules for path specification retrieval
    path_specs_retrieval_modules = filesystem_context_modules[:2]
    
    # Check if the specified module is valid
    if module not in path_specs_retrieval_modules:
        raise ValueError(f"Unsupported module '{module}'. "
                         f"Choose one from {path_specs_retrieval_modules}.")
    
    # Retrieve path specifications based on the chosen module
    obj_specs_dict = path_functions[module](obj_path)
    
    # Optionally, split the file name without extension by the specified delimiter
    if splitdelim:
        obj_specs_dict['name_noext_parts'] = obj_specs_dict['name_noext'].split(splitdelim)
        
    return obj_specs_dict


# Specific component retrieval #
################################

def get_obj_specs(obj_path, obj_spec_key=None, splitdelim=None):
    """
    Retrieve a specific component of a file or directory path.

    This function returns the desired part of the path string, such as the parent directory,
    file name, file name without extension, or file extension.
    It can also split the file name (without extension) into parts based on a delimiter.

    Parameters
    ----------
    obj_path : str or dict
        The file or directory path string to process, 
        or a dictionary with pre-extracted path components.
    obj_spec_key : str
        The part of the path to retrieve. Must be one of the following keys:
        - 'parent': The parent directory.
        - 'name': The full name of the file or directory.
        - 'name_noext': The file name without the extension.
        - 'name_noext_parts': The file name without extension, split by `splitdelim`.
        - 'ext': The file extension (without the dot).
    splitdelim : str, optional
        Delimiter for splitting the file name (without extension) into parts. 
        Required if `obj_spec_key` is 'name_noext_parts'.

    Returns
    -------
    obj_spec : str or list
        The requested part of the path string, 
        or a list of parts if `obj_spec_key` is 'name_noext_parts'.

    Raises
    ------
    ValueError
        If `obj_spec_key` is invalid or if `splitdelim` is not provided when required.
    """
    
    # Ensure the provided obj_spec_key is valid #
    all_arg_names = get_caller_method_args()
    osk_arg_pos = find_substring_index(all_arg_names, "obj_spec_key")
    
    if obj_spec_key not in obj_specs_keylist:
        raise ValueError(f"Invalid '{all_arg_names[osk_arg_pos]}' key. "
                         f"Choose from {obj_specs_keylist}.")
        
    # If obj_path is not already a dictionary, get the path specifications
    if not isinstance(obj_path, dict):
        obj_specs_dict = obj_path_specs(obj_path, splitdelim=splitdelim)
    else:
        obj_specs_dict = obj_path
    
    # If obj_spec_key is 'name_noext_parts', ensure that splitdelim is provided
    if obj_spec_key == obj_specs_keylist[3] and not splitdelim:
        raise ValueError("You must specify a splitting character "
                         f"if 'obj_spec_key' == '{obj_spec_key}'.")
    
    # Return the requested path component
    obj_spec = obj_specs_dict.get(obj_spec_key)
    return obj_spec


# Path parts modifier #
#######################

def modify_obj_specs(target_path_obj, obj2modify, new_obj=None, str2add=None):    
    """
    Modify a specified part of a file path string, such as the parent directory, 
    filename, or extension. Changes can include replacing the object or 
    appending a string to the existing part. Returns the modified path.

    Parameters
    ----------
    target_path_obj : str or dict
        The original file path to modify, or a dictionary containing path specifications.
    obj2modify : str
        Specifies which part of the path to modify. Must be one of ['parent', 'name', 'name_noext', 'ext'].
    new_obj : str, optional
        The new object to replace the specified part of the path. For 'name_noext', must be a tuple with (old, new) values.
    str2add : str, optional
        A string to append to the specified part of the path (if applicable).
    
    Returns
    -------
    new_obj_path_joint : str
        The modified file path.
    
    Raises
    ------
    ValueError
        If obj2modify is invalid or new_obj is missing for certain modifications.
    TypeError
        If new_obj is not a tuple when modifying 'name_noext'.
    """
     
    # Argument validation and control #
    all_arg_names = get_caller_method_args()
    obj2ch_arg_pos = find_substring_index(all_arg_names, "obj2modify")
    new_obj_arg_pos = find_substring_index(all_arg_names, "new_obj")
    str2add_arg_pos = find_substring_index(all_arg_names, "str2add")
    
    if not isinstance(str2add, str):
        str2add = str(str2add)
    
    # Validate object part to modify (arg 'obj2modify') #
    obj_specs_keylist_practical = obj_specs_keylist[:3] + [obj_specs_keylist[-1]]
    if obj2modify not in obj_specs_keylist_practical:
        raise ValueError("Invalid object name to modify, "
                         f"argument '{all_arg_names[obj2ch_arg_pos]}'. "
                         f"Choose one from {obj_specs_keylist}.")
    
    # Get path specifications as a dict if input is a path string
    if not isinstance(target_path_obj, dict):
        obj_specs_dict = obj_path_specs(target_path_obj)
    else:
        obj_specs_dict = target_path_obj
        
    obj_spec = obj_specs_dict.get(obj2modify)
    
    # Modifying essential components (name_noext, ext)
    obj_specs_keylist_essential = obj_specs_keylist_practical[2:]
    if obj2modify in obj_specs_keylist_essential:
        if obj2modify != obj_specs_keylist_essential[1]:  # Not 'name_noext_parts'
            if str2add:
                new_obj = obj_spec + str2add
                
        else:
            if not isinstance(new_obj, tuple):
                raise TypeError(f"If modifying '{obj_specs_keylist[2]}', "
                                f"'{all_arg_names[new_obj_arg_pos]}' must be a tuple.")
            else:
                name_noext = get_obj_specs(target_path_obj, obj2modify)
                new_obj = substring_replacer(name_noext, new_obj[0], new_obj[1])
                
    else:
        # Handle other cases like 'parent' and 'name'
        if new_obj is None:
            raise ValueError(f"Ambiguous '{all_arg_names[obj2ch_arg_pos]}' = '{obj2modify}' "
                             f"modification with argument '{all_arg_names[str2add_arg_pos]}' "
                             "being provided.\n"
                             "You must provide the new value "
                             f"(argument '{all_arg_names[new_obj_arg_pos]}').")
    
    # Update the path specifications with the modified part
    obj_specs_dict.update({obj2modify: new_obj})
    
    # Join the modified parts and return the final path
    new_obj_path_joint = _join_obj_path_specs(obj_specs_dict)
    return new_obj_path_joint


# Auxiliary methods #
#-#-#-#-#-#-#-#-#-#-#-

# Separate parts joiner #
#########################

def _join_obj_path_specs(obj_specs_dict):
    """
    Joins the parts of a path specification dictionary into a complete file path string.

    Parameters
    ----------
    obj_specs_dict : dict
        A dictionary containing parts of a path, such as 'parent', 'name_noext', and 'ext'.

    Returns
    -------
    joint_obj_path : str
        The complete file path string based on the provided parts.
    """
    obj_path_ext = obj_specs_dict.get(obj_specs_keylist[-1])  # 'ext'
    obj_path_name_noext = obj_specs_dict.get(obj_specs_keylist[2])  # 'name_noext'
    obj_path_parent = obj_specs_dict.get(obj_specs_keylist[0])  # 'parent'
    
    if obj_path_parent is None:
        # If there is no parent directory, join name_noext and ext
        joint_obj_path = f"{obj_path_name_noext}.{obj_path_ext}"
    else:
        # Join parent, name_noext, and ext
        joint_obj_path_noext = os.path.join(obj_path_parent, obj_path_name_noext)
        joint_obj_path = f"{joint_obj_path_noext}.{obj_path_ext}"
        
    return joint_obj_path

# %%

# String part addition methods #
#------------------------------#

def add_to_path(path2tweak, str2add):
    """
    Adds a user-defined string to the part of the path without the extension.

    Parameters
    ----------
    path2tweak : str or dict
        The path object (either a string or dictionary with path components) 
        to which the string should be added.
    str2add : str
        The string to add to the path part without the extension.

    Returns
    -------
    str
        The modified path with the string added to the part without the extension.
    """
    obj2change = "name_noext"
    return modify_obj_specs(path2tweak, obj2change, str2add=str2add)


def append_ext(path2tweak, extension):
    """
    Adds an extension to the path if it does not already have one.

    Parameters
    ----------
    path2tweak : str or dict
        The path object (either a string or dictionary with path components) 
        to which the extension should be added.
    extension : str
        The extension to add if the path does not already have one.

    Returns
    -------
    output_path : str
        The modified path with the extension added, or the original path 
        if it already has one.
    """
    obj2change = "ext"
    
    # Retrieve the current extension from the path
    path_ext = get_obj_specs(path2tweak, obj2change)
    
    # If the path has no extension, add the provided extension
    if not path_ext:
        output_path = modify_obj_specs(path2tweak, obj2change, str2add=extension)
    else:
        output_path = path2tweak  # Return the original path if it already has an extension
    return output_path


# Substring replacements #
#------------------------#

def substring_replacer(string, substr2find, substr2replace, count_std=-1,
                       advanced_search=False,
                       count_adv=0,
                       flags=0):
    """
    Replaces occurrences of a specified substring in a given object
    (string, list, numpy.ndarray, pandas DataFrame, or pandas Series) 
    using either a simple replace method or advanced regex techniques.

    Parameters
    ----------
    string : str, list, numpy.ndarray, pd.DataFrame, or pd.Series
        The input object where the substring will be replaced.
    substr2find : str
        The substring to search for in the input object.
    substr2replace : str
        The substring to replace the found occurrences.
    count_std : int, optional
        The maximum number of occurrences to replace in standard replace mode. 
        Default is -1, which means replace all occurrences.
    advanced_search : bool, optional
        If True, uses regular expressions for more complex search and replace. Default is False.
    count_adv : int, optional
        The maximum number of occurrences to replace when using advanced search. Default is 0.
        If 0, all occurrences will be replaced.
    flags : int, optional
        Flags to modify the behavior of the regex operation. Default is 0.

    Returns
    -------
    str, list, numpy.ndarray, pd.DataFrame, or pd.Series
        Returns the modified object with the specified replacements.

    Notes
    -----
    - If `advanced_search` is True, the function employs regex substitutions, which can be 
      used for strings only. For lists, numpy.ndarray, DataFrames, or Series, 
      the built-in `replace` method is applied, allowing more flexibility in replacements.
    - If `advanced_search` is False, the function uses the built-in `replace` method 
      for all supported input types, enabling straightforward substring replacements.
    """
    
    obj_type = get_obj_type_str(string, lowercase=True)
    
    if obj_type not in str_repl_obj_types:
        raise TypeError("Input object must be of type 'string', 'list', "
                        "'numpy.ndarray', 'DataFrame', or 'Series'.")
            
    if not advanced_search:
        string_replaced = replace_actions[obj_type](string, substr2find, substr2replace, count_std)
        return string_replaced
            
    else:
        if isinstance(string, str):
            string_replaced = re.sub(substr2find, substr2replace, 
                                     string, count_adv, flags)
        else:
            # Apply regex replacement to each element in lists/arrays
            string_replaced = [
                re.sub(substr2find, substr2replace, elem, count_adv, flags) 
                for elem in string
            ]
        return string_replaced
    
# Case handling #
#---------------#
        
def case_modifier(string, case=None):    
    """
    Function to modify the given string case.
    
    Parameters
    ----------
    case : {'lower', 'upper', 'capitalize' 'title'}, optional.
        Case to which modify the string's current one.
            
    Returns
    -------
    String case modified accordingly
    """
    
    if (case is None or case not in case_modifier_option_keys):
        raise ValueError("You must select a case modifying option from "
                         "the following list:\n"
                         f"{case_modifier_option_keys}")
        
    else:
        str_case_modified = case_modifier_option_dict.get(case)(string)
        return str_case_modified

    
# String polisher #
#-----------------#

def strip(string, strip_option='strip', chars=None):
    
    """
    Removes the white spaces -or the given substring- 
    surrounding the string, except the inner ones.
    
    Parameters
    ----------
    strip_option: {'strip', 'lstrip', 'lstrip' 'title'} or None
        Location of the white spaces or substring to strip.
        Default option is the widely used 'strip'.
        
    Raises
    ------
    ValueError
        If 'strip_option' is not within the allowed options.
          
    Returns
    -------
    string_stripped : str
        String with the specified characters surrounding it removed.
    """
    
    if (strip_option is None or strip_option not in strip_option_keys):
        raise ValueError("You must select a case strip option from "
                         f"the following list: {strip_option_keys}")
        
    else:
        string_stripped = strip_option_dict.get(strip_option)(string, chars)
        return string_stripped
    

#--------------------------#
# Parameters and constants #
#--------------------------#

# Allowed options #
#-----------------#

# Standard and essential name lists #
obj_specs_keylist = ['parent', 'name', 'name_noext', 'name_noext_parts', 'ext']

# Search matching object's indexing options #
match_obj_index_option_keys = ["lo", "hi", "both"]

# String case handling options #
case_modifier_option_keys = ["lower", "upper", "capitalize", "title"]

# String stripping options #
strip_option_keys = ["strip", "lstrip", "rstrip"]

# Object types for string replacements #
str_repl_obj_types = ["str", "list", "ndarray", "dataframe", "series"]

# Switch case dictionaries #
#--------------------------#

# String case handling #
case_modifier_option_dict = {
    case_modifier_option_keys[0] : lambda string : string.lower(),
    case_modifier_option_keys[1] : lambda string : string.upper(),
    case_modifier_option_keys[2] : lambda string : string.capitalize(),
    case_modifier_option_keys[3] : lambda string : string.title()
    }

case_modifier_option_keys = list(case_modifier_option_dict.keys())

# String stripping #
strip_option_dict = {
    strip_option_keys[0] : lambda string, chars: string.strip(chars),
    strip_option_keys[1] : lambda string, chars: string.lstrip(chars),
    strip_option_keys[2] : lambda string, chars: string.rstrip(chars),
}

# File or directory path specifications retrieval #
path_functions = {
    'os': lambda obj_path : {
        'parent': os.path.dirname(obj_path),
        'name': os.path.basename(obj_path),
        'name_noext': os.path.splitext(os.path.basename(obj_path))[0],
        'ext': os.path.splitext(os.path.basename(obj_path))[1][1:]
    },
    'Path': lambda obj_path : {
        'parent': Path(obj_path).parent,
        'name': Path(obj_path).name,
        'name_noext': Path(obj_path).stem,
        'ext': Path(obj_path).suffix[1:]
    }
}

# Index return types for pattern matches #
match_index_action_dict = {
    "lo" : lambda matches : [m.start() for m in matches] if matches else [],
    "hi" : lambda matches : [m.end() for m in matches] if matches else [],
    "both" : lambda matches : [m.span() for m in matches] if matches else [],
    }

# Substring replacement actions using simpler methods #
replace_actions = {
    "str": lambda s, sb2find, sb2replace, count_std : s.replace(sb2find, sb2replace, count_std),
    "list": lambda s, sb2find, sb2replace, _ : char.replace(array(s), sb2find, sb2replace),
    "ndarray": lambda s, sb2find, sb2replace, _ : char.replace(s, sb2find, sb2replace),
    "dataframe": lambda s, sb2find, sb2replace, _ : DataFrame.replace(s, sb2find, sb2replace),
    "series": lambda s, sb2find, sb2replace, _ : Series.replace(s, sb2find, sb2replace),
}
    
