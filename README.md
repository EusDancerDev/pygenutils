# pygenutils

**pygenutils** is a versatile Python utility library that provides tools for handling data, performing array operations, processing media, and more. Originally created on April 16, 2024, and reimagined on June 10, 2024, pygenutils builds on its predecessor, *pytools.old*, with significant performance and usability enhancements.

## Project History

This project continues the functionality of *pytools.old*, which underwent a comprehensive re-structuring. The previous repository had multiple areas for improvement:

- **Module Accessibility**:
  - Initially, module accessibility required a setup program, `setup_repo.py`, to initialize paths and directories for the repository. This initializer allowed:
    1. Keeping the repository content in the cloned directory (default).
    2. Moving the repository content to a user-defined directory.
  - The initializer wrote a simple configuration file in `/home/{user}`, defining repository paths and dependencies to ensure modules dependent on others had their directories accurately tracked.
  
- **Performance Optimization**:
  - Enhanced computational performance and removed redundant operations, unifying conditional logic and refining execution paths.
  - Applied OOP principles where appropriate to simplify function calls and improve code readability.

## Key Features and Improvements

pygenutils offers a diverse set of modules, each tailored for specific tasks:

- **Array and List Operations**: 
  - Tools for data manipulation, conversions, and mathematical operations on arrays and lists.
- **Audio and Video Processing**: 
  - Functions for cutting, merging, and handling audio and video files.
- **Data Handling Utilities**:
  - Support for handling JSON, pandas, and xarray data, along with tools for bulk file operations.
- **Geospatial Tools**:
  - Methods for raster file handling, conversion, and geospatial data processing.
- **Text and String Processing**:
  - Utilities for string formatting, multilingual text processing, and translation.
