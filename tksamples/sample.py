#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample: Individual Thin Film Sample Management

Class representing individual thin film samples with measurement storage,
QR code generation, and Crucible integration for metadata and analysis.

Created on Wed Jan  7 17:53:17 2026
@author: roncofaber
"""

import logging

# internal modules
from tksamples.core import CruxObj

# Set up logger for this module
logger = logging.getLogger(__name__)

#%%

class Sample(CruxObj):
    
    def __init__(self, dataset, measurements=None, **kwargs):
        
        # store dataset information of the sample
        self._dataset = dataset.copy()
        
        # Pass crucible core infro to parent class
        mfid = self._dataset["unique_id"]
        time = self._dataset["date_created"]
        super().__init__(mfid=mfid, dtype="sample", creation_time=time)

        # Set to track measurement types
        self._measurements = {}
        self._mtypes       = {}
        if measurements is not None:
            for measurement in measurements.copy():
                self.add_measurement(measurement)

        # Initialize parent/child relationships for genealogy tracking
        self._parents = []
        self._children = []

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
        
        # assign measurement
        new_measurement._assign_to_sample(self)
        
        # add to data structure
        self._measurements[new_measurement.mtype] = new_measurement
        self._mtypes[new_measurement.mtype] = new_measurement
        
        return

    def get_measurements(self, mtype=""):
        """Get all measurements filtered by type."""
        if mtype:
            return {key: value for key, value in self._measurements.items() if value.mtype == mtype}
        return self._measurements
    
    @property
    def measurements(self):
        return list(self._measurements.values())

    def add_parent(self, parent_sample, _skip_reciprocal=False):
        """
        Add a parent sample to this sample's genealogy (bidirectional).

        Automatically adds this sample as a child to the parent.

        Parameters
        ----------
        parent_sample : Sample
            The parent sample object (e.g., a precursor solution)
        """
        if parent_sample not in self._parents:
            self._parents.append(parent_sample)
            
            if not _skip_reciprocal:
                parent_sample.add_child(self, _skip_reciprocal=True)
        return

    def add_child(self, child_sample, _skip_reciprocal=False):
        """
        Add a child sample to this sample's genealogy (bidirectional).

        Automatically adds this sample as a parent to the child.

        Parameters
        ----------
        child_sample : Sample
            The child sample object (e.g., a thin film derived from this sample)
        """
        if child_sample not in self._children:
            self._children.append(child_sample)

            if not _skip_reciprocal:
                child_sample.add_parent(self, _skip_reciprocal=True)
        return

    @property
    def parents(self):
        """Get list of parent samples."""
        return self._parents

    @property
    def children(self):
        """Get list of child samples."""
        return self._children

    @property
    def dataset(self):
        return self._dataset
    
    @property
    def datasets(self):
        return self._dataset["datasets"]
        
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"
    
    def __getattr__(self, key):
        # This is called when an attribute isn't found normally
        if key in self._mtypes:
            return self._mtypes[key]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    
    def view(self):

        if self.image is None:
            logger.info(f"No image associated with {self.sample_name}")
            return

        self.image.image.show()

        