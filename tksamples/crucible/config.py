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
import configparser
from pathlib import Path
from platformdirs import user_config_dir

# Global variable to store loaded config
_config_loaded = False
_crucible_api_key = None


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
            f"\nUse create_config_file() to create the config file automatically."
        )

    return _crucible_api_key


def _load_config():
    """Load configuration from all available sources."""
    global _config_loaded, _crucible_api_key

    # 1. Try environment variable first (highest priority)
    _crucible_api_key = os.environ.get("CRUCIBLE_API_KEY")
    if _crucible_api_key:
        _config_loaded = True
        return

    # 2. Try INI config file in user config directory
    config_dir = Path(user_config_dir("tksamples"))
    config_file = config_dir / "config.ini"

    if config_file.exists():
        config = configparser.ConfigParser()
        config.read(config_file)

        if "crucible" in config and "api_key" in config["crucible"]:
            _crucible_api_key = config["crucible"]["api_key"].strip('"').strip("'")

    _config_loaded = True


def create_config_file(api_key):
    """
    Create a configuration file with the given API key.

    Args:
        api_key (str): The API key to store

    Returns:
        Path: Path to the created config file
    """
    config_dir = Path(user_config_dir("tksamples"))
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.ini"

    config = configparser.ConfigParser()
    config["crucible"] = {"api_key": api_key}

    with open(config_file, 'w') as f:
        config.write(f)

    print(f"Created config file: {config_file}")
    return config_file


def get_config_file_path():
    """Get the path where the config file should be located."""
    return Path(user_config_dir("tksamples")) / "config.ini"


# Auto-load configuration when module is imported
_load_config()