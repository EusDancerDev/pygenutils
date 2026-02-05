# pygenutils Changelog

All notable changes to this project will be documented in this file.

---

## [16.3.2] - 2026-02-05

### Fixed (16.3.2)

#### **Number Bases** (fixing; 16.3.2)

- Module `base_converters.py`:
  - Use a raw regex pattern for binary input validation in `_check_input_binary` to ensure the expression is interpreted correctly.

#### **Strings** (fixing; 16.3.2)

- Module `text_formatters.py`:
  - Correct the brace-matching regex in `format_string` by using the character class `[{}]` so curly braces are treated as literal characters.

#### **Time Handling** (fixing; 16.3.2)

- Module `countdown.py`:
  - Remove redundant argument unpacking in `__countdown` and rely on `format_string` for mapping datetime components.

---

## [16.3.1] - 2025-10-08

### Changed (16.3.1)

#### **Time Handling** (changing; 16.3.1)

- Module `program_snippet_exec_timers.py`:
  - Improve parameter naming for semantic clarity:
    - Rename `roundoff` parameter to `decimal_places` in `snippet_exec_timer()` function
    - Update all related documentation, validation logic, comments, and internal usage

#### **Number Bases** (changing; 16.3.1)

- Module `mathematical_utils.py`:
  - Improve parameter naming for semantic accuracy:
    - *Rationale*: Factorials produce integers; the parameter controls significant digits for scientific notation representation, not decimal places for floating-point rounding.
    - Changes:
      - Rename `decimals` parameter to `significant_digits` in `adapted_factorial()` function
      - Update comment from "roundoff number" to "decimal places position" for consistency
      - Update all related documentation and internal usage

---

## [16.3.0] - 2025-08-19

### Changed (16.3.0)

#### **General** (changing; 16.3.0)

- Change the header section comment `Operations` to `Program progression` to better reflect what it contains in the following modules:

| Subpackage | Module |
|:----------:|:------:|
| `arrays_and_lists` | `data_manipulation.py` |
| `arrays_and_lists` | `patterns.py` |
| `audio_and_video` | `audio_and_video_manipulation.py` |
| `audio_and_video` | `merge_audio_or_video.py` |
| `audio_and_video` | `trim_media.py` |
| `dictionaries` | `dict_operators.py` |
| `operative_systems` | `os_operations.py` |
| `sets_and_intervals` | `interval_handler.py` |
| `sets_and_intervals` | `set_handler.py` |
| `time_handling` | `date_and_time_maths.py` |
| `time_handling` | `date_and_time_utils.py` |
| `time_handling` | `program_snippet_exec_timers.py` |
| `time_handling` | `time_formatters.py` |

- Reorganise the comment hierarchy:
  - Implement a two- or three-level comment hierarchy:
    - Level 1: `#---------------------#`
    - Level 2: `#-#-#-#-#-#-#-#-#-#-#-#`
    - Level 3: `#######################`
  - Clear, consistent, sufficient for current scope, standardising underline lengths and document the hierarchy at the top if/when adding more levels

  - Affected modules are:

  | Subpackage | Module |
  |:----------:|:------:|
  | `operative_systems` | `os_operations.py` |
  | `sets_and_intervals` | `interval_handler.py` |
  | `time_handling` | `date_and_time_maths.py` |
  | `time_handling` | `program_snippet_exec_timers.py` |
  | `time_handling` | `time_formatters.py` |

#### **Time Handling** (changing; 16.3.0)

- Module `time_formatters.py`:
  - Clean up unused parameters in conversion dictionaries:
    - Replace unused parameters with underscores in `_TOTAL_TIME_UNIT_DICT` and in all dictionaries ending with `_OBJ_CONVERSION_DICT`:
      - `DT_OBJ_CONVERSION_DICT`
      - `DT64_OBJ_CONVERSION_DICT`
      - `DT_TIME_OBJ_CONVERSION_DICT`
      - `TIMESTAMP_OBJ_CONVERSION_DICT`
      - `ARROW_OBJ_CONVERSION_DICT`
      - `_DT_LIKE_OBJ_CONVERSION_DICT`
    - Normalise the conversion dispatcher to pass a consistent positional argument sequence, preserving arity and avoiding unexpected keyword issues.
    - Correct minor issues found while reviewing:
      - Fix `np.ndarray` type check in `_to_string`.
      - Use `timedelta(...).total_seconds()` in `__time_component_to_float`.
      - Adjust `dateutil` parsing to not accept strptime-like format strings.
    - No public API changes; improves maintainability and clarity of internal conversions.

---

## [16.2.4] - 2025-08-17

### Changed (16.2.4)

#### **Number Bases** (changing; 16.2.4)

- Module `base_converters`:
  - Clean up `bin2dec_basic`:
    - Update docstring and section headers
    - Simplify variable names and loop structure
  - Streamline `dec2bin_basic`:
    - Replace `while True` with explicit condition
    - Improve control flow and string handling
  - Enhance procedure validation:
    - Add option sets parameter to `_procedure_checker`
    - Split conversion options by function type

## [16.2.3] - 2025-07-28

### Fixed (16.2.3)

#### **Strings** (fixing; 16.2.3)

- Module `text_formatters.py`:
  - Enhance `print_format_string` function with `flush` parameter support to enable immediate terminal output for real-time display applications like countdown timers.

#### **Time Handling** (fixing; 16.2.3)

- Module `countdown.py`:
  - Fix terminal output leftover character issue by implementing string padding to ensure consistent display width during countdown transitions
  - Correct `parse_dt_string` function calls by removing non-existent `end` and `flush` parameters that were causing `TypeError` exceptions
  - Update import from `print_format_string` to `format_string` to allow printing the formatted output later, now instead of directly printing it
  - Enhance countdown display logic with proper terminal control using `\r` and `flush=True` for clean real-time output
  - Update function docstring to accurately reflect the actual output format ("D days H:M:S" or "H:M:S")

---

## [16.2.2] - 2025-07-23

### Fixed (16.2.2)

#### **Arrays and Lists** (fixing; 16.2.2)

- Module `data_manipulation.py`:
  - Fix `extract_1d_unique_basic` function to use proper for loop instead of list comprehension for side effects when `procedure="list"`. This improves code readability and follows Python best practices.

---

## [16.2.1] - 2025-07-18

### Added (16.2.1)

#### **Time Handling** (adding; 16.2.1)

- Module `time_formatters.py`:
  - Introduced `dayfirst` and `yearfirst` parameters to `parse_dt_string()` with default `False` values, updating related functions and dictionaries for compatibility, and ensuring backward compatibility.

---

## [16.2.0] - 2025-07-16

### Changed (16.2.0)

#### **Time Handling** (changing; 16.2.0)

- Module `time_formatters.py` and `time_utils.py`:
  - **Arrow Dependency Made Optional**:
    - Arrow imports are now lazy, reducing core dependencies.
    - Informative error messages guide users to install the arrow package if needed.
    - This change requires explicit installation of the arrow package for its functionality.

#### **Strings** (changing; 16.2.0)

- `string_handler.py`: Improved `find_substring_index()` with options for finding last occurrences and both first/last positions, enhancing flexibility in substring searching.

- `text_formatters.py`: Text formatting functions now use the `.center()` method for better readability and functionality, maintaining backward compatibility while adding new centering capabilities.

---

## [16.1.3] - 2025-07-03

### Fixed

#### **General** (fixing; 16.1.3)

- Use `%F` and `%T` shorthands for date and time formatting, respectively.
  - Replace occurrences of `%Y-%m-%d` and `%H:%M:%S` with `%F` and `%T` where applicable, across multiple modules.

#### **Time Handling** (fixing; 16.1.3)

- Modules `date_and_time_maths.py`:
  - Reference unreferenced parameters in time_handling functions
    - Fix `time_fmt_str` parameter in `dt_average()` by passing it to `_dt_to_radians()`
    - Fix `method` parameter in `natural_year()` by using it in `datetime_obj_converter()` calls

- Module `time_utils.py`:
  - Reference unreferenced parameters in time_handling functions
    - Fix `module` parameter in `_convert_floated_time_to_datetime()` by implementing module-specific datetime creation
    - Implement `unit` parameter in `datetime_obj_converter()` for `numpy datetime64` and `pandas Timestamp` conversions
    - Implement `float_class` parameter by adding `float` conversion target with precision control
    - Implement `int_class` parameter by adding `int` conversion target with precision control
  
---

## [16.0.0] - 2025-07-01

### Changed (16.0.0)

#### **Audio and Video** (changing; 16.0.0)

- Module `audio_and_video_manipulation`:
  - **BREAKING CHANGE**: Replace `quality` and `video_bitrate` parameters with separate bitrate fraction parameters:
    - Add `audio_bitrate_fraction` parameter (default: 5) - multiplied by 32 to get audio kbps
    - Add `video_bitrate_fraction` parameter (default: 5) - multiplied by 32 to get video kbps
    - Remove single `quality` parameter and `video_bitrate` parameter
    - Both fractions can be set to `None` to skip bitrate specification
  - Enhanced parameter documentation with bitrate ranges based on `on_the_bitrate.md`:
    - Audio: 2-16 for 64-512kbps (speech to high-quality music)
    - Video: 31-3125+ for 1-100+Mbps (360p to 4K+)
  - Improved ffmpeg command building logic to handle `None` values properly
  - Updated parameter validation for new fraction-based system
  - Functions affected:
    - `merge_media_files`
    - `merge_individual_media_files`
    - `cut_media_files`

