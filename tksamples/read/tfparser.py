#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 16:57:19 2026

@author: roncofaber
"""

# internal stuff
from tksamples.thinfilm import ThinFilm
from tksamples.crucible.crucible import setup_crux_client

#%%

def get_thin_films_from_crucible():

    client = setup_crux_client()
    
    samples_datasets = client.list_samples(project_id="10k_perovskites", limit=999999)
    
    tf_datasets = []
    for dataset in samples_datasets:
        if dataset["sample_name"].startswith("TF"):
            tf_datasets.append(dataset)
    tf_datasets = sorted(tf_datasets, key=lambda x: x["sample_name"])
    
    thin_films = []
    for dataset in tf_datasets:
        tf = ThinFilm(**dataset)
        thin_films.append(tf)

    return thin_films
