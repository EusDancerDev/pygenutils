#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pytools.parameters_and_constants.global_parameters import operations_sets_list
from pytools.strings.string_handler import find_substring_index
from pytools.utilities.introspection_utils import get_caller_method_args

#-------------------------#
# Define custom functions #
#-------------------------#

def operations_with_sets(array_of_sets1, 
                         array_of_sets2=None, 
                         constructor="built-in",
                         operator="union"):
    
    # Argument validations #
    #-#-#-#-#-#-#-#-#-#-#-#-

    all_arg_names = get_caller_method_args()
    operator_arg_pos = find_substring_index(all_arg_names, "operation")
    constructor_arg_pos = find_substring_index(all_arg_names, "constructor")
    
    if operator not in operations_sets_list:
        raise ValueError("Invalid operator for mathematical sets, "
                         f"argument '{all_arg_names[operator_arg_pos]}' option. "
                         f"Supported options are {operations_sets_list}.")
        
        
    if constructor not in sets_contructor_options: 
        raise ValueError("Unsupported mathematical interval constructor library, "
                         f"argument '{all_arg_names[constructor_arg_pos]}'. "
                         f"Choose one from {sets_contructor_options}.")
        
    # Operations #
    #-#-#-#-#-#-#-
        
    if constructor == "built-in":
        if operator == operations_sets_list[-1]:
            from itertools import product as operations_external_module
              
        else:
            operations_external_module = None
        res_set = operation_dict.get(operator)(array_of_sets1, array_of_sets2,
                                               operations_external_module)
        return res_set
            
    elif constructor == "sympy":        
        # TODO: garatu 'sympy' motako multzoen kasua
        # from sympy import FiniteSet
        raise NotImplementedError("Please for now set argument "
                                  f"'{all_arg_names[constructor_arg_pos]}' to "
                                  f"{sets_contructor_options[0]}.")

#--------------------------#        
# Parameters and constants #
#--------------------------#

sets_contructor_options = ["built-in", "sympy"]

operation_dict = {
    "union" :
        lambda array_of_sets1, array_of_sets2, operations_external_module : array_of_sets1.union(array_of_sets2),
    "intersection" : 
        lambda array_of_sets1, array_of_sets2, operations_external_module : array_of_sets1.intersection(array_of_sets2),
    "difference" : 
        lambda array_of_sets1, array_of_sets2, operations_external_module : array_of_sets1.difference(array_of_sets2),
    "symmetric_difference" : 
        lambda array_of_sets1, array_of_sets2, operations_external_module : array_of_sets1.symmetric_difference(array_of_sets2),
    "cartesian_product" : 
        lambda array_of_sets1, array_of_sets2, operations_external_module : set(operations_external_module(array_of_sets1))
}