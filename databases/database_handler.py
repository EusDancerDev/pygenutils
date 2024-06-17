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

from pandas_data_frames.data_frame_handler import csv2df, excel_handler, ods_handler
from strings import string_handler, information_output_formatters

# Create aliases #
#----------------#

get_obj_specs = string_handler.get_obj_specs
find_substring_index = string_handler.find_substring_index
format_string = information_output_formatters.format_string

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
                     decimal="."):
       
    """
    Load data from input files into an existing SQL database.

    Parameters
    ----------
    input_file_list : str or list
        The path(s) of the input file(s) to be loaded into the database.
    config : dict
        Configuration dictionary containing database credentials.
    database_type : {'mysql', 'postgresql', or 'sqlite'}, optional
        Type of SQL database. Default is 'mysql'.
    if_exists : str, optional
        Action to take if the table already exists in the database.
        Options are 'replace', 'append', or 'fail'. Default is 'replace'.
    import_index : bool, optional
        Whether to import the index of the DataFrame into the database table.
        Default is False.
    separator : str, optional
        The separator used in the input file(s). Affects only CSV files.
        Default is '\t'.
    sheet_name : str, int, list, or None, optional
        Sheet name(s) to be loaded. Default is None (all sheets).
    header : int or list of int, optional
        Row number(s) to use as column names. Default is None.
    parser_engine : str, optional
        Engine to use for reading Excel files. Default is None.
    decimal : str, optional
        Character to recognize as decimal point. Default is ".".

    Returns
    -------
    None
    """
    
    # Create the engine #
    engine = create_engine_with_credentials(config, database_type=database_type)
    
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
        
    # Common keyword argument dictionary #
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
    
    kwargs_data_upload = dict(
        engine=engine,
        if_exists=if_exists,
        import_index=import_index
        )
    
    # Loop through files and upload data to the table names defined by their sheet names
    for file in input_file_list:
        in_extension = get_obj_specs(file, "ext")
        
        # CSV files
        if in_extension == extensions[0]:
            """
            In CSV files there is no 'sheet' concept, so it is assumed
            that the input data comes as is.
            """
            df = csv2df(file, separator, **kwargs_simple)
            table_name = get_obj_specs(file, "name_noext")
            df_loader(df, table_name, **kwargs_data_upload)
    
        # Microsoft Excel files
        elif in_extension == extensions[1]:
            item_dict = excel_handler(file, **kwargs_complete, return_type='dict')
            for sheet_name, df in item_dict.items():
                df_loader(df, table_name, **kwargs_data_upload)
            
        # LibreOffice Calc files
        elif in_extension == extensions[2]:
            item_dict = ods_handler(file, **kwargs_complete, return_type='dict')
            for sheet_name, df in item_dict.items():
                df_loader(df, table_name, **kwargs_data_upload)
        
        
def df_loader(df, table_name, engine, if_exists="replace", import_index=False):
    # TODO: taula osatuko duten zutabeen formatoa ezar daiteke?
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
success_data_load_str = """Data successfully loaded:
Database : {}
Table : {}
"""

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