- Scripts `merge_audio_or_video.py`, `merge_audio_and_video.py`, and `trim_media.py`:
  - Updated to use new `audio_bitrate_fraction` and `video_bitrate_fraction` parameters
  - Added comprehensive parameter documentation with common bitrate ranges
  - Removed deprecated `quality` and `video_bitrate` parameter usage
  - Enhanced configurability with separate audio and video bitrate control

---

## [15.15.2] - 2025-06-27

### Fixed (15.15.2)

#### **Time Handling** (fixing; 15.15.2)

- Modules `countdown.py` and `date_and_time_maths.py`:
  - Point to the correct function to parse the time string: changed `parse_time_string` to `parse_dt_string`

### Changed (15.15.2)

#### **General** (changing; 15.15.2)

- **Type Hint Standardisation**
  - Standardised type hints and docstrings by capitalising typing objects (e.g. `Any`, `Callable`, `Optional`)
  - Updated all `optional` parameters in docstrings to follow lowercase convention
  - Adopted Python 3.10+ union syntax (`|`) consistently across all modules

---

## [15.15.0] - 2025-06-26

### Added (15.15.0)

#### **Arrays and Lists** (adding; 15.15.0)

- Module `data_manipulation.py`: enhanced `flatten_list` function with flexible return and sorting options:
  - Add internal `_flatten_generator` function as the core of the enhancement:
    - Serves as the core of the enhancement
    - As a reusable helper function in dedicated helpers section
  - Define more parameters to gain more flexibility:
    - Added `return_list` parameter (default: `True`) to choose between list and generator output
    - Added `sort` parameter to enable sorting of flattened elements using existing `sort_1d_basic` function
    - Added `reverse` parameter for descending sort order control when sorting is enabled
  - Update documentation and maintain compatibility:
    - Updated comprehensive docstring with new parameters, return types, and usage examples
    - Maintained backward compatibility with existing generator-based usage patterns

### Changed (15.15.0)

#### **General** (changing; 15.15.0)

- **List flattening calls**
  - Removed `list` call on function `flatten_list`, as by default it returns a list

---

## [15.14.1] - 2025-06-24

### Added (15.14.1)

#### **Audio and Video** (adding; 15.14.1)

- Module `audio_and_video_manipulation`:
  - Enhanced user control over encoding parameters in all media processing functions (only applicable when `video_codec` is not "copy"):
    - Added `video_codec` parameter (default: "libx264"): supports "copy", "libx264", "libx265", etc.
    - Added `audio_codec` parameter (default: "aac"): supports "copy", "aac", "mp3", "ac3", etc.
    - Added `preset` parameter (default: "medium"): encoding speed/quality preset for video codecs
    - Added `video_bitrate` parameter (default: None): video bitrate control in kbps
    - Maintained backward compatibility with sensible defaults for all new parameters
  - Updated FFMPEG command templates to use user-configurable parameters instead of hardcoded values
  - Enhanced functions to intelligently apply audio/video-specific parameters only to audio/video files, respectively
  - Added comprehensive parameter validation with descriptive error messages for all new parameters

### Changed (15.14.1)

#### **Dictionaries** (changing; 15.14.1)

- Update variable names:
  - Changes have been made in the original file `global_parameters.py` in the `paramlib` package.
  - These include abbreviation addressing.

| Module | Old variable name | New variable name |
|:------:|:-----------------:|:-----------------:|
| `dict_operators` | `BASIC_FOUR_RULES` | `BASIC_ARITHMETIC_OPERATORS` |

---

## [15.14.0] - 2025-06-20

### Added (15.14.0)

#### **General** (adding; 15.14.0)

- **Comprehensive Nested List Support**
  - Added robust nested list handling across multiple modules
  - Import `flatten_list` from `arrays_and_lists.data_manipulation` for consistent nested structure processing
  - Enhanced functions to handle arbitrarily deep nested list structures
  - Maintained backward compatibility with existing list processing

#### **Dictionaries** (adding; 15.14.0)

- Modules `dict_handler` and `dict_operators`:
  - Add nested list support for dictionary collections:
    - `merge_dictionaries()`: Handle nested lists of dictionaries
    - `sort_object_of_dictionaries()`: Process complex nested dictionary structures
    - `dict_value_basic_operator()`: Support nested dictionary collections

#### **Operative Systems** (adding; 15.14.0)

- Module `os_operations`:
  - Add nested list support for command processing:
    - `run_system_command()`: Flatten nested command argument lists
    - Enhanced system command execution with complex argument structures

#### **Sets and Intervals** (adding; 15.14.0)

- Modules `sets_handler` and `interval_handler`:
  - Add foundation for nested structure handling:
    - Import `flatten_list` for future nested set and interval processing
    - Enhanced data structure flexibility

### Changed (15.14.0)

#### **General** (changing; 15.14.0)

- **PEP-604 Type Annotation Modernisation**: Systematic update of type hints across modules
  - Replace `str or list` with modern `str | list[str]` syntax
  - Enhanced type specificity with generic type parameters
  - Improved IDE support and static type analysis

#### **Strings** (changing; 15.14.0)

- Modules `string_handler` and `text_formatters`:
  - Apply PEP-604 union syntax to function parameters:
    - `substring : str or list-like of str` → `substring : str | list[str]`
  - Add nested list support:
    - `find_substring_index()`: Handle nested substring lists
    - `format_table_from_list()`: Process nested data in table formatting

#### **Time Handling** (changing; 15.14.0)

- Modules `calendar_utils`, `date_and_time_maths`, `date_and_time_utils`, `time_formatters`, `time_utils`, and `program_snippet_exec_timers`:
  - Apply PEP-604 union syntax to function docstrings:
    - `file_path : str or list of str` → `file_path : str | list[str]`
  - Add nested list support for:
    - File path processing in timestamp operations
    - Date/time object collections in mathematical operations
    - Complex nested data structures in calendar operations

#### **Number Bases** (changing; 15.14.0)

- Modules `maths`, `base_converters`, `binary_operations`, and `mathematical_utils`:
  - Apply PEP-604 union syntax to all function docstrings
  - Enhanced type clarity for numerical operations and conversions

---

## [15.13.5] - 2025-06-05

### Changed (15.13.5)

#### **Time Handling** (changing; 15.13.5)

- Module `countdown.py`: force-flush the output buffer after each print statement with carriage return to display cleaner outputs.

---

## [15.13.4] - 2025-06-03

### Added

#### **Time Handling** (adding; 15.13.4)

- Module `time_formatters`:
  - Enhance internal `_format_arbitrary_dt` function with more granular time formatting options:
    - Minutes and seconds only format
    - Seconds only format

---

## [15.13.3] - 2025-05-22

### Fixed (15.13.4)

#### **Time Handling** (fixing; 15.13.3)

- Module `time_formatters`:
  - Enhance `parse_dt_string` function to properly handle non-string inputs:
    - Add type checking before applying string methods when `module="pandas"`
    - Update docstring to clarify that when using the pandas module, the function accepts various object types:
      - Python datetime objects
      - NumPy datetime64 objects
      - Integer/float timestamps
      - Series objects
      - DataFrame columns
      - Lists or arrays of timestamps
    - Maintain backwards compatibility with existing code

---

## [15.13.2] - 2025-05-21

### Added (15.13.2)

#### **Operative Systems** (adding; 15.13.2)

- Module `os_operations`:
  - Added `text` parameter support to `run_system_command` function:
    - Only applicable when using `(module, _class)` combos that equal `("subprocess", "run")` or `("subprocess", "Popen")`.
    - Controls whether subprocess output is returned as strings rather than bytes.
    - If set to `None` (default), the value is determined by whether encoding is provided.

---

## [15.13.1] - 2025-05-10

### Added (15.13.1)

#### **Number Bases** (adding; 15.13.1)

- Add module `mathematical_utils`:
  - Hosts functions for mathematical operations and number formatting.
  - Add `adapted_factorial` function for formatted factorial calculations, supporting extremely large numbers.

### Fixed (15.13.1)

#### **Time Handling** (fixing; 15.13.1)

- Module `time_formatters`:
  - Fixed `parse_dt_string` function to properly handle parameter conflicts:
    - Resolved issue with simultaneous use of `format` and `unit` parameters in `pandas.to_datetime`
    - Removed unused `unit` parameters from lambda functions
  - Enhanced functionality:
    - Made `dt_fmt_str` optional with `None` default
    - Added smart parameter selection based on input type
    - Improved error messages and documentation
  - Maintained backwards compatibility

---

## [15.13.0] - 2025-05-09

### Added (15.13.0)

#### **Audio and Video** (adding; 15.13.0)

- Module `audio_and_video_manipulation`:
  - Added `overwrite` parameter to control file overwriting behaviour in ffmpeg commands:
    - `overwrite=True` (default): overwrite the output file, setting the `-y` flag in the ffmpeg command.
    - `overwrite=False`: prevent overwriting and raise an error if the file already exists, setting the `-n` flag in the ffmpeg command.
  - Added progress visualization to all functions showing which file is currently being processed (e.g., "Creating merged file 2/10...")
  - Improved display of file counts when merging multiple files, showing total number and file type

- Modules `merge_audio_and_video`, `merge_audio_or_video` and `trim_media`:
  - Add the `overwrite` parameter to the calling functions.

### Changed (15.13.0)

#### **Operative Systems** (changing; 15.13.0)

- Module `os_operations`:
  - Enhanced `exit_info` function to handle various output capture scenarios and object types (dict/CompletedProcess), with improved error handling and fallbacks

