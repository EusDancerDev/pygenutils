#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from numeral_systems.base_converters import base2bin, bin2dec

#-------------------------#
# Define custom functions #
#-------------------------#

def bitwise_and(n1, n2):
    res_bitwise_and = n1 & n2
    res_bin = base2bin(res_bitwise_and)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def bitwise_or(n1, n2):
    res_bitwise_or = n1 | n2
    res_bin = base2bin(res_bitwise_or)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def bitwise_xor(n1, n2):
    res_bitwise_xor = n1 ^ n2
    res_bin = base2bin(res_bitwise_xor)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def rightwards_bitshift(n, despl):
    res_right_shift = n >> despl
    res_bin = base2bin(res_right_shift)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)

def leftards_bitshift(n, despl):
    res_left_shift = n << despl
    res_bin = base2bin(res_left_shift)
    res_dec = bin2dec(res_bin)
    return (res_bin, res_dec)