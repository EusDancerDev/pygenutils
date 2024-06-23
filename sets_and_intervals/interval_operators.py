#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pytools.parameters_and_constants.global_parameters import operations_sets_list

from pytools.strings.string_handler import find_substring_index
from pytools.utilities.instrospection_utils import get_caller_method_args

#------------------#
# Define functions #
#------------------#

def define_interval(left_limit, right_limit, constructor="pandas", closed="both"):
    
    # Quality control #
    #-----------------#
    
    # Main argument names and their position on the function's definition #    
    all_arg_names = get_caller_method_args()    
    contructor_arg_pos = find_substring_index(all_arg_names, "constructor")
    
    # constructor argument choice #    
    if constructor not in contructor_arg_pos:
        raise ValueError("Unsupported mathematical interval constructor library, "
                         f"argument '{all_arg_names[contructor_arg_pos]}'. "
                         f"Choose one from {interval_contructor_options}.")
    
    if constructor == "pandas":
        import piso
        piso.register_accessors()
        itv = pd.Interval(left_limit, right_limit, closed=closed)
        
    elif constructor == "intervaltree":
        from intervaltree import Interval
        print(f"WARNING: intervals constructed using {constructor} "
              "do not include upper bound.")
        itv = Interval(left_limit, right_limit)
        
    return itv
    

def basic_interval_operator(interval_array,
                            constructor="pandas",
                            closed="left",
                            operator="union", 
                            force_union=False):
    
    # Quality control #
    #-----------------#
    
    # Main argument names and their position on the function's definition #    
    all_arg_names = get_caller_method_args()
    operator_arg_pos = find_substring_index(all_arg_names, "operator_sets")
    
    # operator_sets and object type argument choices #    
    if operator not in operations_sets_list:
        raise ValueError("Invalid operator for mathematical sets, "
                         f"argument '{all_arg_names[operator_arg_pos]}' option. "
                         f"Supported options are {operations_sets_list}.")
        
    # Operations #
    #------------#
    
        
    if constructor == "pandas":
        import piso
        piso.register_accessors()
         
        itv_pdArray = pd.arrays.IntervalArray(interval_array,
                                              closed=closed)
        
        # TODO: garatu bost kasuak, denak web-orrialde ofizialetik
        
        if operator == "union":
            merged_bin = itv_pdArray.piso.union()[0]
            
            if not force_union:
                return merged_bin
               
            else:
                merged_bin_left = merged_bin.left
                merged_bin_right = merged_bin.right
                
                min_num_interval = itv_pdArray.min()
                min_num_interval_left = min_num_interval.left
                
                max_num_interval = itv_pdArray.max()
                max_num_interval_right = max_num_interval.right
                
                if merged_bin_left != min_num_interval_left\
                or merged_bin_right != max_num_interval_right:

                    merged_bin = define_interval(min_num_interval_left,
                                                 max_num_interval_right,
                                                 closed=closed)
                    
                    return merged_bin
                    
                else:
                    return merged_bin
                
        elif operator == "intersection":
            """do sth"""
            
    
    elif constructor == "intervaltree":
        print(f"WARNING: intervals constructed with method '{constructor}' "
              "do not allow closed upper bounds.")        
        from intervaltree import Interval, IntervalTree
        itv_ItvArray = IntervalTree.from_tuples(interval_array)
        
        # TODO: garatu bost kasuak, denak web-orrialde ofizialetik

#--------------------------#
# Parameters and constants #
#--------------------------#

# Operations with mathematical intervals #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

# Supported mathematical interval constructors #
interval_contructor_options = ["pandas", "intervaltree"]