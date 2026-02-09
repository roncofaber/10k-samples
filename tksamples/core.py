#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core: Base Classes and Crucible Integration

Provides CruxObj base class with Crucible API client setup and QR code
generation functionality for sample identification and tracking.

Created on Thu Jan 22 17:34:02 2026
@author: roncofaber
"""

# handy packages
import qrcode
import webbrowser
from datetime import datetime, timezone

# import client setup (safe from circular imports)
from tksamples.crucible.client import setup_crux_client

#%%

dtype2ext = {
    "sample"  : "sample-graph",
    "dataset" : "dataset",
    "main"    : "",
    }

class CruxObj(object):

    # Class variable for the client
    _client = setup_crux_client()
    
    __slots__ = ["_dtype", "_unique_id", "_creation_time", "_project_id"]

    
    def __init__(self, mfid=None, dtype=None, creation_time=None,
                 project_id=None):
        
        # add data type
        self._dtype     = dtype
        self._unique_id = mfid
        self._creation_time = datetime.fromisoformat(creation_time)
        
        # FIXME: add project_id to samples in Crucible
        if project_id is not None:
            self._project_id = project_id
        else:
            self._project_id = "10k_perovskites"
        
        # initialize QR code
        self._qr_code = qrcode.QRCode(border=1)
        self._qr_code.add_data(self.mfid)
        
        return
    
    @property
    def client(self):
        return self._client  # Return the shared client
    
    @property
    def mfid(self):
        return self._unique_id
    
    @property
    def unique_id(self):
        return self._unique_id
    
    @property
    def project_id(self):
        return self._project_id
    
    @property
    def print_qr(self):
        self._qr_code.print_ascii(invert=True)
    
    @property
    def link(self):
        crux_explorer = "https://crucible-graph-explorer-776258882599.us-central1.run.app/"
        url = f"{crux_explorer}/{self.project_id}/{dtype2ext[self._dtype]}/{self.mfid}"
        return url
    
    def open_in_browser(self):
        webbrowser.open(self.link)
        return
    
    @property
    def age(self):
        """Returns the age of the object as a timedelta"""
        if self._creation_time.tzinfo is None:
            now = datetime.now()
        else:
            now = datetime.now(timezone.utc)
        return now - self._creation_time