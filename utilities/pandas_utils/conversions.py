#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import pandas as pd
from numpy import array

#------------------#
# Define functions #
#------------------#

# Structured array conversion #
#-----------------------------#

def df_to_structured_array(df):
    """
    Converts a pandas DataFrame to a structured NumPy array.
    This type of array is still a conventional one of Numpy,
    but it consists on classifying the data type of each column.
    Then the resulting array contains:
        1. Values in each row displayed as a tuple.
        2. Data type of each column
        
    Parameters
    ----------
    df : pandas.DataFrame
        Pandas DataFrame containing data.
        
    Returns
    -------
    data : numpy.ndarray
        Structured NumPy array with the aforementioned structure.
    
    Raises
    ------
    None
        
    Examples
    --------
    >>> dtype = [('name', 'S10'), ('height', float), ('age', int)]
    >>> values = [('Arthur', 1.8, 41), ('Lancelot', 1.9, 38),
                  ('Galahad', 1.7, 38)]
    >>> a = np.array(values, dtype=dtype)
    array([(b'Arthur', 1.8, 41), (b'Lancelot', 1.9, 38),
           (b'Galahad', 1.7, 38)],
          dtype=[('name', 'S10'), ('height', '<f8'), ('age', '<i8')])
    
    As can be seen, in the structured array values are displayed by rows
    as a tuple, together with the data type of each column, which reads
    strings with a maximum of 10 characters, floats less than 8 bits
    and integers less than 8 bits, respectively.
    
    For readability, converted to a pandas DataFrame is:
        
              name  height  age
    0    b'Arthur'     1.8   41
    1  b'Lancelot'     1.9   38
    2   b'Galahad'     1.7   38
    """
    
    records = df.to_records(index=False)
    data = array(records, dtype=records.dtype.descr)
    return data