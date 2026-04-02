# pygenutils

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/EusDancerDev/pygenutils/blob/main/LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/pygenutils.svg)](https://pypi.org/project/pygenutils/)

**pygenutils** is a comprehensive Python utilities package designed to provide a wide range of general-purpose tools for data manipulation, string handling, time operations, and system interactions. It serves as a collection of commonly needed utilities for Python development.

## Features

- **String Operations**:
  - Advanced string manipulation
  - Text formatting and parsing
  - String pattern matching
  - Text transformation utilities
- **Time Handling**:
  - Date and time calculations
  - Calendar operations
  - Time formatting
  - Program execution timing
  - Countdown functionality
- **Data Structures**:
  - Array and list manipulation
  - Data pattern matching
  - Mathematical operations
  - Data conversion utilities
- **System Operations**:
  - Operating system interactions
  - Process management
  - System information retrieval
- **Audio and Video**:
  - Advanced media file processing with full encoding control
  - Audio/video file merging and concatenation
  - Media file cutting and trimming
  - Comprehensive codec selection (libx264, libx265, aac, mp3, etc.)
  - Encoding preset and bitrate control
  - Format conversion utilities
- **Number Systems**:
  - Base conversion utilities
  - Number system operations
- **Set Operations**:
  - Interval handling
  - Set manipulation
- **Dictionary Operations**:
  - Dictionary manipulation
  - Key-value operations

## Installation Guide

### Dependency Notice

This package has minimal external dependencies and is designed to be lightweight. Most functionality works with Python's standard library.

### Installation Instructions

**For regular users** who want to use the package in their projects:

```bash
pip install pygenutils                    # Core functionality
pip install 'pygenutils[climate]'         # NetCDF / climarraykit features in time_handling
pip install pygenutils[arrow]             # Arrow support (optional)
```

Core install pulls **numpy**, **pandas**, **filewise**, **paramlib**, and **more_itertools**. **climarraykit** (and thus **xarray** for those code paths) is optional.

**Optional extras**:

- `pip install pygenutils` — core only (no climarraykit)
- `pip install 'pygenutils[climate]'` — NetCDF helpers (`ncfile_integrity_status`, `get_file_dimensions` proxies)
- `pip install pygenutils[arrow]` — Arrow for enhanced time handling
- `pip install pygenutils[xarray]` — xarray only (rare; prefer `[climate]` for climarraykit-backed APIs)

### Package Updates

To stay up-to-date with the latest version of this package, simply run:

```bash
pip install --upgrade pygenutils
```

## Development Setup

### For Contributors and Developers

If you're planning to contribute to the project or work with the source code, follow these setup instructions:

#### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/EusDancerDev/pygenutils.git
cd pygenutils

# Install with development dependencies (includes latest Git versions)
pip install -e .[dev]
```

**Note**: The `-e` flag installs the package in "editable" mode. The `[dev]` extra includes development tools **and** `climarraykit` so time-handling tests and NetCDF code paths work without a separate `[climate]` install.

#### Alternative Setup (Explicit Git Dependencies)

If you prefer to use the explicit development requirements file:

```bash
# Clone the repository
git clone https://github.com/EusDancerDev/pygenutils.git
cd pygenutils

# Install development dependencies from requirements-dev.txt
pip install -r requirements-dev.txt

# Install in editable mode (add [climate] if you skip Git climarraykit and need NetCDF features)
pip install -e .[dev]
```

This approach gives you Git checkouts of **filewise**, **climarraykit**, and **paramlib** plus pinned scientific stack; use **`pip install -e .[dev]`** so editable **pygenutils** matches **`pyproject.toml`** (including dev + climarraykit).

#### Development with Optional Dependencies

For full development capabilities, including testing and linting:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Or install specific optional dependencies
pip install -e ".[climate]"   # climarraykit / NetCDF-related time_handling
pip install -e ".[xarray]"    # xarray only (optional; [climate] is usually preferred)
```

### For Multiple Package Development

If you're working on multiple interdependent packages simultaneously:

```bash
# Clone all repositories
git clone https://github.com/EusDancerDev/pygenutils.git
git clone https://github.com/EusDancerDev/filewise.git
git clone https://github.com/EusDancerDev/climarraykit.git
git clone https://github.com/EusDancerDev/paramlib.git

# Install each in editable mode (order: dependencies first)
pip install -e ./filewise
pip install -e ./paramlib
pip install -e ./climarraykit
pip install -e ./pygenutils[dev]
```

### Troubleshooting

If you encounter import errors after cloning:

1. **For regular users**: Run `pip install pygenutils` (core dependencies) or `pip install 'pygenutils[climate]'` for NetCDF/climarraykit features
2. **For developers**: Run `pip install -e .[dev]` (includes dev tools and climarraykit)
3. **Verify Python environment**: Make sure you're using a compatible Python version (3.10+)

### Verify Installation

To verify that your installation is working correctly, you can run this quick test:

```python
# Test script to verify installation
try:
    import pygenutils
    from filewise.general.introspection_utils import get_type_str
    from paramlib.global_parameters import BASIC_ARITHMETIC_OPERATORS
    
    print("✅ All imports successful!")
    print(f"✅ pygenutils version: {pygenutils.__version__}")
    print("✅ Installation is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 For regular users: pip install pygenutils  # add [climate] for NetCDF features")
    print("💡 For developers: pip install -e .[dev]")
```

### Implementation Notes

- **Core PyPI dependencies**: **more_itertools**, **numpy**, **pandas**, **filewise**, **paramlib**.
- **Optional `[climate]`**: **climarraykit** (pulls **xarray**) for NetCDF-related helpers in `time_handling`.
- **Optional `[dev]`**: development tools plus **climarraykit** for a full local test stack.
- **Git-based `requirements-dev.txt`**: optional bleeding-edge **filewise**, **climarraykit**, **paramlib** before `pip install -e .[dev]`.

### Package Structure

The package is organised into several specialised modules:

- **strings/**: String manipulation utilities
  - `string_handler.py`: Core string operations
  - `text_formatters.py`: Text formatting utilities

- **time_handling/**: Time and date operations
  - `date_and_time_utils.py`: Date/time calculations
  - `time_formatters.py`: Time formatting
  - `calendar_utils.py`: Calendar operations
  - `program_snippet_exec_timers.py`: Execution timing
  - `countdown.py`: Countdown functionality

- **arrays_and_lists/**: Data structure operations
  - `data_manipulation.py`: Data handling
  - `patterns.py`: Pattern matching
  - `conversions.py`: Data conversion
  - `maths.py`: Mathematical operations

- **operative_systems/**: System operations
  - System interaction utilities
  - Process management tools

- **audio_and_video/**: Media handling
  - Media file operations
  - Format conversion

- **number_bases/**: Number system operations
  - Base conversion utilities

- **sets_and_intervals/**: Set operations
  - Interval handling
  - Set manipulation

- **dictionaries/**: Dictionary operations
  - Dictionary manipulation tools

For detailed version history and changes, please refer to:

- [Changelog](https://github.com/EusDancerDev/pygenutils/blob/main/pygenutils/CHANGELOG.md): comprehensive list of changes for each version
- [Versioning](https://github.com/EusDancerDev/pygenutils/blob/main/pygenutils/VERSIONING.md): versioning policy and guidelines

## Usage Examples

### String Operations

```python
from pygenutils.strings import string_handler, text_formatters

# String manipulation
modified_str = string_handler.modify_obj_specs("example.txt", "new")
formatted_text = text_formatters.print_format_string("Hello, {name}!", name="World")
```

### Time Operations

```python
from pygenutils.time_handling import date_and_time_utils, time_formatters

# Date calculations
next_week = date_and_time_utils.add_days_to_date("2024-03-20", 7)
formatted_time = time_formatters.format_time_string("14:30:00", "HH:MM")
```

### Array Operations

```python
from pygenutils.arrays_and_lists import data_manipulation, patterns

# Data manipulation
processed_data = data_manipulation.process_array([1, 2, 3, 4, 5])
matched_pattern = patterns.find_pattern([1, 2, 3, 1, 2, 3], [1, 2, 3])
```

### Audio and Video Operations

```python
from pygenutils.audio_and_video import audio_and_video_manipulation

# Merge audio and video files with custom encoding
audio_and_video_manipulation.merge_media_files(
    audio_files=["audio1.mp3", "audio2.mp3"],
    video_files=["video1.mp4", "video2.mp4"],
    video_codec="libx265",  # High-efficiency codec
    audio_codec="aac",      # Modern audio codec
    preset="slow",          # Better quality
    video_bitrate=2000      # 2000 kbps video bitrate
)

# Cut media files with encoding control
audio_and_video_manipulation.cut_media_files(
    media_inputs=["input.mp4"],
    start_time_list=["00:01:30"],
    end_time_list=["00:05:45"],
    video_codec="copy",     # No re-encoding for speed
    audio_codec="copy"      # Preserve original quality
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/EusDancerDev/pygenutils/blob/main/LICENSE) file in the repository for details.
