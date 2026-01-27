"""
tksamples: UV-Vis Spectroscopy and Thin Film Sample Analysis

This package provides tools for UV-Vis spectroscopy analysis of thin film samples,
with support for HDF5 data processing, Crucible API integration, and automated
sample characterization workflows.
"""

# Configuration and utilities
from .crucible import get_crucible_api_key, create_config_file, get_config_file_path

# Core classes
from .thinfilm import ThinFilm
from .thinfilms import ThinFilms

# Data reading and measurements
from .measurements import Measurement, NirvanaUVVis, TFImage

__version__ = "0.1.2"
__author__ = "roncofaber"

__all__ = [
    "ThinFilm",
    "ThinFilms",
    "Measurement",
    "NirvanaUVVis",
    "TFImage",
    "get_crucible_api_key",
    "create_config_file",
    "get_config_file_path"
]