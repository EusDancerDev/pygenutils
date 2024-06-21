#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from sqlalchemy import Column, DateTime, Integer, String, create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus

from datetime import datetime as dt

#-----------------------#
# Import custom modules #
#-----------------------#

from pytools.pandas_data_frames.data_frame_handler import csv2df, excel_handler, ods_handler

from pytools.strings.information_output_formatters import format_string
from pytools.strings.string_handler import find_substring_index, get_obj_specs

from pytools.utilities.introspection_utils import get_obj_type_str, retrieve_function_name

#----------------#
# Create objects #
#----------------#

# Define the base class for declarative class definitions
Base = declarative_base()

#------------------#
# Define functions #
#------------------#

# Database connection creator #
#-----------------------------# 

def create_engine_with_credentials(config, database_type="mysql"):
    
    """
    Create a SQLAlchemy engine with the provided credentials
    for connecting to a SQL database.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing database credentials.
        Expected keys:
        - 'username': str, the username for accessing the database.
        - 'password': str, the password for accessing the database.
        - 'host': str, the host address of the database.
        Optional keys:
        - 'database_name': str, the name of the database.
          For example, if the MySQL query is precisely to create a database,
          then creating an engine with this parameter is nonsensical, 
          hence the reason to be optional.
          
    database_type : {'mysql', 'postgresql', or 'sqlite'}, optional
        Type of SQL database. Default is 'mysql'.

    Returns
    -------
    sqlalchemy.engine.base.Engine
        An SQLAlchemy engine object.

    Raises
    ------
    None
    
    Note
    ----
    Special characters like '@' in the password can cause issues 
    when constructing the connection string. 
    These characters need to be URL-encoded using 'urllib.parse.quote_plus'.
    """
    
    # Proper database type argument control #
    database_type_list = list(db_alias_dict.keys())
    if database_type not in database_type_list:
        raise ValueError(f"Wrong database type. Options are {database_type_list}")
    
    # URL-encode the password #
    password = quote_plus(config.get('password'))
    
    # Create the database alias #
    db_alias = db_alias_dict.get(database_type)
    
    # Gather the arguments in a string to convert into an engine prompt #    
    if database_type in database_type_list[:-1]:
        engine = create_engine(f"{db_alias}://{config['username']}:"
                               f"{password}@{config['host']}/{config['database_name']}")
    else:
        engine = create_engine(f"{db_alias}:///{config['database_name']}.db")
    return engine


# Database creations #
#--------------------#

