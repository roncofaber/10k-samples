#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 13:41:02 2026

@author: roncofaber
"""

# load relevant modules
from tksamples.read.h5tosample import h5_to_samples
from tksamples.core import NirvanaSamples

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

file1 = "data/251210_173817_pollux_oospec_multipos_line_scan_TRAY3_4.h5"
file2 = "data/251218_130227_pollux_oospec_multipos_line_scan_TRAY3_4_1week.h5"
file3 = "data/260107_151134_pollux_oospec_multipos_line_scan__TRAY3_4_4weeks.h5"

nir1 = NirvanaSamples(file1, erange=[320, 650])
nir2 = NirvanaSamples(file2, erange=[320, 650])
nir3 = NirvanaSamples(file3, erange=[320, 650])

#%%

sidx = 6

s1 = nir1[sidx]
s2 = nir2[sidx]
s3 = nir3[sidx]

# plotting stuff
import matplotlib.pyplot as plt
import seaborn as sns
cm = 1/2.54  # centimeters in inches
sns.set_theme(style="white")
sns.set_style("ticks")
fs = 10




labels = ["1 day", "1 week", "4 weeks"]
colors = ["k", "orange", "red"]

fig, ax = plt.subplots(figsize=(9.5*cm, 6*cm))

for cc, sample in enumerate([s1, s2, s3]):
    # get 
    y_axis = sample.absorbances[2]
    ax.plot(sample.wavelengths, y_axis, label=labels[cc], color=colors[cc])

ax.set_title(s1.poskey)

ax.set_xlabel("Wavelength [nm]", fontsize=fs)
ax.set_ylabel("Absorbance [-]", fontsize=fs)
ax.yaxis.set_tick_params(labelsize=fs-1)
ax.xaxis.set_tick_params(labelsize=fs-1)

# Set scientific notation for y-axis
ax.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
ax.yaxis.get_offset_text().set_fontsize(fs-1)

ax.set_xlim(left=nir1[0]._erange[0], right=nir1[0]._erange[1])

# set legend outside axes, right side, compact
ax.legend(fontsize=fs-1, framealpha=1, edgecolor='k', 
          loc="upper right", ncols=3, title=None, title_fontsize=14,
          handlelength=0.5, handletextpad=0.2, labelspacing=0.3)

fig.tight_layout()
# fig.subplots_adjust(right=0.75)  # Make room for legend on the right
fig.show()