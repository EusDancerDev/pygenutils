#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from numpy import array, char, unique
import pandas as pd

#-----------------------#
# Import custom modules #
#-----------------------#

from pyutils.arrays_and_lists.data_manipulation import find_duplicated_elements
from pyutils.files_and_directories import file_and_directory_handler, file_and_directory_paths
from pyutils.parameters_and_constants import global_parameters
from pyutils.strings.string_handler import ext_adder, find_substring_index, get_obj_specs
from pyutils.strings.information_output_formatters import format_string, get_obj_type_str
from pyutils.time_handling.time_formatters import parse_time_string
from pyutils.utilities.introspection_utils import get_caller_method_args

# Create aliases #
#----------------#

basic_time_format_strs = global_parameters.basic_time_format_strs
common_delim_list = global_parameters.common_delim_list

remove_files_by_globstr = file_and_directory_handler.remove_files_by_globstr
find_files_by_globstr = file_and_directory_paths.find_files_by_globstr

#------------------#
# Define functions #
#------------------#

# Dataframe intrinsic #
#---------------------#

# Date and time detection and handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def infer_time_frequency(df_or_index):
    
    """
    Infer the most likely frequency given the input index,
    using pandas's 'infer_freq' method.
    If the frequency is uncertain, a warning will be printed.
    
    Parameters
    ----------
    df_or_index : pandas.DataFrame or pandas.Series or DatetimeIndex or TimedeltaIndex
    
        The method will first assume that the input argument 
        is a pandas object, so that is has a date key column,
        and will attempt to infer the time frequency.
        
        To do so, the already defined 'find_date_key' attempts
        to find the date column. If cannot be found,
        that will mean that the input argument is not a pandas object
        but a DatetimeIndex of TimedeltaIndex object instead.
    
    Returns
    -------
    str
        The time frequency.
        If the frequency cannot be determined, pandas.infer_freq
        method returns None. In such case, this function is designed
        to raise a ValueError that indicates so.
    
    Note
    ----
    If passed a pandas's Series 
    will use the values of the series (NOT THE INDEX).
    """
   
    try:
        date_key = find_date_key(df_or_index)
        time_freq = pd.infer_freq(df_or_index[date_key])
    except (TypeError, ValueError):
        time_freq = pd.infer_freq(df_or_index)
        
    if time_freq is None:
        raise ValueError("Could not determine the time frequency.")
    else:
        return time_freq

    
def infer_full_period_of_time(df):
    
    date_key = find_date_key(df)
    years = unique(df[date_key].dt.year)
    full_period = f"{years[0]-years[-1]}"
    
    return full_period


def find_date_key(df):
    
    """
    Function that searches for date key in the columns of a Pandas DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Pandas data frame containing data.
    
    Returns
    -------
    date_key : str
        String which date key is identified with.
    """
    
    try:
        df_cols = char.lower(df.columns.tolist())    
    except AttributeError:
        input_obj_type = get_obj_type_str(df)
        raise TypeError(format_string(unsupported_obj_type_err_str, input_obj_type))
    else:
        try:
            date_key_idx = find_substring_index(df_cols, time_kws)
            date_key = df_cols[date_key_idx]
        except KeyError:
            raise KeyError("Grouper name 'date' or similar not found")
        else:
            return date_key
    
    
# Data grouping #
#-#-#-#-#-#-#-#-#

def create_pivot_table(df, df_values, df_index, func_apply_on_values):    
    pivot_table = pd.pivot_table(df,
                                 values=df_values, 
                                 index=df_index,
                                 aggfunc=func_apply_on_values)
    
    return pivot_table


def count_data_by_concept(df, df_cols):
    data_count = df.groupby(df_cols).count()
    return data_count    


# Dataframe appearance polishing #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def polish_df_column_names(df, sep_to_polish="\n"):
      
    """
    Function to polish a Pandas DataFrames' column names, by eliminating
    the specified separator that might appear when reading files such as
    Microsoft Excel or LibreOffice Calc document.
    
    It uses the 'rename' method to rename the columns by using a 'lambda';
    it simply takes the final entry of the list obtained by splitting 
    each column name any time there is a new line.
    If there is no new line, the column name is unchanged.
    
    Parameters
    ----------
    df : pandas.Dataframe
        Dataframe containing data
    sep_to_polish : str
        Separator to detect and eliminate from the string formed
        by all column names.
        
    Returns
    -------
    df_fixed : pandas.Dataframe
        Dataframe containing exactly the same data as the input one,
        with column names polished accordingly.    
    """
    
    df_fixed = df.rename(columns=lambda x: x.split(sep_to_polish)[-1])
    return df_fixed

    
    
# Data frame value handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def sort_df_values(df,
                   by,
                   ignore_index_bool=False,
                   axis=0,
                   ascending_bool=True,
                   na_position="last",
                   key=None):
    
    """
    Sort by the values along either axis
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    by : str or list of str
        Name or list of names to sort by.
    ignore_index : bool
        Boolean to determine whether to relabel indices
        at ascending order: 0, 1, ..., n-1 or remain them unchanged.
        Defaults False.
    axis : {0, 'index', 1, 'columns'}
        Axis to be sorted; default value is 0.
    ascending : bool or list of bool
        Sort ascending vs. descending. Specify list for multiple sort
        orders. Default is True boolean.
    na_position : {'first', 'last'}
        Puts NaNs at the beginning if 'first'; 'last' puts NaNs at the end.
        Defaults to "last".
    key : callable, optional
        Apply the key function to the values
        before sorting. This is similar to the 'key' argument in the
        builtin :meth:'sorted' function, with the notable difference that
        this 'key' function should be *vectorized*.
    """
    
    df = df.sort_values(by=by,
                        axis=axis, 
                        ascending=ascending_bool,
                        na_position=na_position,
                        ignore_index=ignore_index_bool,
                        key=key)

    return df

    
