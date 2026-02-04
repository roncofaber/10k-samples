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
    
    def __init__(self, dataset, measurements=None, **kwargs):
        
        # store dataset information of the sample
        self._dataset = dataset.copy()
        
        # Pass crucible core infro to parent class
        mfid = self._dataset["unique_id"]
        time = self._dataset["date_created"]
        super().__init__(mfid=mfid, dtype="sample", creation_time=time)

        # Set to track measurement types
        self._measurements = {}
        self._measurement_types = set()
        if measurements is not None:
            for measurement in measurements.copy():
                self.add_measurement(measurement)
             
        # Makes easier to access uvvis and image, #TODO change
        self.uvvis = None
        self.image = None

        return
    
    @property
    def sample_name(self):
        return self._dataset["sample_name"]
    
    @property
    def sample_type(self):
        return self._dataset["sample_type"]
    
    @property
    def idx(self):
        return int(self.sample_name[2:])
    
    @property
    def description(self):
        return self._dataset["description"]
    
    def add_measurement(self, new_measurement):
        """Add a measurement to thin film."""
        
        new_measurement._assign_to_sample(self)
        
        self._measurements[new_measurement.mfid] = new_measurement
        
        # Add the measurement type to the set
        self._measurement_types.add(new_measurement.mtype)  # Assuming new_measurement has a 'mtype' attribute.
        
        if new_measurement.mtype == "uvvis":
            self.uvvis = new_measurement
        elif new_measurement.mtype == "image":
            self.image = new_measurement
        
        return

    def get_measurements(self, mtype=""):
        """Get all measurements filtered by type."""
        if mtype:
            return {key: value for key, value in self._measurements.items() if value.mtype == mtype}
        return self._measurements
    
    @property
    def measurements(self):
        return list(self._measurements.values())
    
    @property
    def dataset(self):
        return self._dataset
    
    @property
    def datasets(self):
        return self._dataset["datasets"]
        
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"
    
    def view(self):
        
        if self.image is None:
            print("No image associated with this TF.")
            return
        
        self.image.image.show()

        