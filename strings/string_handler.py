#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import os.path
from pathlib import Path

from numpy import array, vectorize, char

import pandas as pd
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
    
    # TODO: add docstring (ChatGPT)
    
    """
    substring: str or [list, np.ndarray, tuple] of str
          If 'str' then it can either be as is or a regex.
          In the latter case, there is no need to explicitly define as so,
          because it connects with Python's built-in 're' module.
    """
    
    # Proper argument selection control #
    #-----------------------------------#
    
    all_arg_names = get_caller_method_args()
    match_index_pos = all_arg_names.index("return_match_index")
    match_index_str_pos = all_arg_names.index("return_match_str")
    
    if return_match_index and return_match_str:
        raise ValueError(f"Arguments '{all_arg_names[match_index_pos]}' "
                         f"and '{all_arg_names[match_index_str_pos]}' "
                         "cannot be True at the same time.")
        
    else:
        if return_match_index and not (return_match_index in match_obj_index_option_keys):
            raise ValueError(f"Invalid indexation name, argument '{all_arg_names[match_index_pos]}'. "
                             f"Choose one name from {match_obj_index_option_keys}.")
            
        if not (isinstance(return_match_str, bool)):
            raise ValueError("Argument '{all_arg_names[match_index_str_pos]}' "
                             "must be a boolean.")
    
    # Case studies #
    #--------------#
    
    if (isinstance(string, str) and isinstance(substring, str)):
        if advanced_search:
            substr_match_obj = advanced_pattern_searcher(string, substring, 
                                                         return_match_index,
                                                         return_match_str,
                                                         case_sensitive,
                                                         find_whole_words,
                                                         all_matches)
        else:
            """
            Do not use np.char.find for this simplest case, 
            simplify and save computation time.
            """
            substr_match_obj = string.find(substring)

    
    elif get_obj_type_str(string) in ["list", "ndarray", "tuple"]:
        if isinstance(substring, str):
    
            if not advanced_search:
                if get_obj_type_str(string) == "ndarray":
                    substr_match_obj_nofilter = char.find(string, substring,
                                                          start=start, end=end)
                    
                    substr_match_obj = [idx
                                         for idx in substr_match_obj_nofilter
                                         if idx != -1]
                    
                else:
                    if end is None:
                        end = 9223372036854775807 # Highest defined index for a tuple
                    substr_match_obj = string.index(substring, start, end)
                    
                
            else:
                substr_match_obj_no_filter = advanced_pattern_searcher(string, substring,
                                                                       return_match_index,
                                                                       return_match_str,
                                                                       case_sensitive, 
                                                                       find_whole_words,
                                                                       all_matches)
      
                substr_match_obj = [n
                                     for n in substr_match_obj_no_filter
                                     if n != -1]
                
        elif get_obj_type_str(substring) in ["list", "ndarray", "tuple"]:
            if not advanced_search:
                substr_match_obj_no_filter = \
                char.find(string, substring, start=start, end=end)  
            else:   
                substr_match_obj_no_filter = advanced_pattern_searcher(string, substring,
                                                                       return_match_index,
                                                                       return_match_str,
                                                                       case_sensitive, 
                                                                       find_whole_words,
                                                                       all_matches)
      
            substr_match_obj = [n
                                 for n in substr_match_obj_no_filter
                                 if n != -1]
                
            
    elif get_obj_type_str(string) == "Series":
        try:
            substr_match_obj_no_filter = string.str.contains(substring)
        except AttributeError:
            substr_match_obj_no_filter = string.iloc[:,0].str.contains[substring]
        
        substr_match_obj = \
        list(substr_match_obj_no_filter[substr_match_obj_no_filter].index)
       

    if isinstance(substr_match_obj, list) and len(substr_match_obj) == 0:
        return -1
    elif isinstance(substr_match_obj, list) and len(substr_match_obj) == 1:
        return substr_match_obj[0]
    else:
        return substr_match_obj


# Core method #
#-#-#-#-#-#-#-#

