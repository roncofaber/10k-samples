#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 17:53:17 2026

@author: roncofaber
"""

# usual
import numpy as np

# internal modules
import tksamples
from tksamples.read.h5tosample import h5_to_samples
from tksamples.utils.plotting import plot_inhomogeneity
from tksamples.crucible.crucible import get_uvvis_measurement, match_measurements_to_sample

# os and other
import os
import glob

#%%

class ThinFilm(object):
    
    def __init__(self, uuid=None, measurements=dict(), get_measurements=False):
        
        # initialize sample arrays
        self._measurements = measurements
        
        # set TF uuid
        self.uuid = uuid
        
        # setup sample from scratch
        self._setup_sample()
        
        return
    
    def _setup_sample(self):
        
        # setup connection to client
        self.client = self._get_crux_client()
        
        # update info by connecting to the crux
        self._update_crucible_info()
        
        # assign important variables
        self.sample_name = self.dataset_info["sample_name"]
        
        return
    
    def _update_crucible_info(self):
        self.dataset_info = self.client.get_sample(self.uuid)
        return
        
    @staticmethod
    def _get_crux_client():
        from pycrucible import CrucibleClient
        api_url = 'https://crucible.lbl.gov/testapi'
        api_key = tksamples.get_crucible_api_key()
        return CrucibleClient(api_url, api_key)
    
    def get_measurements(self):
        
        for dataset in self.datasets:
            if dataset["measurement"] == "pollux_oospec_multipos_line_scan":
                if dataset["unique_id"] in self._measurements:
                    continue
                else:
                    measurements = get_uvvis_measurement(self.client, dataset["unique_id"])
                    self._measurements[dataset["unique_id"]] = \
                        match_measurements_to_sample(measurements, self)
                
        return
        

    @property
    def datasets(self):
        return self.dataset_info["datasets"]
    
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"
        