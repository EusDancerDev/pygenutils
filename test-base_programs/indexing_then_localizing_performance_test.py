#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jun  1 09:03:17 2023

@author: jgabantxo_ext
"""

#----------------#
# Import modules #
#----------------#


import numpy as np
import pandas as pd

import timeit

#------------------#
# Define functions #
#------------------#

def a_sel(a, rows, cols):
    a1 = a[rows][:, cols]
    return a1
    
def df_sel(df, rows,cols):
    df1 = df.loc[rows,cols]
    return df1

def a_where(a,val1,val2):
    anpw = np.where((a == val1) * (a == val2))
    return anpw
    
def df_where(df,val1,val2):
    dfw = df[(df == val1) & (df == val2)]
    return dfw
        
#-------------------#
# Define parameters #
#-------------------#

# Highest random number #
n = int(1e6)

# Calculus repetitions and increment #
repeats = 10
number = 1
step = 0.05

# Numpy random array attributes #
a = np.random.randint(0,n,size = (n,4))
la = len(a)

# Data frame attributes #
cols = ['itvs','a', 'b', 'c', 'd']
rows = np.unique(np.random.randint(0,n,size = la//2))
cols1 = [2,3]
cols1df = cols[slice(2,5,2)]

# Test values #
val1 = 27
val2 = 54

# Progress information string #
res_info_str = """Execution times for {} loops with {} reps:
    
INDEXING
--------
    
Numpy generic: {}; best {}
Pandas: {}; best {}

LOCALIZING
----------
    
Numpy where: {}; best {}
Pandas: {}; best {}

"""

#-------------------#
# Program operation #
#-------------------#

# Numpy array and Pandas DataFrame 
itvs = [pd.Interval(i,i+step, closed = "left") for i in range(la)]

a = np.append(np.array(itvs)[:, np.newaxis], a, axis = 1)

df = pd.DataFrame(a, columns = cols)

# Snippet execution timer arguments #
arg_dict_a_sel = dict(stmt="a_sel(a,rows,cols1)", 
                      repeat = repeats,
                      number = number, 
                      globals = globals())

arg_dict_df_sel = dict(stmt="df_sel(df,rows,cols1df)",
                       repeat = repeats, 
                       number = number, 
                       globals = globals())


arg_dict_a_where = dict("a_where(a,val1,val2)", 
                        repeat = repeats,
                        number = number, 
                        globals = globals())

arg_dict_df_where = dict("df_where(df,val1,val2)", 
                         repeat = repeats,
                         number = number,
                         globals = globals())

# Computation of snippet execution times #
a_sel_elapsed_times = np.round(timeit.repeat(**arg_dict_a_sel), 3)
df_sel_elapsed_times = np.round(timeit.repeat(**arg_dict_df_sel), 3)
a_where_elapsed_times = np.round(timeit.repeat(**arg_dict_a_where), 3)
df_where_elapsed_times = np.round(timeit.repeat(**arg_dict_df_where), 3)

# Print the results using the preformatted string #
res_arg_tuple = (repeats, number, 
                 a_sel_elapsed_times, min(a_sel_elapsed_times),
                 df_sel_elapsed_times, min(df_sel_elapsed_times),
                 a_where_elapsed_times, min(a_where_elapsed_times),
                 df_where_elapsed_times, min(df_where_elapsed_times))

print(res_info_str.format(*res_arg_tuple))
