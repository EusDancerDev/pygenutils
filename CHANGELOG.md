# pygenutils Changelog

All notable changes to this project will be documented in this file.

---

## [v15.7.7] - 2025-02-18

### Changed

**General**

- For all relevant modules, perform several term replacements:
    - Replace `method` with `procedure` to more accurately describe the approach or technique used in functions, except when referring to class method calls.
    - Replace `action` with `procedure` to align with the context of operations being performed.
    Additionally, these changes improve clarity by ensuring consistent terminology, making it clear that functions can employ different procedures to achieve their goals.

These changes enhance terminology consistency in all affected modules. No user-facing changes are expected, hence only the patch number is incremented.

---

## [v15.7.0] - 2025-02-03

### Added

**Number Bases**

- Module `base_converters`:
	- Added helper function `_check_input_binary` to check if the input binary number is in the correct format.
	- Introduce two basic functions to convert between base 10 and base 2: `dec2bin_basic` and `bin2dec_basic`. Both perform mathematical computations by definition.

**Arrays and Lists**

- Module `data_manipulation`: add flipping utilities of lists and NumPy arrays with N >= 1 dimensions.

### Changed

**General**

- Peform several term replacements in many modules:
	- `method` with `function`, if no object is instantiated throughout the module.
	- `method` with `procedure` (or `algorithm`/`module`), to more accurately describe the approach or technique used in functions.
	Additionally, this change effectively communicates that a function can employ different methods or techniques to achieve its goal.

---

## [v15.6.0] - 2024-12-18

### Changed

**Strings**

- Module `string_handler`: enhanced substring search logic: returns single data object for one match, (-1, -1) for no matches, and enforces {"lo", "hi", "both"} for index return options.

---

## [v15.5.0] - 2024-11-23

### Changed

**Arrays and Lists**

- Module `data_manipulation`: enhance `remove_elements` function to support multiple indices for list inputs.

**Time Handling**

- Module `calendar_utils`: corrected the absolute path in the import of the `unique_type_objects` function.
---

## [v15.4.4] - 2024-11-17

### Changed

**General**

- Minor syntax appearance improvements in many modules.

**Strings**

- Renamed module `information_output_formatters` to `text_formatters` for improved clarity. Changes have been applied for all affected modules.

**Time Handling**

- Module `date_and_time_utils`:
	- Added timezone handling to `get_current_datetime` function with optional 'pytz' support
	- Added `display_user_timestamp` function with conditional timezone support.
	- Enhanced module with global timezone handling using a `pytz` availability check.
	- Minor refactoring and structure reorganization for improved modularity.

---

## [v15.3.0] - 2024-11-14

### Changed

**Web Scraping**

- Renamed the sub-pakcage to `web_automation` for broader web automation use.
- After performing the operation, moved it from `pygenutils` package to `DataOpsHub` package.

---

## [v15.2.0] - 2024-11-03

### Added

- Added `__init__.py` files to all first-level and deeper sub-packages for enhanced import access.

### Changed

- Remove the redundant import of the deprecated and removed `parameters_and_constants` module in all affected modules.

---

## [v15.0.0] - 2024-10-30

### Changed

- Current package `pyutils` has been renamed to `pygenutils` to align with the purpose of being a general-tool, Swiss army knife.

- The following sub-packages have been moved out to form separate packages as their own:
	- `climalab`
 	- `geosptools`
	- `filewise`
	- `LinguaLab`
	- `paramlib`
	- `statkit`
	- `test-base_programs`
		- Will not be a candidate to release, as it consists of programs for testing code snippets
		
	- The following sub-packages form a new package:
		- `data_entry_forms` |
		- `databases`        | <span>&#8594;</span> `DataOpsHub`
		- `security`         |
		
- Once all above changes made, absolutely all imports have been updated to match the package where a sub-package or module is.

---

## [v14.0.0] - 2024-10-28

### Changed

<h3>Changes in functions along modules and sub-packages</h3>

**Varnames**
- Variable name `all_arg_names`, which contains all variables (required and optional) of the caller function, has been renamed to `param_keys`.
	- All this changes have been applied to all affected modules.

<h3>Specific changes regarding sub-packages</h3>

**Dictionaries**
- Module `table_formatters`:
	- Moved all functions to the module `information_output_formatters` (**Strings** sub-package)

**General File Utils**
- Module `introspection_utils`:
	- Renamed the following functions:
	<table>
		<thead>
			<tr>
				<th>Original Function Name</th>
				<th>Refactored Function Name</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>retrieve_function_name</td>
				<td>get_func_name</td>
			</tr>
			<tr>
				<td>get_function_args</td>
				<td>get_func_args</td>
			</tr>
			<tr>
				<td>get_function_all_args</td>
				<td>get_all_func_args</td>
			</tr>
			<tr>
				<td>get_full_function_signature</td>
				<td>get_func_signature</td>
			</tr>
			<tr>
				<td>get_caller_function_args</td>
				<td>get_caller_args</td>
			</tr>
			<tr>
				<td>get_caller_function_all_args</td>
				<td>get_all_caller_args</td>
			</tr>
			<tr>
				<td>get_full_caller_function_signature</td>
				<td>get_caller_signature</td>
			</tr>
			<tr>
				<td>get_attribute_names</td>
				<td>get_attr_names</td>
			</tr>
			<tr>
				<td>get_obj_type_str</td>
				<td>get_type_str</td>
			</tr>
		</tbody>
	</table>

- All this changes have been applied to all affected modules.

**Format Converters**
- Module `file_format_tweaker`:
	- Renamed the following functions:
	<table>
		<thead>
			<tr>
				<th>Old function name</span></th>
				<th>New function name</span></th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>check_essential_prog_installation</td>
				<td>_check_essential_progs (marked as internal)</td>
			</tr>
			<tr>
				<td>pdf_file_tweaker</td>
				<td>file_tweaker</td>
			</tr>
			<tr>
				<td>pdf_file_compressor</td>
				<td>file_compressor</td>
			</tr>
			<tr>
				<td>merge_pdf_files</td>
				<td>merge_files</td>
			</tr>
			<tr>
				<td>eml2pdf</td>
				<td>eml_to_pdf</td>
			</tr>
			<tr>
				<td>msg2pdf</td>
				<td>msg_to_pdf</td>
			</tr>
		</tbody>
	</table>