def insert_column_in_df(df, index_col, column_name, values):
    
    """
    Function that inserts a column on a simple, non multi-index
    Pandas DataFrame, specified by an index column.
    Note that this method is in-place.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Data frame containing data.
    index_col : int
        Denotes the column position to insert new data.
        It is considered that data is desired to introduced
        at the LEFT of that index, so that once inserted data on that position, 
        the rest of the data will be displaced rightwards.
    column_name : str
        Name of the column to be inserted.
    values : list, numpy.array or pandas.Series
    """
    
    ncols = len(df.iloc[0])
    
    if index_col < 0:
        index_col += ncols + 1

    df.insert(index_col, column_name, values)
    
    
def insert_row_in_df(df, index_row, values=float('nan'), reset_indices=False):
    
    """
    Function that inserts a row on a simple, non multi-index
    Pandas DataFrame, in a specified index column.
    That row can be introduced at the begginning, ending,
    or in any position between them.
    This function works either with integer or DatetimeIndex arrays.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Data frame containing data.
    index_row : int, str, datetime.datetime or pandas._libs.tslibs.timestamps.Timestamp
        Denotes the row position to insert new data.
        It is considered that data is desired to introduced
        ABOVE that index, so that once inserted data on that position, 
        the rest of the data will be displaced downwards.
        
        Strictly speaking, this function distinguishes between four cases:
        1. The index is an integer:
            If index_row == 0 then the row will be introduced
            at the begginning, ending if index_row == -1,
            else at any other position.
        2. The index is a datetime.datetime tuple:
            The index will be introduced at the end of the data frame,
            and then the indices will be sorted.
            Note this means that the new time array spacing is NOT even.
              
    values : single value or list or numpy.ndarray or pandas.Series
        The type of the value(s) is considered as irrelevant.
        Default value is NaN.
    """
    
    idx = df.index
    
    if isinstance(idx, pd.RangeIndex)\
    or isinstance(idx, pd.Float64Index):
    
        if index_row == 0:
            df_shift = df.shift()
            df_shift.loc[idx[-1]+1] = df.loc[idx[-1]] 
            df_shift.loc[idx[0], :] = values
            df = df_shift
            
        elif index_row == -1:
            df.loc[idx[-1]+1, :] = values
            
        else:
            index_between = index_row - 0.5
            df.loc[index_between, :] = values
            
            if reset_indices:
                df = df.reset_index(drop=True)
    
    else:
        try:
            time_freq = pd.infer_freq(idx)
        except (TypeError, ValueError):
            time_freq = pd.infer_freq(idx[100])
            
        time_abbrs = basic_time_format_strs
        
        if isinstance(index_row, str):
            if time_freq not in time_abbrs:
                dt_format = basic_time_format_strs["H"]
            else:
                dt_format = basic_time_format_strs[time_freq]
                
            index_row = parse_time_string(index_row, dt_format)
        
        df.loc[index_row, :] = values
        df.sort_index()
        
    return df
        
    
# Data frame index handling #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def sort_df_indices(df,
                    axis=0,
                    ignore_index_bool=False,
                    level=None,
                    ascending_bool=True,
                    na_position="last",
                    sort_remaining_bool=True,
                    key=None):
    
    """
    Returns a new data frame sorted 
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    level : int or level name or list of ints or list of level names
        If not None, sort on values in specified index level(s)
    axis : {0, 'index', 1, 'columns'}
        Axis to be sorted; default value is 0.
    ignore_index : bool
        Boolean to determine whether to relabel indices
        at ascending order: 0, 1, ..., n-1 or remain them unchanged.
        Defaults False.
    ascending : bool or list of bool
        Sort ascending vs. descending. Specify list for multiple sort
        orders. Default is True boolean.
    na_position : {'first', 'last'}.
        Puts NaNs at the beginning if 'first'; 'last' puts NaNs at the end.
        Defaults to "last".
    sort_remaining : bool
        If True and sorting by level and index is multilevel, sort by other
        levels too (in order) after sorting by specified level.
        Default value is True.
    key : callable, optional
        Apply the key function to the values
        before sorting. This is similar to the 'key' argument in the
        builtin :meth:'sorted' function, with the notable difference that
        this 'key' function should be *vectorized*.
    """
            
    df.sort_index(axis=axis, 
                  level=level,
                  ascending=ascending_bool,
                  na_position=na_position,
                  sort_remaining=sort_remaining_bool,
                  ignore_index=ignore_index_bool,
                  key=key)
    
    return df


def reindex_df(df, col_to_replace=None, vals_to_replace=None):
    
    """
    Further function than df.reset_index attribute,
    for resetting the index of the given Pandas DataFrame,
    using any specified column and then resetting the latter.
    This method applies only for one-leveled objects
    (i.e, cannot have a MultiIndex) and can contain any tipe of index.
    It can also be applied for simple reindexing.
    
    Parameters
    ----------
    df : pandas.DataFrame or pandas.Series.
    vals_to_replace : list, np.ndarray or pandas.Series
        New labels / index to conform to.
    col_to_replace : str or int
        If further reindexing is required,
        an it is a string, then it selects the columns to put as index.
        Otherwise it selects the number column.
        Defaults to None, that is, to simple reindexing.
    """
    
    if col_to_replace is None and vals_to_replace is None:
        raise ValueError("You must provide an object containing values to"
                         "put as index.")
        
    elif col_to_replace is None and vals_to_replace is not None:
        df = df.reindex(vals_to_replace)
        
    else:
        
        if isinstance(col_to_replace, str):

            # Substitute the index as desired #  
            df_reidx_drop_col\
            = df.reindex(df[col_to_replace]).drop(columns=col_to_replace)
            
            # Assign the remaining values to the new data frame #
            df_reidx_drop_col.loc[:,:]\
            = df.drop(columns=col_to_replace).values
            
        elif isinstance(col_to_replace, int):
            
            columns = df.columns
            colname_to_drop = columns[col_to_replace]
            
            # Substitute the index as desired #              
            df_reidx_drop_col\
            = df.reindex(df.iloc[:, col_to_replace]).drop(columns=colname_to_drop)
        
            # Assign the remaining values to the new data frame #
            df_reidx_drop_col.loc[:,:]\
            = df.drop(columns=colname_to_drop).values
        
    return df_reidx_drop_col
    

