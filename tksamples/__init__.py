"""
tksamples: UV-Vis Spectroscopy and Thin Film Sample Analysis

This package provides tools for UV-Vis spectroscopy analysis of thin film samples,
with support for HDF5 data processing, Crucible API integration, and automated
sample characterization workflows.
"""

import logging

# Configuration and utilities
from .crucible import get_crucible_api_key, create_config_file, get_config_file_path

# Core classes
from .sample import Sample
from .collection import SampleCollection
from .samples import Samples

# Data reading and measurements
from .measurements import Measurement, NirvanaUVVis, TFImage

# Genealogy module (import as submodule)
from . import graph

__version__ = "0.1.2"
__author__ = "roncofaber"

__all__ = [
    "Sample",
    "SampleCollection",
    "Samples",
    "Measurement",
    "NirvanaUVVis",
    "TFImage",
    "get_crucible_api_key",
    "create_config_file",
    "get_config_file_path",
    "setup_logging"
]


def setup_logging(level=logging.INFO, format_string=None):
    """
    Configure logging for the tksamples package.

    Parameters
    ----------
    level : int, optional
        Logging level (e.g., logging.DEBUG, logging.INFO, logging.WARNING).
        Default is logging.INFO.
    format_string : str, optional
        Custom format string for log messages. If None, uses a default format.

    Examples
    --------
    >>> import tksamples
    >>> tksamples.setup_logging(level=logging.DEBUG)  # Show all messages
    >>> tksamples.setup_logging(level=logging.WARNING)  # Only warnings and errors
    """
    if format_string is None:
        format_string = '%(name)s - %(levelname)s - %(message)s'

    # Configure the root logger for the tksamples package
    logger = logging.getLogger('tksamples')
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and add it to the handler
    formatter = logging.Formatter(format_string)
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


# Auto-configure logging with a reasonable default when package is imported
setup_logging(level=logging.WARNING)