"""
tksamples: Thin Film Sample Characterization and Analysis

This package provides tools for characterizing thin film samples through multiple
measurement types including UV-Vis spectroscopy, imaging, and other analytical methods.
"""

# Core classes
from .thinfilm import ThinFilm
from .tksamples import TKSamples

# Data reading and measurements
from .read.h5tosample import h5_to_samples
from .measurements.uvvis import NirvanaUVVis

# Configuration and utilities
from .config import get_crucible_api_key, create_config_file, get_config_file_path
from .utils import plot_sample, plot_inhomogeneity, visualize_carrier

# Optional imports with graceful fallback
try:
    from .crucible import get_uvvis_measurement, download_dataset_to_memory
    _HAS_CRUCIBLE = True
except ImportError:
    _HAS_CRUCIBLE = False

try:
    from .image import carrier2samples, isolate_carrier
    _HAS_IMAGE = True
except ImportError:
    _HAS_IMAGE = False

__version__ = "0.1.0"
__author__ = "roncofaber"

__all__ = [
    "ThinFilm",
    "TKSamples",
    "h5_to_samples",
    "NirvanaUVVis",
    "plot_sample",
    "plot_inhomogeneity",
    "visualize_carrier",
    "get_crucible_api_key",
    "create_config_file",
    "get_config_file_path"
]

# Conditionally add optional imports to __all__
if _HAS_CRUCIBLE:
    __all__.extend(["get_uvvis_measurement", "download_dataset_to_memory"])

if _HAS_IMAGE:
    __all__.extend(["carrier2samples", "isolate_carrier"])