# Data file reading #
#-------------------#

# TXT files #
#-#-#-#-#-#-#

def read_table(file_path,
               separator="\s+",
               dtype=None,
               engine=None,
               encoding=None,
               header="infer"):
 
    """
    Function that uses pandas module to read a text file
    and converts to a data frame.
    
    It assumes that the text file is well organised,
    with no irregular spaces, and that spaces mean 
    there should be different columns.
    
    It is still assumed that the whitespace is one character long
    throughout the whole data frame.
    
    Parameters
    ---------- 
    file_path : str
        Path of the file to be examined.
    separator : str, default '\\t' (tab-stop)
        Delimiter to use. If sep is None, the C engine cannot automatically detect
        the separator, but the Python parsing engine can, meaning the latter will
        be used and automatically detect the separator by Python's builtin sniffer
        tool, ''csv.Sniffer''. In addition, separators longer than 1 character and
        different from ''\s+'' will be interpreted as regular expressions and
        will also force the use of the Python parsing engine. Note that regex
        delimiters are prone to ignoring quoted data. Regex example: '\r\t'.
    dtype : Type name or dict of column -> type, optional
        Data type for data or columns. E.g. {'a': np.float64, 'b': np.int32,
        'c': 'Int64'}
        Use 'str' or 'object' together with suitable 'na_values' settings
        to preserve and not interpret dtype.
        If converters are specified, they will be applied INSTEAD
        of dtype conversion.
    engine : {'c', 'python', 'pyarrow'}, optional
        Parser engine to use. The C and pyarrow engines are faster, 
        while the python engine is currently more feature-complete. 
        Multithreading is currently only supported by the pyarrow engine.
        Defaults to None.
    encoding : str
        String that identifies the encoding to use for UTF
        when reading/writing.
        Default value is 'utf-8' but it can happen that
        the text file has internal strange characters that
        UTF-8 encoding is not able to read.
        In such cases "latin1" is reccommended to use.
   
    header : int, list of int, None, default 'infer'
        Row number(s) to use as the column names, and the start of the data.
        Default behaviour is to infer the column names: if no names are passed
        the behaviour is identical to header=0 and column names are inferred
        from the first line of the file.
        
        If column names are passed explicitly then the behaviour
        is identical to header=None, where the text file's header
        are only column names.
        
        Explicitly pass header=0 to be able to replace existing names.
        The header can be a list of integers that specify row locations
        for a multi-index on the columns e.g. [0,1,3].
        
        This parameter ignores commented lines and empty lines if
        skip_blank_lines=True (not included in the arguments for simplicity),
        so header=0 denotes the first line of data
        rather than the first line of the file.
          
    Returns
    -------
    new_df : pandas.Dataset
        Text file converted to a data frame.
    """
     
    df = pd.read_table(file_path,
                       engine=engine,
                       encoding=encoding,
                       header=header,
                       sep=separator,
                       dtype=dtype)
    return df


# Microsoft Excel spreadsheets #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

def excel_handler(file_path, 
                  sheet_name=None,
                  header=None,
                  engine=None,
                  decimal='.', 
                  return_obj_type='dict'):
    
    """
    Reads an Excel file and processes its sheets either into a 
    dictionary of DataFrames or a single merged DataFrame.

    Parameters:
    -----------
    file_path : str
        Path to the Excel file.
    sheet_name : str, int, list, or None, default 0
        Strings are used for sheet names. Integers are used in zero-indexed
        sheet positions (chart sheets do not count as a sheet position).
        Lists of strings/integers are used to request multiple sheets.
        Specify ``None`` to get all worksheets.
    header : int, list of int, default None
        Row (0-indexed) to use for the column labels of the parsed DataFrame.
    engine : {'openpyxl', 'calamine', 'odf', 'pyxlsb', 'xlrd'}, default None
        Engine to use for reading Excel files. If None, defaults to the 
        appropriate engine for the file type.
    decimal : str, default '.'
        Character to recognize as decimal point (e.g., ',' in Europe).
    return_obj_type : str, default 'dict'
        Type of output to return. Must be either 'dict' to return a dictionary
        of DataFrames, or 'df' to return a single merged DataFrame.

    Returns:
    --------
    dict or pd.DataFrame
        If 'return_type' is 'dict', returns a dictionary where keys are
        sheet names and values are DataFrames.
        If 'return_type' is 'df', returns a single DataFrame
        with data from all sheets merged.

    Raises:
    -------
    TypeError
        If 'return_type' is not 'dict' or 'df'.

    Example usage:
    --------------
    result_dict = excel_handler('file_path.xlsx', return_type='dict')
    result_df = excel_handler('file_path.xlsx', return_type='df')
    """
    
    # Validate the return type argument #
    if return_obj_type not in excel_handling_return_options:        
        raise TypeError("Invalid type of the object to return. "
                        f"Choose one from {excel_handling_return_options}.")

    else:
        sheetname_and_data_dict = pd.read_excel(file_path,
                                                sheet_name=sheet_name,
                                                header=header,
                                                engine=engine,
                                                decimal=decimal)
    
        if return_obj_type == 'dict':
            polished_sheetname_and_val_dict = {}
            for sheet_name, sheet_df in sheetname_and_data_dict.items():
                df_polished_colnames = polish_df_column_names(sheet_name, sheet_df)
                indiv_polished_dict = {sheet_name: df_polished_colnames}
                polished_sheetname_and_val_dict.update(indiv_polished_dict)
            return polished_sheetname_and_val_dict
    
        elif return_obj_type == 'df':
            all_value_df = pd.DataFrame()
            for sheet_name, sheet_df in sheetname_and_data_dict.items():
                df_polished_colnames = polish_df_column_names(sheet_name, sheet_df)
                all_value_df = pd.concat([all_value_df, df_polished_colnames])
                
            all_value_df.reset_index(inplace=True, drop=True)
            all_value_df = all_value_df.drop(columns=['sheet'])
            return all_value_df



