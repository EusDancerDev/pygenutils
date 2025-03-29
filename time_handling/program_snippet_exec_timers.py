#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from numpy import round as np_round

import os
import time
import timeit

#-----------------------#
# Import custom modules #
#-----------------------#

from filewise.general.introspection_utils import get_caller_args
from pygenutils.strings import text_formatters, string_handler
from pygenutils.time_formatters import parse_float_time

# Create aliases #
#----------------#

find_substring_index = string_handler.find_substring_index
format_string = text_formatters.format_string
print_format_string = text_formatters.print_format_string

#------------------#
# Define functions #
#------------------#

# Input validation streamliners #
#-------------------------------#

def _validate_option(explanation, option, allowed_options):
    """
    Validate if the given option is within the list of allowed options.

    Parameters
    ----------
    explanation : str
        A brief description or context of the validation.
    option : object
        The option to be validated.
    allowed_options : list/iterable
        A list or iterable of valid options.

    Raises
    ------
    ValueError: 
        If the option is not in the list of allowed options, with a detailed explanation.
    """
    if option not in allowed_options:
        raise ValueError(f"{explanation} '{option}' not supported for this operation. "
                         f"Choose one from {allowed_options}.")

def _validate_precision(frac_precision, min_prec=0, max_prec=9):
    """
    Validate the precision level for a floating-point number and ensure it is within a valid range.
    
    Parameters
    ----------
    frac_precision : int or None
        The desired fractional precision to validate.
    min_prec : int, optional
        The minimum allowed precision. Default is 0.
    max_prec : int, optional
        The maximum allowed precision. Default is 9.
    
    Raises
    ------
    ValueError
        If `frac_precision` is outside the range [min_prec, max_prec] or
        `frac_precision` is greater than or equal to 7 but `option` is not "pandas".
    """
    if ((frac_precision is not None) and not (min_prec <= frac_precision <= max_prec)):
        raise ValueError(f"Fractional precision must be between {min_prec} and {max_prec}.")

# Timers #
#--------#

def program_exec_timer(mode, module="time", frac_precision=3):
    """
    General purpose method that measures and returns the execution time
    of a code snippet based on the specified module.

    Parameters
    ----------
    mode : {"start", "stop"}
        Mode to start or stop the timer.
    module : {"os", "time", "timeit"}, optional
        Module to use for timing. Default is "time".
    frac_precision : int [0,6] or None
        Precision of the fractional seconds.

    Returns
    -------
    str
        Formatted string of the elapsed time if mode is "stop".
        
    Raises
    ------
    ValueError
        If the specified module is not supported or if the mode is invalid.
    """

    global ti
   
    # Input validations #
    #-------------------#
    
    # Module #
    _validate_option("Module", module, module_list)

    # Fractional second precision #        
    _validate_precision(frac_precision, max_prec=6)
    
    # Operations #
    #------------#
    
    if mode == "start":
        ti = module_operation_dict[module]()
        
    elif mode == "stop":
        tf = module_operation_dict[module]()
        elapsed_time = abs(ti - tf)
       
        elapsed_time_kwargs = dict(
            module="str",
            origin="arbitrary",
            frac_precision=frac_precision
            )
            
        return parse_float_time(elapsed_time, **elapsed_time_kwargs)
    
    else:
        raise ValueError("Invalid mode. Choose 'start' or 'stop'.")

    
def snippet_exec_timer(snippet_str, 
                       repeats=None, 
                       trials=int(1e4), 
                       roundoff=None,
                       format_time_str=False,
                       return_best_time=False):
        
    # Roundoff validation #
    param_keys = get_caller_args()
    roundoff_arg_pos = find_substring_index(param_keys, "roundoff")
    
    if not isinstance(roundoff, int):
        raise TypeError(format_string(type_error_template, f'{param_keys[roundoff_arg_pos]}'))
    
    # Set keyword argument dictionary for float time parsing #
    float_time_parsing_kwargs =  dict(
        module="str",
        origin="arbitrary",
        frac_precision=roundoff
    )

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
            exec_time_norep = np_round(exec_time_norep, roundoff)
        
        if not format_time_str:
            time_unit_str = sec_time_unit_str
        else:
            exec_time_norep = parse_float_time(exec_time_norep, **float_time_parsing_kwargs)
            time_unit_str = default_time_unit_str
        
        # Complete and display the corresponding output information table #
        arg_tuple_exec_timer1 = (time_unit_str, trials, exec_time_norep)
        print_format_string(norep_exec_time_info_template, arg_tuple_exec_timer1)
      
    # Execution time in the specified number of trials for several repeats #
    else:
        exec_time_rep = timeit.repeat(setup=snippet_str, 
                                      repeat=repeats,
                                      number=trials,
                                      globals=globals())
        
        if roundoff is not None:
            exec_time_rep = np_round(exec_time_rep, roundoff)
        
        # Compute best time
        best_time = min(exec_time_rep) 
        
        # Format floated times to string representation (arbitrary origin)
        if not format_time_str:
            time_unit_str = sec_time_unit_str
        else:
            exec_time_rep = [parse_float_time(t, **float_time_parsing_kwargs)
                             for t in exec_time_rep]
            best_time = parse_float_time(best_time, **float_time_parsing_kwargs)
            time_unit_str = default_time_unit_str
          
        # Complete and display the corresponding output information table
        arg_tuple_exec_timer2 = (time_unit_str, repeats, trials, exec_time_rep)
        exec_timer2_str = format_string(rep_exec_time_info_template, arg_tuple_exec_timer2)
        
        if not return_best_time:
            print_format_string(rep_exec_time_info_template, arg_tuple_exec_timer2)
        else:
            arg_tuple_exec_timer3 = (exec_timer2_str, best_time)
            print_format_string(rep_exec_time_info_best_template, arg_tuple_exec_timer3)
    
#%%

#--------------------------#
# Parameters and constants #
#--------------------------#

# List of libraries containing methods for code execution timing #
module_list = ["os", "time", "timeit"]

# Time units #
sec_time_unit_str = 's'
default_time_unit_str = 'formatted'

# Template strings #
#------------------#

# Informative #
norep_exec_time_info_template = \
"""Snippet execution time ({}), for {} trials with no repeats: {}"""

rep_exec_time_info_template = \
"""Snippet execution time ({}), for {} trials with and {} repeats:\n{}"""

rep_exec_time_info_best_template = \
"""{}\nBest: {}"""

# Error messages #
type_error_template = """Argument '{}' must be of type 'int'."""
unsupported_module_choice_template = """Unsupported module option, choose one from {}."""

# Switch case dictionaries #
#--------------------------#

# Methods for code execution timing #
module_operation_dict = {
    module_list[0]: lambda: os.times()[-1],
    module_list[1]: lambda: time.time(),
    module_list[2]: lambda: timeit.default_timer(),
}
