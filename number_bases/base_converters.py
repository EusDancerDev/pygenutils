#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Goal**

This module provides functions to perform conversions between various number bases.
The supported bases include binary, octal, decimal, and hexadecimal, as well as
arbitrary bases.
"""

#-------------------------#
# Define custom functions #
#-------------------------#

# Quality control functions #
#---------------------------#

def check_input_number_format(x):
    """
    Ensures the input number is in string format.

    Parameters
    ----------
    x : int or str
        The input number.

    Returns
    -------
    str
        The input number as a string.
    """
    if isinstance(x, int):
        x_str = str(x)
    else:
        x_str = x
    return x_str

def method_checker(arg):
    """
    Checks if the provided method is valid.

    Parameters
    ----------
    arg : str
        The method to check.

    Raises
    ------
    ValueError : If the method is not valid.
    """
    if arg not in method_opts:
        raise ValueError(f"Wrong method. Options are {method_opts}.")
        
# Operations with frequently used bases #
#---------------------------------------#

def base2bin(n, method="format_string", zero_pad=4):
    """
    Converts a number to binary.

    Parameters
    ----------
    n : int
        The input number.
    method : str
        The method to use for conversion ('default' or 'format_string').
    zero_pad : int
        The number of zeros to pad (used with 'format_string').

    Returns
    -------
    str
        The binary representation of the input number.
    """
    method_checker(method)

    if method == "default":
        n_bin = bin(n)
    elif method == "format_string":
        n_bin = f"{n:0{zero_pad}b}"
    return n_bin

def base2oct(n, method="format_string", zero_pad=4):
    """
    Converts a number to octal.

    Parameters
    ----------
    n : int
        The input number.
    method : str
        The method to use for conversion ('default' or 'format_string').
    zero_pad : int
        The number of zeros to pad (used with 'format_string').

    Returns
    -------
    str
        The octal representation of the input number.
    """
    method_checker(method)

    if method == "default":
        n_oct = oct(n)
    elif method == "format_string":
        n_oct = f"{n:0{zero_pad}o}"
    return n_oct

def base2hex(n, method="format_string", zero_pad=4):
    """
    Converts a number to hexadecimal.

    Parameters
    ----------
    n : int
        The input number.
    method : str
        The method to use for conversion ('default' or 'format_string').
    zero_pad : int
        The number of zeros to pad (used with 'format_string').

    Returns
    -------
    str
        The hexadecimal representation of the input number.
    """
    method_checker(method)

    if method == "default":
        if isinstance(n, float):
            n_hex = n.hex()
        else:
            n_hex = hex(n)
    elif method == "format_string":
        n_hex = f"{n:0{zero_pad}x}"
    return n_hex

# From above bases to decimal #
def bin2dec(n_bin):
    """
    Converts a binary number to decimal.

    Parameters
    ----------
    n_bin : str
        The binary number as a string.

    Returns
    -------
    int
        The decimal equivalent of the binary number.
    """
    if isinstance(n_bin, int):
        n = n_bin
    else:
        n = int(n_bin, base=2)
    return n

def oct2dec(n_oct):
    """
    Converts an octal number to decimal.

    Parameters
    ----------
    n_oct : str
        The octal number as a string.

    Returns
    -------
    int
        The decimal equivalent of the octal number.
    """
    if isinstance(n_oct, int):
        n = n_oct
    else:
        n = int(n_oct, base=8)
    return n

def hex2dec(n_hex):
    """
    Converts a hexadecimal number to decimal.

    Parameters
    ----------
    n_hex : str
        The hexadecimal number as a string.

    Returns
    -------
    int
        The decimal equivalent of the hexadecimal number.
    """
    if isinstance(n_hex, int):
        n = n_hex
    else:
        n = int(n_hex, base=16)
    return n

# Operations with arbitrary bases #
#---------------------------------#

def arbitrary_base_to_dec(x, base=10):
    """
    Converts a number from an arbitrary base to decimal.

    Parameters
    ----------
    x : str
        The number as a string.
    base : int
        The base of the input number.

    Returns
    -------
    int
        The decimal equivalent of the input number.
    """
    x = check_input_number_format(x)
    n = int(x, base=base)
    return n

def convert_among_arbitrary_bases(x, base):
    """
    Converts a number from one arbitrary base to another.

    Parameters
    ----------
    x : str
        The number as a string.
    base : int
        The base of the input number.

    Returns
    -------
    int
        The number converted to the specified base.
    """
    x = check_input_number_format(x)
    y = int(x, base=base)
    return y

#--------------------------#
# Parameters and constants #
#--------------------------#

method_opts = ['default', 'format_string']