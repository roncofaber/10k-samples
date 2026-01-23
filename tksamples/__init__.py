"""
tksamples: UV-Vis Spectroscopy and Thin Film Sample Analysis

This package provides tools for UV-Vis spectroscopy analysis of thin film samples,
with support for HDF5 data processing, Crucible API integration, and automated
sample characterization workflows.
"""

# Core classes
from .thinfilm import ThinFilm
from .tksamples import TKSamples

# Data reading and measurements
from .measurements.measurement import Measurement
from .measurements.uvvis import NirvanaUVVis

# Configuration and utilities
from .crucible import get_crucible_api_key, create_config_file, get_config_file_path

__version__ = "0.1.1"
__author__ = "roncofaber"

__all__ = [
    "ThinFilm",
    "TKSamples",
    "Measurement",
    "NirvanaUVVis",
    "get_crucible_api_key",
    "create_config_file",
    "get_config_file_path"
]