#### **Audio and Video** (changing; 15.13.0)

- Module `audio_and_video_manipulation`:
  - Improved system command execution in `merge_media_files`, `merge_individual_media_files`, and `cut_media_files` to properly handle cases where command output isn't captured.

---

## [15.12.9] - 2025-05-08

### Added (15.12.9)

#### **Audio and Video** (adding; 15.12.9)

- Module `audio_and_video_manipulation`:
  - Added `_escape_path` helper function using `shlex.quote` to properly escape file paths with spaces and special characters in shell commands
  - Enhanced `_load_file_list` to support direct file path strings, improving API flexibility
  - Added the following internal helper functions to centralise file validation logic:
    - `_validate_files`
    - `_is_audio_file`
    - `_is_video_file`

### Changed (15.12.9)

#### **Audio and Video** (changing; 15.12.9)

- Module `audio_and_video_manipulation`:
  - Improve `ffmpeg` command handling:
    - Centralise file loading functions into internal `_load_file_list` helper
    - Add support for direct file paths and nested lists
    - Add `-y` flag to prevent overwrite prompts
    - Improve error handling and path escaping
  - Improve code quality:
    - Use more descriptive variable names
    - Remove redundant string formatting
    - Add flexible command execution parameters

- Modules `merge_audio_and_video`, `merge_audio_or_video` and `trim_media`:
  - Add command execution parameters as constants:
    - `CAPTURE_OUTPUT`
    - `RETURN_OUTPUT_NAME`
    - `ENCODING`
    - `SHELL`
  - Update calling function to use the new constants

- Module `trim_media`:
  - Besides above changes, lowercase `zero_padding` instead of uppercase `ZERO_PADDING` where it is used as an input parameter in the calling function.

#### **Operative Systems** (changing; 15.12.9)

- Module `os_operations`:
  - Enhanced `subprocess_run_helper` to print `stderr` before raising `CalledProcessError` for better error diagnosis.
  - Improved `exit_info` function to display both `stdout` and `stderr` when available.
  - Better handling of commands like `ffmpeg` that use `stderr` for normal output while maintaining successful exit status.

---

## [15.12.6] - 2025-05-07

### Changed (15.12.6)

#### **Audio and Video** (changing; 15.12.6)

- Module `audio_and_video_manipulation`:
  - Update import to use `parse_dt_string` instead of the deprecated `parse_time_string` from the module `time_formatters`.
  - Add support for `None` as a valid value for the `zero_padding` parameter in both `merge_media_files` and `cut_media_files` functions, disabling padding when generating default output filenames.

### Fixed (15.12.1)

#### **Audio and Video** (fixing; 15.12.6)

- Module `merge_audio_and_video`:
  - Correct the import path for the function `find_files` from the `filewise` package.
  - Correct the argument `output_file_name_list` to `output_file_list` as supported by the function `merge_media_files`.
  - Lowercase the argument `ZERO_PADDING` (not the constant), as that is considered as a parameter in the function `merge_media_files`.
  - Replace the suffix `_GLOBSTR` with `_PATTERN` as the former does not reflect a wildcarded string anymore.
  - Remove the wildcard asterisk from the constants with the updated suffix, as the function `find_files` implements wildcards.

- Module `merge_audio_or_video`:
  - Expose the `safe` parameter to allow toggling ffmpeg safe mode when merging media files.
  - Remove the `ZERO_PADDING` parameter, as it is not supported by the function `merge_individual_media_files`.

#### **Strings** (fixing; 15.12.6)

- Module `text_formatters`: ensure the result from `find_substring_index` is always handled as a list in the `format_string` function, preventing errors when formatting strings with a single pair of brackets.

#### **Time Handling** (fixing; 15.12.6)

- Module `time_formatters`: correct the name of the deprecated function: from `parse_time_string` to `parse_dt_string`.

### Deprecated

#### **Time Handling** (deprecating; 15.12.6)

- Module `time_formatters`:
  - Function `parse_time_string` is deprecated in favor of `parse_dt_string`

---

## [15.12.1] - 2025-05-06

### Changed (15.12.1)

#### **Operative Systems** (changing; 15.12.1)

- Module `os_operations`:
  - Improve code readability by only passing `return_output_name` to `subprocess.Popen`
  - Update `run_system_command` docstring to clearly specify parameter applicability
  - Remove unused `return_output_name` parameter from helper functions where not applicable
  - Add conditional logic in `run_system_command` to handle parameter appropriately

---

## [15.12.0] - 2025-05-05

### Added (15.12.0)

#### **Time Handling** (adding; 15.12.0)

- Module `time_utils`:
  - Add the following internal and public functions to the module:
    - Internal:
      - `_convert_floated_time_to_datetime`
      - `_nano_floated_time_str`
    - Public:
      - `get_datetime_object_unit`
      - `get_nano_datetime`
  - The addition implies breaking a circular dependency.

### Changed (15.12.0)

#### **Time Handling** (changing; 15.12.0)

In general, several changes have been made to break a circular dependency.

- Module `calendar_utils`:
  - Move imports of the functions `interp_pd` and `interp_xr` inside the function `standardise_calendar`.

### Fixed (15.12.0)

#### **Time Handling** (fixing; 15.12.0)

- Module `date_and_time_utils`:
  - Correct the module name from which the function `datetime_obj_converter` is imported.
  - Move the following public and internal functions from `date_and_time_utils` to `time_utils`:
    - Public functions:
      - `get_datetime_object_unit`
      - `get_nano_datetime`
    - Internal functions:
      - `_convert_floated_time_to_datetime`
      - `_nano_floated_time_str`

- Module `time_formatters`:
  - Reinstate (correct) import of functions `get_datetime_object_unit` and `get_nano_datetime` from module `date_and_time_utils.py` to `time_utils.py`.

---

## [15.11.3] - 2025-05-02

### Changed (15.11.3)

#### **Time Handling** (changing; 15.11.3)

- Module `time_formatters.py`:

  - Rename objects containing `(date)time` to `dt` for date-time operations

    | Type | Original Name | New Name | Description |
    |:----:|:-------------:|:--------:|:-----------:|
    | Public Function | `parse_float_time` | `parse_float_dt` | Main function for parsing float values to datetime objects |
    | Internal Function | `_float_time_parser` | `_float_dt_parser` | Parser for converting float values to datetime objects |
    | Internal Function | `_format_arbitrary_time` | `_format_arbitrary_dt` | Formatter for arbitrary datetime values |
    | Internal Function | `_total_time_unit` | `_total_dt_unit` | Converter for datetime objects to total time units |
    | Internal Function | `_total_time_complex_data` | `_total_dt_complex_data` | Handler for complex data types with datetime values |

    Functions kept with `time` in their names as they handle time-only operations:

    | Type | Name | Description |
    |:----:|:----:|:-----------:|
    | Internal Function | `__time_component_to_float` | Specifically deals with time components |
    | Internal Function | `_to_time_struct` | Specifically deals with time structure |

    Constants renamed:

    | Original Name | New Name | Description |
    |:-------------:|:--------:|:-----------:|
    | `DATETIME_OBJ_CONVERSION_DICT` | `DT_OBJ_CONVERSION_DICT` | Dictionary of functions for converting datetime objects to various formats |
    | `DATETIME64_OBJ_CONVERSION_DICT` | `DT64_OBJ_CONVERSION_DICT` | Dictionary of functions for converting datetime64 objects to various formats |
    | `DATETIME_TIME_OBJ_CONVERSION_DICT` | `DT_TIME_OBJ_CONVERSION_DICT` | Dictionary of functions for converting datetime objects to time objects |

- Module `countdown`:
  - Rename public function `return_time_string_parts` to `return_dt_string_parts` as it handles both dates and times.

- Module `date_and_time_maths`:
  - Rename the following public functions as they handle both dates and times, while improving conciseness:

  | Original Name | New Name |
  |:-------------:|:--------:|
  | `extract_datetime_part` | `extract_dt_part` |
  | `sum_dt_times` | `sum_dt_objects` |
  | `dt_time_average` | `dt_average` |
  | `_time_to_radians` | `_dt_to_radians` |

- Module `date_and_time_utils`:
  - Rename public function `find_time_key` to `find_dt_key` as it handles both dates and times.

### Deprecated (15.11.3)

#### **Time Handling** (deprecating; 15.11.3)

- Module `time_formatters`:
  - The following functions are deprecated in favor of their `dt`-prefixed versions:
    - `parse_float_time` → `parse_float_dt`
    - `_float_time_parser` → `_float_dt_parser`
    - `_format_arbitrary_time` → `_format_arbitrary_dt`
    - `_total_time_unit` → `_total_dt_unit`
    - `_total_time_complex_data` → `_total_dt_complex_data`
  - The following constants are deprecated in favor of their `DT`-prefixed versions:
    - `DATETIME_OBJ_CONVERSION_DICT` → `DT_OBJ_CONVERSION_DICT`
    - `DATETIME64_OBJ_CONVERSION_DICT` → `DT64_OBJ_CONVERSION_DICT`
    - `DATETIME_TIME_OBJ_CONVERSION_DICT` → `DT_TIME_OBJ_CONVERSION_DICT`

- Module `countdown`:
  - Function `return_time_string_parts` is deprecated in favor of `return_dt_string_parts`

- Module `date_and_time_maths`:
  - The following functions are deprecated in favor of their new names:
    - `extract_datetime_part` → `extract_dt_part`
    - `sum_dt_times` → `sum_dt_objects`
    - `dt_time_average` → `dt_average`
    - `_time_to_radians` → `_dt_to_radians`

