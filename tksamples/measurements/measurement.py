#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measurement: Base Class for All Measurement Types

Provides the abstract Measurement class that serves as a foundation for
specific measurement implementations like UV-Vis spectroscopy, with common
properties for sample identification and metadata management.

Created on Fri Jan 16 18:22:21 2026
@author: roncofaber
"""

# internal modules
from tksamples.core import CruxObj

#%%

class Measurement(CruxObj):
    
    def __init__(self, dataset=None, sample_name=None, sample_mfid=None,
                 measurement_type=None, creation_time=None):
        
        dataset = dataset.copy()
        
        super().__init__(mfid=dataset["unique_id"],
                         dtype="dataset",
                         creation_time=dataset["creation_time"]
                         )
        
        self._sample_name  = sample_name
        self._sample_mfid  = sample_mfid
        self.measurement_type = measurement_type
        
        self._is_assigned = False
    
        return
    
    def _assign_to_sample(self, sample):
        
        if self.sample_mfid != sample.mfid:
            raise ValueError(f"Measurement MFID {self.sample_mfid}"\
                             f" does not match sample MFID {sample.mfid}")
        if self._is_assigned:
            raise ValueError(f"Measurement is already assigned to {self.sample}")
                
        self.sample = sample
        self._is_assigned = True
        
        return
    
    @property
    def sample_name(self):
        return self._sample_name
    
    @property
    def sample_mfid(self):
        return self._sample_mfid
    
    @property
    def mtype(self):
        return self.measurement_type.lower()
    
    def __repr__(self): #make it pretty
        return f"{self.measurement_type}({self.sample_name})"