- All this changes have been applied to all affected modules.
- After having these changes made, the module has been **renamed** to `pdf_tools`.

**Operative systems**
- Module `OS Operations`
	- In function `run_system_command`, default value of argument `encoding` was changed from `None` to `utf-8`.
		- This change has been applied in every affected module.

**Strings**
- Module `string_handler`: Renamed the following functions:
<table>
	<thead>
		<tr>
			<th>Old function name</span></th>
			<th>New function name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>add_str_to_path</td>
			<td>add_to_path</td>
		</tr>
		<tr>
			<td>ext_adder</td>
			<td>append_ext</td>
		</tr>
	</tbody>
</table>

- All this changes have been applied to all affected modules.

<h3>Changes in **sub-package** names</h3>
- The following renamings have been performed:
<table>
	<thead>
		<tr>
			<th>Old package name</span></th>
			<th>New package name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>geospatial_tools</td>
			<td>geosptools</td>
		</tr>
		<tr>
			<td>parameters_and_constants</td>
			<td>paramlib</td>
		</tr>
		<tr>
			<td>multilingual_text_processing</td>
			<td>LinguaLab</td>
		</tr>
	</tbody>
</table>

---

## [v13.3.2] - 2024-10-25 

### Changed

<h3>Changes in functions along modules and sub-packages</h3>

**General**
- Switched to British English every verb written in American accent. For example:
	- *standardize* <span>&#8594;</span> <i>standardi**S**e</i>
	- *serialize* <span>&#8594;</span> <i>seriali**S**</i>
	
- All `.lower()` instances of the string returned by the function `get_obj_type_str` (module `introspection_utils`, sub-package **General Utils**),<br>
  have been substituted in favour of setting the argument `lowercase` to True.
  
- The renaming of the module `file_and_directory_handler` to `ops_handler` has been applied to all affected files.
- The renaming of the module `file_and_directory_paths` to `path_utils` has been applied to all affected files.

**Climate Data Utils**
- Module `cdo_tools`:
	- Refactored multiple CDO processing functions, optimised internal helpers, and updated file handling functions with section headers and internal visibility changes.
	- Renamed the following functions:
	<table>
		<thead>
			<tr>
				<th>Old function name</span></th>
				<th>New function name</span></th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>get_variable_name_in_file_name</td>
				<td>_get_varname_in_filename (marked as internal)</td>
			</tr>
			<tr>
				<td>change_file_names_byvar</td>
				<td>change_filenames_by_var</td>
			</tr>
			<tr>
				<td>standardise_file_name</td>
				<td>_standardise_filename (marked as internal)</td>
			</tr>
		</tbody>
	</table>
	
	
<h3>Specific changes regarding sub-packages</h3>

- The following renamings have been made:
<table>
	<thead>
		<tr>
			<th>Old package name</span></th>
			<th>New package name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>climate_data_utils</th>
			<th>climalab</th>
		</tr>
		<tr>
			<th>statistics</th>
			<th>statkit</th>
		</tr>
		<tr>
			<th>utilities</th>
			<th>filewise</th>
		</tr>
		<tr>
			<th>complementary-to_remodule</th>
			<th>supplementary_tools</th>
		</tr>
	</tbody>
</table>

- All this changes have been applied to all affected modules.

---

## [v13.0.0] - 2024-10-22

### Changed

<h2>File Operations</h2>

<h4>Module <i>file_and_directory_handler</i></h4>

- Refactored and optimised file and directory operations; consolidated functions, introduced helper functions, and removed shell command dependencies.
- Renamed the following functions:
<table>
	<thead>
		<tr>
			<th>Old function name</span></th>
			<th>New function name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>move_files_by_ext_from_exec_code</td>
			<td>move_files</td>
		</tr>
		<tr>
			<td>copy_files_by_ext_from_exec_code</td>
			<td>copy_files</td>
		</tr>
		<tr>
			<td>remove_files_by_ext</td>
			<td>remove_files</td>
		</tr>
		<tr>
			<td>move_entire_directories</td>
			<td>move_directories</td>
		</tr>
		<tr>
			<td>copy_entire_directories</td>
			<td>copy_directories</td>
		</tr>
		<tr>
			<td>remove_entire_directories</td>
			<td>remove_directories</td>
		</tr>
		<tr>
			<td>make_parent_directories</td>
			<td>make_directories</td>
		</tr>
		<tr>
			<td>move_files_by_globstr_from_exec_code</td>
			<td>move_files</td>
		</tr>
		<tr>
			<td>copy_files_by_globstr_from_exec_code</td>
			<td>copy_files</td>
		</tr>
		<tr>
			<td>remove_files_by_globstr</td>
			<td>remove_files</td>
		</tr>
		<tr>
			<td>rsync</td>
			<td>(unchanged)</td>
		</tr>
		<tr>
			<td>rename_objects</td>
			<td>(unchanged)</td>
		</tr>
	</tbody>
</table>

- All this changes have been applied to all affected modules.
- After having these changes made, the module has been **renamed** to simply `ops_handler`.

<h4>Module <i>file_and_directory_paths</i></h4>

- Refactored file and directory path search logic; introduced switch-case for match_type, shortened function names, and optimised code.
- The following functions have been merged and renamed:
<table>
	<thead>
		<tr>
			<th>First function</span></th>
			<th>Second function</span></th>
			<th>Merged function name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>find_files_by_ext</td>
			<td>find_files_by_globstr</td>
			<td>find_files</td>
		</tr>
			<tr>
			<td>find_all_directories</td>
			<td>find_all_file_extensions</td>
			<td>find_all_ext_or_dirs (later renamed to `find_items`)</td>
		</tr>
		<tr>
			<td>find_file_containing_dirs_by_ext</td>
			<td>find_file_containing_dirs_by_globstr</td>
			<td>find_dirs_with_files</td>
		</tr>
	</tbody>
