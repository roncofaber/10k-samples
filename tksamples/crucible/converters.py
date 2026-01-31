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
from tksamples.measurements.image import TFImage

from .client import get_data_from_crux

#%%

def get_uvvis_measurement(client, dataset, output_dir=".", use_cache=False,
                          overwrite_existing=False):
    """Convert Crucible dataset to UV-Vis measurement objects."""
    
    h5_extensions = [".h5"]
    dataset_id = dataset["unique_id"]
    filename = f"{dataset_id}.h5"


    h5file = get_data_from_crux(client, dataset_id, h5_extensions,
                                output_dir=output_dir, fname=filename,
                                use_cache=use_cache, overwrite_existing=overwrite_existing)
    if h5file is not None:
        return h5_to_samples(dataset, h5file)
    else:
        return
    
# function to get carrier image from uuid
def get_image_measurement(client, dataset, output_dir=".", use_cache=False,
                          overwrite_existing=False):
    """Download dataset images directly into memory as arrays."""
    
    image_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.tif',
                        '.svg', '.webp', '.heif', '.heic']
    dataset_id = dataset["unique_id"]
    filename = f"{dataset_id}.png"

    imgfile = get_data_from_crux(client, dataset_id, image_extensions,
                                output_dir=output_dir, fname=filename,
                                use_cache=use_cache, overwrite_existing=overwrite_existing)
    
    if imgfile is not None:
        return TFImage(image=imgfile, dataset=dataset)
    else:
        return