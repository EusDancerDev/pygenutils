#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules # 
#----------------#

import inspect
import sys

#------------------#
# Define functions #
#------------------#

# Methods #
#---------#

# Function names #
def retrieve_function_name(library="inspect"):
    """Returns the name of the method defined in situ."""

    if library not in method_name_retrieval_libraries:
        raise ValueError("Unsupported library, choose one from "
                          f"{method_name_retrieval_libraries}.")
    else:
        if library == "inspect":
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back  # Get the caller's frame
            frame_info = inspect.getframeinfo(caller_frame)
            return frame_info.function
        elif library == "sys":
            method_name = sys._getframe(1).f_code.co_name  # Get the caller's frame (1 level up)
        return method_name
    

# Function arguments #
#-#-#-#-#-#-#-#-#-#-#-

# General frame #
#################

def get_method_args(method):
    """
    Returns the argument names of the given method.

    This function uses the inspect module to get the signature of the provided method
    and then extracts the names of required arguments (those without default values).

    Args
    ----
    method : function
        The method whose argument names are to be retrieved.

    Returns
    -------
    required_arg_names : list
        A list of required argument names of the given method.

    Example
    -------
    def example_method(arg1, arg2, kwarg1=None):
        pass
    
    arg_names = get_method_args(example_method)
    print(arg_names)  # Output: ['arg1', 'arg2']
    """
    sig = inspect.signature(method)
    required_arg_names = [param.name 
                          for param in sig.parameters.values()
                          if param.default == inspect.Parameter.empty
                          and param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, 
                                             inspect.Parameter.KEYWORD_ONLY)]
    
    return required_arg_names

def get_method_all_args(method):
    """
    Returns all argument names of the given method, including those with default values.

    This function uses the inspect module to get the signature of the provided method
    and then extracts all argument names.

    Args
    ----
    method : function
        The method whose argument names are to be retrieved.

    Returns
    -------
    all_arg_list : list
        A list of all argument names of the given method.

    Example
    -------
    def example_method(arg1, arg2, kwarg1=None):
        pass
    
    param_keys = get_method_all_args(example_method)
    print(param_keys)  # Output: ['arg1', 'arg2', 'kwarg1']
    """
    sig = inspect.signature(method)
    all_arg_list = [param.name for param in sig.parameters.values()]
    return all_arg_list

def get_full_method_signature(method):
    """
    Returns the full signature of the given method, including argument names and default values.

    This function uses the inspect module to get the signature of the provided method
    and returns it as an inspect.Signature object.

    Args
    ----
    method : function
        The method whose signature is to be retrieved.

    Returns
    -------
    full_signature : inspect.Signature
        The full signature of the given method, which includes
        information about parameters and their default values.

    Example
    -------
    def example_method(arg1, arg2, kwarg1=None, kwarg2='default'):
        pass
    
    full_signature = get_full_method_signature(example_method)
    print(full_signature)  # Output: (arg1, arg2, kwarg1=None, kwarg2='default')
    """
    full_signature = inspect.signature(method)
    return full_signature


# Caller's frame #
##################

def get_caller_method_args():
    """
    Returns the argument names of the caller method.

    This function uses the inspect module to get the current stack frame
    and then accesses the caller's stack frame to retrieve the argument names.

    Returns
    -------
    caller_args_list : list
        A list of argument names used in the caller method.

    Example
    -------
    def example_method(arg1, arg2):
        arg_names = get_caller_method_args()
        print(arg_names)  # Output: ['arg1', 'arg2']
    """
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back  # Go back one frame to get the caller's frame
    caller_args, _, _, _ = inspect.getargvalues(caller_frame)
    caller_args_list = list(caller_args)  # Return the argument names as a list
    return caller_args_list
    

def get_caller_method_all_args():
    """
    Returns all argument names and their values of the caller method, including those with default values.

    This function uses the inspect module to get the current stack frame
    and then accesses the caller's stack frame to retrieve the argument names and their values.

    Returns
    -------
    caller_args_dict : dict
        A dictionary where keys are argument names and values are the corresponding argument values.

    Example
    -------
    def example_method(arg1, arg2, kwarg1=None):
        param_keys = get_caller_method_all_args()
        print(param_keys)  # Output: {'arg1': 1, 'arg2': 2, 'kwarg1': None}
    """
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back  # Go back one frame to get the caller's frame
    caller_args, _, _, caller_values = inspect.getargvalues(caller_frame)
    caller_args_dict = {arg: caller_values[arg] for arg in caller_args}
    return caller_args_dict

def get_full_caller_method_signature():
    """
    Returns the full signature of the caller method, including argument names and default values.

    This function uses the inspect module to get the current stack frame,
    accesses the caller's stack frame, and retrieves the method object
    to get its full signature using inspect.signature.

    Returns
    -------
    full_signature : inspect.Signature
        The full signature of the caller method, which includes
        information about parameters and their default values.

    Example
    -------
    def example_method(arg1, arg2, kwarg1=None, kwarg2='default'):
        full_signature = get_full_caller_method_signature()
        print(full_signature)  # Output: (arg1, arg2, kwarg1=None, kwarg2='default')
    """
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back  # Go back one frame to get the caller's frame
    caller_code = caller_frame.f_code
    caller_func_name = caller_code.co_name
    caller_func = caller_frame.f_globals[caller_func_name]
    full_signature = inspect.signature(caller_func)
    return full_signature


# Attributes #
#------------#

def get_attribute_names(obj):
    """Returns the names of all attributes of an object."""
    attr_list = [attr 
                 for attr in dir(obj)
                 if not callable(getattr(obj, attr))]
    
    return attr_list

# Object types #
#--------------#

def get_obj_type_str(obj, lowercase=False):
    """Returns the type of an object as a string"""
    obj_type_class = type(obj)
    obj_type_str = obj_type_class.__name__
    return obj_type_str.lower() if lowercase else obj_type_str

# More functions related to introspection or utility as needed #
#--------------------------------------------------------------#

# Example of potential future expansion
def inspect_memory_usage(obj):
    """Inspects memory usage of an object."""
    # Implementation details
    
#--------------------------#
# Parameters and constants #
#--------------------------#

# Supported library list for method name retrievals #
method_name_retrieval_libraries = ["inspect", "sys"]