- Module `date_and_time_utils`:
  - Function `find_time_key` is deprecated in favor of `find_dt_key`

**NOTE** (15.11.3)

- **All above changes regarding public functions have been applied to all affected modules.**

---

## [15.11.2] - 2025-05-01

### Fixed (15.11.2)

#### **Time Handling** (fixing; 15.11.2)

- Module `calendar_utils`: update import from `statkit` to `statflow` package to reflect the package's new name.

---

## [15.11.1] - 2025-04-27

### Changed (15.11.1)

#### **General** (changing; 15.11.1)

- Modify the comment header `Import custom modules` to `Import project modules` in all modules having it.

#### **Audio and Video** (changing; 15.11.1)

- Convert all **constant names** under the header `Define parameters` to uppercase in the following files:
  - `merge_audio_and_video.py`
  - `merge_audio_or_video.py`
  - `trim_media.py`

#### **Strings** (changing; 15.11.1)

- Module `string_handler`: modify the constant `splitdelim` to `SPLIT_DELIM`.

---

## [15.11.0] - 2025-04-25

### Added (15.11.0)

#### **Time Handling** (adding; 15.11.0)

- Module `date_and_time_utils`:
  - Add back the function `find_time_key`, moved to the module `time_utils.py` in version 15.10.0, as it semantically suits better in this module.

### Changed (15.11.0)

#### **General** (changing; 15.11.0)

- Replace direct imports with `__all__` definition in all sub-packages:
  - `arrays_and_lists`
  - `audio_and_video`
  - `dictionaries`
  - `number_bases`
  - `operative_systems`
  - `sets_and_intervals`
  - `strings`
  - `time_handling`

#### **Arrays and Lists** (changing; 15.11.0)

- Modules `data_manipulation`, `maths` and `patterns`:
  - Convert constant names to uppercase and update references

#### **Audio and Video** (changing; 15.11.0)

- Module `audio_and_video_manipulation`:
  - Convert constant names to uppercase and update references

#### **Dictionaries** (changing; 15.11.0)

- Modules `dict_handler` and `dict_operators`:
  - Convert constant names to uppercase and update references
  - Add parameter validation and improve sorting functionality

#### **Number Bases** (15.13.0)

- Modules `base_converters` and `binary_operations`:
  - Convert constant names to uppercase and update references

#### **Operative Systems** (changing, v15.11.0)

- Module `os_operations`:
  - Convert constant names to uppercase and update references
  - Convert imported constants from `global_parameters.py` to uppercase

#### **Sets and Intervals**

- Module `sets_handler`:
  - Convert constant names to uppercase and update references
  - Convert imported constants from `global_parameters.py` to uppercase
  - Sort project modules alphabetically

- Module `interval_handler`:
  - Convert constant names to uppercase and reorganise imports
  - Add parameter validation and fix constructor bug

#### **Strings** (changing)

- Module `text_formatters`:
  - Convert constant names to uppercase and update references
  - Sort project modules alphabetically

#### **Time Handling** (changing)

- Module `time_formatters`:
  - Convert constant names to uppercase and update references
  - Convert imported constants from `global_parameters.py` to uppercase
  - Sort modules according to PEP 8 standards

- Modules `date_and_time_utils` and `program_snippet_exec_timers`:
  - Convert constant names to uppercase and update references
  - Reorganise imports and sort modules according to PEP 8 standards

- Modules `date_and_time_maths` and `countdown`:
  - Convert constant names to uppercase and update references

### Removed

#### **Time Handling** (removing)

- Module `time_utils`: after moving the function `find_time_key` to the module `date_and_time_utils`, it is no longer needed and it was removed.

---

## [15.10.0] - 2025-04-21

### Added (15.10.0)

#### **Time Handling** (15.10.0)

- Module `time_utils`: move the function `find_time_key` from the module `date_and_time_utils` to avoid circular dependency.

### Changed (15.10.0)

#### **Arrays and Lists** (15.10.0)

- Module `data_manipulation`:
  - Move the function `decompose_cumulative_data` to the module `time_series` in the package `statkit` to avoid circular dependency.

---

## [15.9.1] - 2025-04-17

### Fixed (15.9.1)

#### **Time Handling** (fixing; 15.9.1)

- Module `calendar_utils`: replace non-existent `find_time_dimension` import with available `get_file_dimensions` function and add handling for list return type.

- Module `date_and_time_maths`: replace wrong package import for `select_elements` function.

---

## [15.9.0] - 2025-04-12

### Changed (15.9.0)

#### **General** (changing; 15.9.0)

- Rename all variable names that start with `arg_tuple` to `format_args` to follow a more consistent naming convention `format_args` prefix.

### Fixed (15.9.0)

#### **Time Handling** (fixing; 15.9.0)

- Module `calendar_utils`: replace non-existent `find_time_dimension` import with available `get_file_dimensions` function and add handling for list return type.

---

## [15.8.1] - 2025-03-29

### Changed (15.8.1)

#### **General** (changing; 15.8.1)

- Further update comments and variable names to replace `syntax` and `command` with `template`.

---

## [15.8.0] - 2025-03-23

### Added (15.8.0)

#### **Audio and Video** (adding; 15.8.0)

- Module `audio_and_video_manipulation`: add import for `find_files` from the `filewise` package to enable dynamic file discovery.

### Changed (15.7.6)

#### **General** (changing; 15.8.0)

- Update terminology from `Preformatted Strings` to `Template Strings` in headers and variables.
  - On that basis, rename name 'preformatted' to 'template' in headers and variables wherever necessary.
  - Update comments and variable names to replace `syntax` and `command` with `template` for better clarity in describing variables and constants that use empty `{}` for formatting.

#### **Audio and Video** (changing; 15.8.0)

- Module `audio_and_video_manipulation`:
  - Renamed functions for clarity: `merge_audio_and_video_files` to `merge_media_files`, and `merge_audio_or_video_files` to `merge_individual_media_files`.
  - Improved argument naming.
- Module `trim_media`:
  - Rename from `cut_media_files` to avoid conflicts.
  - Update `zero_padding` to `ZERO_PADDING` and improve quality settings.
- Modules `merge_audio_and_video` and `merge_audio_or_video`:
  - Enhance script flexibility with dynamic file handling.
  - Update variable names for clarity and consistency.

### Removed (15.8.0)

#### **Audio and Video** (removing; 15.8.0)

- Deleted the old `cut_media_files` module as it has been renamed to `trim_media`.

---

## [15.7.7] - 2025-02-18

### Changed (15.7.7)

#### **General** (changing; 15.7.7)

- For all relevant modules, perform several term replacements:
  - Replace `method` with `procedure` to more accurately describe the approach or technique used in functions, except when referring to class method calls.
  - Replace `action` with `procedure` to align with the context of operations being performed.
  - Additionally, these changes improve clarity by ensuring consistent terminology, making it clear that functions can employ different procedures to achieve their goals.

These changes enhance terminology consistency in all affected modules. No user-facing changes are expected, hence only the patch number is incremented.

---

## [v15.7.0] - 2025-02-03

### Added (v15.7.0)

#### **Number Bases** (v15.7.0)

- Module `base_converters`:
  - Added helper function `_check_input_binary` to check if the input binary number is in the correct format.
  - Introduce two basic functions to convert between base 10 and base 2: `dec2bin_basic` and `bin2dec_basic`. Both perform mathematical computations by definition.

#### **Arrays and Lists** (v15.7.0)

- Module `data_manipulation`: add flipping utilities of lists and NumPy arrays with N >= 1 dimensions.

### Changed (v15.7.0)

#### **General** (v15.7.0)

- Peform several term replacements in many modules:
  - `method` with `function`, if no object is instantiated throughout the module.
  - `method` with `procedure` (or `algorithm`/`module`), to more accurately describe the approach or technique used in functions.
  Additionally, this change effectively communicates that a function can employ different methods or techniques to achieve its goal.

---

## [15.6.0] - 2024-12-18

### Changed (15.6.0)

#### **Strings** (15.6.0)

- Module `string_handler`: enhanced substring search logic: returns single data object for one match, (-1, -1) for no matches, and enforces {"lo", "hi", "both"} for index return options.

---

## [15.5.0] - 2024-11-23

### Changed (15.5.0)

#### **Arrays and Lists** (15.5.0)

- Module `data_manipulation`: enhance `remove_elements` function to support multiple indices for list inputs.

### Fixed (15.5.0)

#### **Time Handling** (15.5.0)

- Module `calendar_utils`: corrected the absolute path in the import of the `unique_type_objects` function.

---

## [15.4.4] - 2024-11-17

### Changed (15.4.4)

#### **General** (15.4.4)

- Minor syntax appearance improvements in many modules.

#### **Strings** (15.4.4)

- Renamed module `information_output_formatters` to `text_formatters` for improved clarity. Changes have been applied for all affected modules.

#### **Time Handling** (15.4.4)

- Module `date_and_time_utils`:
  - Added timezone handling to `get_current_datetime` function with optional 'pytz' support
  - Added `display_user_timestamp` function with conditional timezone support.
  - Enhanced module with global timezone handling using a `pytz` availability check.
  - Minor refactoring and structure reorganization for improved modularity.

---

## [15.3.0] - 2024-11-14

### Changed (15.3.0)

#### **Web Scraping**

- Renamed the sub-pakcage to `web_automation` for broader web automation use.
- After performing the operation, moved it from `pygenutils` package to `DataOpsHub` package.

---

## [15.2.0] - 2024-11-03

