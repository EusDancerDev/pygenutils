#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import os

#-----------------------#
# Import custom modules # 
#-----------------------#

from pyutils.parameters_and_constants.global_parameters import filesystem_context_modules

#------------------#
# Define functions #
#------------------#

def exec_shell_command(command_str):
    # TODO: eman aukera 'os' edota 'subprocess' moduluak erabiltzeko
    # TODO: aurrekoa kontuan hartuz, horietako bat ere aukeratzen ez bada, errorea jaulki
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
    # TODO: eman aukera 'os' edota 'subprocess' moduluak erabiltzeko
    # TODO: aurrekoa kontuan hartuz, horietako bat ere aukeratzen ez bada, errorea jaulki
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


#--------------------------#
# Parameters and constants #
#--------------------------#

native_os_operation_modules = filesystem_context_modules[0::3]