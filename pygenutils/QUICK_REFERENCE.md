# pygenutils Quick Reference Guide

**A condensed changelog for regular users focusing on major features, breaking changes, and important updates.**

---

## 🚀 Latest Release: v15.13.5 (2025-06-05)

### Recent Notable Features

#### ✨ **Audio & Video Processing** (v15.13.0+)

- **NEW**: `overwrite` parameter for media processing functions
- **IMPROVED**: Progress visualization when merging files
- **ENHANCED**: Better file path handling with spaces and special characters

#### 🧮 **Mathematical Operations** (v15.13.1+)

- **NEW**: `adapted_factorial()` function for extremely large numbers
- **NEW**: Mathematical utilities module

#### ⏰ **Time & Date Handling** (v15.13.3+)

- **IMPROVED**: Better support for various datetime object types
- **FIXED**: Parameter conflicts in date/time parsing

---

## 🔥 Major Version History

### **v15.0.0** (2024-10-30) - Package Restructuring

**⚠️ BREAKING CHANGE**: Package renamed from `pyutils` to `pygenutils`

#### Architecture Changes

- Several sub-packages moved to separate packages:
  - `climalab` (Climate analysis)
  - `geosptools` (Geospatial tools)  
  - `filewise` (File operations)
  - `LinguaLab` (Text processing)
  - `paramlib` (Parameters)
  - `statkit` (Statistics)
  - `DataOpsHub` (Databases & data entry)

### **v14.0.0** (2024-10-28) - Function Modernisation

#### Breaking Changes

- Many functions renamed for clarity:
  - `retrieve_function_name()` → `get_func_name()`
  - `pdf_file_tweaker()` → `file_tweaker()`
  - `add_str_to_path()` → `add_to_path()`
- British English standardisation (e.g., `standardize` → `standardise`)

### **v13.0.0** (2024-10-22) - File Operations Overhaul

#### Major Simplifications

- **File Operations**: Consolidated multiple similar functions
- **Path Utilities**: Merged extension-based and pattern-based functions
- **Module Renames**:
  - `file_and_directory_handler` → `ops_handler`
  - `file_and_directory_paths` → `path_utils`

### **v12.0.0** (2024-10-18) - Data Conversion Updates

#### Function Renames

- `basic_value_data_type_converter()` → `convert_data_type()`
- `list_array_to_std_array()` → `combine_arrays()`
- `flatten_content_to_string()` → `flatten_to_string()`

### **v10.0.0** (2024-10-02) - Statistics & Utilities Expansion

#### Major Additions

- **New Sub-packages**
  - **Core Statistics**: Signal processing, curve fitting, interpolation
  - **Pandas Utils**: DataFrame operations, conversions
  - **Xarray Utils**: NetCDF/GRIB handling, data manipulation

### **v8.0.0** (2024-09-29) - Climate Data & Statistics

#### New Features

- **Climate Data Utils**: CDO tools, CDS API integration
- **Statistics Package**: Time series analysis, signal processing
- **Reorganisation**: Weather and climate modules restructured

---

## 📋 Quick Feature Overview

### **🔧 Core Utilities**

- **Arrays & Lists**: Data manipulation, sorting, element operations
- **Dictionaries**: Merging, sorting, JSON operations  
- **Strings**: Text formatting, pattern matching, table generation
- **File Operations**: Bulk operations, path utilities, permissions

### **⏰ Time & Date**

- DateTime parsing and formatting
- Time zone handling
- Calendar operations
- Countdown and timing utilities

### **🎵 Media Processing**

- Audio/video merging and trimming
- FFmpeg integration
- Batch processing with progress tracking

### **🔢 Mathematics**

- Number base conversions
- Set operations and intervals
- Factorial calculations
- Signal processing

### **💾 Data Handling**

- Pandas DataFrame utilities
- Xarray/NetCDF operations
- CSV/Excel file processing
- Database connections

### **🖥️ System Operations**

- Cross-platform command execution
- Process management
- File system operations

---

## ⚠️ Migration Guide

### **From v14.x to v15.x**

- Update package name: `pyutils` → `pygenutils`
- Check for moved sub-packages (many now separate packages)
- Update import statements accordingly

### **From v13.x to v14.x**

- Review function renames (use search-replace for bulk updates)
- Update American to British spelling in function calls

### **From v12.x to v13.x**

- Update file operation function names
- Check module imports (`file_and_directory_*` modules renamed)

---

## 🔍 Finding What You Need

### By Use Case

- **File Management**: `filewise` package (separate as of v15.0.0)
- **Data Analysis**: `statkit` package (separate as of v15.0.0)  
- **Text Processing**: `LinguaLab` package (separate as of v15.0.0)
- **Climate Data**: `climalab` package (separate as of v15.0.0)
- **Time Operations**: `time_handling` sub-package
- **Media Processing**: `audio_and_video` sub-package

### Common Functions

```python
# Time formatting
from pygenutils.time_handling import parse_dt_string, format_dt

# File operations (if using v15.0.0+, consider separate filewise package)
from pygenutils.operative_systems import run_system_command

# String utilities
from pygenutils.strings import format_string, string_underliner

# Mathematical operations
from pygenutils.number_bases import dec2bin, bin2dec
```

---

## 📚 Documentation Notes

- **Detailed Changes**: See full `CHANGELOG.md` for comprehensive technical details
- **Breaking Changes**: Always marked with ⚠️ and version increment
- **Deprecations**: Functions marked deprecated before removal
- **British English**: All function names and documentation use British spelling

---

Last Updated: 2025-06-12 | Version: 15.13.5
