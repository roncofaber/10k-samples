#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 18:22:21 2026

@author: roncofaber
"""

# internal modules
from tksamples.core import CruxObj

#%%

class Measurement(CruxObj):
    
    def __init__(self, unique_id=None, sample_name=None, sample_mfid=None, measurement_type=None):
        
        super().__init__(mfid=unique_id, dtype="dataset")
        
        self._sample_name  = sample_name
        self._sample_mfid  = sample_mfid
        self.measurement_type = measurement_type
    
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