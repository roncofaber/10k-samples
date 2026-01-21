#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:17:33 2026

@author: roncofaber
"""

# usual
import numpy as np

# internal modules
from tksamples.read.h5tosample import h5_to_samples
from tksamples.utils.plotting import plot_inhomogeneity

# os and other
import os
import glob

#%%

class TKSamples:
    
    def __init__(self, h5files=None, erange=None, path=None,
                 samples=None):
        
        # use a path to a folder to look up all h5 files
        if path is not None:
            abspath = os.path.abspath(path)
            
            h5files = glob.glob(f"{abspath}/*.h5")
            h5files.sort()
        
        if samples is None:
            # make sure it's a list
            if isinstance(h5files, str):
                h5files = [h5files]
            
            samples = []
            for h5file in h5files:
                temp_samples = h5_to_samples(h5file, erange=erange)
                samples.extend(temp_samples)

        # store samples
        self._samples = samples
        
        # set them up
        self._setup_samples()
        
        return
    
    def _setup_samples(self):
        
        # define sample map
        self._sample_map = {sample.sample_uuid: sample for sample in self._samples}
        
        
        return
    
    @property
    def samples(self):
        return self._samples
    
    @property
    def nsamples(self):
        return len(self._samples)
    
    def set_erange(self, erange=None, left=None, right=None):
        for sample in self:
            sample.set_erange(erange=erange, left=left, right=right)
        return
    
    # get inhomogenity of all samples
    def get_inhomogeneities(self, value="cor_intensities", spots=None):
        
        # iterate over samples and get inhomogenity
        inhomogenity = [sample.get_inhomogeneity(spots=spots, value=value) for sample in self]
        
        return inhomogenity
    
    # plot inhomogeneities
    def plot_inhomogeneities(self, value="cor_intensities", spots=None):
        
        inhomogeneity = self.get_inhomogeneities(value=value, spots=spots)
        
        plot_inhomogeneity(inhomogeneity)
        return
    
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
            return TKSamples(samples=self.samples[index])
        else:  # integer index
            return self.samples[index]
    
    def __setitem__(self, index, value):
        if isinstance(index, str):
            # Update by ID
            for i, sample in enumerate(self._samples):
                if sample.id == index:
                    self._samples[i] = value
                    self._sample_map[index] = value
                    return
            raise KeyError(f"Sample with ID '{index}' not found")
        else:
            self._samples[index] = value
            self._setup_samples()  # Rebuild map
    
    def __delitem__(self, index):
        if isinstance(index, str):  # Delete by ID
            for i, sample in enumerate(self._samples):
                if sample.id == index:
                    del self._samples[i]
                    self._setup_samples()  # Rebuild map
                    return
            raise KeyError(f"Sample with ID '{index}' not found")
        else:  # Delete by integer index
            del self._samples[index]
            self._setup_samples()  # Rebuild map

    def __contains__(self, sample):
        return sample in self.samples
    
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.nsamples} TFs)"