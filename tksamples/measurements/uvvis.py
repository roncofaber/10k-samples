#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 10:42:15 2025

@author: roncofaber
"""

# numpy is my rock and scipy is my gospel
import numpy as np
import scipy
from scipy.integrate import simpson

# internal modules
import tksamples
from tksamples.utils.plotting import plot_sample
from tksamples.measurements.measurement import Measurement

#%%

class NirvanaUVVis(Measurement):
    
    def __init__(self, sample_attrs=None, tray_well=None, wavelengths=None,
                 raw_intensities=None, blank_intensities=None, dark_intensities=None,
                 erange=None, measurement_settings=dict(), carrier_attrs=dict()):
        
        # initialize measurement
        super().__init__(
            sample_name = sample_attrs["sample_name"],
            sample_uuid = sample_attrs["sample_uuid"]
            )
        
        # set dataset ID
        self.tray_well    = tray_well
        self.sample_attrs = sample_attrs
        
        # set measurement data
        self._wavelengths     = wavelengths
        self._raw_intensities = raw_intensities
        
        # initialize references
        self._set_blank_and_dark(blank_intensities, dark_intensities)

        # calculate corrected intensities, transmissions, absorbances
        self._initialize_uvvis()
        
        # set sample position on carrier
        self._set_sample_position()

        # assign energy range (if provided)
        self.set_erange(erange=erange)
            
        # assign measurement settings (if provided)
        self.measurement_settings = measurement_settings
        self.carrier_attrs = carrier_attrs
        
        return
    
    def _set_blank_and_dark(self, blank_intensities, dark_intensities):
        
        if blank_intensities.ndim == 2:
            npos = len(blank_intensities)
            blank_intensities = blank_intensities[npos//2]
        if dark_intensities.ndim == 2:
            npos = len(dark_intensities)
            dark_intensities = dark_intensities[npos//2]
        
        # store arrays
        self._blank_intensities = blank_intensities
        self._dark_intensities  = dark_intensities
        
        return
    
    def _initialize_uvvis(self):
        
        # get corrected intensities (remove dark)
        self._cor_intensities = abs(np.clip(
            self._raw_intensities - self._dark_intensities))
        
        # calculate transmissions
        cor_blank_intensities = abs(np.clip(
            self._blank_intensities - self._dark_intensities))
        
        self._transmissions = self._cor_intensities/cor_blank_intensities.mean(axis=0)
        
        # calculcate absorbances
        self._absorbances = -np.log10(self._transmissions)
        
        return
    
    def _set_sample_position(self):
        self.xy_center    = np.array([self.sample_attrs["x_center"],
                                      self.sample_attrs["y_center"]])
        self.xy_positions = np.array([self.sample_attrs["x_positions"],
                                      self.sample_attrs["y_positions"]]).T
        return
    
    # define bunch of properties so that they are already masked with the correct
    # energy range
    @property
    def wavelengths(self):
        return self._wavelengths[self._emask]
    
    @property
    def absorbances(self):
        return self._absorbances[:,self._emask]
    
    @property
    def transmissions(self):
        return self._transmissions[:,self._emask]
    
    @property
    def raw_intensities(self):
        return self._raw_intensities[:,self._emask]
    
    @property
    def cor_intensities(self):
        return self._cor_intensities[:,self._emask]
    
    @property
    def nspots(self):
        return len(self.absorbances)
    
    @property
    def int_time(self):
        return self.sample_attrs["integration_time"]
    
    # set erange
    def set_erange(self, erange=None, left=None, right=None):
        if erange is not None:
            self._erange = erange
        if left is not None:
            self._erange[0] = left
        if right is not None:
            self._erange[1] = right
        if erange is None and left is None and right is None:
            self._erange = (np.min(self._wavelengths), np.max(self._wavelengths))
            
        self._setup_emask()
        return

    # set proper mask according to erange
    def _setup_emask(self):
        eleft, eright = self._erange
        self._emask = (self._wavelengths >= eleft) & (self._wavelengths <= eright)
        
        # self._emask[self._blank_intensities]
        
        return
    
    # get inhomogenity within sample
    def get_inhomogeneity(self, value="cor_intensities", spots=None):
        
        if self.nspots < 2:
            raise ValueError("At least two spots are required to calculate inhomogeneity.")
        
        if spots is None:
            spots = list(range(self.nspots))
            
        # get relevant values
        value2calc = getattr(self, value)
        
        abs_diffs = []
        for cc, ii in enumerate(spots):
            for jj in spots[cc+1:]:
                
                spectra1 = value2calc[jj]/simpson(value2calc[jj], self.wavelengths)
                spectra2 = value2calc[ii]/simpson(value2calc[ii], self.wavelengths)
                
                abs_diff  = np.abs(spectra1 - spectra2)
                area_diff = simpson(abs_diff, self.wavelengths)
                abs_diffs.append(area_diff)
        
        return np.array(abs_diffs)
    
    # main plotting function
    def _plot_sample(self, value="absorbances", spots=None):
        
        value2plot = getattr(self, value)
        
        if spots is None:
            spots = list(range(self.nspots))
        
        title = f"{self.sample_name} @ {self.tray_well}"
        
        # plot sample
        plot_sample(value2plot, self.wavelengths, spots, title, self._erange, value)
        
        return
    
    # wrapper to plot attributes    
    def plot_transmissions(self, spots=None):
        self._plot_sample(value="transmissions", spots=spots)
        return

    def plot_absorbances(self, spots=None):
        self._plot_sample(value="absorbances", spots=spots)
        return
    
    def plot_intensities(self, spots=None):
        self._plot_sample(value="cor_intensities", spots=spots)
        return