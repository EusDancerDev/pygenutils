"""
**Note**

This program is an application of the main module 'database_handler',
and it uses some of its attributes and/or functions.
YOU MAY REDISTRIBUTE this program along with any other directory
and adapt it to your needs.

Purpose
-------
- This program loads data from various file types (CSV, Excel, ODS) into a MySQL database.
- The method 'load_file_to_sql' from 'database_handler' is utilized for this task.
- Parameters can be modified to suit different data files and database configurations.

For 'dtype_dict_obj' Usage, please refer the docs of parameter 'dtype_dict'
at 'load_file_to_sql' method

Data Type Options
-----------------
Refer to the following table for mapping Pandas data types to MySQL data types:

| Pandas Data Type | MySQL Data Type     |
|------------------|---------------------|
| `int64`          | `BIGINT`            |
| `int32`          | `INTEGER`           |
| `float64`        | `DOUBLE`            |
| `float32`        | `FLOAT`             |
| `bool`           | `BOOLEAN`           |
| `datetime64`     | `DATETIME`          |
| `timedelta[ns]`  | `TIME`              |
| `object`         | `TEXT` or `VARCHAR` |
| `category`       | `VARCHAR`           |

Data Files
----------
- The 'input_file_obj' variable can be assigned a single file path or a list of paths.
- Alternatively, files can be searched using methods 'find_files_by_globstr' 
  for glob strings or 'find_files_by_ext' for extensions 
  from the 'file_and_directory_paths' module.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from databases.database_handler import load_file_to_sql
# from files_and_directories.file_and_directory_paths import find_files_by_globstr
# from files_and_directories.file_and_directory_paths import find_files_by_ext

#-------------------#
# Define parameters #
#-------------------#

# Config dictionary containing database credentials #
#---------------------------------------------------#

config_dict = {
    "username": "username",
    "password": "cool-password",
    "host": "host",
    "database_name": "dbname",
}

# Database type #
#---------------#

database_type = "mysql"

# Table parameters #
#------------------#

table_param_dict = dict(
    if_exists="replace",
    import_index=False,
    separator="\t", 
    header=0,
    parser_engine=None,
    decimal=","
    )

# Data type dictionary to apply for one or more sheets #
#------------------------------------------------------#

dtype_dict_obj = {
    'column1': 'int64',
    'column2': 'float64',
    'column3': 'object'
}

# dtype_dict_obj = [
#     {
#         'file1_column1': 'int64',
#         'file1_column2': 'float64',
#         'file1_column3': 'object'
#     },
#     {
#         'file2_column1': 'int64',
#         'file2_column2': 'float64',
#         'file2_column3': 'object'
#     },
# ]

# dtype_dict_obj = None

# Data files #
#------------#

input_file_obj = "/home/jonander/Documents/gordetegiak/pytools/databases/test.csv"

# input_file_obj = [
#     "/home/jonander/Documents/gordetegiak/pytools/databases/test1.csv",
#     "/home/jonander/Documents/gordetegiak/pytools/databases/test2.csv",
#     "/home/jonander/Documents/gordetegiak/pytools/databases/test3.csv"
#     ]

# input_file_obj = find_files_by_globstr("test*",
#                                        path_to_walk_into=".", 
#                                        top_path_only=True)

# input_file_obj = find_files_by_ext(".csv",
#                                    path_to_walk_into=".", 
#                                    top_path_only=True)

#------------------#
# Perform the task #
#------------------#

load_file_to_sql(input_file_obj,
                 config_dict, 
                 database_type=database_type, 
                 **table_param_dict,
                 dtype_dict=dtype_dict_obj)
