# Changelog

## [v10.0.0] - 2024-09-26

### Changed
- Delete the part `array_` referring to the method `select_array_elements`
- Delete the part `array_` referring to the methods `sort_array_rows_by_column` and `sort_array_columns_by_row`
- Delete readme file (written in Basque) which urged to delete the part of every file in `arrays_and_lists` beginning with `arrays_`
- Delete part of the file name `arrays_` because there are 3 other files which began like that, making the names together redundant.
- Remove triple quoted template string
- Refactor to improve performance, readability, and maintainability
- Rewrite the definition of `polynomial_fitting` method to a single line
- Lowercase variable `ZERO_PADDING`
- Rename inexistent module `padding` to `conversion`
- Delete file because it has been replaced with its equivalent, removing the initial fragment `arrays_`

---

## [v9.3.0] - 2024-09-25

### Changed
- Improve readability and streamline functions
- Substitute `print_exit_info` with `exit_info` as done in the original module `os_operations`
- Replace varname `time_format` by `dt_format` as this generally represents both date and time (abbreviated as `dt`).

### Added
- Add functionalities to media manipulation methods for merging and cutting audio/video files
- Add options to include files containing audio and video file names, respectively.
- Add the argument `quality` as a factor to be multiplied by 32, denoting the bit rate.
- Add and reorganize section header comments
- Add an external program that applies `merge_audio_or_video` method of the module `audio_and_video_manipulation`
- Add an external program that applies `cut_media_files` method of the module `audio_and_video_manipulation`
- Add note for ChatGPT-aware creation in method `standardize_calendar`, at xarray object handling part

---

## [v9.0.0] - 2024-09-23

### Changed
- Rename method `remove_elements_from_array` to `remove_elements`
- Eliminate `exec_command_shell` method and, if present, `catch_shell_prompt_output` in favor of the renewed and complete `run_system_command` from module `os_operations`
- Refactor command execution module

### Added
- Add docstring for every method
- Add module to store configuration data like credentials, host info, etc.
- Add type to every parameter missing it in all docstrings
- Add dictionary with conversion factors from the provided floated time to the given unit

---

## [v8.1.0] - 2024-09-20

### Changed
- Delete `todo` from the code as the task there is already done
- Specify the name and type of the returning variable in method `string_underliner`

### Added
- Add optional argument, comments explaining key parts of the code and simplify the f-strings
- Add type to the parameter `datetime_obj` in the docstring of the internal method `_total_time_unit`
- Add type to every parameter missing it in all docstrings

---

## [v8.0.0] - 2024-09-18

### Changed
- Eliminate need of the old method `time_format_tweaker` in favor of the renewed `datetime_obj_converter` from module `time_formatters`
- Rewrite some lazy imports and fix a typo as a result

### Added
- Add further fractional second precision choice at internal method `_format_arbitrary_time`
- Add support for **datetime.time** object conversion to other datetime-like objects

---

## v6.7.0 (2024-09-06)
### Added
- Enhanced performance by importing frequently used NumPy libraries and utilizing `get_obj_type_str` for type checks.
- Implemented a simple calculator functionality using a dictionary-based switch-case approach, accepting multiple arguments.
- Improved input validation and functionalities in `sort_dictionary_by_keys` and `merge_dictionaries` methods.
  
### Changed
- Restored accidentally removed code during editing.
- Renamed a file for better clarity and precision, maintaining tested functionality.

### Removed
- Deleted `webdriver_Firefox-Chrome_settings_check.py` in favor of the more descriptively named `webdriver_Firefox-Chrome_setup_test.py`.

---

## v6.6.0 (2024-08-21)
### Added
- Created directories for lambda functions and assertion documentation in Python.

### Changed
- Renamed directories for improved readability and intuitive understanding.
- Removed unnecessary directories due to renaming or redundancy.

### Removed
- Eliminated `git` directory as Git does not depend on Python.

---

## v6.5.3 (2024-08-20)
### Added
- Combined character splitting instructions into single lines for efficiency.
  
### Changed
- Enhanced the `format_table_from_lists` method for better error handling.
- Improved readability by splitting long lines into shorter ones.
- Introduced a new folder for Web Scraping modules.

---

## v6.5.0 (2024-08-08)
### Added
- Functionality to select column delimiters in all relevant methods.
- New method to underline single or multiple line strings.

### Changed
- Revised the docstring in `format_table_from_lists` to reflect new functionalities.
- Fixed issues in the `format_table_from_lists` method related to multi-row values.

### Removed
- Removed the `Constants` section from general notes.

---

## v6.3.0 (2024-07-15)
### Added
- Optional argument for setting the index starting number in `format_table_from_list` and `format_table_from_lists`.
- New module for formatting dictionaries or lists into tables.

### Changed
- Clarified overwriting behavior in `serialize_dict_to_json`.
- Simplified the try-except block structure in `print_format_string`.

### Removed
- Removed a JSON test file.

---

## v6.2.0 (2024-07-10)
### Added
- Created a subpackage for JSON functionalities.

### Changed
- Polished section comments for clarity.

### Removed
- Removed redundant JSON file utilities, centralizing them in the `json_file_handler` module.

---

## v6.0.0 (2024-06-29)
### Added
- Various references updated from `pytools` to `pyutils`.
- New warning codes and documentation improvements.

### Changed
- Created a file to track significant changes in the repository.
  
### Removed
- No removals in this version.

---

## v5.0.0 (2024-06-26)
### Added
- Several subpackages for various utility functions and modules.

### Changed
- Relocated methods and optimized imports.

### Removed
- Deleted files that have been relocated.

## v4.0.0 (2024-06-24)
### Added
- Introduced new functionalities for handling regex and optimizing code structure.

### Changed
- Updated imports to absolute and improved error handling.

### Removed
- No removals in this version.

Feel free to let me know if you`d like to add any specific notes or further refine this summary!

---

## [v1.3.0] - 2024-06-14
### Added
- Add todo for when method `time_format_tweaker` at module `time_formatters` is optimized and incorporated more functionalities to it.

### Optimized
- Optimize the code of the main method `clock_time_average`, as well as the auxiliary methods, and add and refine the docstrings in all of them.
- Refine module and custom module import syntax in method `standardize_calendar`.

### Renamed
- Rename `ofile` variable to `out_file_obj`, which all `.write` instances are referenced from.

### Fixed
- Fix todo list for main method `clock_time_average` and auxiliaries; add detailed docstring to the method `natural_year` and optimize inner code and comments.
- Optimize the whole try-except block and handle specific errors gracefully.

### Modified
- Modify method `datetime_range_operator` to `merge_datetime_dataframes`.
- Update method `get_current_time` to `get_current_datetime`; fix typo when writing to the object `report_file_obj`.

---

## [v1.1.0] - 2024-06-12
### Added
- Add docstrings and polish the main methods `sum_clock_times` and `sum_date_objects`, as well as their auxiliary methods.
- Add methods to sum or subtract dates and/or times (preliminary version).

### Deleted
- Delete to-do list with date and time maths.

---

## [v1.0.1] - 2024-06-11
### Added
- Import the method to return an object type`s string part.
- Add multidimensional indexing functionality for NumPy arrays in `select_array_elements` method.

### Renamed
- Rename the method to return an object type`s string part.

---

## [v1.0.0] - 2024-06-10
### Added
- Add module for climate and environment data manipulation and extraction.
- Add module for date and time management methods.
- Add module initiator file.
- Add module for string management.
- Add directory containing small manuals and web extracts about external Python modules and methods.
- Add module for mathematical operations with sets.

### Removed
- Remove method `json2dict` as dictionaries are semantically handled.