</table>

- All this changes have been applied to all affected files.
- After having these changes made, the module has been **renamed** to `path_utils`.

---

## [v12.0.0] - 2024-10-18

### Changed

<h2>Arrays and Lists</h2>

<h4>Module <i>conversions</i></h4>

- Optimised data conversion and flattening functions, improved handling of pandas and NumPy objects, added error handling, and streamlined code structure.
- Renamed the following functions:
<table>
	<thead>
		<tr>
			<th>Old function name</span></th>
			<th>New function name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>basic_value_data_type_converter</th>
			<th>convert_data_type</th>
		</tr>
		<tr>
			<th>list_array_to_std_array</th>
			<th>combine_arrays</th>
		</tr>
		<tr>
			<th>flatten_content_to_string</th>
			<th>flatten_to_string</th>
		</tr>
	</tbody>
</table>
	
<h2>General Utilities</h2>

<h4>'file_operations' sub-package</h4>

- The following **module** renamings have been made:
<table>
	<thead>
		<tr>
			<th>Old function name</span></th>
			<th>New function name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>bulk_rename_index_main</th>
			<th>bulk_rename_auto</th>
		</tr>
		<tr>
			<th>bulk_rename_index_manual</th>
			<th>bulk_rename_manual</th>
		</tr>
	</tbody>
</table>

<h4>'scripts' sub-package</h4>

- Contains application programs of several functions in the modules of sub-package `file_operations`:
- The following **module** renamings have been made:
<table>
	<thead>
		<tr>
			<th>Old function name</span></th>
			<th>New function name</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>change_permissions_exec</th>
			<th>modify_properties</th>
		</tr>
		<tr>
			<th>pdf_file_compressor_exec</th>
			<th>compress_pdf</th>
		</tr>
		<tr>
			<th>pdf_file_tweaker_exec</th>
			<th>tweak_pdf</th>
		</tr>
		<tr>
			<th>bulk_rename_index_exec</th>
			<th>bulk_rename</th>
		</tr>
	</tbody>
</table>

<h2>Databases</h2>
- Rename module `upload_data_to_mysql_database` to `upload_data`.

### Removed

- After the renamings the following modules have been removed:
	- `bulk_rename_index_exec`
	- `bulk_rename_index_main`
	- `bulk_rename_index_manual`
	- `change_permissions_exec`
	- `pdf_file_compressor_exec`
	- `pdf_file_tweaker_exec`
	- `upload_data_to_mysql_database`

---

## [v11.0.0] - 2024-10-17 

### Changed

**Arrays and Lists**
- Module `data_manipulation`
	- Optimised and grouped functions by categories, added support for pandas objects, and improved docstrings.
	- In functions `sort_rows_by_column` and `sort_columns_by_row`, argument `sort_order` has been substituted by `reverse`, where its mechanism is the same as for lists.
	- function `decompose_24h_cumulative_data`:
		- Rename to `decompose_cumulative_data`.
		- Introduce a new `fill_value` parameter to allow the user to choose how to handle negative differences.
	
**File Utils**
- Module `change_permissions_main`:
	- Refactored function `modify_obj_permissions` to allow no-change option for permissions and improved detection of files/directories.
	- Enhanced `modify_obj_owner` with no-change defaults for owner/group, flexible ID handling, and improved error handling.
	- After performing these changes, rename the module to `permission_manager`.
	
**Xarray Utils**
- Module `data_manipulation`:
	- Shortened function/variable names, optimised code, added docstrings.
	- Renamed the following functions:
	<table>
		<thead>
			<tr>
				<th>Old function name</span></th>
				<th>New function name</span></th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<th>extract_and_store_latlon_bounds</th>
				<th>extract_latlon_bounds</th>
			</tr>
			<tr>
				<th>extract_and_store_period_bounds</th>
				<th>extract_time_bounds</th>
			</tr>
			<tr>
				<th>extract_and_store_time_formats</th>
				<th>extract_time_formats</th>
			</tr>
		</tbody>
	</table>

- Moved function `create_ds_component` from module `data_manipulation` to `xarray_obj_handler`.

### Removed

- After the displacement of the function `create_ds_component`, `change_permissions_main` module was removed.

---

## [v10.11.3] - 2024-10-12

### Added

**Core Statistics**
- Created `interpolation_functions` module with `interpolate_numpy`, `interpolate_pandas`, and `interpolate_xarray` for flexible interpolation across various object types.

### Changed

**Climatology Statistics**
- Module `representative_series`
	- Delegate interpolation logic for numpy, pandas and xarray objects to module `interpolation_functions` (**Core Statistics**).

**Time Handling**
- function `standardize_calendar`:
	- Rename to British English nomenclature: `standardise_calendar`.
	- Optimised by refactoring type handling.
	- Delegate interpolation logic for numpy, pandas and xarray objects to module `interpolation_functions` (**Core Statistics**).
	
**Geospatial Tools**
- In module `geospatial_tools`, rename function `netcdf2raster` to `nc2raster`.

---

## [v10.9.2] - 2024-10-11

### Added

**General Utilities**
- `introspection_utils`: function `get_obj_type_str` now accepts the argument lowercase to change the case of the object type's name to lower.

### Changed

**Sets and Intervals**
- Modules
	- `interval_operators` and `operators_sets` have been renamed to `interval_handler`and `sets_handler` to align better conceptually 
	- Refactored the `interval_operators` to support switch-case dictionaries, improved `union` behaviour with `force_union` parameter for true unions.
- functions
	- Refactored `operations_with_sets`, streamlined operations with `default` and `sympy` constructors using switch-case dictionaries.
		- After that, renamed the function to `sets_operator`.
		