# Define a User class #
class User(Base):
    """
    Data model for the 'users' table in a database.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=dt.utcnow)
    
# Method to create the database according to the base class #
def create_sql_database_base(config):
    
    """
    Create an SQL database and initialize the connection session,
    according to the base class.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing database credentials and type.

    Returns
    -------
    sqlalchemy.orm.session.Session
        A session connected to the created database.
    """
    
    # Create the engine
    engine = create_engine_with_credentials(config)
        
    # Create all tables in the engine
    Base.metadata.create_all(engine)
    
    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)
    
    # Create a session
    session = Session()
    
    return session

# Generic, standard database creator #
def create_sql_database(config, db_name):
    
    """
    Create an SQL database and initialize the connection session.

    Parameters
    ----------
    config : dict
        Configuration dictionary containing database credentials and type.
    db_name : str
        Name of the database to be created.

    Returns
    -------
    None
    """
    
    # Create the engine
    engine = create_engine_with_credentials(config)
        
    # MySQL server query string #
    db_creation_str = f"CREATE DATABASE {db_name}"
    
    # Create the database
    custom_database_query(db_creation_str, engine)
    

#%%

# Data uploading #
#----------------#

def load_file_to_sql(input_file_list, 
                     config,
                     database_type="mysql",
                     if_exists="replace",
                     import_index=False,
                     separator="\t",
                     sheet_name=None,
                     header=None,
                     parser_engine=None,
                     decimal=".",
                     dtype_dict=None):
    """
    Load data from various file types into a MySQL database.

    Parameters
    ----------
    input_file_list : str or list of str
        Path(s) to the input file(s).
    config : dict
        Database configuration. For the accepted arguments, 
        refer the docs in 'create_engine_with_credentials' method.
    database_type : {'mysql', 'postgresql', or 'sqlite'}, optional
        Type of SQL database. Default is 'mysql'.
    if_exists : {'replace', 'append', or 'fail'}, optional
        Action to take when the table already exists in the database.
        Default is 'replace'.
    import_index : bool, optional
        Whether to import the DataFrame index into the database table.
        Default is False.
    separator : str, optional
        Separator for only CSV files. Default is "\t".
    sheet_name : str or None
        Sheet name for Excel and ODS files. Default is None.
    header : int or None
        Row number(s) to use as the column names.
        Default is None (take into account all sheets).
    parser_engine : str or None
        Parser engine for reading the files. Default is None.
    decimal : str
        Character to recognize as decimal point (default is ".").
    dtype_dict : dict or list of dict or None
        Data type definitions for columns. Default is None.

    Returns
    -------
    None
    """
    
    """
    Load data from various file types into a MySQL database.

    Parameters
    ----------
    input_file_list : str or list of str
        Path(s) to the input file(s).
    config : dict
        Database configuration. For the accepted arguments, 
        refer the docs in 'create_engine_with_credentials' method.
    database_type : {'mysql', 'postgresql', or 'sqlite'}, optional
        Type of SQL database. Default is 'mysql'.
    if_exists : {'replace', 'append', or 'fail'}, optional
        Action to take when the table already exists in the database.
        Default is 'replace'.
    import_index : bool, optional
        Whether to import the DataFrame index into the database table.
        Default is False.
    separator : str, optional
        Separator for only CSV files. Default is "\t".
    sheet_name : str or None, optional
        Sheet name for Excel and ODS files. Default is None.
    header : int or None, optional
        Row number(s) to use as the column names.
        Default is None (take into account all sheets).
    parser_engine : str or None, optional
        Parser engine for reading the files. Default is None.
    decimal : str, optional
        Character to recognize as decimal point (default is ".").
    dtype_dict : dict or None, optional
        Data type definitions for columns. Ddefault is None.
        
        Usage Notes
        -----------
        - The 'dtype_dict_obj' parameter used to specify data types for columns 
          in the DataFrame.
        - Usage is identical to the 'dtype_dict_obj' parameter in the 
          'load_file_to_sql' method, and it is optional.
        - If several files are being processed, construct a list of dictionaries 
          (one per file).
        - It is not necessary to mention every data table column in a dictionary.
        - If no dtype is needed: 
            * For a single file, set 'dtype_dict_obj' to None or an empty dictionary.
            * For a list of files, for each file in which dtype is not needed, 
              proceed in the same way for the corresponding dict in the list of them.
        
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
        
    Returns
    -------
    None
    """
    
    # Argument adecuacy controls #
    ##############################
    
    # Retrieve argument names for error handling #
    arg_names = retrieve_function_name()
    dtype_dict_arg_pos = find_substring_index(arg_names, "dtype_dict")
    
    # Convert the input file list to that if it's a string
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
        
    # Convert 'dtype_dict' argument to list if it's a single dictionary
    if isinstance(dtype_dict, dict):
        dtype_dict = [dtype_dict]
          
    # Common keyword arguments #
    ############################
        
    # Common keyword argument dictionary for CSV and other file handlers
    kwargs_simple = dict(
        engine=parser_engine,
        header=header, 
        decimal=decimal,
    )
    
    kwargs_complete = dict(
        engine=parser_engine,
        sheet_name=sheet_name,
        header=header, 
        decimal=decimal,
    )
    
    # Operations #
    ##############
    
    # Create the database engine
    engine = create_engine_with_credentials(config, database_type=database_type)
  
    # Keyword arguments for data upload
    kwargs_data_upload = dict(
        engine=engine,
        if_exists=if_exists,
        import_index=import_index,
    )
    
    # Loop through files and upload data to the table names defined by their sheet names
    for file, dtype in zip(input_file_list, dtype_dict):
        in_extension = get_obj_specs(file, "ext")
        
        try:
            # CSV files
            if in_extension == extensions[0]:
                """
                In CSV files there is no 'sheet' concept, so it is assumed
                that the input data comes as is.
                """
                df = csv2df(file, separator, **kwargs_simple)
                table_name = get_obj_specs(file, "name_noext")
                if dtype:
                    df = df.astype(dtype)
                df_loader(df, table_name, **kwargs_data_upload)
        
            # Microsoft Excel files
            elif in_extension == extensions[1]:
                item_dict = excel_handler(file, **kwargs_complete, return_type='dict')
                for sheet_name, df in item_dict.items():
                    if dtype:
                        df = df.astype(dtype)
                    df_loader(df, sheet_name, **kwargs_data_upload)
                
            # LibreOffice Calc files
            elif in_extension == extensions[2]:
                item_dict = ods_handler(file, **kwargs_complete, return_type='dict')
                for sheet_name, df in item_dict.items():
                    if dtype:
                        df = df.astype(dtype)
                    df_loader(df, sheet_name, **kwargs_data_upload)
                    
        except ValueError:
            # Handle ValueError for unsupported data types
            raise ValueError(format_string(unsupported_dtype_err_str, file))
        except TypeError:
            # Handle TypeError for incorrect dtype_dict type
            dtype_arg_type = get_obj_type_str(dtype_dict)
            arg_list_typeerror = [file, arg_names[dtype_dict_arg_pos], dtype_arg_type]
            raise TypeError(incorrect_arg_type_str, arg_list_typeerror)
        
        
def df_loader(df, table_name, engine, if_exists="replace", import_index=False):
    """
    Load a DataFrame into a SQL database table.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be loaded into the database.
    table_name : str
        The name of the table in the database.
    engine : sqlalchemy.engine.base.Engine
        The SQLAlchemy engine object.
    if_exists : {'replace', 'append', 'fail'}, optional
        Action to take if the table already exists in the database. 
        Default is 'replace'.
        - 'replace': Drop the table before inserting new values.
        - 'append': Insert new values to the existing table.
        - 'fail': Raise a ValueError if the table exists.
    import_index : bool, optional
        Whether to import the index of the DataFrame into the database table.
        Default is False.

    Returns
    -------
    str
        A message indicating successful data load to the specified
        database and table name.

    Raises
    ------
    ValueError
        If the data upload fails due to incorrect database credentials
        or other issues.
    SQLAlchemyError
        If an error occurs within SQLAlchemy during the upload process.
    Exception
        For any other errors, providing an intuitive error message.

    Notes
    -----
    This function uses pandas `to_sql` method to upload the DataFrame to the database.
    It handles different types of errors and provides meaningful error messages based
    on the error code.

    Example
    -------
    >>> df_loader(df, 'my_table', engine)
    'Data successfully loaded: Database: my_database Table: my_table'
    """
    
    try:
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=import_index)
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except SQLAlchemyError as se:
        print(f"SQLAlchemyError: {se}")
    except Exception as e:
        err_code = find_substring_index(str(e), "[0-9]{4}", 
                                        advanced_search=True, 
                                        return_match_index=False,
                                        return_match_str=True)
        intuitive_err = data_uploading_error_dict.get(err_code)
        raise ValueError(intuitive_err)
    else:
        database_name = engine.url.database
        arg_list_data_load = [database_name, table_name]
        return format_string(success_data_load_str, arg_list_data_load)
        
#%%
        
# Database queries #
#------------------#

def custom_database_query(query_str, engine):
    """
    Execute a query to a SQL database.

    Parameters
    ----------
    query_str : str
        The SQL query string.
    engine : sqlalchemy.engine.base.Engine
        The SQLAlchemy engine object.

    Returns
    -------
    None
    
    Raises
    ------
    SQLAlchemyError
        If there is an error in the SQL execution.
    OperationalError
        If there is a database operation error.

    Notes
    -----
    'conn.execute()' method expects an executable SQL object, not a plain string. 
    Use SQLAlchemy's 'text' module to create an executable SQL object 
    from the query string.
    """
    try:
        with engine.connect() as conn:
            query = text(query_str)
            result = conn.execute(query)
            
            # Check if the result returns anything
            if result.returns_rows:
                for row in result:
                    print(row)
            else:
                print("Query executed successfully, no results to display.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
    except OperationalError as e:
        print(f"Operational error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


#--------------------------#
# Parameters and constants #
#--------------------------#

# File in_extension #
extensions = ["csv", "xlsx", "ods"]

# Preformatted strings #
#----------------------#

# Informative strings #
success_data_load_str = """Data successfully loaded:
Database : {}
Table : {}
"""

# Error strings #
unsupported_dtype_err_str = "File: {}\nUnsupported data type(s) provided"
incorrect_arg_type_str = "File: {}\nExpected dictionary for argument '{}', got {}"

# Switch dictionaries #
#---------------------#

# Database alias dictionary #
db_alias_dict = {
    "mysql" : "mysql+pymysql",
    "postgresql" : "postgresql",
    "sqlite" : "sqlite"
}

# Data uploading error messages #
data_uploading_error_dict = {
    "1045" : "Wrong username",
    "1049" : "Unknown database name",
    "1698" : "Wrong password",
    "2003" : "Wrong host name"
    }