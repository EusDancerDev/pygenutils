#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np

import time
import timeit

#-----------------------#
# Import custom modules #
#-----------------------#

from pytools.strings import information_output_formatters, string_handler
from pytools.time_formatters import time_format_tweaker
from pytools.utilities.introspection_utils import get_caller_method_args

# Create aliases #
#----------------#

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

find_substring_index = string_handler.find_substring_index

#------------------#
# Define functions #
#------------------#

# TODO: 'time_format_tweaker' optimizatutakoan, berrikusi hura deitzeko sintaxia
# TODO: 'else' blokean switch case hiztegi bat garatu
def program_exec_timer(mode, module="time", return_days=False):
    
    global ti
    
    if module not in module_list:
        raise ValueError(format_string(wrong_module_choice_str, module_list))
        
    else:
        if mode == "start":  
            if module == "os":
                import os
                ti = os.times()[-1]
            elif module == "time":
                ti = time.time()
            elif module == "timeit":
                ti = timeit.default_timer()
            
        elif mode == "stop":
            if module == "os":
                tf = os.times()[-1]
            elif module == "time":
                tf = time.time()
            elif module == "timeit":
                tf = timeit.default_timer()
                
            elapsed_time = abs(ti-tf)
            
            return time_format_tweaker(elapsed_time,
                                       return_str="extended", 
                                       return_days=return_days)

    
def snippet_exec_timer(snippet_str, 
                       repeats=None, 
                       trials=int(1e4), 
                       roundoff=None,
                       format_time_str=False,
                       return_best_time=False):
        
    # Quality control #
    all_arg_names = get_caller_method_args()
    roundoff_arg_pos = find_substring_index(all_arg_names, "roundoff")
    
    # Execution time in the specified number of trials with no repeats #
    if repeats is None:
        exec_time_norep = timeit.timeit(setup=snippet_str,
                                        number=trials,
                                        globals=globals())
        """
        Equivalent to the following
        ---------------------------
        exec_time_norep = timeit.repeat(snippet_str, repeat=1, number=10000)[0]
        """
        
        if roundoff is not None:
            if not isinstance(roundoff, int):
                raise TypeError(format_string(type_error_str, f'{all_arg_names[roundoff_arg_pos]}'))
            else:
                exec_time_norep = np.round(exec_time_norep, roundoff)
        
        if not format_time_str:
            time_unit_str = sec_time_unit_str
        else:
            exec_time_norep = time_format_tweaker(exec_time_norep,
                                                  return_str="extended")
            time_unit_str = default_time_unit_str
        
        # Complete and display the corresponding output information table #
        arg_tuple_exec_timer1 = (time_unit_str, trials, exec_time_norep)
        print_format_string(norep_exec_time_info_str, arg_tuple_exec_timer1)
      
    # Execution time in the specified number of trials for several repeats #
    else:
        exec_time_rep = timeit.repeat(setup=snippet_str, 
                                      repeat=repeats,
                                      number=trials,
                                      globals=globals())
        
        if roundoff is not None:
            if not isinstance(roundoff, int):
                raise TypeError(format_string(type_error_str, f'{all_arg_names[roundoff_arg_pos]}'))
            else:
                exec_time_rep = np.round(exec_time_rep, roundoff)
                time_unit_str = sec_time_unit_str
        
        if not format_time_str:
            time_unit_str = sec_time_unit_str
        else:
            exec_time_rep = time_format_tweaker(exec_time_rep,
                                                return_str="extended")
            time_unit_str = default_time_unit_str
          
        # Complete and display the corresponding output information table #
        arg_tuple_exec_timer2 = (time_unit_str, repeats, trials, exec_time_rep)
        exec_timer2_str = format_string(rep_exec_time_info_str, arg_tuple_exec_timer2)
        
        if not return_best_time:
            print_format_string(rep_exec_time_info_str, arg_tuple_exec_timer2)
        else:
            best_time = np.min(exec_time_rep)
            arg_tuple_exec_timer3 = (exec_timer2_str, best_time)
            print_format_string(rep_exec_time_info_best_str, arg_tuple_exec_timer3)
    
#%%

#--------------------------#
# Parameters and constants #
#--------------------------#

# List of libraries containing methods for code execution timing #
module_list = ["os", "time", "timeit"]

# Time units #
sec_time_unit_str = 's'
default_time_unit_str = 'formatted'

# Preformatted strings #
#----------------------#

# Informative #
norep_exec_time_info_str = \
"""Snippet execution time ({}), for {} trials with no repeats: {}"""

rep_exec_time_info_str = \
"""Snippet execution time ({}), for {} trials with and {} repeats:\n{}"""

rep_exec_time_info_best_str = \
"""{}\nBest: {}"""

# Error messages #
type_error_str = """Argument '{}' must be of type 'int'."""
wrong_module_choice_str = """Unsupported module option, choose one from {}."""