#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optional climarraykit-backed helpers for NetCDF and dimension utilities.

Install with::

    pip install 'pygenutils[climate]'
"""

from functools import cache

_INSTALL_MSG = (
    "NetCDF / climarraykit features require optional dependencies. "
    "Install with: pip install 'pygenutils[climate]'"
)


@cache
def _ncfile_integrity_status_fn():
    try:
        from climarraykit.file_utils import ncfile_integrity_status
    except ImportError as exc:
        raise ImportError(_INSTALL_MSG) from exc
    return ncfile_integrity_status


def ncfile_integrity_status(*args, **kwargs):
    """Proxy to :func:`climarraykit.file_utils.ncfile_integrity_status` when ``[climate]`` is installed."""
    return _ncfile_integrity_status_fn()(*args, **kwargs)


@cache
def _get_file_dimensions_fn():
    try:
        from climarraykit.patterns import get_file_dimensions
    except ImportError as exc:
        raise ImportError(_INSTALL_MSG) from exc
    return get_file_dimensions


def get_file_dimensions(*args, **kwargs):
    """Proxy to :func:`climarraykit.patterns.get_file_dimensions` when ``[climate]`` is installed."""
    return _get_file_dimensions_fn()(*args, **kwargs)
