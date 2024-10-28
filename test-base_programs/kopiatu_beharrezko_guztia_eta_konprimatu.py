#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:11:21 2023

@author: jonander

**Deskribapena**
Artxibo batzuk haiei dagokien direktoriotik hona kopiatu ondoren
karpeta konprimatu batean gordetzeko programa.
"""

#----------------#
# Import modules #
#----------------#

import os
import time

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists import conversions, data_manipulation, patterns
from pyutils.filewise.file_operations import ops_handler, path_utils
from pyutils.strings.string_handler import find_substring_index

# Create aliases #
#----------------#

convert_data_type = conversions.convert_data_type
flatten_to_string = conversions.flatten_to_string

remove_elements = data_manipulation.remove_elements
select_elements = patterns.select_elementss

copy_files = ops_handler.copy_files
remove_files = ops_handler.remove_files
rename_objects = ops_handler.rename_objects

find_dirs_with_files = path_utils.find_dirs_with_files

#----------------------#
# Parametroak definitu #
#----------------------#

docpath = "/home/jonander/Documents/"
exts = ["jpg", "pdf", "zip"]

key_word = "kopiatu"

kw_del_list = ["kopiatu", "RDT"]

#---------------------#
# Kontrol-etengailuak #
#---------------------#

compress_copied_and_renamed_files = True

#--------------------------#
# Zehaztu artxiboen izenak #
#--------------------------#

# Jatorrizko izenak #
#-------------------#

file_list_orig = [
    f"2023_garbiago.{exts[0]}",
    f"Jon_Ander_Gabantxo_betea.{exts[1]}",
    f"NAN_aurrealdea.{exts[0]}",
    f"NAN_atzealdea.{exts[0]}",
    f"aurrealdea.{exts[0]}",
    f"atzealdea.{exts[0]}",
    f"lan-bizitza_2023-10-20.{exts[1]}",
    f"meteorologia-ikastaroa.{exts[1]}",
    f"Aula_Carpe_Diem-MySQL_PHP.{exts[1]}",
    f"EGA.{exts[1]}",
    f"titulu_ofiziala.{exts[1]}",
    f"HEO-ingelesa_C1.{exts[1]}",
    f"titulo_oficial.{exts[1]}"
]

# Berrizendaketak (hizkuntza edo testua soilik) #
#-----------------------------------------------#

file_list_2rename = [
    f"2023.{exts[0]}",
    f"CV_betea.{exts[1]}",
    f"NAN_aurrealdea.{exts[0]}",
    f"NAN_atzealdea.{exts[0]}",
    f"gida-baimena_aurrealdea.{exts[1]}",
    f"gida-baimena_atzealdea.{exts[1]}",
    f"lan-bizitza_2023-10-20.{exts[1]}",
    f"meteorologia-ikastaroa_ziurtagiria.{exts[1]}",
    f"MySQL-PHP_ziurtagiria.{exts[0]}",
    f"EGA-titulu_ofiziala.{exts[1]}",
    f"fisikako_gradua-titulu_ofiziala.{exts[1]}",
    f"ingelesa_C1-titulu_ofiziala.{exts[1]}",
    f"master_meteorologia_titulo_oficial.{exts[1]}"
]

# Ezabatu direktorio honetako fitxategi guztiak, batzuk izan ezik #
#-----------------------------------------------------------------#

print("Direktorio honetako fitxategiak batzuk izan ezik ezabatzen...")

# Artxiboak zerrendatu #
file_list_cwd = os.listdir()

# Zerrendatik programa batzuk ezabatu #
del_file_obj = find_substring_index(file_list_cwd, kw_del_list)

if isinstance(del_file_obj, dict):
    del_file_idx = [key for key in del_file_obj if len(del_file_obj[key]) > 0]
elif isinstance(del_file_obj, list):
    del_file_idx = del_file_obj.copy()
else:
    del_file_idx = del_file_obj


files2delete = remove_elements(file_list_cwd, del_file_idx)
files2delete = convert_data_type(files2delete, 'U', 'O', convert_to_list=True)

# Ezabatu zerrenda erresultantean ageri diren artxiboak #
remove_files(files2delete, ".", match_type="glob")

# Bilatu euskaraz izendatutako artxiboak #
#----------------------------------------#

print("Jatorrizko programak bilatzen...")
dir_list_orig = find_dirs_with_files(file_list_orig, search_path=docpath, match_type="glob")

# Kopiatu bilatutako artxiboak direktorio hona #
#----------------------------------------------#

print("Bilatutako programak direktorio honetara bertara kopiatzen...")
copy_files(file_list_orig, 
           input_directories=dir_list_orig, 
           destination_directories=".", 
           match_type="glob")

# Kopiatutako artxiboak berrizendatu #
#------------------------------------#

print("Kopiatutako programak berrizendatzen...")

rename_objects(file_list_orig, file_list_2rename)

# Berrizendatutako artxiboak karpeta konprimatu batean gorde #
#------------------------------------------------------------#

if compress_copied_and_renamed_files:
    
    print("Berrizendatutako programak karpeta konprimatu batean gordetzen...")
    time.sleep(0.5)
    
    output_zip_file = f"Jon_Ander_Gabantxo.{exts[-1]}"
    
    file_list_2rename_str = flatten_to_string(file_list_2rename)
    files_excluded_from_zipping\
    = flatten_to_string(select_elements(file_list_cwd, del_file_idx))
    
    zip_command = f"zip {output_zip_file} {file_list_2rename_str} -x {files_excluded_from_zipping}"
    os.system(zip_command)
