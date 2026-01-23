"""
Measurements module for tksamples

Contains base and specific measurement classes for analyzing various measurement
types including UV-Vis spectroscopy with support for data processing and analysis.
"""

from .measurement import Measurement
from .uvvis import NirvanaUVVis

__all__ = ["Measurement", "NirvanaUVVis"]