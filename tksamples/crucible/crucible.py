#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 14:40:26 2026

@author: roncofaber
"""

# os and stuff
import re

# internal packages
import tksamples
from tksamples.read import h5_to_samples

# scicomp
import numpy as np

# specific packages
from PIL import Image
from io import BytesIO
import requests
from typing import Optional

#%%

# setup the crucible client
def setup_crux_client():
    from pycrucible import CrucibleClient
    api_url = 'https://crucible.lbl.gov/testapi'
    api_key = tksamples.get_crucible_api_key()
    return CrucibleClient(api_url, api_key)

# basic function that returns a BytesIO stream of a dataset
def get_data_from_crux(signed_url):
    try:
        response = requests.get(signed_url, timeout=30)
        response.raise_for_status()
        return BytesIO(response.content)
    except (requests.RequestException, Image.UnidentifiedImageError):
        return
    
def get_uvvis_measurement(client, dsid):
    links = client.get_dataset_download_links(dsid)
    for link in links:
        if link.endswith(".h5"):
            l2down = links[link]
    return h5_to_samples(get_data_from_crux(l2down))


# function to get carrier image from uuid
def download_dataset_to_memory(client, dsid: str, file_name: Optional[str] = None,
                             image_extensions: tuple = ('.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp')) -> dict:
    """Download dataset images directly into memory as arrays."""

    download_urls = client.get_dataset_download_links(dsid)

    if file_name is not None:
        file_regex = fr"({file_name})"
        download_urls = {k: v for k, v in download_urls.items() if re.fullmatch(file_regex, k)}

    # Filter for image files, exclude thumbnails
    image_files = {}
    for fname, url in download_urls.items():
        if (any(fname.lower().endswith(ext) for ext in image_extensions) and
            'thumbnail' not in fname.lower()):
            image_files[fname] = url

    images = {}
    for fname, signed_url in image_files.items():
        data = get_data_from_crux(signed_url)
        img = Image.open(data)
        images[fname.split("/")[-1]] = np.array(img)
    return images

def match_measurements_to_sample(measurements, sample):
    valid_measurements = []
    for measurement in measurements:
        if measurement.sample_uuid == sample.uuid:
            valid_measurements.append(measurement)
    return measurement