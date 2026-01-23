#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:34:02 2026

@author: roncofaber
"""

import qrcode



#%%

dtype2ext = {
    "sample"  : "sample-graph",
    "dataset" : "dataset",
    "main"    : ""
    }

class CruxObj(object):
    
    def __init__(self, mfid=None, dtype=None):
        
        from tksamples.crucible.crucible import setup_crux_client
        
        # setup client
        self.client = setup_crux_client()
        
        # add data type
        self._dtype     = dtype
        self._unique_id = mfid
        
        return
    
    @property
    def mfid(self):
        return self._unique_id
    
    @property
    def unique_id(self):
        return self._unique_id
    
    @property
    def qr_code(self):
        qr_code = qrcode.QRCode(border=1)
        qr_code.add_data(self.mfid)
        return qr_code
    
    @property
    def print_qr(self):
        self.qr_code.print_ascii(invert=True)
        
    @property
    def link(self):
        crux_explorer = "https://crucible-graph-explorer-776258882599.us-central1.run.app/10k_perovskites/"
        print(f"{crux_explorer}//{self.mfid}")
        return