def save2excel(file_path,
               frame_obj,
               indiv_sheet_name="Sheet1",
               save_index=False,
               save_header=False,
               engine="xlsxwriter"):
    
    """
    Save a DataFrame or a dictionary of DataFrames to an Excel file with separate sheets.

    Parameters
    ----------
    file_path : str
        Path to the Excel file where data will be saved.
    frame_obj : dict or pandas.DataFrame
        Data to be saved to the Excel file. If a dictionary is provided,
        keys are used as sheet names and values as DataFrames.
        If a single DataFrame is provided, it will be saved to one sheet.
    indiv_sheet_name : str, optional
        Name of the sheet to give when 'frame_obj' is a single DataFrame.
        Default is "Sheet1".
    save_index : bool, optional
        Whether to include the DataFrame index as a column in the Excel sheet. Default is False.
    save_header : bool, optional
        Whether to include the DataFrame column headers in the Excel sheet. Default is False.
    engine : {'openpyxl', 'xlsxwriter'}, optional
        The engine to use for writing to the Excel file. Default is "xlsxwriter".

    Returns
    -------
    int
        Always returns 0 to indicate successful execution.

    Examples
    --------
    Save a single DataFrame to an Excel file:
    
    >>> df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    >>> save2excel("output.xlsx", df)

    Save multiple DataFrames to an Excel file with custom sheet names:
    
    >>> dfs = {"Sheet1": pd.DataFrame({"A": [1, 2]}), "Sheet2": pd.DataFrame({"B": [3, 4]})}
    >>> save2excel("output.xlsx", dfs)
    """
    
    # Get the file path's components #
    #--------------------------------#
    
    # Extension #
    """
    There can be some times in which the file does not have any extension,
    as a result of any other manipulation with any of the modules of this package.
    If so, Excel file extension is automatically added.
    """
    file_ext = get_obj_specs(file_path, obj_spec_key="ext")
    lne = len(file_ext)
    
    if lne == 0:
        file_path = ext_adder(file_path, extensions[1])
    
    # Name and parent #
    file_name = get_obj_specs(file_path, obj_spec_key="name")
    fn_parent = get_obj_specs(file_path, obj_spec_key="parent")
    
    # Check if the file already exists #
    #----------------------------------#
    
    file_already_exists\
    = bool(len(find_files_by_globstr(file_name, 
                                     fn_parent,
                                     top_path_only=True)))
    
    # Save the file according to the input data type #
    #------------------------------------------------#
    
    if isinstance(frame_obj, dict):
        writer = pd.ExcelWriter(file_path, engine=engine)
        
        for sheet, frame in frame_obj.items():
            frame.to_excel(writer,
                           sheet_name=sheet,
                           index=save_index,
                           header=save_header)
            
        # If the file to be created already exists, prompt to overwrite it #    
        if file_already_exists:
            arg_list_file_exists = [file_name, fn_parent]
            overwrite_stdin\
            = input(format_string(already_existing_file_warning, arg_list_file_exists))
            
            while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                overwrite_stdin = input(overwrite_prompt_warning)
            else:  
                # In this case, save the file directly
                if overwrite_stdin == "y":
                    writer.close() 
                    return 0
                else:
                    pass
        
        # Else, save it directly #
        else:
            writer.close()
            return 0


    elif isinstance(frame_obj, pd.DataFrame):
        
        # If the file to be created already exists, prompt to overwrite it #    
        if file_already_exists:
            arg_list_file_exists = [file_name, fn_parent]
            overwrite_stdin\
            = input(format_string(already_existing_file_warning, arg_list_file_exists))
            
            while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                overwrite_stdin = input(overwrite_prompt_warning)
            else:
                # If chosen to overwrite, data cannot be directly overriden.
                # Instead, delete the original file and create a new one
                # of the same name with the new data
                if overwrite_stdin == "y":
                    remove_files_by_globstr(file_path, fn_parent)
                    frame_obj.to_excel(file_path, 
                                       sheet_name=indiv_sheet_name,
                                       index=save_index,
                                       header=save_header)
                    return 0
                else:
                    pass
          
        # Else, save it directly #
        else:
            frame_obj.to_excel(file_path, save_index, save_header)
            return 0
        
    else:
        raise ValueError("Unsupported type of frame. "
                         "It must either be of type 'dict' or 'pandas.DataFrame'.")
        

