#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pygenutils/__init__.py

# Import sub-packages to expose them as attributes of the pygenutils package.
# This ensures that you can access sub-packages like `pygenutils.arrays_and_lists` directly.
from . import arrays_and_lists  # Handles operations related to arrays and lists
from . import audio_and_video  # For audio and video processing
from . import dictionaries  # Utilities for handling dictionary operations
from . import number_bases  # Includes modules for base conversions and bitwise operations
from . import operative_systems  # Functions for OS-level operations
from . import sets_and_intervals  # Tools for set operations and interval handling
from . import strings  # String manipulation and formatting utilities
from . import time_handling  # Date and time utilities and formatters
from . import web_scraping  # Tools and utilities for web scraping and browser setup

# Note: 
# Each sub-package (e.g., arrays_and_lists, strings) should have its own `__init__.py` if you want 
# to further expose their internal modules or make them importable as `pygenutils.subpackage.module`.

