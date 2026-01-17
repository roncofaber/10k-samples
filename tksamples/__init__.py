"""
tksamples: Analysis of UV-Vis spectroscopy data from 10k sample measurements

This package provides tools for processing and analyzing UV-Vis spectroscopy data
from HDF5 files.
"""

from .read.h5tosample import h5_to_samples
from .measurements.uvvis import NirvanaUVVis
from .config import get_crucible_api_key, create_config_file, get_config_file_path

__version__ = "0.1.0"
__author__ = "roncofaber"

__all__ = [
    "h5_to_samples",
    "NirvanaUVVis",
    "get_crucible_api_key",
    "create_config_file",
    "get_config_file_path"
]
