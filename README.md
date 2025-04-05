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

## Package Structure

pygenutils is organized into several sub-packages, each focused on specific functionality:

- **arrays_and_lists**: Tools for data manipulation, conversions, and mathematical operations on arrays and lists.
- **audio_and_video**: Functions for cutting, merging, and handling audio and video files.
- **dictionaries**: Utilities for dictionary operations and transformations.
- **number_bases**: Functions for converting between different number bases.
- **operative_systems**: Tools for interacting with the operating system.
- **sets_and_intervals**: Utilities for working with sets and mathematical intervals.
- **strings**: Functions for string manipulation, formatting, and processing.
- **time_handling**: Tools for date and time operations, including calendar utilities.

## Key Features

pygenutils offers a diverse set of modules, each tailored for specific tasks:

- **Data Manipulation**: Tools for handling arrays, lists, and dictionaries with efficient operations.
- **Media Processing**: Functions for audio and video file manipulation, including cutting and merging.
- **Time Management**: Comprehensive utilities for date and time operations, calendar handling, and timezone support.
- **String Processing**: Tools for string formatting, manipulation, and text processing.
- **System Operations**: Functions for interacting with the operating system and file management.
- **Mathematical Utilities**: Support for number base conversions, set operations, and interval handling.

## Installation Guide

### Dependency Notice

Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**: some common dependencies include the latest versions of NumPy, Pandas, and others as specified.
  - more_itertools
  - numpy
  - pandas

  - You can install them via pip:

    ```bash
    pip3 install more_itertools numpy pandas 
    ```

  - Alternatively, you can install them via Anaconda. Currently, the recommended channel from where to install for best practices is `conda-forge`:

    ```bash
    conda install -c conda-forge more_itertools numpy pandas 
    ```

- **Optional Third-Party Libraries**: some packages are only used for certain configurations of the methods.
  - xarray

  - If necessary, you can also install them via pip:

    ```bash
    pip3 install xarray
    ```

- **Other Internal Packages**: these are other packages created by the same author. To install them as well as the required third-party packages, refer to the README.md document of the corresponding package:
  - filewise
  - paramlib
  - statkit

**Note**: In the future, this package will be available via PyPI and Anaconda, where dependencies will be handled automatically.

### Unconventional Installation Instructions

Until this package is available on PyPI or Anaconda, please follow these steps:

1. **Clone the Repository**: Download the repository to your local machine by running:

   ```bash
   git clone https://github.com/EusDancerDev/pygenutils.git
   ```

2. **Check the Latest Version**: Open the `CHANGELOG.md` file in the repository to see the latest version information.

3. **Build the Package**: Navigate to the repository directory and run:

   ```bash
   python setup.py sdist
   ```

   This will create a `dist/` directory containing the package tarball.

4. **Install the Package**:
   - Navigate to the `dist/` directory.
   - Run the following command to install the package:

     ```bash
     pip3 install pygenutils-<latest_version>.tar.gz
     ```

     Replace `<latest_version>` with the version number from `CHANGELOG.md`.

**Note**: Once available on PyPI and Anaconda, installation will be simpler and more conventional.

## Package Updates

To stay up-to-date with the latest version of this package, follow these steps:

1. **Check the Latest Version**: Open the `CHANGELOG.md` file in this repository to see if a new version has been released.

2. **Pull the Latest Version**:
   - Navigate to the directory where you initially cloned the repository.
   - Run the following command to update your local copy:

     ```bash
     git pull origin main
     ```

This will download the latest changes from the main branch of the repository. After updating, you may need to rebuild and reinstall the package as described in the [Installation Guide](#installation-guide) above.

## Versioning

This package follows semantic versioning (SemVer) with the format `vX.Y.Z`:

- **X** (Major): Incremented when making incompatible API changes or significant structural modifications
- **Y** (Minor): Incremented when adding functionality in a backward-compatible manner
- **Z** (Patch): Incremented when making backward-compatible bug fixes or minor improvements

For more details on the versioning scheme, please refer to the [VERSIONING.md](VERSIONING.md) file.

## Changelog

For a detailed history of changes, please refer to the [CHANGELOG.md](CHANGELOG.md) file.