**Core Statistics**
- function `polynomial_fitting` has been moved from module `curve_fitting` to `interpolation_functions`.

<u>**Time handling**</u>
**`date_and_time_utils`**
- Merged and optimised functions for inferring frequency, date ranges, and finding date/time keys across pandas and NetCDF/xarray objects with lazy xarray imports.

- <span style="font-weight:bold; color:maroon">NOTE</span>: although every function has been moved to this module, except in one case the function pairs have been named identically,<br>
so it is worth describing their origins, referring to the latest version in which these moves have been performed (to this module).

<table>
	<thead>
		<tr>
			<th>Function name 1</th>
			<th>Module referring to 1</th>
			<th>sub-package referring to 1</th>
			<th>Function name 2</th>
			<th>Module referring to 2</th>
			<th>sub-package referring to 2</th>
			<th>Merged function name</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>find_date_key</td>
			<td>data_frame_handler</td>
			<td>pandas_data_frames/core</td>
			<td>find_time_dimension</td>
			<td>netcdf_handler</td>
			<td>weather_and_climate</td>
			<td>find_time_key</td>
		</tr>
		<tr>
			<td>infer_full_period_of_time</td>
			<td>data_frame_handler</td>
			<td>pandas_data_frames/core</td>
			<td>infer_full_period_of_time</td>
			<td>netcdf_handler</td>
			<td>weather_and_climate</td>
			<td>infer_dt_range</td>
		</tr>
		<tr>
			<td>infer_time_frequency</td>
			<td>data_frame_handler</td>
			<td>pandas_data_frames/core</td>
			<td>infer_time_frequency</td>
			<td>netcdf_handler</td>
			<td>weather_and_climate</td>
			<td>infer_frequency</td>
		</tr>
	</tbody>
</table>

### Removed

- After the displacement of the function `polynomial_fitting`, `curve_fitting` module was removed.

---

## [v10.4.0] - 2024-10-06

### Changed

- The following functions in **Xarray Utils** have been merged into a single one:
	- `find_time_dimension` and `find_time_dimension_raise_none` <span>&#8594;</span> `find_time_dimension`.
	- `find_coordinate_variables` and `find_coordinate_variables_raise_none` <span>&#8594;</span> `find_coordinate_variables`.
	
- As a consequence, the following modules which originally used `find_time_dimension_raise_none` and/or `find_coordinate_variables_raise_none` have been adapted:
	- **Climate Data Utils**: `cdo_tools`
	- **Xarray Utils**: `patterns` and `data_manipulation`

- Rename module `date_and_time_operators` to `date_and_time_utils` to emphasize <i>utility</i> or <u>tool</i> concept; originally in sub-package `time_handling`, no displacement.

### Removed

- Delete sub-package `varied_documentation` as its content has been relocated to a local directory.

---

## [v10.0.0] - 2024-10-02

### Added

- Add the following directories and modules in `statistics` sub-package:
	- **Core Statistics**: 
		- `signal_processing`: signal processing functions (signal whitening, low-pass, high-pass, and band-pass filters) 