def advanced_pattern_searcher(string, substring,
                              return_match_index,
                              return_match_str,
                              case_sensitive,
                              find_whole_words,
                              all_matches):
    """
    Perform advanced pattern searching on the input string or list of strings.

    Parameters
    ----------
    string : str, list, np.ndarray, or tuple
        The input string or collection of strings to search within.
    substring : str
        The substring pattern to search for.
    return_match_index : bool
        If True, return the start index of the match.
    return_match_str : bool
        If True, return the matched substring.
    case_sensitive : bool
        If True, the search is case-sensitive.
    find_whole_words : bool
        If True, match the whole word exactly.
    all_matches : bool
        If True, find all matches instead of just the first one.

    Returns
    -------
    match_obj_spec : list or array
        A list or array of matching results based on the input arguments.
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
        match_obj_spec = vectorize(return_search_obj_spec_aux)(*arg_list)
    else:
        match_obj_spec = return_search_obj_spec_aux(*arg_list)
        
    return match_obj_spec
       

# Complementary functions #
#-#-#-#-#-#-#-#-#-#-#-#-#-#

def return_search_obj_spec_aux(string, substring, re_obj_str,
                               return_match_index, return_match_str,
                               iterator_considered, case_sensitive,
                               find_whole_words, all_matches):
    """
    Auxiliary function to handle the pattern searching and result extraction.
    """
    match_obj = re_obj_str(substring, string)
    
    if iterator_considered:
        matches = [m for m in match_obj]
    else:
        matches = [match_obj] if match_obj else []
    
    if return_match_index:
        indices = [m.start() for m in matches] if matches else []
    else:
        indices = []
    
    if return_match_str:
        match_strings = [m.group() for m in matches] if matches else []
    else:
        match_strings = []
    
    return indices, match_strings
 
   
# PosixPath string management #
#-----------------------------#

# Main method #
#-#-#-#-#-#-#-#

def obj_path_specs(obj_path, module="os", splitdelim=None):
    # TODO: if-elif baldintzak 'switch_dict' bidez gauzatzea ez da oso praktikoa?
    
    path_specs_retrieval_modules = filesystem_context_modules[:2]
    
    if module not in path_specs_retrieval_modules:
        raise ValueError("Unsupported module. "
                         f"Choose one from {path_specs_retrieval_modules}.")
    
    if module == "Path":
        obj_PATH = Path(obj_path)
        obj_path_parent = obj_PATH.parent
        obj_path_name = obj_PATH.name
        obj_path_name_noext = obj_PATH.stem
        obj_path_ext = obj_PATH.suffix[1:]
        
    elif module == "os":
        obj_path_parent = os.path.dirname(obj_path)
        obj_path_name = os.path.basename(obj_path)
        obj_path_name_noext = os.path.splitext(obj_path_name)[0]
        obj_path_ext =  os.path.splitext(obj_path_name)[1][1:]
        
    obj_specs_dict = {
        obj_specs_keylist[0] : obj_path_parent,
        obj_specs_keylist[1] : obj_path_name,
        obj_specs_keylist[2] : obj_path_name_noext,
        obj_specs_keylist[4] : obj_path_ext
        }
    
    if splitdelim is not None:
        obj_path_name_noext_parts = obj_path_name_noext.split(splitdelim)
        item_dict_to_add = {obj_specs_keylist[3] : obj_path_name_noext_parts}
        obj_specs_dict.update(item_dict_to_add)
        
    return obj_specs_dict


# Part picker #
#-#-#-#-#-#-#-#

def get_obj_specs(obj_path,
                  obj_spec_key=None,
                  splitdelim=None):
    
    # Proper argument selection control #
    all_arg_names = get_caller_method_args()
    osk_arg_pos = find_substring_index(all_arg_names, "obj_spec_key")
    
    if obj_spec_key not in obj_specs_keylist:
        raise ValueError(f"Invalid path object name, argument '{all_arg_names[osk_arg_pos]}'. "
                         f"Choose one from {obj_specs_keylist}.")
        
    # Get the object specification name #
    if not isinstance(obj_path, dict):
        obj_specs_dict = obj_path_specs(obj_path, splitdelim)
    
    if obj_spec_key == obj_specs_keylist[3] and splitdelim is None:
        raise ValueError("You must specify a string-splitting character "
                         f"if '{all_arg_names[osk_arg_pos]}' == '{obj_spec_key}'.")
    else:
        obj_spec = obj_specs_dict.get(obj_spec_key)
        return obj_spec


# Path parts modifier #
#-#-#-#-#-#-#-#-#-#-#-#

def modify_obj_specs(target_path_obj,
                     obj2modify,
                     new_obj=None,
                     str2add=None):
    
    """
    target_path_obj : str or dict
    """
     
    # Proper argument selection control #
    all_arg_names = get_caller_method_args()
    obj2ch_arg_pos = find_substring_index(all_arg_names, "obj2modify")
    new_obj_arg_pos = find_substring_index(all_arg_names, "new_obj")
    str2add_arg_pos = find_substring_index(all_arg_names, "str2add")
    
    
    if obj2modify not in obj_specs_keylist:
        raise ValueError("Invalid object name to modify, "
                         f"argument '{all_arg_names[obj2ch_arg_pos]}'. "
                         f"Choose one from {obj_specs_keylist}.")
    
    # Get the object specification name #
    if not isinstance(target_path_obj, dict):
        obj_specs_dict = obj_path_specs(target_path_obj)
        
    obj_spec = obj_specs_dict.get(obj2modify)
    
    if obj2modify in obj_specs_keylist_essential:
        if obj2modify != obj_specs_keylist_essential[1]:
            if str2add is not None:
                new_obj = obj_spec + str2add
                
        else:
            if not isinstance(new_obj, tuple):
                raise TypeError(f"If the object to modify is '{obj_specs_keylist[3]}', "
                                "then the provided new object must also be of type 'tuple'")
            
            else:
                name_noext = get_obj_specs(target_path_obj, obj_spec)
                new_obj = substring_replacer(name_noext, new_obj[0], new_obj[1])
                
    else:
        if new_obj is None:
            raise ValueError(f"For '{all_arg_names[obj2ch_arg_pos]}' = '{obj2modify}', "
                             f"'{all_arg_names[str2add_arg_pos]}' argument is ambiguous; "
                             "you must provide yourself the new path object "
                             f"(argument '{all_arg_names[new_obj_arg_pos]}') .")
            
       
    item2updateDict = {obj2modify : new_obj}
    obj_specs_dict.update(item2updateDict)
    
    new_obj_path_joint = join_obj_path_specs(obj_specs_dict)
    return new_obj_path_joint


# Auxiliar string part addition methods #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def add_str_to_aux_path(path2tweak, str2add):
    obj2change = "name_noext"
    output_path_aux = modify_obj_specs(path2tweak, obj2change, str2add=str2add)
    return output_path_aux


def aux_ext_adder(path2tweak, extension):
    obj2change = "ext"
    path_ext = get_obj_specs(path2tweak, obj2change)
    
    if len(path_ext) == 0:
        output_path = modify_obj_specs(path2tweak, obj2change, str2add=extension)
    else:
        output_path = path2tweak
    return output_path


# Separate parts joiner #
#-#-#-#-#-#-#-#-#-#-#-#-#

def join_obj_path_specs(obj_specs_dict):
           
    obj_path_ext = obj_specs_dict.get(obj_specs_keylist[-1])
    obj_path_name_noext = obj_specs_dict.get(obj_specs_keylist[2])
  
    obj_path_parent = obj_specs_dict.get(obj_specs_keylist[0])  
    if obj_path_parent is None:
        joint_obj_path = f"{obj_path_name_noext}.{obj_path_ext}"
    else:
        joint_obj_path_noext = os.path.join(obj_path_parent, obj_path_name_noext)
        joint_obj_path = f"{joint_obj_path_noext}.{obj_path_ext}"
        
    return joint_obj_path
    

# Substring replacements #
#------------------------#

def substring_replacer(string, string2find, string2replace, count_std=-1,
                       advanced_search=False,
                       count_adv=0,
                       flags=0):
    
    all_arg_names = get_caller_method_args()
    adv_search_arg_pos = find_substring_index(all_arg_names, "advanced_search")
            
    if not advanced_search:
        if isinstance(string, str):
            string_replaced = string.replace(string2find, string2replace, count_std)
            
        elif get_obj_type_str(string) in ["list", "ndarray"]:
            if isinstance(string, list):
                string = array(string)
            string_replaced = char.replace(string, string2find, string2replace)
            
        elif get_obj_type_str(string) == "DataFrame":
            string_replaced = pd.DataFrame.replace(string, string2find, string2replace)
            
        elif get_obj_type_str(string) == "Series":
            string_replaced = pd.Series.replace(string, string2find, string2replace)
            
        return string_replaced
            
    else:
        if not isinstance(string, str):
            raise ValueError("Input object must only be of type 'string' "
                             f"if '{all_arg_names[adv_search_arg_pos]}' is True.")
        else:
            string_replaced = re.sub(string2find, string2replace, 
                                     string,
                                     count_adv,
                                     flags)
        
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
          
    Returns
    -------
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

# Standard and essential name lists #
obj_specs_keylist = ['parent', 'name', 'name_noext', 'name_noext_parts', 'ext']
obj_specs_keylist_essential = obj_specs_keylist[2:]

# Substring search available method list #
combined_case_search_method_list = ['default', 'numpy_basic', 'numpy_advanced']

# Search matching object's indexing options #
match_obj_index_option_keys = ["lo", "hi", "span", False]

# String case handling options #
case_modifier_option_keys = ["lower", "upper", "capitalize", "title"]

# String stripping options #
strip_option_keys = ["strip", "lstrip", "rstrip"]

# Switch-type dictionaries #
#--------------------------#

# Search matching object's indexing options #
match_obj_index_option_dict = {
    match_obj_index_option_keys[0] : lambda span: span[0],
    match_obj_index_option_keys[1] : lambda span: span[-1],
    match_obj_index_option_keys[2] : lambda span: span
}

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