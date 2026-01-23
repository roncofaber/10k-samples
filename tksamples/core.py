#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:34:02 2026

@author: roncofaber
"""

import qrcode



#%%

class CruxObj(object):
    
    def __init__(self):
        
        from tksamples.crucible.crucible import setup_crux_client
        
        self.client = setup_crux_client()
        return
    
    @property
    def qr_code(self):
        qr_code = qrcode.QRCode(border=1)
        qr_code.add_data(self.mfid)
        return qr_code
    
    @property
    def print_qr(self):
        self.qr_code.print_ascii(invert=True)