def merge_excel_files(input_file_list,
                      output_file_path,
                      header=None,
                      engine=None,
                      decimal=".",
                      save_index=False,
                      save_header=False,
                      save_merged_file=False):
    """
    Merge data from multiple Excel files into a single Excel file or dictionary.

    Parameters
    ----------
    input_file_list : str or list of str
        Path or paths of the input Excel file(s) to be merged.
    output_file_path : str
        Path or name of the output Excel file. If 'save_merged_file' is False,
        this parameter is ignored.
    header : int, list of int, default None
        Row (0-indexed) to use for the column labels of the parsed DataFrame.
        If a list of integers is passed, those row positions will be combined
        into a ``MultiIndex``. Use None if there is no header.
    engine : str or sqlalchemy.engine.base.Engine, optional
        SQLAlchemy engine or connection string for connecting to database files.
    decimal : str, default '.'
        Character recognized as decimal separator.
    save_index : bool, default False
        Whether to include a column in the output Excel file that identifies row numbers.
    save_header : bool, default False
        Whether to include a row in the output Excel file that identifies column numbers.
    save_merged_file : bool, default False
        Whether to save the merged data as an Excel file.

    Returns
    -------
    int or dict
        If 'save_merged_file' is True, returns 0 to indicate successful file saving.
        If 'save_merged_file' is False, returns a dictionary containing DataFrames
        with merged data, separated by file names.

    Raises
    ------
    ValueError
        If 'input_file_list' contains only one file.

    Notes
    -----
    If multiple files contain sheets with identical names, the method appends
    the original file name to the sheet names to avoid key conflicts
    in the output dictionary.
    """
    
    # Quality control section #
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
        
    lifn = len(input_file_list)    
    if lifn == 1:
        raise ValueError(below_minimum_file_warning)
        
    # For simplicity and convenience, even if any file has only one sheet, 
    # follow the natural behaviour, that is, conserving the key containing
    # object as a list, instead of indexing to an integer
    all_file_sheetname_list_of_lists = [list(excel_handler(file, 
                                                           engine=engine,
                                                           return_type='dict').keys())
                                        for file in input_file_list]
    
    
    """
    Handle duplicated sheet names, if any, by adding the corresponding
    file name after it. Otherwise, because in a dictionary cannot appear
    repeated keys, the information pertaining to the second key and beyond,
    among the duplicated ones, will be lost.
        
    For example, if the previous instruction gives a list of lists 
    like the following one:
        
    [['sheet1', 'test_sheet'], ['sheet1', 'savings']]
    
    To identify the duplicated names, as well as remembering which
    file do they correspond to:
    
    - Each individual list corresponds to the sheets contained in a file,
      which will be identified as a key.
    - A first index is necessary to idenfity which file does the potentially
      duplicated element correspond to, i.e. the position of the individual list.
    - Another index serves to locate the duplicated element within the
      mentioned individual list and modify its name.
      * The previous two indices will be contained in a tuple.
      * Because duplicated elements appear minimum twice,
        there will be more than one tuple, contained in a list,
        in order to preserve performance.
      
    The application of the method results in a dictionary as follows:
    res_dict = {'sheet1' : [(0,0), (1,0)]}
    
    In this case, the repeated key is 'sheet1', which appears in the sheets
    of the first and second file (first indices 0 and 1, respectively),
    and that sheet name is located in the first position for both files
    (second index 0 in both cases).
    """
    duplicated_sheetname_index_dict = find_duplicated_elements(all_file_sheetname_list_of_lists)
    ldsid = len(duplicated_sheetname_index_dict)
    if ldsid > 0:
        for sheet_name in list(duplicated_sheetname_index_dict.keys()):
            index_tuple_list = duplicated_sheetname_index_dict[sheet_name]
            for tupl in index_tuple_list:
                new_sheet_name = f"{sheet_name}_{input_file_list[tupl[0]]}"
                all_file_sheetname_list_of_lists[tupl[0]][tupl[1]] = new_sheet_name
        
    all_file_sheetname_list_of_lists = [lst[i] 
                                        for lst in all_file_sheetname_list_of_lists
                                        for i in range(len(lst))]
    

    # Gather data #     
    all_file_data_dict = {file_sheetname : excel_handler(file, 
                                                         header=header,
                                                         engine=engine, 
                                                         decimal=decimal,
                                                         return_type='dict')
                          for file_sheetname, file in zip(all_file_sheetname_list_of_lists, 
                                                          input_file_list)}

    # File saving 
    if save_merged_file:
        saving_result = save2excel(output_file_path,
                                   all_file_data_dict, 
                                   save_index=save_index, 
                                   save_header=save_header)
        return saving_result
     
    else:
        return all_file_data_dict
        

# CSV files #
#-#-#-#-#-#-#

def save2csv(file_path,
             data_frame,
             separator=',',
             save_index=False,
             save_header=False,
             decimal=".",
             date_format=None):
    """
    Save a DataFrame to a CSV file.

    Parameters
    ----------
    file_path : str
        Path of the output CSV file.
    data_frame : pandas.DataFrame
        DataFrame containing the data to be saved.
    separator : str, default ','
        String used to separate data columns.
    save_index : bool, default False
        Whether to include a column in the CSV file that identifies row numbers.
    save_header : bool, default False
        Whether to include a row in the CSV file that identifies column names.
    decimal : str, default '.'
        Character recognized as the decimal separator.
    date_format : str, optional
        Format string for datetime columns.

    Returns
    -------
    int
        Returns 0 to indicate successful execution.

    Raises
    ------
    TypeError
        If 'data_frame' is not of type 'pandas.DataFrame'.

    Notes
    -----
    - This method is designed to work with simple CSV files, typically with only one sheet.
    - If 'file_path' does not have a file extension, '.csv' is automatically appended to it.
    - If the specified file already exists, the method prompts to confirm overwrite before saving.
    """

    
    if isinstance(data_frame, pd.DataFrame):
        
        # Get the file path's components #
        #--------------------------------#
        
        # Extension #
        """
        There can be some times in which the file does not have any extension,
        as a result of any other manipulation with any of the modules of this package.
        If so, Excel file extension is automatically added.
        """
        
        file_ext = get_obj_specs(file_path, obj_spec_key="ext")
        lne = len(file_ext)
        
        if lne == 0:
            file_path = ext_adder(file_path, extensions[0])
        
        
        # Name and parent #
        file_name = get_obj_specs(file_path, obj_spec_key="name")
        fn_parent = get_obj_specs(file_path, obj_spec_key="parent")
        
        # Check if the file already exists #
        #----------------------------------#
        
        file_already_exists\
        = bool(len(find_files_by_globstr(file_name, 
                                         fn_parent,
                                         top_path_only=True)))
        
        # Save the file according to the input data type #
        #------------------------------------------------#
        
        if date_format is None:
            
            # If the file to be created already exists, prompt to overwrite it #  
            if file_already_exists:
                arg_list_file_exists = [file_name, fn_parent]
                overwrite_stdin\
                = input(format_string(already_existing_file_warning, arg_list_file_exists))
                
                while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                    overwrite_stdin = input(overwrite_prompt_warning)
                else:
                    # If chosen to overwrite, data cannot be directly overriden.
                    # Instead, delete the original file and create a new one
                    # of the same name with the new data
                    if overwrite_stdin == "y":
                        remove_files_by_globstr(file_path, fn_parent)
                        data_frame.to_csv(file_path,
                                          sep=separator,
                                          decimal=decimal,
                                          index=save_index,
                                          header=save_header)
                        return 0
                    else:
                        pass
                
            # Else, save it directly #
            else:
                data_frame.to_csv(file_path,
                                  sep=separator,
                                  decimal=decimal,
                                  index=save_index,
                                  header=save_header)
                return 0
                
            
        else:
            # If the file to be created already exists, prompt to overwrite it #  
            if file_already_exists:
                arg_list_file_exists = [file_name, fn_parent]
                overwrite_stdin\
                = input(format_string(already_existing_file_warning, arg_list_file_exists))
                
                while (overwrite_stdin != "y" and overwrite_stdin != "n"):
                    overwrite_stdin = input(overwrite_prompt_warning)
                else:
                    # If chosen to overwrite, data cannot be directly overriden.
                    # Instead, delete the original file and create a new one
                    # of the same name with the new data
                    if overwrite_stdin == "y":
                        remove_files_by_globstr(file_path, fn_parent)
                        data_frame.to_csv(file_path,
                                          sep=separator,
                                          decimal=decimal,
                                          date_format=date_format,
                                          index=save_index,
                                          header=save_header)
                        return 0                        
                    else:
                        pass
                
            # Else, save it directly #
            else:
                data_frame.to_csv(file_path,
                                  sep=separator,
                                  decimal=decimal,
                                  date_format=date_format,
                                  index=save_index,
                                  header=save_header)
                return 0
            
    else:        
        input_obj_type = get_obj_type_str(data_frame)
        raise TypeError(format_string(unsupported_obj_type_err_str, input_obj_type))
        
        
    
