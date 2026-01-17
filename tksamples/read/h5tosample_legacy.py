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

# echfive
import h5py

#%%

def get_sample_data(h5group, poskey):
    
    pos = h5group[poskey]
    
    # get sample attributes
    sample_attrs = dict(pos.attrs)
    
    # get raw intensities
    try:
        raw_intensities = pos['raw_intensities'][()]
    except:
        raw_intensities = pos['spectral_data'][()]
    
    # get position information
    x_center = pos['x_center'][()]
    y_center = pos['y_center'][()]
    
    x_positions = pos['x_positions'][()] #TODO add x_positions
    y_positions = pos['y_positions'][()]
    
    return sample_attrs, raw_intensities, np.array([x_center, y_center]),\
        np.array([x_positions, y_positions]).T
        
def get_measurement_settings(h5file):
    
    settings_group = h5file['measurement/pollux_oospec_multipos_line_scan/settings']
    measurement_settings = dict(settings_group.attrs)
        
    return measurement_settings

def h5_to_samples(h5filename, erange=None):
    
    
    with h5py.File(h5filename, 'r') as h5file:
        
        # get carrier information
        carrier_attrs = dict(h5file.attrs)
        
        # get wavelengths (same for all measurments)
        wavelengths = h5file['measurement/pollux_oospec_multipos_line_scan/wavelengths'][()]
        
        # get measurements settings
        measurement_settings = get_measurement_settings(h5file)
        
        # isolate relevant H5 group and get list of positions
        h5group   = h5file['measurement/pollux_oospec_multipos_line_scan/positions']
        
        # start with no blank and dark
        dark_sample  = None
        blank_sample = None
        
        # read each position and return NirvanaUVVis object
        samples_list = []
        for poskey in h5group:
            
            sample_attrs, raw_intensities, xy_center, xy_positions = get_sample_data(h5group, poskey)
                
            # make it an object
            uvvis_sample = NirvanaUVVis(sample_attrs=sample_attrs,
                                        position_key=poskey,
                                        wavelengths=wavelengths,
                                        raw_intensities=raw_intensities,
                                        xy_center = xy_center,
                                        xy_positions = xy_positions,
                                        dark_sample=dark_sample,
                                        blank_sample=blank_sample,
                                        erange=erange,
                                        measurement_settings=measurement_settings
                                        )
            
            # TODO we assume dark and blank always come first --> would fail otherwise!
            if "dark_ref" in sample_attrs["sample_name"]:
                dark_sample  = uvvis_sample
            elif "blank_ref" in sample_attrs["sample_name"]:
                blank_sample = uvvis_sample
            else: # true samples go here
                samples_list.append(uvvis_sample)
                
    return carrier_attrs, samples_list