#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import inspect

from pathlib import Path

import numpy as np
import pandas as pd
import re

#-----------------------#
# Import custom modules # 
#-----------------------#

from parameters_and_constants.global_parameters import common_delim_list

#------------------#
# Define functions #
#------------------#

# String pattern management #
#---------------------------#

# Main method #
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
    substring: str or [list, np.ndarray, tuple] of str
          If 'str' then it can either be as is or a regex.
          In the latter case, there is no need to explicitly define as so,
          because it connects with Python's built-in 're' module.
    """
    
    # Proper argument selection control #
    #-----------------------------------#
    
    arg_names = find_substring_index.__code__.co_varnames
    match_index_pos = [i for i,arg in enumerate(arg_names) 
                       if arg == "return_match_index"][0]
    
    match_index_str_pos = [i for i,arg in enumerate(arg_names) 
                           if arg == "return_match_str"][0]
    
    if return_match_index and return_match_str:
        raise ValueError(f"Arguments '{arg_names[match_index_pos]}' "
                         f"and '{arg_names[match_index_str_pos]}' "
                         "cannot be True at the same time.")
        
    else:
        if return_match_index and not (return_match_index in match_obj_index_option_keys):
            raise ValueError(f"Wrong value for argument '{arg_names[match_index_pos]}' "
                             f"Options are: {match_obj_index_option_keys}")
            
        if not (isinstance(return_match_str, bool)):
            raise ValueError("Argument '{arg_names[match_index_str_pos]}' "
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

    
    elif isinstance(string, (list, np.ndarray, tuple)):
        if isinstance(substring, str):
    
            if not advanced_search:
                if isinstance(string, np.ndarray):
                    substr_match_obj_nofilter = np.char.find(string, substring,
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
                

        elif isinstance(substring, (list, np.ndarray, tuple)):  
            if not advanced_search:
                substr_match_obj_no_filter = \
                np.char.find(string, substring, start=start, end=end)  
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
                
            
    
    elif isinstance(string, pd.Series):
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
def advanced_pattern_searcher(string, substring,
                              return_match_index,
                              return_match_str,
                              case_sensitive,
                              find_whole_words,
                              all_matches):
    
    
    """
    string: str or [list, np.ndarray, tuple]
    substring : str ONLY
    """
    
    # No option selected #
    #--------------------#
    
    if not case_sensitive and not all_matches and not find_whole_words:
        re_obj_str = "re.search(substring, string, re.IGNORECASE)"
        iterator_considered = False
        
        
    # One option selected #
    #---------------------#
        
    elif case_sensitive and not all_matches and not find_whole_words:
        re_obj_str = "re.search(substring, string)"
        iterator_considered = False
        
    elif not case_sensitive and all_matches and not find_whole_words:
        re_obj_str = "re.finditer(substring, string, re.IGNORECASE)"
        iterator_considered = True        
        
    elif not case_sensitive and not all_matches and find_whole_words:
        re_obj_str = "re.fullmatch(substring, string, re.IGNORECASE)"
        iterator_considered = False


    # Two options selected #
    #----------------------# 
    
    elif case_sensitive and all_matches and not find_whole_words:
        re_obj_str = "re.finditer(substring, string)"
        iterator_considered = True        
        
    elif case_sensitive and not all_matches and find_whole_words:
        re_obj_str = "re.fullmatch(substring, string)"
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
    
    
    if isinstance(string, (list, np.ndarray, tuple)):
        match_obj_spec = \
        np.vectorize(return_search_obj_spec_aux)(*arg_list)
        
    else:
        match_obj_spec = return_search_obj_spec_aux(*arg_list)     
        
    return match_obj_spec
       

# Complementary functions #
#-#-#-#-#-#-#-#-#-#-#-#-#-#
        
# Main methods #
def return_search_obj_spec(match_obj, return_match_index, return_match_str):
    if return_match_index:
        try:
            match_obj_span = match_obj.span()
        except AttributeError:
            return -1
        else:
            match_obj_idx = eval(match_obj_index_option_dict.get(return_match_index))
            return match_obj_idx
            
    elif return_match_str:
        match_obj_str = match_obj.group()
        return match_obj_str
    
    
    
def return_search_obj_spec_iterators(callable_iterator, 
                                     return_match_index,
                                     return_match_str):
    if return_match_index:
        match_obj_span = [match_obj.span()
                          if hasattr(match_obj, "span")
                          else -1
                          for match_obj in callable_iterator] 

        match_obj_idx = eval(match_obj_index_option_dict.get(return_match_index))
        return match_obj_idx
            
    elif return_match_str:
        match_obj_str = [match_obj.group()
                         if hasattr(match_obj, "group")
                         else -1
                         for match_obj in callable_iterator]
        return match_obj_str
    
    
# Auxiliary method that gathers the two previous #
def return_search_obj_spec_aux(string, substring, re_obj_str,
                               return_match_index, return_match_str, 
                               iterator_considered,
                               case_sensitive,
                               find_whole_words,
                               all_matches):

    
    if not iterator_considered:
        match_obj_spec = return_search_obj_spec(eval(re_obj_str),
                                                return_match_index,
                                                return_match_str)
        
    else:
        match_obj_spec = return_search_obj_spec_iterators(eval(re_obj_str),
                                                          return_match_index,
                                                          return_match_str)
    
    return match_obj_spec
   
# PosixPath string management #
#-----------------------------#

# Main method #
#-#-#-#-#-#-#-#

def obj_path_specs(obj_path, splitdelim=None):
    
    obj_PATH = Path(obj_path)
    
    obj_path_parent = obj_PATH.parent
    obj_path_name = obj_PATH.name
    obj_path_name_noext = obj_PATH.stem
    obj_path_ext = obj_PATH.suffix[1:]
    
    obj_specs_dict = {
        obj_specs_keylist[0] : obj_path_parent,
        obj_specs_keylist[1] : obj_path_name,
        obj_specs_keylist[2] : obj_path_name_noext,
        obj_specs_keylist[4] : obj_path_ext
        }
    
    if splitdelim is not None:
        obj_path_name_noext_parts = obj_path_name_noext.split(splitdelim)
        addItemDict = {obj_specs_keylist[3] : obj_path_name_noext_parts}
        obj_specs_dict.update(addItemDict)
        
    return obj_specs_dict


# Part picker #
#-#-#-#-#-#-#-#

def get_obj_specs(obj_path,
                  obj_spec_key=None,
                  splitdelim=None):
    
    # Proper argument selection control #
    arg_names = get_obj_specs.__code__.co_varnames
    osk_arg_pos = find_substring_index(arg_names, "obj_spec_key")
    
    if obj_spec_key not in obj_specs_keylist:
        raise ValueError(f"Wrong '{arg_names[osk_arg_pos]}' option. "
                         f"Options are {obj_specs_keylist}.")
        
    # Get the object specification name #
    if not isinstance(obj_path, dict):
        obj_specs_dict = obj_path_specs(obj_path, splitdelim)
    
    if obj_spec_key == obj_specs_keylist[3] and splitdelim is None:
        raise ValueError("You must specify a string-splitting character "
                         f"if '{arg_names[osk_arg_pos]}' == '{obj_spec_key}'.")
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
    arg_names = modify_obj_specs.__code__.co_varnames
    obj2ch_arg_pos = find_substring_index(arg_names, "obj2modify")
    new_obj_arg_pos = find_substring_index(arg_names, "new_obj")
    str2add_arg_pos = find_substring_index(arg_names, "str2add")
    
    
    if obj2modify not in obj_specs_keylist:
        raise ValueError(f"Wrong '{arg_names[obj2ch_arg_pos]}' option. "
                         f"Options are {obj_specs_keylist}.")
    
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
            raise ValueError(f"For '{arg_names[obj2ch_arg_pos]}' = '{obj2modify}', "
                             f"'{arg_names[str2add_arg_pos]}' argument is ambiguous; "
                             "you must provide yourself the new path object "
                             f"(argument '{arg_names[new_obj_arg_pos]}') .")
            
       
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
        joint_obj_path = f"{obj_path_parent}/{obj_path_name_noext}.{obj_path_ext}"
        
    return joint_obj_path
    

# Substring replacements #
#------------------------#

def substring_replacer(string, string2find, string2replace, count_std=-1,
                       advanced_search=False,
                       count_adv=0,
                       flags=0):
    
    arg_names = substring_replacer.__code__.co_varnames
    adv_search_arg_pos = find_substring_index(arg_names, 
                                              "advanced_search",
                                              advanced_search=True,
                                              find_whole_words=True)
            
    if not advanced_search:
        if isinstance(string, str):
            string_replaced = string.replace(string2find, string2replace, count_std)
            
        elif isinstance(string, (list, np.ndarray)):
            if isinstance(string, list):
                string = np.array(string)
            string_replaced = np.char.replace(string, string2find, string2replace)
            
        elif isinstance(string, pd.DataFrame):
            string_replaced = pd.DataFrame.replace(string, string2find, string2replace)
            
        elif isinstance(string, pd.Series):
            string_replaced = pd.Series.replace(string, string2find, string2replace)
            
        return string_replaced
            
    else:
        if not isinstance(string, str):
            raise ValueError("Input object must only be of type 'string' "
                             f"if '{arg_names[adv_search_arg_pos]}' is True.")
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
        str_case_modified = eval(case_modifier_option_dict.get(case))
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
        string_stripped = eval(strip_option_dict.get(strip_option))
        return string_stripped
    

# String creators from array-like objects #
#-----------------------------------------#

def condense_array_content_as_string(obj, add_final_space=False):
    method_name = inspect.currentframe().f_code.co_name
    
    if not (isinstance(obj, (list, np.ndarray, pd.DataFrame, pd.Series))):
        raise TypeError(f"'{method_name}' method works only for lists, "
                        "NumPy arrays and pandas DataFrames and series.")
        
    else:        
        if isinstance(obj, list):
            obj_val_array = obj.copy()
            
        elif isinstance(obj, (pd.DataFrame, pd.Series)):
            # Get the pandas DataFrame's or Series's value array #
            obj_val_array = obj.values
            
        
        """
        In the case of NumPy arrays and pandas DataFrames and series,
        if the object's dimension is N > 1, i.e. has the attribute 'flatten', 
        precisely flatten it.
        """
        if hasattr(obj, "flatten"):
            obj_val_array = obj_val_array.flatten()
            
            
        """
        In order to join every content in a single string, each element
        inside the object must be a string.
        Then, by default, each element is going to be converted to a string
        """
        
        obj_list = [str(el) for el in obj_val_array]
        
        # Merge the content of the resulting list #
        allobj_string = local_delim.join(obj_list)
        
        """
        If other procedures or methods require a final space in the string,
        add it as requested
        """
        if add_final_space:
            allobj_string += local_delim
        
        return allobj_string


#--------------------------#
# Parameters and constants #
#--------------------------#

# Standard and essential name lists #
obj_specs_keylist = ['parent', 'name', 'name_noext', 'name_noext_parts', 'ext']
obj_specs_keylist_essential = obj_specs_keylist[2:]

# Substring search availanble method list #
combined_case_search_method_list = ['default', 'numpy_basic', 'numpy_advanced']

# Switch-type dictionaries #
#--------------------------#

# Search matching object's indexing options #
match_obj_index_option_dict = {
    'lo'   : 'match_obj_span[0]',
    'hi'   : 'match_obj_span[-1]',
    'span' : 'match_obj_span'
    }
    
match_obj_index_option_keys = list(match_obj_index_option_dict.keys()) + [False]

# String case handling #
case_modifier_option_dict = {
    'lower'      : 'string.lower()',
    'upper'      : 'string.upper()',
    'capitalize' : 'string.capitalize()',
    'title'      : 'string.title()'
    }

case_modifier_option_keys = list(case_modifier_option_dict.keys())

# String stripping #
strip_option_dict = {
    'strip'  : 'string.strip(chars)',
    'lstrip' : 'string.lstrip(chars)',
    'rstrip' : 'string.rstrip(chars)',
    }

strip_option_keys = list(strip_option_dict.keys())

# Character delimiter #
local_delim = common_delim_list[6]
