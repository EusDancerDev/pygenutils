#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------#
# Define functions #
#------------------#

# Encoding and decoding functions for unsupported object types #
#--------------------------------------------------------------#

def to_json(python_object):
    if isinstance(python_object, bytes):
        json_dict = {'__class__':'bytes', '__value__': list(python_object)}
        return json_dict
    raise TypeError(f"{repr(python_object)} non serializable")

def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'bytes':
            bytes_obj = bytes(json_object['__value__'])
            return bytes_obj
    return json_object
