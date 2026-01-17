#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 14:27:15 2026

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

class NirvanaSamples:
    
    def __init__(self, h5files=None, erange=None, path=None):
        
        # use a path to a folder to look up all h5 files
        if path is not None:
            abspath = os.path.abspath(path)
            
            h5files = glob.glob(f"{abspath}/*.h5")
            h5files.sort()
        
        # make sure it's a list
        if isinstance(h5files, str):
            h5files = [h5files]
        
        samples = []
        for h5file in h5files:
            temp_samples = h5_to_samples(h5file, erange=erange)
            samples.extend(temp_samples)
        
        self._samples = samples
        
        return
    
    @property
    def samples(self):
        return self._samples
    
    def set_erange(self, erange=None, left=None, right=None):
        for sample in self:
            sample.set_erange(erange=erange, left=left, right=right)
        return
    
    # get inhomogenity of all samples
    def get_inhomogeneities(self, value="cor_intensities", spots=None):
        
        # iterate over samples and get inhomogenity
        inhomogenity = np.array([sample.get_inhomogeneity(spots=spots, value=value) for sample in self])
        
        return inhomogenity
    
    # plot inhomogeneities
    def plot_inhomogeneities(self, value="cor_intensities", spots=None):
        
        inhomogeneity = self.get_inhomogeneities(value=value, spots=spots)
        
        plot_inhomogeneity(inhomogeneity)
        return
    
    # make class iterable
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, index):
        return self.samples[index]

    def __setitem__(self, index, value):
        self.samples[index] = value
    
    def __delitem__(self, index):
        del self.samples[index]
    
    def __contains__(self, sample):
        return sample in self.samples