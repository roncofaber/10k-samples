#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 17:53:17 2026

@author: roncofaber
"""

# internal modules
from tksamples.core import CruxObj

# os and other
from datetime import datetime, timezone

#%%

class ThinFilm(CruxObj):
    
    def __init__(self, unique_id=None, sample_name=None, datasets=None,
                 description=None, date_created=None, measurements=None,
                 **kwargs):
        
        super().__init__(mfid=unique_id, dtype="sample")

        # setup thin film data
        self.sample_name  = sample_name
        self.datasets     = datasets if datasets is not None else []
        self.date_created = datetime.fromisoformat(date_created)

        # initialize measurements storage
        self._measurements = measurements if measurements is not None else {}

        return
    
    def add_measurement(self, new_measurement):
        """Add a measurement to thin film."""
        
        if new_measurement.sample_mfid != self.mfid:
            raise ValueError(f"Measurement MFID {new_measurement.sample_mfid}"\
                             f" does not match sample MFID {self.mfid}")
        
        self._measurements[new_measurement.mfid] = new_measurement
        
        return

    def get_measurements(self, mtype=""):
        """Get all measurements filtered by type."""
        return self._measurements
    
    @property
    def measurements(self):
        return list(self._measurements.values())

    @property
    def age(self):
        """Returns the age of the object as a timedelta"""
        # If created_at is naive, use naive now
        if self.date_created.tzinfo is None:
            now = datetime.now()
        else:
            now = datetime.now(timezone.utc)
        
        return now - self.date_created
        
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"
    

        