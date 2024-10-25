#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:45:40 2024

@author: jonander

**Purpose**

Analyze the advanced possibilities for pattern searching, 
either being that a substring or regular expression.

Case studies
------------

1. Input array : [list, np.ndarray or tuple] of str
    1.1 Substrings or regular expression : str
    1.2 Substrings or regular expression : [list, np.ndarray or tuple] of str
"""

#%% MODULE AND METHOD DEFINITIONS

# Import modules #
#----------------#

import numpy as np
import re

# Define functions #
#------------------#

# Function to search for pattern using regular expression #
def find_pattern(s, pattern):
    match = re.search(pattern, s)
    return match.start() if match else -1


#%% DEFINE PARAMETERS

# Array-like of strings #
strings = np.array(['apple', 'banana', 'cherry', 'orange'])
# strings = ['apple', 'banana', 'cherry', 'orange'] # list baliozkoa
# strings = ('apple', 'banana', 'cherry', 'orange') # tuple baliozkoa!!!

# Patterns to search for #
pattern = 'an'
pattern_array = np.array(['an', 'na', 'rr', 'ge'])

# Output information strings #
case_study_info_str = """Case study : {}
Input array of strings : {}
Pattern : {}
"""

output_info_str_1 = "Indices of pattern '{}' in each string: {}"
output_info_str_2 = """String: '{}' || Pattern: '{}' || Index: {}"""

#%% FIRST MINOR CASE

# Analysis part #
#-#-#-#-#-#-#-#-#

# Apply the function to each element of the array #
arg_list_vectorise_1 = [strings, pattern]

# indices = np.vectorize(find_pattern)(strings, pattern)
indices = np.vectorize(find_pattern)(*arg_list_vectorise_1)

# Print the case study information #
arg_list_out_info_1 = ["First", strings, pattern]
print(case_study_info_str.format(*arg_list_out_info_1))

# Print the search results #
arg_list_search_1 = [pattern, indices]
print(output_info_str_1.format(*arg_list_search_1))


#%% SECOND MINOR CASE

# Apply the function to each pair of elements in the arrays
arg_list_vectorise_2 = [strings, pattern_array]

# indices = np.vectorize(find_pattern)(strings, pattern_array)
indices = np.vectorize(find_pattern)(*arg_list_vectorise_2)

# Print the case study information #
arg_list_out_info_2 = ["Second", strings, pattern_array]

print("\n################################\n")
print(case_study_info_str.format(*arg_list_out_info_2))

# Print the search results #
print("\nIndices of patterns in each string:")
for i, (string, pattern, index) in enumerate(zip(strings, pattern_array, indices)):
    arg_list_search_2 = [string, pattern, index]
    print(output_info_str_2.format(*arg_list_search_2))