- Add the following directories and modules in `utilities` sub-package:
	- **Pandas Utils**: 
		- `conversions`: module designed to handle pandas object type conversions, starting with DataFrame to NumPy`s structured array conversion.
		- `data_manipulation`: higher-level data manipulations using pandas.
		- `pandas_obj_handler`: handles various file operations for pandas DataFrames, including reading, merging, and saving Excel, CSV, and ODS files, with support for handling duplicated sheet names, managing file overwrites, and customizing output formats.
	- **Xarray Utils**: 
		- `conversions`: module designed to handle xarray object type conversions, starting with GRIB to netCDF conversion.
		- `data_manipulation`: higher-level data manipulations using xarray.
		- `file_utils`: comprehensive utilities for scanning, validating, and managing netCDF files.
		- `patterns`: utility functions for coordinate, time, and model data handling, enhancing flexibility, error handling, and performance.
		- `xarray_obj_handler`: optimised module for saving xarray Datasets and DataArrays to NetCDF and CSV, with enhanced handling of variable dimensions, attributes, and spatial coordinates.

### Changed

- After the creations in **Core Statistics**, the following changes have been made:

<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>signal_whitening</th>
			<th>time_series</th>
			<th>statistics/core</th>
			<th>(unchanged)</th>
			<th>signal_processing</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>low_pass_filter</th>
			<th>time_series</th>
			<th>statistics/core</th>
			<th>(unchanged)</th>
			<th>signal_processing</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>high_pass_filter</th>
			<th>time_series</th>
			<th>statistics/core</th>
			<th>(unchanged)</th>
			<th>signal_processing</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>band_pass1</th>
			<th>time_series</th>
			<th>statistics/core</th>
			<th>(unchanged)</th>
			<th>signal_processing</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>band_pass2</th>
			<th>time_series</th>
			<th>statistics/core</th>
			<th>(unchanged)</th>
			<th>signal_processing</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>band_pass3</th>
			<th>time_series</th>
			<th>statistics/core</th>
			<th>(unchanged)</th>
			<th>signal_processing</th>
			<th>(unchanged)</th>
		</tr>
	</tbody>
</table>

- After the creations in **Xarray Utils**, the following changes have been made:

1. To `time_handling` and `data_manipulation`:

<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>create_ds_component</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>data_manipulation</th>
		</tr>
		<tr>
			<th>extract_and_store_latlon_bounds</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>data_manipulation</th>
		</tr>
		<tr>
			<th>extract_and_store_period_bounds</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>data_manipulation</th>
		</tr>
		<tr>
			<th>extract_and_store_time_formats</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>data_manipulation</th>
		</tr>
		<tr>
			<th>netcdf_regridder</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>data_manipulation</th>
		</tr>	
	</tbody>
<table>
	
2. To `file_utils`:
	
<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>get_netcdf_file_dir_list</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>file_utils</th>
		</tr>
		<tr>
			<th>get_netcdf_file_list</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>file_utils</th>
		</tr>
		<tr>
			<th>netcdf_file_scanner</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>scan_ncfiles</th>
			<th>file_utils</th>
			<th>utilities/xarray_utils</th>
		</tr>
		<tr>
			<th>ncfile_integrity_status</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>file_utils</th>
		</tr>
	</tbody>
</table>

3. To `patterns`:

<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>find_coordinate_variables</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>find_coordinate_variables_raise_none</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>find_nearest_coordinates</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>find_time_dimension</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>find_time_dimension_raise_none</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>get_file_dimensions</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>get_file_variables</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>get_latlon_bounds</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>get_latlon_deltas</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
		<tr>
			<th>get_model_list</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>patterns</th>
		</tr>
	</tbody>
</table>

4. To `xarray_obj_handler`:

<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<thead>
		<tr>
			<th>grib2netcdf</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>grib2nc</th>
			<th>utilities/xarray_utils</th>
			<th>conversions</th>
		</tr>
		<tr>
			<th>save_data_array_as_csv</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>xarray_obj_handler</th>
		</tr>
		<tr>
			<th>save_data_as_netcdf_std</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>xarray_obj_handler</th>
		</tr>
		<tr>
			<th>save_nc_data_as_csv</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>utilities/xarray_utils</th>
			<th>xarray_obj_handler</th>
		</tr>
	</tbody>	
</table>

- <span style="font-weight:bold; color:maroon">NOTE</span>: any function rename above has also been applied to all files using the old function name.

### Removed

- Once every addition and changes performed regarding **Xarray Utils**, removed sub-package `netcdf_handler`.

---

## [v9.0.0] - 2024-10-01

### Added

- Add the following directories and modules in `statistics` sub-package:
	- **Core Statistics**: 
		- `approximation_techniques`: for functions focusing on general approximation techniques not necessarily tied to specific curve fitting or interpolation.
		- `curve_fitting`: for functions like polynomial fitting and other curve fitting techniques.
		- `interpolation_functions`: for interpolation techniques, including the `hdy_interpolation` function.
	- **Climate Statistics** (`fields/climatology`)
		- `representative_series`: analysis of time series resulting from representativity criteria.

### Changed

- Once above creations done, the following moves and/or renamings have been made:

**functions**

1. In `statistics` sub-package:

<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	</tbody>
		<tr>
			<th>polynomial_fitting</th>
			<th>regressions</th>
			<th>statistics/core</th>
			<th>(unchanged)</th>
			<th>curve_fitting</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>calculate_HDY</th>
			<th>variables</th>
			<th>statistics/fields/climatology</th>
			<th>(unchanged)</th>
			<th>representative_series</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>hdy_interpolation (once moved, changed visibility to internal)</th>
			<th>variables</th>
			<th>statistics/fields/climatology</th>
			<th>(unchanged)</th>
			<th>representative_series</th>
			<th>(unchanged)</th>
		</tr>
	</tbody>	
</table>
	
2. To `time_handling` sub-package:

<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>infer_full_period_of_time</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>date_and_time_operators</th>
			<th>time_handling</th>
		</tr>
		<tr>
			<th>infer_full_period_of_time</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>date_and_time_operators</th>
			<th>time_handling</th>
		</tr>
		<tr>
			<th>find_date_key</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>date_and_time_operators</th>
			<th>time_handling</th>
		</tr>
		<tr>
			<th>infer_time_frequency</th>
			<th>netcdf_handler</th>
			<th>climate_data_utils</th>
			<th>(unchanged)</th>
			<th>date_and_time_operators</th>
			<th>time_handling</th>
		</tr>
		<tr>
			<th>infer_time_frequency</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>date_and_time_operators</th>
			<th>time_handling</th>
		</tr>
	</tbody>
</table>

3. To `utilities/pandas_utils` sub-package (depth level 2)
<br>

3.1  To `conversions.py` module

<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>df_to_structured_array</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>conversions</th>
			<th>utilities/pandas_utils</th>
		</tr>
	</tbody>
</table>

<br>
3.2 To `data_manipulation` module
	
<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>create_pivot_table</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>concat_dfs_aux</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>count_data_by_concept</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>insert_column_in_df</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>insert_row_in_df</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>polish_df_column_names</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>reindex_df</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>sort_df_indices</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>sort_df_values</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>data_manipulation</th>
			<th>utilities/pandas_utils</th>
		</tr>
	</tbody>
</table>
<br>

3.3  To `pandas_obj_handler` module
	
<table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>csv2df</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>excel_handler</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>merge_csv_files</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>merge_excel_files</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>merge_ods_files</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>ods_handler</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>read_table</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>save2csv</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>save2excel</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
		<tr>
			<th>save2ods</th>
			<th>data_frame_handler</th>
			<th>pandas_data_frames</th>
			<th>(unchanged)</th>
			<th>pandas_obj_handler</th>
			<th>utilities/pandas_utils</th>
		</tr>
	</tbody>
</table>

**Modules**
	
</table>
	<thead>
		<tr>
			<th>Original function name</span></th>
			<th>Original module</span></th>
			<th>Original sub-package path</span></th>
			<th>New function name</span></th>
			<th>New module</span></th>
			<th>New sub-package path</span></th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>---</th>
			<th>climate_indicators</th>
			<th>statistics/fields/climatology</th>
			<th>---</th>
			<th>indicators</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>---</th>
			<th>climate_variables</th>
			<th>statistics/fields/climatology</th>
			<th>---</th>
			<th>variables</th>
			<th>(unchanged)</th>
		</tr>
		<tr>
			<th>---</th>
			<th>calendar_operators</th>
			<th>time_handling</th>
			<th>---</th>
			<th>calendar_utils</th>
			<th>(unchanged)</th>
		</tr>
	</tbody>
</table>

### Removed

- Once every addition and changes performed, removed sub-package `pandas_data_frames`.

---

## [v8.0.0] - 2024-09-29

### Added

1. sub-package `climate_data_utils`:

- Handles operations focused on data manipulation for climate datasets, with a special focus on file management, downloads, and plotting.
- The following content has been added, each supporting specific utilities:

<u>**Modules**</u>

* `cdo_tools.py`
	- Provides wrappers and utilities for working with the Climate Data Operators (CDO) tool.
	- Contains functions to interact with the Climate Data Store (CDS) API for downloading and managing climate data from the Copernicus Climate Data Store.
	- Facilitates data requests and efficient downloads of large datasets.

* `cds_tools.py`
	- Contains functions to interact with the Climate Data Store (CDS) API for downloading and managing climate data from the Copernicus Climate Data Store.
	- Facilitates data requests and efficient downloads of large datasets.
	
* `detect_faulty_ncfiles`
	- Implements functionality to detect and manage faulty NetCDF files, ensuring data integrity during processing and analysis.

* `extract_netcdf_basics`
	- Provides functions for extracting basic information from NetCDF files, such as metadata and variable summaries, facilitating data exploration.

* `nco_tools`
	- Offers utilities for working with the NetCDF Operators (NCO) tool, allowing for data manipulation and operations specific to NetCDF file formats.

* `netcdf_handler`
	- Central module for handling various operations related to NetCDF files, including reading, writing, and modifying NetCDF datasets.

* `weather_software_file_creator`
	- Contains functions for creating weather software files based on processed climate data, ensuring compatibility with various weather analysis tools.

<u>**Further sub-packages**</u>

* `complementary-to_remodule`
	- A sub-package containing various auxiliary and complementary functions aimed at climate data analysis and visualization. It includes:
		- <b>auxiliary_functions</b>: Utility functions to assist with common tasks such as file handling, data transformations, and helper routines.
		- <b>ba_mean_and_var</b>: Implements functions to compute bias-adjusted mean and variance from climate data.
		- <b>ba_mean</b>: Provides functions for calculating bias-adjusted means from climate datasets, allowing for more accurate representation of data characteristics.

* `data_downloads`
	- A module dedicated to managing the download of climate data. It contains:
		- <b>codes</b>: Includes scripts and configurations necessary for utilizing the Copernicus API for efficient data downloads.
		- <b>input_data</b> A folder for storing downloaded climate data, ensuring organised access to data files.


2. sub-package `statistics`:

- Introduced a new sub-package `statistics` to encapsulate numerical and statistical functions.,<br>
  aiming for modularity and organization across general and field-specific domains.

- **Core Modules:**
	- `time_series`: General functions for time series analysis, including signal processing.
	- `regressions`: Polynomial regression and other regression models.
	- `signal_forcing`: Signal whitening and noise handling.
- **Domains Supported:**
	- **Time Series Analysis:** functions for handling trends, noise, and filtering in time-series data.
	- **Signal Processing:** Includes signal filtering, whitening, and band-pass filters.
	- **Statistical Testing:** Initial support for statistical tests.

- **Improved Structure:** Consolidated statistical logic from various modules under a unified sub-package, with plans for expanding into domain-specific functions.


3. `statistical_tests` as a `core` module:

- **Hypothesis Testing**:
	* Added basic functions for hypothesis testing in the `statistical_tests.py` module, including:
		* `z_test_two_means` and `chi_square_test` which provide common statistical hypothesis tests.
	* Each function includes a full docstring with parameter descriptions, examples, and returns, designed to be easily expanded for more complex use cases in the future.


### Changed

- Many functions have been moved out from the modules in the old `weather_and_climate` sub-package to `statistics`.
- Information about the original module and new function name and location is displayed next:

<table>
	<thead>
		<tr>
			<th>Original function name</th>
			<th>Original module</th>
			<th>Original sub-package path</th>
			<th>New function name</th>
			<th>New module</th>
			<th>New sub-package path</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>calculate_WSDI</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>WSDI</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_SU</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>SU</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_CSU</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>CSU</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_FD/td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>FD</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_TN</td>
			<td>TN</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_RR</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>RR</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_CWD</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>CWD</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_HWD</td>
			<td>HWD</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_HWD</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>HWD</td>
			<td>climate_indicators</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_HDY</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>HDY</td>
			<td>climate_variables</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>hdy_interpolation</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>(unchanged)</td>
			<td>climate_variables</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_biovars</td>
			<td>climate_indicators</td>
			<td>weather_and_climate</td>
			<td>biovars</td>
			<td>climate_variables</td>
			<td>statistics/fields/climatology</td>
		</tr>
	</tbody>
</table>
	
<table>
	<thead>
		<tr>
			<th>Original function name</th>
			<th>Original module</th>
			<th>Original sub-package path</th>
			<th>New function name</th>
			<th>New module</th>
			<th>New sub-package path</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>periodic_statistics</td>
			<td>climate_statistics</td>
			<td>weather_and_climate</td>
			<td>(unchanged)</td>
			<td>time_series</td>
			<td>statistics/core</td>
		</tr>
		<tr>
			<td>climat_periodic_statistics</td>
			<td>climate_statistics</td>
			<td>weather_and_climate</td>
			<td>(unchanged)</td>
			<td>periodic_climat_stats</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>calculate_and_apply_deltas</td>
			<td>climate_statistics</td>
			<td>weather_and_climate</td>
			<td>(unchanged)</td>
			<td>simple_bias_correction</td>
			<td>statistics/fields/climatology</td>
		</tr>
		<tr>
			<td>window_sum/td>
			<td>climate_statistics</td>
			<td>weather_and_climate</td>
			<td>(unchanged)</td>
			<td>moving_operations</td>
			<td>statistics/core</td>
		</tr>
		<tr>
			<td>moving_average</td>
			<td>climate_statistics</td>
			<td>weather_and_climate</td>
			<td>(unchanged)</td>
			<td>moving_operations</td>
			<td>statistics/core</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th>Original function name</th>
			<th>Original module</th>
			<th>Original sub-package path</th>
			<th>New function name</th>
			<th>New module</th>
			<th>New sub-package path</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>autocorrelate</td>
			<td>climatic_signal_modulators</td>
			<td>weather_and_climate</td>
			<td>(unchanged)</td>
			<td>time_series</td>
			<td>statistics/core</td>
		</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<td>Original function name</td>
			<td>Original module</td>
			<td>Original sub-package path</td>
			<td>New function name</td>
			<td>New module</td>
			<td>New sub-package path</td>
		</tr>
	</thead>
	<tbody>
		<tr>
			<th>get_1hour_time_step_data</th>
			<th>consecutive_idx_statistics</th>
			<th>weather_and_climate</th>
			<th>hourly_ts_cumul</th>
			<th>time_series</th>
			<th>statistics/core</th>
		</tr>
		<tr>
			<th>count_consecutive_days_maxdata</th>
			<th>consecutive_idx_statistics</th>
			<th>weather_and_climate</th>
			<th>consec_occurrences_maxdata</th>
			<th>time_series</th>
			<th>statistics/core</th>
		</tr>
		<tr>
			<th>count_consecutive_days_mindata</th>
			<th>consecutive_idx_statistics</th>
			<th>weather_and_climate</th>
			<th>consec_occurrences_mindata</th>
			<th>time_series</th>
			<th>statistics/core</th>
		</tr>
	</tbody>
</table>
	
- <span style="font-weight:bold; color:maroon">NOTE</span>: prior to these movements, every single function until here has been refactored, functionalities enhanced and optimised inner codes.

5. Rest of the content:

- The following content has been moved to the new sub-package `climate_data_utils`:

1. **Modules**:
	* `cdo_tools`
	* `cds_tools`
	* `detect_faulty_ncfiles`
	* `extract_netcdf_basics`
	* `__init__`
	* `meteorological_variables`
	* `nco_tools`
	* `netcdf_handler`
	* `weather_software_file_creator`
	
2. **Further sub-packages**:
	* `data_downloads`
	* `complementary-to_remodule`

### Removed

- Once every operation above performed, delete sub-package `weather_and_climate`.

---

## [v7.3.3] - 2024-09-28

### Added

`climatic_signal_modulators`

- **Autocorrelation Function**:
   * Streamlined the logic by handling smaller arrays using `numpy.correlate` and larger arrays with `scipy.signal.correlate`.
   * Updated the docstring to clarify parameters and computation flow, explaining when to use two-sided or one-sided autocorrelation.

- **Signal Whitening functions**:
   * Developed two signal whitening functions: `signal_whitening_classic` and `signal_whitening_pca`.
   * `signal_whitening_classic` applies a traditional approach using Cholesky decomposition with `numpy.linalg`.
   * `signal_whitening_pca` uses Principal Component Analysis (PCA) via `sklearn` for whitening data.
   * Enhanced docstrings for both functions, clarifying inputs, outputs, and providing comprehensive usage examples.
   
- **Band-Pass Filtering functions**:
	* Refined three band-pass filtering functions (`band_pass1`, `band_pass2`, `band_pass3`), created during the Master in Meteorology, now translated:
		* Simplified internal variable names and loops for more concise code.
		* Added detailed docstrings, explaining how each function works with frequency domain transformations and filtering based on custom low and high-frequency ranges.
		* Used consistent terminology and enhanced explanations for different approaches to band-pass filtering.
   
- **Low and High-Pass Filtering functions**:
	- Refined `low_pass_filter` and `high_pass_filter` functions, also created during the Master in Meteorology: 
		* Improved performance by applying zero-phase filtering and optimizing how filters are designed based on cutoff frequencies.
		* Expanded the docstring to include explanations on filter design and its effect on different time series data.

### Changed

1. `climatic_statistics`

- `window_sum`:
	* Optimised performance by using `np.convolve` for faster sliding window summation.
	* Added edge case handling for empty arrays or when the window size exceeds the array length.
	* Refined docstring to clarify input parameters, particularly around window size and handling of edge cases.

- `moving_average`:
	* Rewritten using `np.convolve` for efficient computation of moving averages over a window.
	* Added option for handling arrays shorter than the window size, ensuring graceful failure or warning.
	* Clarified the docstring, highlighting that this function handles general numerical arrays, and specifying the nature of the windowing process.
	
2. `climatic_signal_modulators`

- `polynomial_fitting`
	 * Optimised the logic by simplifying variable names and improving handling of edge cases.
	 * Enhanced the docstring to detail the parameters, added alternative polynomial function usage, and described the fixing of edges in polynomial interpolation.

---

## [v7.0.0] - 2024-09-26

### Changed

- Delete part of the file name `arrays_` contained in all modules of the sub-package `arrays_and_lists`,<br>
  then delete all old-named modules.
- Module `climate_statistics`: refactor the following functions to improve performance, readability and maintainability:
	* `periodic_statistics`
	* `climat_periodic_statistics`
	* `calculate_and_apply_deltas`
	* `window_sum`
	* `moving_average`
- Remove the substring `array_` of functions `select_array_elements` (module `patterns`), <btr>
  `sort_array_rows_by_column` and `sort_array_columns_by_row` (both in module `data_manipulation`).
- Remove triple quoted template string.

---

## [v6.8.2] - 2024-09-25

### Added

- Add functionalities to media manipulation functions for merging and cutting audio/video files
- Add two external programs that apply functions of the module `audio_and_video_manipulation`.
- Add and reorganize section header comments

### Changed

- Improve readability and streamline functions
- Substitute `print_exit_info` with `exit_info` as done in the original module `os_operations`
- Replace varname `time_format` by `dt_format` as this generally represents both date and time (abbreviated as `dt`).

---

## [v6.6.0] - 2024-09-23

### Added

- Add docstring for every function
- Add module to store configuration data like credentials, host info, etc.
- Add type to every parameter missing it in all docstrings
- Add dictionary with conversion factors from the provided floated time to the given unit

### Changed

- Rename function `remove_elements_from_array` to `remove_elements`
- Eliminate `exec_command_shell` function and, if present, `catch_shell_prompt_output` <br>
  in favour of the renewed and complete `run_system_command` from module `os_operations`
- Refactor command execution module

---

## [v6.3.4] - 2024-09-20

### Added

- Add optional argument, comments explaining key parts of the code and simplify the f-strings
- Add type to the parameter `datetime_obj` in the docstring of the internal function `_total_time_unit`
- Add type to every parameter missing it in all docstrings.

### Changed

- Delete `todo` from the code as the task there is already done
- Specify the name and type of the returning variable in function `string_underliner`

---

## [v6.3.0] - 2024-09-18

### Added

- Add further fractional second precision choice at internal function `_format_arbitrary_time`
- Add support for `datetime.time` object conversion to other datetime-like objects

### Changed

- Eliminate need of the old function `time_format_tweaker` in favour of the renewed `datetime_obj_converter` from module `time_formatters`
- Rewrite some lazy imports and fix a typo as a result

---

## [v6.0.0] (2024-09-06)

### Added

- Created directories for lambda functions and assertion documentation in Python.
- Enhanced performance by importing frequently used NumPy libraries and utilizing `get_obj_type_str` for type checks.
- Implemented a simple calculator functionality using a dictionary-based switch-case approach, accepting multiple arguments.
- Improved input validation and functionalities in `sort_dictionary_by_keys` and `merge_dictionaries` functions.
  
### Changed

- Restored accidentally removed code during editing.
- Sub-package `arrays_and_lists`:
	* Move out some functions in `array_data_manipulation` and `array_maths` to other modules in this sub-package.
	* Rewrite section headers to align with the nature of functions under them. Clarity and precision gained.
- Renamed directories for improved readability and intuitive understanding.
- Removed unnecessary directories due to renaming or redundancy.

### Removed

- Deleted `webdriver_Firefox-Chrome_settings_check.py` in favour of the more descriptively named `webdriver_Firefox-Chrome_setup_test.py`.
- Eliminated `git` directory as Git does not depend on Python.

---

## [v5.5.5] (2024-08-20)

### Added

- Combined character splitting instructions into single lines for efficiency.
  
### Changed

- Enhanced the `format_table_from_lists` function for better error handling.
- Improved readability by splitting long lines into shorter ones.
- Introduced a new folder for Web Scraping modules.

---

## [v5.4.2] (2024-08-08)

### Added

- Functionality to select column delimiters in all relevant functions.
- New function to underline single or multiple line strings.

### Changed

- Revised the docstring in `format_table_from_lists` to reflect new functionalities.
- Fixed issues in the `format_table_from_lists` function related to multi-row values.

### Removed

- Removed the `Constants` section from general notes.

---

## [v5.2.2] (2024-07-15)

### Added

- Optional argument for setting the index starting number in `format_table_from_list` and `format_table_from_lists`.
- New module for formatting dictionaries or lists into tables.

### Changed

- Clarified overwriting behaviour in `serialize_dict_to_json`.
- Simplified the try-except block structure in `print_format_string`.

### Removed

- Removed a JSON test file.

---

## [v5.0.0] (2024-07-10)

### Added

- Created a sub-package for JSON functionalities.

### Changed

- Polished section comments for clarity.

### Removed

- Removed redundant JSON file utilities, centralizing them in the `json_file_handler` module.

---

## [v4.9.0] (2024-06-29)

### Added
- Various references updated from `pytools` to `pyutils`.
- New warning codes and documentation improvements.

### Changed
- Created a file to track significant changes in the repository.

---

## [v4.0.0] (2024-06-26)

### Added

- Several sub-packages for various utility functions and modules.

### Changed

- Relocated functions and optimised imports.

### Removed

- Deleted files that have been relocated.

---

## [v3.0.0] (2024-06-24)

### Added

- Introduced new functionalities for handling regex and optimizing code structure.

### Changed

- Updated imports to absolute and improved error handling.

---

## [v2.7.4] - 2024-06-14

### Added

- Add todo for when function `time_format_tweaker` at module `time_formatters` is optimised and incorporated more functionalities to it.
- Add detailed docstring to the function `natural_year` and optimize inner code and comments.

### Changed

- Modify function `datetime_range_operator` to `merge_datetime_dataframes`.
- Update function `get_current_time` to `get_current_datetime`; fix typo when writing to the object `report_file_obj`.
- Optimize the code of the main function `clock_time_average`, as well as the auxiliary functions, and add and refine the docstrings in all of them.
- Refine module and custom module import syntax in function `standardize_calendar`.
- Rename `ofile` variable to `out_file_obj`, which all `.write` instances are referenced from.
- Fix todo list for main function `clock_time_average` and auxiliaries
- Optimize the whole try-except block and handle specific errors gracefully.

---

## [v2.4.0] - 2024-06-12


### Added

- Add docstrings and polish the main functions `sum_clock_times` and `sum_date_objects`, as well as their auxiliary functions.
- Add functions to sum or subtract dates and/or times (preliminary version).

### Removed

- Delete to-do list with `date_and_time_maths`.

---

## [v2.1.0] - 2024-06-11

### Added

- Import the function to return an object type`s string part.
- Add multidimensional indexing functionality for NumPy arrays in `select_array_elements` function.

### Renamed

- Rename the function to return an object type`s string part.

---

## [v2.0.0] - Initial release - 2024-06-10

### Added
- Add module for climate and environment data manipulation and extraction.
- Add module for date and time management functions.
- Add module initiator file.
- Add module for string management.
- Add directory containing small manuals and web extracts about external Python modules and functions.
- Add module for mathematical operations with sets.

### Removed

- Remove function `json2dict` as dictionaries are semantically handled.
