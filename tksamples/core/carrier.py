#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 14:31:10 2026

@author: roncofaber
"""

# usual
import numpy as np

# internal modules
import tksamples
from tksamples.read.h5tosample import h5_to_samples
from tksamples.utils.plotting import plot_inhomogeneity, visualize_carrier
from tksamples.core.core import NirvanaSamples
from tksamples.utils.crucible import download_dataset_to_memory

# os and other
import os
import glob

# crucible integration
from PIL import Image
from io import BytesIO
import re
import requests
from typing import Optional, List, Dict, Any

# plotting stuff
import matplotlib.pyplot as plt

#%%

image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp')

class NirvanaCarrier(NirvanaSamples):
    
    def __init__(self, h5file=None, erange=None, path=None):
        
        # read file and get sample and carrier attrs
        h5_attrs, samples = h5_to_samples(h5file, erange=erange)
        
        self._samples = samples
        self.h5_attrs = h5_attrs
        
        try:
            self.images = self.get_carrier_image()
        except:
            print("Not working")
        
        return
    
    @property
    def uuid(self):
        return self.h5_attrs["unique_id"]
    
    @property
    def client(self):
        from pycrucible import CrucibleClient
        api_url = 'https://crucible.lbl.gov/testapi'
        api_key = tksamples.get_crucible_api_key()
        return CrucibleClient(api_url, api_key)
    
    def get_carrier_image(self):
        
        # get dataset ids of sample
        dataset_ids = self.client.get_sample(self[0].uuid)
        
        dsid = next(d['unique_id'] for d in dataset_ids["datasets"] if d['measurement'] == 'thin film carrier image')
        
        # fetch image 
        images = download_dataset_to_memory(self.client, dsid)
        
        return images
    
    def visualize(self):
        
        for fname, img_array in self.images.items():
            visualize_carrier(img_array, fname)
        
        return