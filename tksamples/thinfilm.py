#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ThinFilm: Individual Thin Film Sample Management

Class representing individual thin film samples with measurement storage,
QR code generation, and Crucible integration for metadata and analysis.

Created on Wed Jan  7 17:53:17 2026
@author: roncofaber
"""

# internal modules
from tksamples.core import CruxObj

#%%

class ThinFilm(CruxObj):
    
    def __init__(self, unique_id=None, sample_name=None, datasets=None,
                 description=None, date_created=None, measurements=None,
                 **kwargs):
        
        super().__init__(mfid=unique_id, dtype="sample", creation_time=date_created)

        # setup thin film data
        self.sample_name  = sample_name
        self.datasets     = datasets if datasets is not None else []

        # initialize measurements storage
        self._measurements = measurements if measurements is not None else {}

        return
    
    def add_measurement(self, new_measurement):
        """Add a measurement to thin film."""
        
        new_measurement._assign_to_sample(self)
        
        self._measurements[new_measurement.mfid] = new_measurement
        
        return

    def get_measurements(self, mtype=""):
        """Get all measurements filtered by type."""
        return self._measurements
    
    @property
    def measurements(self):
        return list(self._measurements.values())
        
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"
    

        