#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 15:24:53 2025

@author: roncofaber
"""

# pn
import numpy as np

# internal modules
from tksamples.measurements.uvvis import NirvanaUVVis
from tksamples.utils.auxiliary import number_to_well

# echfive
import h5py

#%%

def get_sample_data(h5group, poskey):
    
    pos = h5group[poskey]
    
    # get sample attributes
    sample_attrs = dict(pos.attrs)
    
    # get raw intensities
    raw_intensities = pos['raw_intensities'][()]

    # get blank intensities
    blank_intensities = pos['blank_intensities'][()]
    
    # get dark intensities
    dark_intensities = pos['dark_intensities'][()]
    
    return sample_attrs, raw_intensities, blank_intensities, dark_intensities

def h5_to_samples(h5filename, erange=None):
    
    
    with h5py.File(h5filename, 'r') as h5file:
        
        # get carrier information
        carrier_attrs = dict(h5file.attrs)
        
        # get wavelengths (same for all measurments)
        wavelengths = h5file['measurement/pollux_oospec_multipos_line_scan/wavelengths'][()]
        
        # get measurements settings
        measurement_settings = dict(h5file['measurement/pollux_oospec_multipos_line_scan/settings'].attrs)
        
        # isolate relevant H5 group and get list of positions
        h5group   = h5file['measurement/pollux_oospec_multipos_line_scan/positions']
        
        # read each position and return NirvanaUVVis object
        samples_list = []
        for poskey in h5group:
            
            sample_attrs, raw_intensities, blank_intensities, dark_intensities = get_sample_data(h5group, poskey)
            
            tray_well = number_to_well(int(poskey.split("_")[1]))
            
            # make it an object
            uvvis_sample = NirvanaUVVis(sample_attrs=sample_attrs,
                                        tray_well=tray_well,
                                        wavelengths=wavelengths,
                                        raw_intensities=raw_intensities,
                                        blank_intensities=blank_intensities,
                                        dark_intensities=dark_intensities,
                                        erange=erange,
                                        measurement_settings=measurement_settings,
                                        carrier_attrs=carrier_attrs
                                        )
            
            samples_list.append(uvvis_sample)
                
    return samples_list