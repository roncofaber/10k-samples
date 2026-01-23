#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TKSamples: Thin Film Collection Management

Main container class for managing collections of thin film samples with integrated
Crucible API access for automated data retrieval and measurement association.

Created on Tue Jan 20 11:17:33 2026
@author: roncofaber
"""

# usual
import numpy as np

# internal modules
from tksamples.core import CruxObj
from tksamples.crucible.crucible import setup_crux_client, get_uvvis_measurement
from tksamples.read.tfparser import get_thin_films_from_crucible

# to not make ppl waiting
from tqdm import tqdm

#%%

#TODO make this better lol
bad_datasets = [
    # Trays 3/4, repeated measurements on same tray
    "251218_130227_pollux_oospec_multipos_line_scan_TRAY3_4_1week",
    "260107_151134_pollux_oospec_multipos_line_scan__TRAY3_4_4weeks",
    "260109_111702_pollux_oospec_multipos_line_scan",
    
    # Trays 51/52, Tim fucked up
    "260119_183317_pollux_oospec_multipos_line_scan"
    ]

class TKSamples(CruxObj):
    
    def __init__(self, samples=None, from_crucible=True):
        
        super().__init__(dtype="main")

        if samples is None and from_crucible:
            samples = get_thin_films_from_crucible()
            
        # store samples
        self._samples = samples
        
        # set up internal structure
        self._setup_samples()
        
        # initialize crux
        self.client = setup_crux_client()
        
        return
    
    def _setup_samples(self):
        
        # define sample map
        self._sample_map = {sample.unique_id: sample for sample in self._samples}
        
        return
    
    def get_measurements_datasets(self, mtype):
        
        measurement_datasets = {}
        for dataset in self.samples_datasets:
            if dataset["measurement"] == mtype:
                
                skip = False
                for bad_data in bad_datasets:
                    if bad_data in dataset["dataset_name"]:
                        skip = True
                        break
                if skip:
                    continue
                
                if dataset["unique_id"] not in measurement_datasets:
                    measurement_datasets[dataset["unique_id"]] = dataset
                    
        return list(measurement_datasets.values())
    
    def get_uvvis_data(self):
        
        uvvis_datasets = self.get_measurements_datasets(
            mtype="pollux_oospec_multipos_line_scan")
        
        uvvis_data = []
        for dataset in tqdm(uvvis_datasets, desc="Getting UV-Vis", unit="dts", leave=False):
            data = get_uvvis_measurement(self.client, dataset["unique_id"])
            if data is not None:
                uvvis_data.extend(data)
                
        for uvvis in uvvis_data:
            sample = self.get_sample(uvvis.sample_mfid)
            sample.add_measurement(uvvis)
            
        return
       
    
    @property
    def samples_datasets(self):
        datasets = []
        for tf in self:
            datasets.extend(tf.datasets)
        return datasets
    
    @property
    def samples(self):
        return self._samples
    
    @property
    def nsamples(self):
        return len(self._samples)
    
    # make class iterable
    def __len__(self):
        return len(self.samples)
    
    def get_sample(self, sample_id):
        """Get sample by its identifier."""
        return self._sample_map.get(sample_id)

    def __getitem__(self, index):
        if isinstance(index, str):  # ID lookup
            return self._sample_map[index]
        elif isinstance(index, slice):  # slice
            return TKSamples(samples=self.samples[index], from_crucible=False)
        else:  # integer index
            return self.samples[index]

    def __contains__(self, sample):
        return sample in self.samples
    
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.nsamples} TFs)"