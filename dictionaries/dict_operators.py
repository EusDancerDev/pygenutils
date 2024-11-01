#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pygenutils.dictionaries.dict_handler import sort_dictionary_by_keys
from paramlib.parameters_and_constants.global_parameters import basic_four_rules

from functools import reduce

#------------------#
# Define functions #
#------------------#

# Mathematical operations #
#-------------------------#

def dict_value_basic_operator(dict_list,
                              math_operator,
                              return_sorted_keys=False):
    """
    Perform a mathematical operation between dictionaries in a list.

    This function applies the specified mathematical operation to values
    of common keys across dictionaries. It supports basic operations and
    includes floor division and exponentiation.

    Parameters
    ----------
    dict_list : list of dicts
        A list of dictionaries with float or int values.
    math_operator : {'+', '-', '*', '/', '//', '**'}
        The mathematical operation to perform. Must be one of the specified operators.
    return_sorted_keys : bool, optional
        If True, returns the resulting dictionary with sorted keys. Default is False.

    Returns
    -------
    dict
        A dictionary with the result of the operation applied to values of common keys.
        Keys will be sorted if `return_sorted_keys` is True.

    Raises
    ------
    TypeError
        If `dict_list` is not a list of dictionaries.
    ValueError
        If `dict_list` contains fewer than two dictionaries
        or if an invalid `math_operator` is provided.

    Notes
    -----
    The function assumes that all dictionaries in `dict_list` have at least some common keys.
    The operation is only performed on these common keys.
    """
    
    # Input validation #
    #-#-#-#-#-#-#-#-#-#-
    
    # Validate input data type #
    if not (isinstance(dict_list, list)) or not all((isinstance(element, dict) for element in dict_list)):
        raise TypeError("Unsupported object type. Must be a list composed "
                        "only of dictionaries.")
    
    # Validate number of dictionaries in the list #
    if len(dict_list) < 2:
        raise ValueError("At least two dictionaries must be provided.")
    
    # Validate mathematical operator #
    if math_operator not in allowed_calc_dict:
        raise ValueError ("Invalid basic operator sign. "
                          f"Choose one from {list(allowed_calc_dict.keys())}.")
    
    # Operations #
    #-#-#-#-#-#-#-
    
    # Perform the computation #
    operation = allowed_calc_dict.get(math_operator)
    result_dict = reduce(operation, dict_list)
    
    # Order resulting dictionary's keys if desired #
    if return_sorted_keys: 
        result_dict = sort_dictionary_by_keys(result_dict)
        
    return result_dict

#--------------------------#
# Parameters and constants #
#--------------------------#

# Basic calculator operations #
allowed_calc_dict = {
    basic_four_rules[0] : lambda d1, d2 : {k : d1[k]+d2[k] for k in d1.ks() & d2},
    basic_four_rules[1] : lambda d1, d2 : {k : d1[k]-d2[k] for k in d1.ks() & d2},
    basic_four_rules[2] : lambda d1, d2 : {k : d1[k]*d2[k] for k in d1.ks() & d2},
    basic_four_rules[3] : lambda d1, d2 : {k : d1[k]/d2[k] for k in d1.ks() & d2},
    "//" : lambda d1, d2 : {k : d1[k]//d2[k] for k in d1.ks() & d2},
    "**" : lambda d1, d2 : {k : d1[k]**d2[k] for k in d1.ks() & d2}
}
