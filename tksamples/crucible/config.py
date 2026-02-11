#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Configuration Management for tksamples

This module re-exports configuration from pycrucible.config for backward compatibility.
All configuration is now managed by pycrucible.

@author: roncofaber
"""

# Import everything from pycrucible.config
from pycrucible.config import (
    config,
    Config,
    get_crucible_api_key,
    get_api_url,
    get_cache_dir,
    get_orcid_id,
    get_client,
    create_config_file,
    get_config_file_path,
)

__all__ = [
    "config",
    "Config",
    "get_crucible_api_key",
    "get_api_url",
    "get_cache_dir",
    "get_orcid_id",
    "get_client",
    "create_config_file",
    "get_config_file_path",
]
