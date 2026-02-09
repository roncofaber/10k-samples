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

import logging

# internal modules
from tksamples.core import CruxObj

# Set up logger for this module
logger = logging.getLogger(__name__)

#%%

class Measurement(CruxObj):
    
    def __init__(self, dataset=None, sample_name=None, sample_mfid=None,
                 measurement_type=None):
        
        #make sure it's a copy
        dataset = dataset.copy()
        
        # store info
        self._dataset = dataset
        
        # initialize parent class
        super().__init__(mfid          = dataset["unique_id"],
                         project_id    = dataset["project_id"],
                         creation_time = dataset["creation_time"],
                         dtype         = "dataset",
                         )
        
        # store sample information
        self._sample_name  = sample_name
        self._sample_mfid  = sample_mfid
        self.measurement_type = measurement_type
        
        # easy way to access metadata
        self.scientific_metadata = dataset.get("scientific_metadata")["scientific_metadata"]
        
        # initialize sample assignment variables
        self._is_assigned = False
    
        return
    
    def _assign_to_sample(self, sample):

        if self.sample_mfid != sample.mfid:
            logger.warning(f"Measurement MFID mismatch - expected {sample.mfid}")
            logger.debug(f"Measurement MFID: {self.sample_mfid}, Sample MFID: {sample.mfid}")
        if self._is_assigned:
            logger.warning(f"Measurement is already assigned to sample {self.sample.sample_name}")
            logger.debug(f"Attempting to reassign to {sample.sample_name}")

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