### Added (15.2.0)

- Added `__init__.py` files to all first-level and deeper sub-packages for enhanced import access.

### Changed (15.2.0)

- Remove the redundant import of the deprecated and removed `parameters_and_constants` module in all affected modules.

---

## [15.0.0] - 2024-10-30

### Changed (15.0.0)

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
    - `databases`        | → `DataOpsHub`
    - `security`         |

- Once all above changes made, absolutely all imports have been updated to match the package where a sub-package or module is.

---

## [14.0.0] - 2024-10-28

### Changed (14.0.0)

#### **Changes in functions along modules and sub-packages**

##### **Varnames**

- Variable name `all_arg_names`, which contains all variables (required and optional) of the caller function, has been renamed to `param_keys`.
  - All this changes have been applied to all affected modules.

#### **Specific changes regarding sub-packages**

##### **Dictionaries** (14.0.0)

- Module `table_formatters`:
  - Moved all functions to the module `information_output_formatters` (**Strings** sub-package)

##### **General File Utils**

- Module `introspection_utils`:
  - Renamed the following functions

  | Original Function Name | Refactored Function Name |
  |:----------------------:|:------------------------:|
  | `retrieve_function_name` | `get_func_name` |
  | `get_function_args` | `get_func_args` |
  | `get_function_all_args` | `get_all_func_args` |
  | `get_full_function_signature` | `get_func_signature` |
  | `get_caller_function_args` | `get_caller_args` |
  | `get_caller_function_all_args` | `get_all_caller_args` |
  | `get_full_caller_function_signature` | `get_caller_signature` |
  | `get_attribute_names` | `get_attr_names` |
  | `get_obj_type_str` | `get_type_str` |

##### **Format Converters**

- Module `file_format_tweaker`:
  - Renamed the following functions

  | Old function name | New function name |
  |:----------------:|:-----------------:|
  | `check_essential_prog_installation` | `_check_essential_progs` (marked as internal) |
  | `pdf_file_tweaker` | `file_tweaker` |
  | `pdf_file_compressor` | `file_compressor` |
  | `merge_pdf_files` | `merge_files` |
  | `eml2pdf` | `eml_to_pdf` |
  | `msg2pdf` | `msg_to_pdf` |

- All this changes have been applied to all affected modules.
- After having these changes made, the module has been **renamed** to `pdf_tools`.

##### **Operative systems**

- Module `OS Operations`
  - In function `run_system_command`, default value of argument `encoding` was changed from `None` to `utf-8`.
    - This change has been applied in every affected module.

##### **Strings** (15.3.0)

- Module `string_handler`: Renamed the following functions:

  | Old function name | New function name |
  |:-----------------:|:-----------------:|
  | `add_str_to_path` | `add_to_path` |
  | `ext_adder` | `append_ext` |

- All this changes have been applied to all affected modules.

#### **Changes in sub-package names**

- The following renamings have been performed:

  | Old package name | New package name |
  |:----------------:|:-----------------:|
  | `geospatial_tools` | `geosptools` |
  | `parameters_and_constants` | `paramlib` |
  | `multilingual_text_processing` | `LinguaLab` |

---

## [13.3.2] - 2024-10-25

### Changed (13.3.2)

#### **Changes in functions along modules and sub-packages** (13.3.2)

##### **General** (13.3.2)

- Switched to British English every verb written in American accent. For example:
  - *standardize* → 'standardi**S**e'
  - *serialize* → 'seriali**S**e'

- All `.lower()` instances of the string returned by the function `get_obj_type_str` (module `introspection_utils`, sub-package **General Utils**),  
  have been substituted in favour of setting the argument `lowercase` to True.
  
- The renaming of the module `file_and_directory_handler` to `ops_handler` has been applied to all affected files.
- The renaming of the module `file_and_directory_paths` to `path_utils` has been applied to all affected files.

##### **Climate Data Utils**

- Module `cdo_tools`:
  - Refactored multiple CDO processing functions, optimised internal helpers, and updated file handling functions with section headers and internal visibility changes.
  - Renamed the following functions:

  | Old function name | New function name |
  |:----------------:|:-----------------:|
  | `get_variable_name_in_file_name` | `_get_varname_in_filename` (marked as internal) |
  | `change_file_names_byvar` | `change_filenames_by_var` |
  | `standardise_file_name` | `_standardise_filename` (marked as internal) |

##### **Specific changes regarding sub-packages** (13.3.2)

- The following renamings have been made:

  | Old package name | New package name |
  |:----------------:|:-----------------:|
  | `climate_data_utils` | `climalab` |
  | `statistics` | `statkit` |
  | `utilities` | `filewise` |
  | `complementary-to_remodule` | `supplementary_tools` |

- All these changes have been applied to all affected modules.

---

## [13.0.0] - 2024-10-22

### Changed (13.0.0)

#### **File Operations**

##### **Module 'file_and_directory_handler'**

- Refactored and optimised file and directory operations; consolidated functions, introduced helper functions, and removed shell command dependencies.

- Renamed the following functions:

  | Old function name | New function name |
  |:----------------:|:-----------------:|
  | `move_files_by_ext_from_exec_code` | `move_files` |
  | `copy_files_by_ext_from_exec_code` | `copy_files` |
  | `remove_files_by_ext` | `remove_files` |
  | `move_entire_directories` | `move_directories` |
  | `copy_entire_directories` | `copy_directories` |
  | `remove_entire_directories` | `remove_directories` |
  | `make_parent_directories` | `make_directories` |
  | `move_files_by_globstr_from_exec_code` | `move_files` |
  | `copy_files_by_globstr_from_exec_code` | `copy_files` |
  | `remove_files_by_globstr` | `remove_files` |
  | `rsync` | (unchanged) |
  | `rename_objects` | (unchanged) |

- All this changes have been applied to all affected modules.
- After having these changes made, the module has been **renamed** to simply `ops_handler`.

##### **Module 'file_and_directory_paths'**

- Refactored file and directory path search logic; introduced switch-case for match_type, shortened function names, and optimised code.

- The following functions have been merged and renamed:

  | First function | Second function | Merged function name |
  |:--------------:|:---------------:|:--------------------:|
  | `find_files_by_ext` | `find_files_by_globstr` | `find_files` |
  | `find_all_directories` | `find_all_file_extensions` | `find_items` |
  | `find_file_containing_dirs_by_ext` | `find_file_containing_dirs_by_globstr` | `find_dirs_with_files` |

- All this changes have been applied to all affected files.
- After having these changes made, the module has been **renamed** to `path_utils`.

---

## [12.0.0] - 2024-10-18

### Changed (12.0.0)

#### **Arrays and Lists** (12.0.0)

##### **Module 'conversions'**

- Optimised data conversion and flattening functions, improved handling of pandas and NumPy objects, added error handling, and streamlined code structure.

- Renamed the following functions:

  | Old function name | New function name |
  |:----------------:|:-----------------:|
  | `basic_value_data_type_converter` | `convert_data_type` |
  | `list_array_to_std_array` | `combine_arrays` |
  | `flatten_content_to_string` | `flatten_to_string` |

##### **General Utilities**

##### **'file_operations' sub-package**

- The following **module** renamings have been made:

  | Old function name | New function name |
  |:----------------:|:-----------------:|
  | `bulk_rename_index_main` | `bulk_rename_auto` |
  | `bulk_rename_index_manual` | `bulk_rename_manual` |

##### **'scripts' sub-package**

- Contains application programs of several functions in the modules of sub-package `file_operations`.

- The following **module** renamings have been made:

  | Old function name | New function name |
  |:----------------:|:-----------------:|
  | `change_permissions_exec` | `modify_properties` |
  | `pdf_file_compressor_exec` | `compress_pdf` |
  | `pdf_file_tweaker_exec` | `tweak_pdf` |
  | `bulk_rename_index_exec` | `bulk_rename` |

##### **Databases**

- Rename module `upload_data_to_mysql_database` to `upload_data`.

### Removed (15.10.0)

- After the renamings the following modules have been removed:
  - `bulk_rename_index_exec`
  - `bulk_rename_index_main`
  - `bulk_rename_index_manual`
  - `change_permissions_exec`
  - `pdf_file_compressor_exec`
  - `pdf_file_tweaker_exec`
  - `upload_data_to_mysql_database`

---

## [11.0.0] - 2024-10-17

### Changed (11.0.0)

#### **Arrays and Lists** (11.0.0)

- Module `data_manipulation`
  - Optimised and grouped functions by categories, added support for pandas objects, and improved docstrings.
  - In functions `sort_rows_by_column` and `sort_columns_by_row`, argument `sort_order` has been substituted by `reverse`, where its mechanism is the same as for lists.
  - function `decompose_24h_cumulative_data`:
    - Rename to `decompose_cumulative_data`.
    - Introduce a new `fill_value` parameter to allow the user to choose how to handle negative differences.

#### **File Utils**

- Module `change_permissions_main`:
  - Refactored function `modify_obj_permissions` to allow no-change option for permissions and improved detection of files/directories.
  - Enhanced `modify_obj_owner` with no-change defaults for owner/group, flexible ID handling, and improved error handling.
  - After performing these changes, rename the module to `permission_manager`.

#### **Xarray Utils**

- Module `data_manipulation`:
  - Shortened function/variable names, optimised code, added docstrings.
  - Renamed the following functions:

  | Old function name | New function name |
  |:----------------:|:-----------------:|
  | `extract_and_store_latlon_bounds` | `extract_latlon_bounds` |
  | `extract_and_store_period_bounds` | `extract_time_bounds` |
  | `extract_and_store_time_formats` | `extract_time_formats` |

