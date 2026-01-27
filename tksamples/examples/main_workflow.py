#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 14:05:48 2026

@author: roncofaber
"""

# Load relevant modules
from tksamples import ThinFilms  # Import the ThinFilms class from the tksamples package

#%%
# Initialize the ThinFilms object
# Use cache to avoid redundant downloads and set overwrite_cache to False
tfilms = ThinFilms(from_crucible=True, use_cache=True, overwrite_cache=False)

#%%

# Retrieve well images for the thin films
tfilms.get_well_images()

# Retrieve UV-Vis data for the thin films
tfilms.get_uvvis_data()