def csv2df(file_path,
           separator=None,
           engine="python",
           encoding=None,
           header='infer',
           parse_dates=False,
           index_col=None,
           decimal="."):
    
    
    """
    Function that loads a CSV file and loads the content
    into a Pandas DataFrame to a CSV file.
    
    Parameters
    ----------
    file_path : str
        Path of the file to evaluate.
    sep : str, default None
        Character or regex pattern to treat as the delimiter. If ``sep=None``, the
        C engine cannot automatically detect
        the separator, but the Python parsing engine can, meaning the latter will
        be used and automatically detect the separator from only the first valid
        row of the file by Python's builtin sniffer tool, ``csv.Sniffer``.
        In addition, separators longer than 1 character and different from
        ``'\s+'`` will be interpreted as regular expressions and will also force
        the use of the Python parsing engine. Note that regex delimiters are prone
        to ignoring quoted data. Regex example: ``'\r\t'``.
    engine : {'c', 'python', 'pyarrow'}, default 'python'
        Parser engine to use. The C and pyarrow engines are faster, 
        while the python engine is currently more feature-complete. 
        Multithreading is currently only supported by the pyarrow engine.
        Defaults to None.
    encoding : str
        Encoding to use for UTF when reading or writing.
        When this is 'None', 'errors="replace"' is passed to 'open()'; 
        technically no encoding is used.
        Otherwise, 'errors="strict"' is passed to 'open()'.
    header : int, list of int, str or NoneType
        Row number(s) to use as the column names, and the start of the
        data. Default behaviour is to infer the column names: if no names
        are passed the behaviour is identical to 'header=0' and column
        names are inferred from the first line of the file, if column
        names are passed explicitly then the behaviour is identical to
        'header=None'. Explicitly pass 'header=0' to be able to
        replace existing names.
    parse_dates : bool or list of int or names or list of lists or dict, default False
        The behaviour is as follows:
            * boolean. If True -> try parsing the index.
            * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3
              each as a separate date column.
            * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as
              a single date column.
            * dict, e.g. {'foo' : [1, 3]} -> parse columns 1, 3 as date and call
              result 'foo'
    
    index_col : int, str, sequence of int / str, False or NoneType
        Column(s) to use as the row labels of the 'DataFrame', either given as
        string name or column index. If a sequence of int / str is given, a
        MultiIndex is used.
    decimal : str, default '.'
        Character to recognize as decimal point for parsing string columns to numeric.
        Note that this parameter is only necessary for columns stored as TEXT in Excel,
        any numeric columns will automatically be parsed, regardless of display
        format (e.g. use ',' for European data).      
        
    Returns
    -------
    df : pandas.DataFrame
        Single DataFrame containing data of the CSV file, molded according to
        the reading parameters.
    """

    df = pd.read_csv(file_path, 
                     sep=separator,
                     decimal=decimal,
                     encoding=encoding,
                     header=header,
                     engine=engine,
                     parse_dates=parse_dates,
                     index_col=index_col)    
    return df