- Moved function `create_ds_component` from module `data_manipulation` to `xarray_obj_handler`.

### Removed (11.0.0)

- After the displacement of the function `create_ds_component`, `change_permissions_main` module was removed.

---

## [10.11.3] - 2024-10-12

### Added (10.11.3)

#### **Core Statistics**

- Created `interpolation_functions` module with `interpolate_numpy`, `interpolate_pandas`, and `interpolate_xarray` for flexible interpolation across various object types.

### Changed (10.11.3)

#### **Climatology Statistics**

- Module `representative_series`
  - Delegate interpolation logic for numpy, pandas and xarray objects to module `interpolation_functions` (**Core Statistics**).

#### **Time Handling** (10.11.3)

- function `standardize_calendar`:
  - Rename to British English nomenclature: `standardise_calendar`.
  - Optimised by refactoring type handling.
  - Delegate interpolation logic for numpy, pandas and xarray objects to module `interpolation_functions` (**Core Statistics**).

#### **Geospatial Tools**

- In module `geospatial_tools`, rename function `netcdf2raster` to `nc2raster`.

---

## [10.9.2] - 2024-10-11

### Added (10.9.2)

#### **General Utilities** (10.9.2)

- `introspection_utils`: function `get_obj_type_str` now accepts the argument lowercase to change the case of the object type's name to lower.

### Changed (10.9.2)

#### **Sets and Intervals** (10.9.2)

- Modules
  - `interval_operators` and `operators_sets` have been renamed to `interval_handler`and `sets_handler` to align better conceptually.
  - Refactored the `interval_operators` to support switch-case dictionaries, improved `union` behaviour with `force_union` parameter for true unions.
- functions
  - Refactored `operations_with_sets`, streamlined operations with `default` and `sympy` constructors using switch-case dictionaries.
  - After that, renamed the function to `sets_operator`.

#### **Core Statistics** (10.9.2)

- function `polynomial_fitting` has been moved from module `curve_fitting` to `interpolation_functions`.

#### **Time handling** (10.9.2)

- Module `date_and_time_utils`:
  - Merged and optimised functions for inferring frequency, date ranges, and finding date/time keys across pandas and NetCDF/xarray objects with lazy xarray imports.

- **NOTE**: although every function has been moved to this module, except in one case the function pairs have been named identically,  
so it is worth describing their origins, referring to the latest version in which these moves have been performed (to this module).

| Function name 1 | Module referring to 1 | sub-package referring to 1 | Function name 2 | Module referring to 2 | sub-package referring to 2 | Merged function name |
|:--------------:|:--------------------:|:------------------------:|:--------------:|:--------------------:|:------------------------:|:--------------------:|
| `find_date_key` | `data_frame_handler` | `pandas_data_frames/core` | `find_time_dimension` | `netcdf_handler` | `weather_and_climate` | `find_time_key` |
| `infer_full_period_of_time` | `data_frame_handler` | `pandas_data_frames/core` | `infer_full_period_of_time` | `netcdf_handler` | `weather_and_climate` | `infer_dt_range` |
| `infer_time_frequency` | `data_frame_handler` | `pandas_data_frames/core` | `infer_time_frequency` | `netcdf_handler` | `weather_and_climate` | `infer_frequency` |

### Removed (10.9.2)

- After the displacement of the function `polynomial_fitting`, `curve_fitting` module was removed.

---

## [10.4.0] - 2024-10-06

### Changed (10.4.0)

- The following functions in **Xarray Utils** have been merged into a single one:
  - `find_time_dimension` and `find_time_dimension_raise_none` → `find_time_dimension`.
  - `find_coordinate_variables` and `find_coordinate_variables_raise_none` → `find_coordinate_variables`.

- As a consequence, the following modules which originally used `find_time_dimension_raise_none` and/or `find_coordinate_variables_raise_none` have been adapted:
  - **Climate Data Utils**: `cdo_tools`
  - **Xarray Utils**: `patterns` and `data_manipulation`

- Rename module `date_and_time_operators` to `date_and_time_utils` to emphasise 'utility' or 'tool' concept; originally in sub-package `time_handling`, no displacement.

### Removed (10.4.0)

- Delete sub-package `varied_documentation` as its content has been relocated to a local directory.

---

## [10.0.0] - 2024-10-02

### Added (10.0.0)

- Add the following directories and modules in `statistics` sub-package:
  - **Core Statistics**
    - `signal_processing`: signal processing functions (signal whitening, low-pass, high-pass, and band-pass filters).

