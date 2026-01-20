#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 18:22:21 2026

@author: roncofaber
"""

class Measurement(object):
    
    def __init__(self, sample_name=None, sample_uuid=None):
        
        self.sample_name  = sample_name
        self.sample_uuid  = sample_uuid
    
        return
    
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.sample_name})"