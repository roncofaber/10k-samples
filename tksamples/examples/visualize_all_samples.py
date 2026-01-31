#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 14:32:30 2026

@author: roncofaber
"""

# Load relevant modules
from tksamples import ThinFilms  # Import the ThinFilms class from the tksamples package
import matplotlib.pyplot as plt

#%%
# Initialize the ThinFilms object
# Use cache to avoid redundant downloads and set overwrite_cache to False
tfilms = ThinFilms(use_cache=True, overwrite_cache=False, from_crucible=True,
                   project_id="10k_perovskites", sample_type="thin film")

# # Retrieve well images for the thin films
tfilms.get_well_images()

#%% Plot the grid

from tksamples.plot.tfgrid import plot_tfilms_grid

fig_width = 16
target_ratio = 16/9

fig = plot_tfilms_grid(tfilms, target_ratio=target_ratio, fig_width=fig_width,
                       show_label=False)


#%% To save the figure:
    
fig.savefig('all_tfilm_images_16x9.png', dpi=200, bbox_inches=None,
            facecolor='black', edgecolor='none', pad_inches=0)