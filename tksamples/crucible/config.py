#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Configuration Management for tksamples

This module re-exports configuration from nano-crucible.config for backward compatibility.
All configuration is now managed by nano-crucible.

@author: roncofaber
"""

# Import everything from nano-crucible.config
from crucible.config import (
    config,
    Config,
    get_crucible_api_key,
    get_api_url,
    get_cache_dir,
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
    "get_client",
    "create_config_file",
    "get_config_file_path",
]
