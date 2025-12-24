#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 15:23:50 2025

@author: roncofaber
"""

# load relevant modules
from nirvana10k.read.h5tosample import h5_to_samples

# plotting functions
import matplotlib.pyplot as plt
import seaborn as sns
cm = 1/2.54  # centimeters in inches
sns.set_theme(style="white")
sns.set_style("ticks")
fs = 10

# scientific libraries
import numpy as np

#%%

filename = "251210_173817_pollux_oospec_multipos_line_scan.h5"

nirvana10ks = h5_to_samples(filename, erange=[320, 650])

#%%

# example on how to get inhomogenity
sample = nirvana10ks[0] # get sample

# choose spots
spots = [0,1,2,3]

# get ino
ino = sample.get_inhomogenity(spots=spots)

#%% plot across all samples

mean_values = [sample.get_inhomogenity(spots=spots).mean() for sample in nirvana10ks]
std_values  = [sample.get_inhomogenity(spots=spots).std() for sample in nirvana10ks]

fig, ax = plt.subplots(figsize=(9.5 * cm, 6 * cm))

x_indices = np.arange(len(nirvana10ks))

# Create an errorbar plot
ax.errorbar(x_indices, mean_values, yerr=std_values, fmt='o', color='black', 
            markersize=5, elinewidth=2, capsize=5)

ax.set_xlabel('Sample idx [-]', fontsize=fs)
ax.set_ylabel('Inhomogeneity [-]', fontsize=fs)
ax.yaxis.set_tick_params(labelsize=fs-1)
ax.xaxis.set_tick_params(labelsize=fs-1)

ax.axhline(y=np.mean(mean_values), linestyle="--", color="gray", zorder=-10)

# ax.legend(fontsize=fs-1, framealpha=1, edgecolor='black', loc="upper right", 
          # ncols=1, title=None, title_fontsize=14)

# ax.set_ylim(bottom=0)  # Adjust according to your data range
ax.set_xlim(left=-0.5, right=len(nirvana10ks)-0.5)

ax.set_xticks(x_indices)  # Fires at each sample index

# ax.set_xlim(left=0)

fig.tight_layout()
fig.show()
