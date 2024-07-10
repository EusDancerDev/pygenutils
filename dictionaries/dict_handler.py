#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------#
# Define functions #
#------------------#

def sort_dictionary_by_keys(dic):
    """
    Sort a dictionary by its keys.

    Parameters
    ----------
    dic : dict
        The dictionary to be sorted.

    Returns
    -------
    dict
        The dictionary sorted by keys.
    """
    keys_sorted_list = sorted(dic)
    dic_sorted_by_keys = {key: dic[key] for key in keys_sorted_list}
    return dic_sorted_by_keys


def merge_dictionaries(dict_list):
    """
    Merge a list of dictionaries into a single dictionary.

    Parameters
    ----------
    dict_list : list
        The list of dictionaries to be merged.

    Returns
    -------
    dict
        The merged dictionary.

    Raises
    ------
    ValueError
        If the list contains less than two dictionaries.
    """
    if len(dict_list) < 2:
        raise ValueError("At least 2 dictionaries must be passed.")
    
    merged_dict = {}
    for d in dict_list:
        merged_dict.update(d)
    return merged_dict