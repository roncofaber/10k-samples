#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Configuration Management

Loads Crucible API keys and configuration from:
1. Environment variables (highest priority)
2. INI config file in user config directory

@author: roncofaber
"""

import os
import logging
import configparser
from pathlib import Path
from platformdirs import user_config_dir, user_cache_dir

# Set up logger for this module
logger = logging.getLogger(__name__)

# Global variable to store loaded config
_config_loaded = False
_crucible_api_key = None
_cache_dir = None


def get_crucible_api_key():
    """
    Get the Crucible API key from configuration.

    Priority order:
    1. CRUCIBLE_API_KEY environment variable
    2. crucible_api_key from ~/.config/tksamples/config.ini

    Returns:
        str: The API key

    Raises:
        ValueError: If no API key is found anywhere
    """
    global _config_loaded, _crucible_api_key

    if not _config_loaded:
        _load_config()

    if _crucible_api_key is None:
        config_file = Path(user_config_dir("tksamples")) / "config.ini"
        raise ValueError(
            f"Crucible API key not found. Please set it using one of these methods:\n"
            f"1. Environment variable: export CRUCIBLE_API_KEY='your_key_here'\n"
            f"2. Config file: Create {config_file} with:\n"
            f"   [crucible]\n"
            f"   api_key = your_key_here\n"
            f"\nUse create_config_file() to create the config file automatically:\n"
            f"from tksamples.crucible.config import create_config_file\n"
            f"create_config_file('your_key_here')"
        )

    return _crucible_api_key


def get_cache_dir():
    """
    Get the cache directory for storing downloaded data.

    Priority order:
    1. TKSAMPLES_CACHE_DIR environment variable
    2. cache_dir from ~/.config/tksamples/config.ini
    3. Default: ~/.cache/tksamples/ (platform-specific)

    Returns:
        Path: The cache directory path
    """
    global _config_loaded, _cache_dir

    if not _config_loaded:
        _load_config()

    if _cache_dir is None:
        # Use default platform-specific cache directory
        cache_path = Path(user_cache_dir("tksamples"))
    else:
        # Expand ~ and convert to Path, handling both strings and Path objects
        cache_path = Path(os.path.expanduser(str(_cache_dir)))

    # Ensure the cache directory exists
    cache_path.mkdir(parents=True, exist_ok=True)

    return cache_path


def _load_config():
    """Load configuration from all available sources."""
    global _config_loaded, _crucible_api_key, _cache_dir

    # 1. Try environment variables first (highest priority)
    _crucible_api_key = os.environ.get("CRUCIBLE_API_KEY")
    _cache_dir = os.environ.get("TKSAMPLES_CACHE_DIR")

    # 2. Try INI config file in user config directory
    config_dir = Path(user_config_dir("tksamples"))
    config_file = config_dir / "config.ini"

    if config_file.exists():
        config = configparser.ConfigParser()
        config.read(config_file)

        # Load API key if not already set from environment
        if "crucible" in config:
            if _crucible_api_key is None and "api_key" in config["crucible"]:
                _crucible_api_key = config["crucible"]["api_key"].strip('"').strip("'")

            if _cache_dir is None and "cache_dir" in config["crucible"]:
                _cache_dir = config["crucible"]["cache_dir"].strip('"').strip("'")

    _config_loaded = True


def create_config_file(api_key, cache_dir=None):
    """
    Create a configuration file with the given API key and optional cache directory.

    Args:
        api_key (str): The API key to store
        cache_dir (str, optional): Custom cache directory path. If not provided,
                                   defaults to platform-specific cache directory

    Returns:
        Path: Path to the created config file
    """
    config_dir = Path(user_config_dir("tksamples"))
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.ini"

    config = configparser.ConfigParser()

    # Set up crucible section with API key
    config["crucible"] = {"api_key": api_key}

    # Add cache_dir if provided
    if cache_dir is not None:
        config["crucible"]["cache_dir"] = str(cache_dir)

    with open(config_file, 'w') as f:
        config.write(f)

    logger.info(f"Created config file: {config_file}")
    if cache_dir:
        logger.debug(f"Cache directory: {cache_dir}")
    return config_file


def get_config_file_path():
    """Get the path where the config file should be located."""
    return Path(user_config_dir("tksamples")) / "config.ini"


# Auto-load configuration when module is imported
_load_config()