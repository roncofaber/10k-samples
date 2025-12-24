#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 15:24:53 2025

@author: roncofaber
"""

# internal modules
from nirvana10k.measurements.uvvis import NirvanaUVVis

# echfive
import h5py

#%%

def get_sample_data(h5group, poskey):
    
    sample_name   = h5group[poskey]['sample_name'][()].decode('utf-8')
    
    raw_intensities    = h5group[poskey]['spectral_data'][()]
    
    x_center = h5group[poskey]['x_center'][()]
    y_center = h5group[poskey]['y_center'][()]
    
    x_positions = None #h5group[poskey]['x_positions'][()] #TODO add x_positions
    y_positions = h5group[poskey]['y_positions'][()]
    # for now returns None
    
    return sample_name, raw_intensities,  x_center, y_center, x_positions, y_positions
        
def get_measurement_settings(h5file):
    
    measurement_settings = dict()
    
    measurement_settings["spectra_int_time"] =\
        float(h5file['measurement/pollux_oospec_multipos_line_scan/spec_integration_time'][()])
    measurement_settings["spectra_averaged"] =\
        int(h5file['measurement/pollux_oospec_multipos_line_scan/spectra_averaged'][()])
    measurement_settings["y_scan_length"] =\
        float(h5file['measurement/pollux_oospec_multipos_line_scan/y_scan_length'][()])
        
    return measurement_settings

def h5_to_samples(h5filename, erange=None):
    
    samples_list = []
    
    with h5py.File(h5filename, 'r') as h5file:
        
        # get wavelengths (same for all measurments)
        wavelengths = h5file['measurement/pollux_oospec_multipos_line_scan/wavelengths'][()]
        
        # get measurements settings
        measurement_settings = get_measurement_settings(h5file)
        
        # isolate relevant H5 group and get list of positions
        h5group   = h5file['measurement/pollux_oospec_multipos_line_scan/positions']
        positions = h5group.keys()
        
        # start with no blank and dark
        
        dark_sample  = None
        blank_sample = None
        # read each position and return Nirvana10kSample class
        for poskey in positions:
            
            # read here
            sample_name, raw_intensities, x_center, y_center, x_positions,\
            y_positions = get_sample_data(h5group, poskey)
                
            # make it an object
            uvvis_sample = NirvanaUVVis(sample_name=sample_name,
                                        position_key=poskey,
                                        wavelengths=wavelengths,
                                        raw_intensities=raw_intensities,
                                        x_center=x_center,
                                        y_center=y_center,
                                        x_positions=x_positions,
                                        y_positions=y_positions,
                                        dark_sample=dark_sample,
                                        blank_sample=blank_sample,
                                        erange=erange,
                                        measurement_settings=measurement_settings
                                        )
            
            # TODO we assume dark and blank always come first --> would fail otherwise!
            if "dark_ref" in sample_name:
                dark_sample  = uvvis_sample
            elif "blank_ref" in sample_name:
                blank_sample = uvvis_sample
            else: # true samples go here
                samples_list.append(uvvis_sample)
                
    return samples_list