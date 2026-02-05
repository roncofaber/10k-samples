#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Client: Basic API Client and Data Download

Provides Crucible API client setup and basic data download functionality
without dependencies on measurement classes. Core utilities for API access,
signed URL handling, and image processing.

Created on Tue Jan 13 14:40:26 2026
@author: roncofaber
"""

# os and stuff
import re
import os
import logging

# internal packages
from .config import get_crucible_api_key
from tksamples.utils.auxiliary import filter_links

# scicomp
import numpy as np

# specific packages
from PIL import Image
from io import BytesIO
import requests
from typing import Optional

# Set up logger for this module
logger = logging.getLogger(__name__)

#%%

# setup the crucible client
def setup_crux_client():
    from pycrucible import CrucibleClient
    api_url = 'https://crucible.lbl.gov/testapi'
    api_key = get_crucible_api_key()
    return CrucibleClient(api_url, api_key)


def get_data_from_crux(client, dataset_id, extension, output_dir=".", fname=None,
                        use_cache=False, overwrite_existing=False):
    
    # Define the local download path if caching is enabled
    download_path = os.path.join(output_dir, fname) if use_cache else None

    # If using cache, check if the file exists
    if use_cache and not overwrite_existing and download_path and os.path.exists(download_path):
        return download_path
    
    #Find download link
    download_link = get_links_with_extension(client, dataset_id, extension)
    
    if not bool(download_link):
        return None
    
    # Handle if the download_link is a dictionary
    if isinstance(download_link, dict):
        download_link = next(iter(download_link.values()))
    
    # Perform the HTTP GET request
    try:

        response = requests.get(download_link, stream=True, timeout=30)
        response.raise_for_status()

        # Create a BytesIO stream to hold the downloaded content
        response_content = BytesIO()

        # If caching is enabled, create the directory and save to both file and BytesIO
        if use_cache and download_path:
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            with open(download_path, 'wb') as f:
                # Stream the content to both the file and BytesIO
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    response_content.write(chunk)
        else:
            # If not caching, only write to BytesIO
            for chunk in response.iter_content(chunk_size=8192):
                response_content.write(chunk)

        # Ensure the BytesIO stream pointer is at the beginning
        response_content.seek(0)

        # Return the BytesIO stream of the downloaded content
        return response_content

    except requests.RequestException as e:
        logger.error(f"Failed to download data from dataset {dataset_id}: {e}")
        logger.debug(f"Download URL: {download_link}")
        return None
        
        

def get_links_with_extension(client, dsid, endings):
    # Get all download links from the dataset
    all_links = client.get_dataset_download_links(dsid)

    valid_links = {}
    
    # Ensure endings is a list
    if not isinstance(endings, list):
        endings = [endings]  # Convert to a list if a single string was provided

    for datafile, link in all_links.items():
        # Check if the datafile ends with any of the specified extensions
        if any(datafile.endswith(ending) for ending in endings):
            valid_links[datafile] = link

    return filter_links(valid_links)