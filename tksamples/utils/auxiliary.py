#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary Utilities: Helper Functions

Contains utility functions for well position conversion and data filtering
used across the tksamples package for sample identification and data processing.

Created on Fri Jan 16 17:32:08 2026
@author: roncofaber
"""

def number_to_well(n):
    """
    Convert number 0-15 to well position (A1, A2, ..., D4)
    
    Args:
        n: Integer from 0-15
    
    Returns:
        Well position string (e.g., 'A1', 'B3')
    """
    if not 0 <= n <= 15:
        raise ValueError("Number must be between 0 and 15")
    
    row = chr(65 + n // 4)  # 65 is ASCII for 'A'
    col = (n % 4) + 1
    
    return f"{row}{col}"

#%%

def filter_links(links):
    """
    If multiple links are provided, return the dict entry containing 'corrected'.
    Otherwise, return the single link dict or string.
    Returns empty dict if no links found.
    """
    if isinstance(links, str):
        return links
    
    if isinstance(links, dict):
        if len(links) == 0:
            return {}
        
        if len(links) == 1:
            return links
        
        # Multiple links - find the one with 'corrected' in the key
        for key, url in links.items():
            if 'corrected' in key.lower():
                return {key: url}
        
        # Fallback to first entry
        first_key = list(links.keys())[0]
        return {first_key: links[first_key]}
    
    # If it's a list
    if len(links) == 0:
        return []
    
    if len(links) == 1:
        return links[0]
    
    for link in links:
        if 'corrected' in link.lower():
            return link
    
    return links[0]