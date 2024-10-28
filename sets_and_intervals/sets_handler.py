#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import sets_operation_list
from pyutils.strings.string_handler import find_substring_index
from pyutils.utilities.introspection_utils import get_caller_method_args

#-------------------------#
# Define custom functions #
#-------------------------#

def sets_operator(array_of_sets1, 
                  array_of_sets2=None, 
                  constructor="default",
                  operator="union"):
    """
    Perform operations on sets using the specified constructor and operator.
    
    Parameters
    ----------
    array_of_sets1 : set or list of sets
        The first set or list of sets to perform operations on.
    array_of_sets2 : set or list of sets, optional
        The second set or list of sets for binary operations like union or intersection.
        Default is None.
    constructor : str, optional
        Specifies which set constructor to use. Options are 'default' or 'sympy'.
        Default is 'default'.
    operator : str, optional
        The operation to perform. Options include 'union', 'intersection', 'difference', 
        'symmetric_difference', 'cartesian_product'. Default is 'union'.
    
    Returns
    -------
    Resulting set based on the operation and constructor.
    
    Raises
    ------
    ValueError
        If an unsupported constructor or operator is specified.
    """
    
    # Argument validations #
    #-#-#-#-#-#-#-#-#-#-#-#-

    param_keys = get_caller_method_args()
    constructor_arg_pos = find_substring_index(param_keys, "constructor")
    operator_arg_pos = find_substring_index(param_keys, "operator")
    
    if operator not in sets_operation_list:
        raise ValueError(f"Invalid operator for mathematical sets (option {operator_arg_pos}). "
                         f"Supported options are {sets_operation_list}.")
        
    if constructor not in sets_contructor_options: 
        raise ValueError(f"Unsupported set constructor library (position {constructor_arg_pos}). "
                         f"Choose one from {sets_contructor_options}.")
    
    # Operations #
    #-#-#-#-#-#-#-

    if constructor == "default":
        if operator == "cartesian_product":
            from itertools import product as operations_external_module
        else:
            operations_external_module = None
        
        # Call appropriate operation from the dictionary
        return default_operation_dict[operator](array_of_sets1, array_of_sets2, operations_external_module)

    elif constructor == "sympy":
        from sympy import FiniteSet
        
        # Transform inputs to FiniteSets
        finite_set1 = FiniteSet(*array_of_sets1)
        finite_set2 = FiniteSet(*array_of_sets2) if array_of_sets2 is not None else None

        # Call appropriate operation from the dictionary
        if operator == sets_operation_list[-1]:
            return set(FiniteSet(*[x*y for x in finite_set1 for y in finite_set1]))
        else:
            return sympy_operation_dict[operator](finite_set1, finite_set2)


#--------------------------#        
# Parameters and constants #
#--------------------------#

# Supported set constructors #
sets_contructor_options = ["default", "sympy"]

# Operation dictionary for the 'default' constructor (using Python's set class)
default_operation_dict = {
    "union": lambda array_of_sets1, array_of_sets2, _: array_of_sets1.union(array_of_sets2),
    "intersection": lambda array_of_sets1, array_of_sets2, _: array_of_sets1.intersection(array_of_sets2),
    "difference": lambda array_of_sets1, array_of_sets2, _: array_of_sets1.difference(array_of_sets2),
    "symmetric_difference": lambda array_of_sets1, array_of_sets2, _: array_of_sets1.symmetric_difference(array_of_sets2),
    "cartesian_product": lambda array_of_sets1, _, operations_external_module: set(operations_external_module(array_of_sets1))
}

# Operation dictionary for the 'sympy' constructor (using Sympy's FiniteSet class)
sympy_operation_dict = {
    "union": lambda finite_set1, finite_set2: finite_set1.union(finite_set2),
    "intersection": lambda finite_set1, finite_set2: finite_set1.intersection(finite_set2),
    "difference": lambda finite_set1, finite_set2: finite_set1 - finite_set2,
    "symmetric_difference": lambda finite_set1, finite_set2: finite_set1.symmetric_difference(finite_set2),
}