def merge_csv_files(input_file_list, 
                    output_file_path,
                    separator_in=None,
                    separator_out=";",
                    engine="python",
                    encoding=None,
                    header='infer',
                    parse_dates=False,
                    index_col=None,
                    decimal=",",                                 
                    save_index=False,
                    save_header=False,
                    out_single_DataFrame=True,
                    keep_data_in_sections=False,
                    save_merged_file=False):

    """
    Merges several CSV files' data into a single one.

    Two options are given:
        1. Merge data of each file into a single DataFrame.
        2. Do not concatenate all DataFrames, but store them separately
           with their corresponding file in a dictionary.
           
    Parameters
    ----------
    input_file_list : str or list of str
        Path or paths of the files to be examined.   
        Each of them can be names or relative paths.
    output_file_path: str
        Name or path of the output file. It can either be a name or relative path.
    separator_in : str, default None
        Character or regex pattern to treat as the delimiter. If ``sep=None``, the
        C engine cannot automatically detect
        the separator, but the Python parsing engine can, meaning the latter will
        be used and automatically detect the separator from only the first valid
        row of the file by Python's builtin sniffer tool, ``csv.Sniffer``.
        In addition, separators longer than 1 character and different from
        ``'\s+'`` will be interpreted as regular expressions and will also force
        the use of the Python parsing engine. Note that regex delimiters are prone
        to ignoring quoted data. Regex example: ``'\r\t'``.        
    separator_out : str, default ';'
        Delimiter to use for the output file.    
    engine : {'c', 'python', 'pyarrow'}, default 'python'
        Parser engine to use. The C and pyarrow engines are faster, 
        while the python engine is currently more feature-complete. 
        Multithreading is currently only supported by the pyarrow engine.
        Defaults to None.
    encoding : str
        String that identifies the encoding to use for UTF
        when reading/writing.
        Default value is 'utf-8' but it can happen that
        the text file has internal strange characters that
        UTF-8 encoding is not able to read.
        In such cases "latin1" is reccommended to use.
   
    header : int, list of int, None, default 'infer'
        Row number(s) to use as the column names, and the start of the data.
        Default behaviour is to infer the column names: if no names are passed
        the behaviour is identical to header=0 and column names are inferred
        from the first line of the file.
        
        If column names are passed explicitly then the behaviour
        is identical to header=None, where the text file's header
        are only column names.
        
        Explicitly pass header=0 to be able to replace existing names.
        The header can be a list of integers that specify row locations
        for a multi-index on the columns e.g. [0,1,3].
        
        This parameter ignores commented lines and empty lines if
        skip_blank_lines=True (not included in the arguments for simplicity),
        so header=0 denotes the first line of data
        rather than the first line of the file.
        
    parse_dates : bool or list of int or names or list of lists or dict, default False
        The behaviour is as follows:
            * boolean. If True -> try parsing the index.
            * list of int or names. e.g. If [1, 2, 3] -> try parsing columns 1, 2, 3
              each as a separate date column.
            * list of lists. e.g.  If [[1, 3]] -> combine columns 1 and 3 and parse as
              a single date column.
            * dict, e.g. {'foo' : [1, 3]} -> parse columns 1, 3 as date and call
              result 'foo'
    
    index_col : int, str, sequence of int / str, False or NoneType
        Column(s) to use as the row labels of the 'DataFrame', either given as
        string name or column index. If a sequence of int / str is given, a
        MultiIndex is used.
    decimal : str
        Character to recognize as decimal point (e.g. use ',' 
        for European data). Default value is ',' (comma).    
    save_index : bool, optional
        Whether to include the DataFrame index as a column in the Excel sheet. Default is False.
    save_header : bool, optional
        Whether to include the DataFrame column headers in the Excel sheet. Default is False.
    out_single_DataFrame : bool, default True
        Determines whether to save all DataFrames into a single one,
        concatenating all of them.
        The counterpart is that if not all of them have the same number
        of rows, the concatenation results in NaN filling.
    keep_data_in_sections : bool, default False
        If chosen, instead of concatenating all DataFrames, each one
        is stored in a dictionary, with the original file name 
        (without the relative path) being the key.
    save_merged_file : bool, default False
        Determines to save the object returned by the choice of the
        previous two arguments.
    
    Returns
    -------
    int
        Irrespective of 'out_single_DataFrame' and/or 'keep_data_in_sections'
        being True or False, if 'save_merged_file', 
        always returns 0 to indicate successful execution.
    all_file_data_df : pandas.DataFrame
        If 'out_single_DataFrame' is set to True, 
        (while 'keep_data_in_sections' to False)
        and 'save_merged_file' to False, the concatenated DataFrame is returned.
    all_file_data_dict : dict
        If 'keep_data_in_sections' is set to True 
        (while 'out_single_DataFrame' to False)
        and 'save_merged_file' to False, the dictionary with DataFrames
        separated by files as keys is returned.
        
    Notes
    -----   
    Usage of 'separator_in' applies for all files, which means
    that every file must have the same separator.
    In order to keep simplicity and practicality, 'out_single_DataFrame'
    and 'keep_data_in_sections' cannot be True at the same time.
    """
        
    # Proper argument selection control # 
    #-----------------------------------#
    
    # Data merging #
    all_arg_names = get_caller_method_args()
    kdis_arg_pos = find_substring_index(all_arg_names, "keep_data_in_sections")
    osd_arg_pos = find_substring_index(all_arg_names, "out_single_DataFrame")
    
    if out_single_DataFrame and keep_data_in_sections:
        raise ValueError(f"Arguments '{all_arg_names[kdis_arg_pos]}' and "
                         f"'{all_arg_names[osd_arg_pos]}' cannot be True at the same time. "
                         "Set one of them True and False the other one.")
    
    # Correct number of input files #
    if isinstance(input_file_list, str):
        input_file_list = [input_file_list]
        
    lifn = len(input_file_list)
    
    if lifn == 1:
        raise ValueError(below_minimum_file_warning)
        
    # Option 1: merge data of all files into a single DataFrame #
    #-----------------------------------------------------------#
    
    if out_single_DataFrame and not keep_data_in_sections:
        
        # Check firstly if all data frames have the same number of columns 
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        
        ind_file_df_nrow_list = []    
        for file in input_file_list:
            file_df = csv2df(separator=separator_in,
                             engine=engine,
                             encoding=encoding,
                             header=header,
                             parse_dates=parse_dates,
                             index_col=index_col,
                             decimal=decimal)
            
            file_df_shape = file_df.shape
            ind_file_df_nrow_list.append(file_df_shape[0])
            
        ind_file_df_nrow_unique = unique(ind_file_df_nrow_list)
        lifdnu = len(ind_file_df_nrow_unique)
        
        # If not the case, warn respectively and prompt to merge anyway #
        if lifdnu > 1:
            merge_anyway_stdin = input("Warning: number of rows of data in some files "
                                       "is not common to all data. "
                                       "Mergeing resulted in concatenation by "
                                       "filling the missing values with NaNs. "
                                       "Proceed anyway? (y/n) ")
            
            
            while (merge_anyway_stdin != "y" and merge_anyway_stdin != "n"):
                merge_anyway_stdin = input("\nPlease select 'y' for 'yes' "
                                           "or 'n' for 'no': ")
                
            else:  
                # Merge now all DataFrames into a single one #
                if merge_anyway_stdin == "y":
                    all_file_data_df = concat_dfs_aux(input_file_list,
                                                      separator_in,
                                                      engine,
                                                      encoding,
                                                      header,
                                                      parse_dates,
                                                      index_col,
                                                      decimal)
                else:
                    pass
                
                
             
        # Otherwise merge all DataFrames into a single one directly #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
        
        else:
            all_file_data_df = concat_dfs_aux(input_file_list,
                                              separator_in,
                                              engine,
                                              encoding,
                                              header,
                                              parse_dates,
                                              index_col,
                                              decimal)
            
        # Prompt to save the merged object #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        
        if save_merged_file:
           saving_result = save2csv(output_file_path, 
                                    all_file_data_df, 
                                    separator=separator_out,
                                    decimal=decimal,
                                    save_index=save_index, 
                                    save_header=save_header)
           return saving_result
            
        else:
            return all_file_data_df
        
        
    # Option 2: save each DataFrame with the corresponding file into a dictionary #
    #-----------------------------------------------------------------------------#
        
    elif not out_single_DataFrame and keep_data_in_sections:
        all_file_data_dict = \
            {get_obj_specs(file,"name_noext") : csv2df(separator=separator_in,
                                                       engine=engine,
                                                       encoding=encoding,
                                                       header=header,
                                                       parse_dates=parse_dates,
                                                       index_col=index_col,
                                                       decimal=decimal)
             for file in input_file_list}
        
        # Prompt to save the merged object #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        
        # Because there is no 'sheet' concept, in case of saving the dictionary
        # it must be done so in an Excel file, not a CSV file
        
        if save_merged_file:
            saving_result = save2excel(output_file_path,
                                       all_file_data_dict, 
                                       save_index=save_index, 
                                       save_header=save_header)
            return saving_result
         
        else:
            return all_file_data_dict
        
        
    
