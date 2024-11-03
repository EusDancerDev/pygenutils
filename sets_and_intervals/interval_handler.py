#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import pandas as pd
from intervaltree import Interval, IntervalTree

#-----------------------#
# Import custom modules #
#-----------------------#

from paramlib.global_parameters import intervals_operation_list
from pygenutils.strings.string_handler import find_substring_index
from filewise.instrospection_utils import get_caller_args

#------------------#
# Define functions #
#------------------#

def define_interval(left_limit, right_limit, constructor="pandas", closed="both"):
    """
    Constructs an interval object using the specified constructor.

    Parameters
    ----------
    left_limit : float or int
        The left limit of the interval.
    right_limit : float or int
        The right limit of the interval.
    constructor : str, optional
        The library to use for constructing the interval. Options are:
        'pandas', 'intervaltree', 'numpy', 'custom_tuple'. Default is 'pandas'.
    closed : str, optional
        Defines whether the interval is closed on the left, right, or both sides.
        Valid values are 'left', 'right', 'both', or 'neither'. Default is 'both'.

    Returns
    -------
    Interval object
        An interval object based on the specified constructor.
        
    Raises
    ------
    ValueError
        If an unsupported constructor is specified.

    Examples
    --------
    >>> define_interval(1, 5, constructor="pandas", closed="both")
    Interval(1, 5, closed='both')
    """
    
    # Input validation # 
    interval_contructor_options = ["pandas", "intervaltree", "numpy", "custom_tuple"]
    
    if constructor not in interval_contructor_options:
        all_args = get_caller_args()
        constr_arg_pos = find_substring_index(all_args, "constructor")
        raise ValueError(f"Unsupported constructor '{constructor}' (position {constr_arg_pos}). "
                         f"Choose one from {interval_contructor_options}.")

    # Operations #
    if constructor == "intervaltree":
        print(f"WARNING: intervals constructed using constructor '{constructor}' "
              f"do not include the upper bound.")
        
    try:
        return interval_constructors[constructor]()
    except Exception as err:
        raise RuntimeError("An error occurred. Check the left and/or right "
                           f"limits values passed: {err}")


def basic_interval_operator(interval_array,
                            constructor="pandas",
                            closed="left", 
                            operator="union",
                            force_union=False):
    """
    Performs operations on an array of interval objects using the specified constructor and operator.

    Parameters
    ----------
    interval_array : array-like
        Array of interval objects to perform operations on.
    constructor : str, optional
        The library used for constructing the intervals. Options are:
        'pandas', 'intervaltree', 'numpy', 'custom_tuple'. Default is 'pandas'.
    closed : str, optional
        Defines whether the intervals are closed on the left, right, or both sides. 
        Valid values are 'left', 'right', 'both', or 'neither'. Default is 'left'.
    operator : str, optional
        The operation to perform on the interval objects. Options are:
        'union', 'intersection', 'difference', 'symmetric_difference', 'comparison'.
        Default is 'union'.
    force_union : bool, optional
        Forces the union of all intervals into a single interval if True.
        Only applies to 'union' and 'pandas' constructor. Default is False.

    Returns
    -------
    Interval object or list of Interval objects
        The result of the operation applied to the intervals.

    Raises
    ------
    ValueError
        If an unsupported constructor or operator is specified.

    Examples
    --------
    >>> basic_interval_operator(interval_array, constructor="pandas", operator="union")
    IntervalArray([...])

    >>> basic_interval_operator(interval_array, constructor="intervaltree", operator="intersection")
    IntervalTree([...])
    """
    
    # Input validation #
    #------------------#
    
    particular_constructor_opts = interval_contructor_options[:2]
    all_args = get_caller_args()
    constr_arg_pos = find_substring_index(all_args, "constructor")
    operator_arg_pos = find_substring_index(all_args, "operator")
    
    if constructor not in particular_constructor_opts:
        raise ValueError(f"Unsupported constructor '{constructor}' (position {constr_arg_pos}) "
                         "for interval computations."
                         f"Choose one from {particular_constructor_opts}.")
        
    if operator not in intervals_operation_list:
        raise ValueError(f"Invalid operator '{operator}' (position {operator_arg_pos}). "
                         f"Supported options are {intervals_operation_list}.")

    # Operations #
    #------------#
    
    try:
        if constructor == "pandas" and operator == "union" and force_union:
            merged_bin = \
            define_interval(pd.arrays.IntervalArray(interval_array, closed=closed).left.min(),
                            pd.arrays.IntervalArray(interval_array, closed=closed).right.max(), 
                            closed=closed)
            return merged_bin        
        else:
            return interval_operations[constructor][operator](interval_array, closed, force_union)
    except Exception as err:
        raise RuntimeError("An error occurred, check that every input value "
                           "is stored into an array-like object, "
                           f"and that they are interval object compatible:\n{err}")

#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported mathematical interval constructors and operations #
interval_contructor_options = ["pandas", "intervaltree", "numpy", "custom_tuple"]

# Switch case dictionaries #
#--------------------------#

# Define interval constructors
interval_constructors = {
    "pandas": lambda left_limit, right_limit, closed : pd.Interval(left_limit, right_limit, closed=closed),
    "intervaltree": lambda left_limit, right_limit, closed: Interval(left_limit, right_limit),
    "numpy": lambda left_limit, right_limit, closed: np.array([left_limit, right_limit]),
    "custom_tuple": lambda left_limit, right_limit, closed: (left_limit, right_limit)
}

# Define operations for pandas and intervaltree constructors
operations_pandas = {
    "union": lambda interval_array, closed: 
        pd.arrays.IntervalArray(interval_array, closed=closed).piso.union()[0],
    "intersection": lambda interval_array, closed: \
        pd.arrays.IntervalArray(interval_array, closed=closed).piso.intersection()[0],
    "difference": lambda interval_array, closed: \
        pd.arrays.IntervalArray(interval_array, closed=closed).piso.difference()[0],
    "symmetric_difference": lambda interval_array, closed: \
        pd.arrays.IntervalArray(interval_array, closed=closed).piso.symmetric_difference()[0],
    "comparison": lambda interval_array, closed: \
        pd.arrays.IntervalArray(interval_array, closed=closed).piso.comparison()[0]
}

operations_intervaltree = {
    "union": lambda interval_array, closed: \
        IntervalTree.from_tuples(interval_array).merge_overlaps(),
    "intersection": lambda interval_array, closed: \
        IntervalTree.from_tuples(interval_array).overlap(),
    "difference": lambda interval_array, closed: \
        IntervalTree.from_tuples(interval_array).difference(),
    "symmetric_difference": lambda interval_array, closed: \
        IntervalTree.from_tuples(interval_array).symmetric_difference(),
    "comparison": lambda interval_array, closed: \
        IntervalTree.from_tuples(interval_array).comparison()
}

# Combine operations into a dictionary for easy access
interval_operations = {
    "pandas": operations_pandas,
    "intervaltree": operations_intervaltree
}
