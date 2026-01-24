#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Converters: Data Conversion and Measurement Processing

Provides functions for converting Crucible datasets into measurement objects.
These functions depend on measurement classes and should be imported separately
from the basic client functions to avoid circular imports.

Created on Tue Jan 13 14:40:26 2026
@author: roncofaber
"""

# internal packages
from tksamples.read import h5_to_samples
from .client import get_links_with_extension, get_data_from_crux

#%%

def get_uvvis_measurement(client, dsid):
    """Convert Crucible dataset to UV-Vis measurement objects."""
    link = get_links_with_extension(client, dsid, ".h5")
    dataset = client.get_dataset(dsid)

    if link:
        return h5_to_samples(dataset, get_data_from_crux(link))
    else:
        return