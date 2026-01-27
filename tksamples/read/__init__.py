"""
Read module for tksamples

Contains functions for reading and parsing HDF5 files.
"""

from .h5tosample import h5_to_samples
from .tfparser import get_thin_films_from_crucible

__all__ = ["h5_to_samples", "get_thin_films_from_crucible"]