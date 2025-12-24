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

# plotting stuff
import matplotlib.pyplot as plt
import seaborn as sns
cm = 1/2.54  # centimeters in inches
sns.set_theme(style="white")
sns.set_style("ticks")
fs = 10

#%%

class NirvanaUVVis:
    
    def __init__(self, sample_name=None, position_key=None, wavelengths=None,
                 raw_intensities=None, x_center=None, y_center=None,
                 x_positions=None, y_positions=None, dark_sample=None,
                 blank_sample=None, erange=None, measurement_settings=dict()):
        
        # assign internal variables according to input
        
        # set dataset ID
        self.poskey      = position_key
        self.sample_name = sample_name
        
        # set measurement data
        self._wavelengths     = wavelengths
        self._raw_intensities = raw_intensities
        
        # assign reference data (if provided)
        self.set_references(dark_sample=dark_sample, blank_sample=blank_sample)
        
        # calculate corrected intensities (only for not dark)
        if not self._is_dark:
            self._initialize_sample()
        
        # set sample position
        self.x_center = x_center
        self.y_center = y_center
        self.x_positions = x_positions
        self.y_positions = y_positions
                
        # assign energy range (if provided)
        if erange is None:
            self.set_erange((-np.inf, np.inf))
        else:
            self.set_erange(erange=erange)
            
        # assign measurement settings (if provided)
        self.measurement_settings = measurement_settings
        
        return
    
    def _initialize_sample(self):
        
        # get dark and blank
        dark_sample  = self._dark_sample
        
        if self._is_blank:
            blank_sample = self
        else:
            blank_sample = self._blank_sample
        
        # get corrected intensities (remove dark)
        self._cor_intensities = abs(np.clip(
            self._raw_intensities - dark_sample._raw_intensities))
        
        # calculate transmissions
        self._transmissions = self._cor_intensities/blank_sample._cor_intensities
        
        # calculcate absorbances
        self._absorbances = -np.log10(self._transmissions)
        
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
    def _is_dark(self):
        if self._dark_sample is None and self._blank_sample is None:
            return True
        else:
            return False
      
    @property
    def _is_blank(self):
        if self._dark_sample is not None and self._blank_sample is None:
            return True
        else:
            return False
    
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"
    
    # set erange
    def set_erange(self, erange=None, left=None, right=None):
        if erange is not None:
            self._erange = erange
        if left is not None:
            self._erange[0] = left
        if right is not None:
            self._erange[1] = right
            
        self._setup_emask()
        return
    
    # set references (blank, dark)
    def set_references(self, dark_sample=None, blank_sample=None):
        self._dark_sample  = dark_sample
        self._blank_sample = blank_sample
        return
    
    # set proper mask according to erange
    def _setup_emask(self):
        eleft, eright = self._erange
        self._emask = (self._wavelengths >= eleft) & (self._wavelengths <= eright)
        return
    
    # get inhomogenity within sample
    def get_inhomogenity(self, spots=None):
        
        if self.nspots < 2:
            raise ValueError("At least two spots are required to calculate inhomogeneity.")
        
        if spots is None:
            spots = list(range(self.nspots))
        
        abs_diffs = []
        for cc, ii in enumerate(spots):
            for jj in spots[cc+1:]:
                
                abs_diff  = np.abs(self.absorbances[jj] - self.absorbances[ii])
                area_diff = simpson(abs_diff, self.wavelengths)
                abs_diffs.append(area_diff)
        
        return np.array(abs_diffs)
    
    def plot_sample(self, spots=None):
        
        
        if spots is None:
            spots = list(range(self.nspots))
        
        fig, ax = plt.subplots(figsize=(9.5*cm, 6*cm))
        
        for spot in spots:
            
            absorbance = self.absorbances[spot]
            label = self.y_positions[spot]
            
            ax.plot(self.wavelengths, absorbance, label=label)
        
        ax.set_title(self.poskey)
        
        ax.set_xlabel("Wavelength [nm]", fontsize=fs)
        ax.set_ylabel("Absorbance [-]", fontsize=fs)
        ax.yaxis.set_tick_params(labelsize=fs-1)
        ax.xaxis.set_tick_params(labelsize=fs-1)
        
        ax.set_xlim(left=self._erange[0], right=self._erange[1])
        
        # set legend
        ax.legend(fontsize=fs-1, framealpha=1, edgecolor='k', loc="upper right",
                  ncols=1, title=None, title_fontsize=14)
        
        fig.tight_layout()
        fig.show()
        
        return