- Add the following directories and modules in `utilities` sub-package:
  - **Pandas Utils**
    - `conversions`: module designed to handle pandas object type conversions, starting with DataFrame to NumPy`s structured array conversion.
    - `data_manipulation`: higher-level data manipulations using pandas.
    - `pandas_obj_handler`: handles various file operations for pandas DataFrames, including reading, merging, and saving Excel, CSV, and ODS files, with support for handling duplicated sheet names, managing file overwrites, and customizing output formats.
  - **Xarray Utils**
    - `conversions`: module designed to handle xarray object type conversions, starting with GRIB to netCDF conversion.
    - `data_manipulation`: higher-level data manipulations using xarray.
    - `file_utils`: comprehensive utilities for scanning, validating, and managing netCDF files.
    - `patterns`: utility functions for coordinate, time, and model data handling, enhancing flexibility, error handling, and performance.
    - `xarray_obj_handler`: optimised module for saving xarray Datasets and DataArrays to NetCDF and CSV, with enhanced handling of variable dimensions, attributes, and spatial coordinates.

### Changed (10.0.0)

- After the creations in **Core Statistics**, the following changes have been made:

#### **Functions**

In `statistics` sub-package:

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `signal_whitening` | `time_series` | `statistics/core` | (unchanged) | `signal_processing` | (unchanged) |
  | `low_pass_filter` | `time_series` | `statistics/core` | (unchanged) | `signal_processing` | (unchanged) |
  | `high_pass_filter` | `time_series` | `statistics/core` | (unchanged) | `signal_processing` | (unchanged) |
  | `band_pass1` | `time_series` | `statistics/core` | (unchanged) | `signal_processing` | (unchanged) |
  | `band_pass2` | `time_series` | `statistics/core` | (unchanged) | `signal_processing` | (unchanged) |
  | `band_pass3` | `time_series` | `statistics/core` | (unchanged) | `signal_processing` | (unchanged) |

- After the creations in **Xarray Utils**, the following changes between sub-packages have been made:

1.1. To `time_handling` and `data_manipulation`:

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `create_ds_component` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `data_manipulation` | `utilities/xarray_utils` |
  | `extract_and_store_latlon_bounds` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `data_manipulation` | `utilities/xarray_utils` |
  | `extract_and_store_period_bounds` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `data_manipulation` | `utilities/xarray_utils` |
  | `extract_and_store_time_formats` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `data_manipulation` | `utilities/xarray_utils` |
  | `netcdf_regridder` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `data_manipulation` | `utilities/xarray_utils` |

1.2. To `file_utils`:

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `get_netcdf_file_dir_list` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `file_utils` | `utilities/xarray_utils` |
  | `get_netcdf_file_list` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `file_utils` | `utilities/xarray_utils` |
  | `netcdf_file_scanner` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `file_utils` | `utilities/xarray_utils` |
  | `ncfile_integrity_status` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `file_utils` | `utilities/xarray_utils` |

1.3. To `patterns`:

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `find_coordinate_variables` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `find_coordinate_variables_raise_none` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `find_nearest_coordinates` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `find_time_dimension` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `find_time_dimension_raise_none` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `get_file_dimensions` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `get_file_variables` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `get_latlon_bounds` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `get_latlon_deltas` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |
  | `get_model_list` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `patterns` | `utilities/xarray_utils` |

1.4. To `xarray_obj_handler`:

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `grib2netcdf` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `xarray_obj_handler` | `utilities/xarray_utils` |
  | `save_data_array_as_csv` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `xarray_obj_handler` | `utilities/xarray_utils` |
  | `save_data_as_netcdf_std` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `xarray_obj_handler` | `utilities/xarray_utils` |
  | `save_nc_data_as_csv` | `netcdf_handler` | `climate_data_utils` | (unchanged) | `xarray_obj_handler` | `utilities/xarray_utils` |

- **NOTE**: any function rename above has also been applied to all files using the old function name.

### Removed (10.0.0)

- Once every operation above performed, delete sub-package `netcdf_handler`.

---

## [9.0.0] - 2024-10-01

### Added (9.0.0)

- Add the following directories and modules in `statistics` sub-package:
  - **Core Statistics**:
    - `approximation_techniques`: for functions focusing on general approximation techniques not necessarily tied to specific curve fitting or interpolation.
    - `curve_fitting`: for functions like polynomial fitting and other curve fitting techniques.
    - `interpolation_functions`: for interpolation techniques, including the `hdy_interpolation` function.
  - **Climate Statistics** (`fields/climatology`)
    - `representative_series`: analysis of time series resulting from representativity criteria.

### Changed (9.0.0)

- Once above creations done, the following moves and/or renamings have been made:

#### **Functions** (9.0.0)

In `statistics` sub-package:

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `polynomial_fitting` | `regressions` | `statistics/core` | (unchanged) | `curve_fitting` | (unchanged) |
  | `calculate_HDY` | `variables` | `statistics/fields/climatology` | (unchanged) | `hdy_interpolation` | (unchanged) |
  | `hdy_interpolation` [once moved, Changed (isibility to internal)] | `variables` | `statistics/fields/climatology` | (unchanged) | `hdy_interpolation` | (unchanged) |

##### To `time_handling` sub-package

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `infer_full_period_of_time` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `date_and_time_operators` | (unchanged) |
  | `infer_time_frequency` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `date_and_time_operators` | (unchanged) |
  | `find_date_key` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `date_and_time_operators` | (unchanged) |
  | `infer_time_frequency` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `date_and_time_operators` | (unchanged) |  

##### To `utilities/pandas_utils` sub-package (depth level 2)

1.1 To `conversions.py` module

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `df_to_structured_array` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `conversions` | (unchanged) |

1.2 To `data_manipulation` module

  | Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
  |:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
  | `create_pivot_table` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `concat_dfs_aux` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `count_data_by_concept` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `insert_column_in_df` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `insert_row_in_df` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `polish_df_column_names` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `reindex_df` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `sort_df_indices` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |
  | `sort_df_values` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `data_manipulation` | (unchanged) |

1.3 To `pandas_obj_handler` module

| Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
|:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
| `csv2df` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `excel_handler` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `merge_csv_files` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `merge_excel_files` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `merge_ods_files` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `ods_handler` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `read_table` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `save2csv` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `save2excel` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |
| `save2ods` | `data_frame_handler` | `pandas_data_frames` | (unchanged) | `pandas_obj_handler` | (unchanged) |

#### **Modules**

| Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
|:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
| --- | `climate_indicators` | `statistics/fields/climatology` | --- | `indicators` | (unchanged) |
| --- | `climate_variables` | `statistics/fields/climatology` | --- | `variables` | (unchanged) |
| --- | `calendar_operators` | `time_handling` | --- | `calendar_utils` | (unchanged) |

### Removed (9.0.0)

- Once every operation above performed, removed sub-package `pandas_data_frames`.

---

## [8.0.0] - 2024-09-29

### Added (8.0.0)

#### sub-package `climate_data_utils`

- Handles operations focused on data manipulation for climate datasets, with a special focus on file management, downloads, and plotting.
- The following content has been added, each supporting specific utilities:

  **Modules**

- `cdo_tools.py`
  - Provides wrappers and utilities for working with the Climate Data Operators (CDO) tool.
  - Contains functions to interact with the Climate Data Store (CDS) API for downloading and managing climate data from the Copernicus Climate Data Store.
  - Facilitates data requests and efficient downloads of large datasets.

- `cds_tools.py`
  - Contains functions to interact with the Climate Data Store (CDS) API for downloading and managing climate data from the Copernicus Climate Data Store.
  - Facilitates data requests and efficient downloads of large datasets.
  
- `detect_faulty_ncfiles`
  - Implements functionality to detect and manage faulty NetCDF files, ensuring data integrity during processing and analysis.

- `extract_netcdf_basics`
  - Provides functions for extracting basic information from NetCDF files, such as metadata and variable summaries, facilitating data exploration.

- `nco_tools`
  - Offers utilities for working with the NetCDF Operators (NCO) tool, allowing for data manipulation and operations specific to NetCDF file formats.

- `netcdf_handler`
  - Central module for handling various operations related to NetCDF files, including reading, writing, and modifying NetCDF datasets.

- `weather_software_file_creator`
  - Contains functions for creating weather software files based on processed climate data, ensuring compatibility with various weather analysis tools.

  **Further sub-packages**

- `complementary-to_remodule`
  - A sub-package containing various auxiliary and complementary functions aimed at climate data analysis and visualization. It includes:
    - **auxiliary_functions**: Utility functions to assist with common tasks such as file handling, data transformations, and helper routines.
    - **ba_mean_and_var**: Implements functions to compute bias-adjusted mean and variance from climate data.
    - **ba_mean**: Provides functions for calculating bias-adjusted means from climate datasets, allowing for more accurate representation of data characteristics.

- `data_downloads`
  - A module dedicated to managing the download of climate data. It contains:
    - **codes**: Includes scripts and configurations necessary for utilizing the Copernicus API for efficient data downloads.
    - **input_data** A folder for storing downloaded climate data, ensuring organised access to data files.

#### sub-package `statistics`

- Introduced a new sub-package `statistics` to encapsulate numerical and statistical functions,  
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

#### `statistical_tests` as a `core` module

- **Hypothesis Testing**:
  - Added basic functions for hypothesis testing in the `statistical_tests.py` module, including: `z_test_two_means` and `chi_square_test` which provide common statistical hypothesis tests.
  - Each function includes a full docstring with parameter descriptions, examples, and returns, designed to be easily expanded for more complex use cases in the future.

### Changed (8.0.0)

- Many functions have been moved out from the modules in the old `weather_and_climate` sub-package to `statistics`.
- Information about the original module and new function name and location is displayed next:

| Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
|:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
| `calculate_WSDI` | `climate_indicators` | `weather_and_climate` | `WSDI` | (unchanged) | (unchanged) |
| `calculate_SU` | `climate_indicators` | `weather_and_climate` | `SU` | (unchanged) | `statistics/fields/climatology` |
| `calculate_CSU` | `climate_indicators` | `weather_and_climate` | `CSU` | (unchanged) | `statistics/fields/climatology` |
| `calculate_FD` | `climate_indicators` | `weather_and_climate` | `FD` | (unchanged) | `statistics/fields/climatology` |
| `calculate_TN` | `climate_indicators` | `weather_and_climate` | `TN` | (unchanged) | `statistics/fields/climatology` |
| `calculate_RR` | `climate_indicators` | `weather_and_climate` | `RR` | (unchanged) | `statistics/fields/climatology` |  
| `calculate_CWD` | `climate_indicators` | `weather_and_climate` | `CWD` | (unchanged) | `statistics/fields/climatology` |
| `calculate_HWD` | `climate_indicators` | `weather_and_climate` | `HWD` | (unchanged) | `statistics/fields/climatology` |
| `calculate_HDY` | `climate_indicators` | `weather_and_climate` | `HDY` | `climate_variables` | `statistics/fields/climatology` |
| `hdy_interpolation` | `climate_indicators` | `weather_and_climate` | (unchanged) | `climate_variables` | `statistics/fields/climatology` |
| `calculate_biovars` | `climate_indicators` | `weather_and_climate` | `biovars` | `climate_variables` | `statistics/fields/climatology` |

| Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
|:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
| `periodic_statistics` | `climate_statistics` | `weather_and_climate` | (unchanged) | `time_series` | `statistics/core` |
| `climat_periodic_statistics` | `climate_statistics` | `weather_and_climate` | (unchanged) | `time_series` | `statistics/core` |
| `calculate_and_apply_deltas` | `climate_statistics` | `weather_and_climate` | (unchanged) | `simple_bias_correction` | `statistics/fields/climatology` |  
| `window_sum` | `climate_statistics` | `weather_and_climate` | (unchanged) | `moving_operations` | `statistics/core` |
| `moving_average` | `climate_statistics` | `weather_and_climate` | (unchanged) | `moving_operations` | `statistics/core` |

| Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
|:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
| `autocorrelate` | `climatic_signal_modulators` | `weather_and_climate` | (unchanged) | `time_series` | `statistics/core` |  

| Original function name | Original module | Original sub-package path | New function name | New module | New sub-package path |
|:----------------------:|:---------------:|:------------------------:|:----------------:|:-----------:|:-------------------:|
| `get_1hour_time_step_data` | `consecutive_idx_statistics` | `weather_and_climate` | `hourly_ts_cumul` | `time_series` | `statistics/core` |
| `count_consecutive_days_maxdata` | `consecutive_idx_statistics` | `weather_and_climate` | `consec_occurrences_maxdata` | `time_series` | `statistics/core` |
| `count_consecutive_days_mindata` | `consecutive_idx_statistics` | `weather_and_climate` | `consec_occurrences_mindata` | `time_series` | `statistics/core` |

- **NOTE**: prior to these movements, every single function until here has been refactored, functionalities enhanced and optimised inner codes.

#### Rest of the content

- The following content has been moved to the new sub-package `climate_data_utils`:

1.1. **Modules**

- `cdo_tools`
- `cds_tools`
- `detect_faulty_ncfiles`
- `extract_netcdf_basics`
- `__init__`
- `meteorological_variables`
- `nco_tools`
- `netcdf_handler`
- `weather_software_file_creator`

1.2. **Further sub-packages**

- `data_downloads`
- `complementary-to_remodule`

### Removed (8.0.0)

- Once every operation above performed, delete sub-package `weather_and_climate`.

---

## [7.3.3] - 2024-09-28

### Added (7.3.3)

Sub-package `climatic_signal_modulators`

- **Autocorrelation Function**
  - Streamlined the logic by handling smaller arrays using `numpy.correlate` and larger arrays with `scipy.signal.correlate`.
  - Updated the docstring to clarify parameters and computation flow, explaining when to use two-sided or one-sided autocorrelation.

- **Signal Whitening functions**
  - Developed two signal whitening functions: `signal_whitening_classic` and `signal_whitening_pca`.
  - `signal_whitening_classic` applies a traditional approach using Cholesky decomposition with `numpy.linalg`.
  - `signal_whitening_pca` uses Principal Component Analysis (PCA) via `sklearn` for whitening data.
  - Enhanced docstrings for both functions, clarifying inputs, outputs, and providing comprehensive usage examples.

- **Band-Pass Filtering functions**
  - Refined three band-pass filtering functions (`band_pass1`, `band_pass2`, `band_pass3`), created during the Master in Meteorology, now translated:
    - Simplified internal variable names and loops for more concise code.
    - Added detailed docstrings, explaining how each function works with frequency domain transformations and filtering based on custom low and high-frequency ranges.
    - Used consistent terminology and enhanced explanations for different approaches to band-pass filtering.

- **Low and High-Pass Filtering functions**
  - Refined `low_pass_filter` and `high_pass_filter` functions, also created during the Master in Meteorology:
    - Improved performance by applying zero-phase filtering and optimizing how filters are designed based on cutoff frequencies.
    - Expanded the docstring to include explanations on filter design and its effect on different time series data.

### Changed (7.3.3)

#### Sub-package `climatic_statistics`

- `window_sum`
  - Optimised performance by using `np.convolve` for faster sliding window summation.
  - Added edge case handling for empty arrays or when the window size exceeds the array length.
  - Refined docstring to clarify input parameters, particularly around window size and handling of edge cases.

- `moving_average`
  - Rewritten using `np.convolve` for efficient computation of moving averages over a window.
  - Added option for handling arrays shorter than the window size, ensuring graceful failure or warning.
  - Clarified the docstring, highlighting that this function handles general numerical arrays, and specifying the nature of the windowing process.

#### Sub-package `climatic_signal_modulators`

- `polynomial_fitting`
  - Optimised the logic by simplifying variable names and improving handling of edge cases.
  - Enhanced the docstring to detail the parameters, added alternative polynomial function usage, and described the fixing of edges in polynomial interpolation.

---

## [7.0.0] - 2024-09-26

### Changed (7.0.0)

- Delete part of the file name `arrays_` contained in all modules of the sub-package `arrays_and_lists`, then delete all old-named modules.
- Module `climate_statistics`: refactor the following functions to improve performance, readability and maintainability:
  - `periodic_statistics`
  - `climat_periodic_statistics`
  - `calculate_and_apply_deltas`
  - `window_sum`
  - `moving_average`
- Remove the substring `array_` of functions `select_array_elements` (module `patterns`),  
  `sort_array_rows_by_column` and `sort_array_columns_by_row` (both in module `data_manipulation`).
- Remove triple quoted template string.

---

## [6.8.2] - 2024-09-25

### Added (6.8.2)

- Add todo for when function `time_format_tweaker` at module `time_formatters` is optimised and incorporated more functionalities to it.
- Add detailed docstring to the function `natural_year` and optimise inner code and comments.

### Changed (6.8.2)

- Modify function `datetime_range_operator` to `merge_datetime_dataframes`.
- Update function `get_current_time` to `get_current_datetime`; fix typo when writing to the object `report_file_obj`.
- Optimise the code of the main function `clock_time_average`, as well as the auxiliary functions, and add and refine the docstrings in all of them.
- Refine module and custom module import syntax in function `standardize_calendar`.
- Rename `ofile` variable to `out_file_obj`, which all `.write` instances are referenced from.
- Fix todo list for main function `clock_time_average` and auxiliaries
- Optimise the whole try-except block and handle specific errors gracefully.

---

## [6.6.0] - 2024-09-23

### Added (6.6.0)

- Add docstring for every function
- Add module to store configuration data like credentials, host info, etc.
- Add type to every parameter missing it in all docstrings
- Add dictionary with conversion factors from the provided floated time to the given unit

### Changed (6.6.0)

- Rename function `remove_elements_from_array` to `remove_elements`
- Eliminate `exec_command_shell` function and, if present, `catch_shell_prompt_output`  
  in favour of the renewed and complete `run_system_command` from module `os_operations`
- Refactor command execution module

---

## [6.3.4] - 2024-09-20

### Added (6.3.4)

- Add optional argument, comments explaining key parts of the code and simplify the f-strings
- Add type to the parameter `datetime_obj` in the docstring of the internal function `_total_time_unit`
- Add type to every parameter missing it in all docstrings.

### Changed (6.3.4)

- Delete `todo` from the code as the task there is already done
- Specify the name and type of the returning variable in function `string_underliner`

---

## [6.3.0] - 2024-09-18

### Added (6.3.0)

- Add further fractional second precision choice at internal function `_format_arbitrary_time`
- Add support for `datetime.time` object conversion to other datetime-like objects

### Changed (6.3.0)

- Eliminate need of the old function `time_format_tweaker` in favour of the renewed `datetime_obj_converter` from module `time_formatters`
- Rewrite some lazy imports and fix a typo as a result

---

## [6.0.0] (2024-09-06)

### Added (6.0.0)

- Created directories for lambda functions and assertion documentation in Python.
- Enhanced performance by importing frequently used NumPy libraries and utilizing `get_obj_type_str` for type checks.
- Implemented a simple calculator functionality using a dictionary-based switch-case approach, accepting multiple arguments.
- Improved input validation and functionalities in `sort_dictionary_by_keys` and `merge_dictionaries` functions.
  
### Changed (6.0.0)

- Restored accidentally removed code during editing.
- Sub-package `arrays_and_lists`:
  - Move out some functions in `array_data_manipulation` and `array_maths` to other modules in this sub-package.
  - Rewrite section headers to align with the nature of functions under them. Clarity and precision gained.
- Renamed directories for improved readability and intuitive understanding.
- Removed unnecessary directories due to renaming or redundancy.

### Removed (6.0.0)

- Deleted `webdriver_Firefox-Chrome_settings_check.py` in favour of the more descriptively named `webdriver_Firefox-Chrome_setup_test.py`.
- Eliminated `git` directory as Git does not depend on Python.

---

## [5.5.5] (2024-08-20)

### Added (5.5.5)

- Combined character splitting instructions into single lines for efficiency.
  
### Changed (5.5.5)

- Enhanced the `format_table_from_lists` function for better error handling.
- Improved readability by splitting long lines into shorter ones.
- Introduced a new folder for Web Scraping modules.

---

## [5.4.2] (2024-08-08)

### Added (5.4.2)

- Functionality to select column delimiters in all relevant functions.
- New function to underline single or multiple line strings.

### Changed (5.4.2)

- Revised the docstring in `format_table_from_lists` to reflect new functionalities.
- Fixed issues in the `format_table_from_lists` function related to multi-row values.

### Removed (5.4.2)

- Removed the `Constants` section from general notes.

---

## [5.2.2] (2024-07-15)

### Added (5.2.2)

- Optional argument for setting the index starting number in `format_table_from_list` and `format_table_from_lists`.
- New module for formatting dictionaries or lists into tables.

### Changed (5.2.2)

- Clarified overwriting behaviour in `serialize_dict_to_json`.
- Simplified the try-except block structure in `print_format_string`.

### Removed (5.2.2)

- Removed a JSON test file.

---

## [5.0.0] (2024-07-10)

### Added (5.0.0)

- Created a sub-package for JSON functionalities.

### Changed (5.0.0)

- Polished section comments for clarity.

### Removed (5.0.0)

- Removed redundant JSON file utilities, centralizing them in the `json_file_handler` module.

---

## [4.9.0] (2024-06-29)

### Added (4.9.0)

- Various references updated from `pytools` to `pyutils`.
- New warning codes and documentation improvements.

### Changed (4.9.0)

- Created a file to track significant changes in the repository.

---

## [4.0.0] (2024-06-26)

### Added (4.0.0)

- Several sub-packages for various utility functions and modules.

### Changed (4.0.0)

- Relocated functions and optimised imports.

### Removed (4.0.0)

- Deleted files that have been relocated.

---

## [3.0.0] (2024-06-24)

### Added (3.0.0)

- Introduced new functionalities for handling regex and optimizing code structure.

### Changed (3.0.0)

- Updated imports to absolute and improved error handling.

---

## [2.7.4] - 2024-06-14

### Added (2.7.4)

- Add todo for when function `time_format_tweaker` at module `time_formatters` is optimised and incorporated more functionalities to it.
- Add detailed docstring to the function `natural_year` and optimise inner code and comments.

### Changed (2.7.4)

- Modify function `datetime_range_operator` to `merge_datetime_dataframes`.
- Update function `get_current_time` to `get_current_datetime`; fix typo when writing to the object `report_file_obj`.
- Optimise the code of the main function `clock_time_average`, as well as the auxiliary functions, and add and refine the docstrings in all of them.
- Refine module and custom module import syntax in function `standardize_calendar`.
- Rename `ofile` variable to `out_file_obj`, which all `.write` instances are referenced from.
- Fix todo list for main function `clock_time_average` and auxiliaries
- Optimise the whole try-except block and handle specific errors gracefully.

---

## [2.4.0] - 2024-06-12

### Added (2.4.0)

- Add docstrings and polish the main functions `sum_clock_times` and `sum_date_objects`, as well as their auxiliary functions.
- Add functions to sum or subtract dates and/or times (preliminary version).

### Removed (2.4.0)

- Delete to-do list with `date_and_time_maths`.

---

## [2.1.0] - 2024-06-11

### Added (2.1.0)

- Import the function to return an object type`s string part.
- Add multidimensional indexing functionality for NumPy arrays in `select_array_elements` function.

### Renamed (2.1.0)

- Rename the function to return an object type`s string part.

---

## [2.0.0] - Initial release - 2024-06-10

### Added (2.0.0)

- Add module for climate and environment data manipulation and extraction.
- Add module for date and time management functions.
- Add module initiator file.
- Add module for string management.
- Add directory containing small manuals and web extracts about external Python modules and functions.
- Add module for mathematical operations with sets.

### Removed (2.0.0)

- Remove function `json2dict`
