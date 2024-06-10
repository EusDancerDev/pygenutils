#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os

#------------------#
# Define functions #
#------------------#

def exec_shell_command(command_str):
    """
    Execute a shell command.

    Parameters
    ----------
    command_str : str
        The shell command to execute.
    
    Returns
    -------
    None
    """
    os.system(command_str)
    
def catch_shell_prompt_output(command_str):
    """
    Execute a shell command and capture its output.

    Parameters
    ----------
    command_str : str
        The shell command to execute.
    
    Returns
    -------
    str
        The output of the shell command.
    """
    output_str = os.popen(command_str).read()
    return output_str