def concat_dfs_aux(input_file_list,
                   separator_in,
                   engine,
                   encoding, 
                   header, 
                   parse_dates, 
                   index_col, 
                   decimal):
    
    all_file_data_df = pd.DataFrame()
    for file in input_file_list:
        file_df = csv2df(separator=separator_in,
                         engine=engine,
                         encoding=encoding,
                         header=header,
                         parse_dates=parse_dates,
                         index_col=index_col,
                         decimal=decimal)
        
        all_file_data_df = pd.concat([all_file_data_df, file_df], axis=1)
    return all_file_data_df
    

# ODS files #
#-#-#-#-#-#-#

def ods_handler(file_path, 
                sheet_name=None,
                header=None,
                decimal='.', 
                return_type='dict'):
    
    """
    Reads a LibreOffice Calc file and processes its sheets either into a 
    dictionary of DataFrames or a single merged DataFrame.
    
    In either case, it calls the 'excel_handler' method, because the only
    difference is the engine called, 'odf', from 'odfpy' library.
    Then this method inherits every functionalities from the mentioned one.

    Parameters:
    -----------
    file_path : str
        Path to the Excel file.
    sheet_name : str, int, list, or None, default 0
        Strings are used for sheet names. Integers are used in zero-indexed
        sheet positions (chart sheets do not count as a sheet position).
        Lists of strings/integers are used to request multiple sheets.
        Specify ``None`` to get all worksheets.
    header : int, list of int, default None
        Row (0-indexed) to use for the column labels of the parsed DataFrame.
    decimal : str, default '.'
        Character to recognize as decimal point (e.g., ',' in Europe).
    return_type : str, default 'dict'
        Type of output to return. Must be either 'dict' to return a dictionary
        of DataFrames, or 'df' to return a single merged DataFrame.

    Returns:
    --------
    dict or pd.DataFrame
        If 'return_type' is 'dict', returns a dictionary where keys are
        sheet names and values are DataFrames.
        If 'return_type' is 'df', returns a single DataFrame
        with data from all sheets merged.

    Raises:
    -------
    TypeError
        If 'return_type' is not 'dict' or 'df'.
    """
    
    # Common keyword argument dictionary #
    kwargs = dict(
        sheet_name=sheet_name,
        header=header, 
        engine="odf", 
        decimal=decimal
        )
    
    # Case studies #
    if return_type == 'dict':
        item_dict = excel_handler(file_path,
                                  **kwargs, 
                                  return_type='dict')        
        return item_dict
    
    elif return_type == 'df':
        all_data_df = excel_handler(file_path,
                                    **kwargs,
                                    return_type='df')
        return all_data_df   
    
    

def save2ods(file_path,
             frame_obj,
             indiv_sheet_name="Sheet1",
             save_index=False,
             save_header=False,
             engine="odf"):
    
    saving_result = save2excel(file_path,
                               frame_obj,
                               indiv_sheet_name=indiv_sheet_name,
                               save_index=save_index,
                               save_header=save_header,
                               engine=engine)    
    return saving_result
    

def merge_ods_files(input_file_list,
                    output_file_path,
                    save_index=False,
                    save_header=False,
                    save_merged_file=False):
    
    saving_result = merge_excel_files(input_file_list,
                                      output_file_path,
                                      save_index=save_index,
                                      save_header=save_header,
                                      save_merged_file=save_merged_file)
    return saving_result


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


#--------------------------#
# Parameters and constants #
#--------------------------#

# File extension list #
extensions = ["csv", "xlsx"]

# String splitting character #
splitdelim = common_delim_list[4]

# Time span shortands #
time_kws = ["da", "fe", "tim", "yy"]

# Preformatted strings #
#----------------------#

already_existing_file_warning = """Warning: file '{}' at directory '{}' \
already exists.\nDo you want to overwrite it? (y/n) """

# Warning strings #
#-----------------#

overwrite_prompt_warning = "\nPlease select 'y' for 'yes' or 'n' for 'no': "
below_minimum_file_warning = """At least 2 files must be given \
in order to perform the merge."""

# Error strings #
#---------------#

unsupported_obj_type_err_str = "Expected a pandas.DataFrame object, got {}"

# Argument choice options #
#-------------------------#

excel_handling_return_options = ["dict", "df"]
