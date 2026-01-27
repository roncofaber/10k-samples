#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TKSamples: Thin Film Collection Management

Main container class for managing collections of thin film samples with integrated
Crucible API access for automated data retrieval and measurement association.

Created on Tue Jan 20 11:17:33 2026
@author: roncofaber
"""

# internal modules
from tksamples.core import CruxObj
from tksamples import ThinFilm
from tksamples.crucible.converters import get_uvvis_measurement, get_image_measurement

# to not make ppl waiting
from tqdm import tqdm

#%%

#TODO make this better lol
bad_datasets = set([
    # Trays 3/4, repeated measurements on same tray
    "251218_130227_pollux_oospec_multipos_line_scan_TRAY3_4_1week",
    "260107_151134_pollux_oospec_multipos_line_scan__TRAY3_4_4weeks",
    "260109_111702_pollux_oospec_multipos_line_scan",
    
    # Trays 51/52, Tim fucked up
    "260119_183317_pollux_oospec_multipos_line_scan"
    ])

class ThinFilms(CruxObj):
    
    def __init__(self, samples=None, from_crucible=True, cache_dir="10k_cache",
                 use_cache=False, overwrite_cache=False):
        
        # this class really does not have mfid or creation time...
        super().__init__(mfid="", dtype="main", creation_time="1993-04-01T01:18:00.0000+01:00")
        
        # store internal variables
        self._use_cache = use_cache
        self._cache_dir = cache_dir
        self._overwrite = overwrite_cache
        
        # read samples from crucible
        if samples is None and from_crucible:
            samples = self._get_samples_from_crucible()

        # store samples
        self._samples = samples
        
        # set up internal structure
        self._setup_mapping()
        
        return
    
    def _get_samples_from_crucible(self):
        
        # list all datasets
        samples_datasets = self.client.list_samples(project_id="10k_perovskites",
                                                    limit=999999)
        
        # filter out what is not a thin film
        tf_datasets = []
        for dataset in samples_datasets:
            if dataset["sample_name"].startswith("TF"):
                tf_datasets.append(dataset)
        tf_datasets = sorted(tf_datasets, key=lambda x: x["sample_name"])
        
        # create a TF obj for each sample dataset
        samples = []
        for dataset in tf_datasets:
            tf = ThinFilm(**dataset)
            samples.append(tf)
    
        return samples
    
    def _setup_mapping(self):
        
        # define sample map
        self._sample_map = {sample.unique_id: sample for sample in self._samples}
        
        # define dataset map
        self._dataset_map = self._get_project_datasets()
        
        return
    
    def _get_project_datasets(self):
        
        # get all project datasets
        all_datasets = self.client.list_datasets(project_id="10k_perovskites",
                                                     limit=999999, include_metadata=True)

        return {dst["unique_id"]:dst for dst in all_datasets}
    
    def get_measurments_datasets_of_type(self, mtype):
        
        measurement_datasets = []
        for dataset in self.samples_datasets:

            # Check for measurement type
            if dataset["measurement"] == mtype:
                # Skip if dataset name contains any bad data
                if any(bad_data in dataset["dataset_name"] for bad_data in bad_datasets):
                    continue
                
                # Append valid datasets
                measurement_datasets.append(self._dataset_map[dataset["unique_id"]])
        
        return measurement_datasets
    
    def get_uvvis_data(self):
        
        uvvis_datasets = self.get_measurments_datasets_of_type(
            mtype="pollux_oospec_multipos_line_scan")
        
        uvvis_data = []
        for dataset in tqdm(uvvis_datasets, desc="Getting UV-Vis", unit="dts", leave=False):

            data = get_uvvis_measurement(self.client, dataset, output_dir=self._cache_dir,
                                         use_cache=self._use_cache,
                                         overwrite_existing=self._overwrite)
            if data is not None:
                uvvis_data.extend(data)
                
        for uvvis in uvvis_data:
            sample = self.get_sample(uvvis.sample_mfid)
            
            if sample is not None:
                sample.add_measurement(uvvis)
            
        return
    
    def get_well_images(self):
        
        well_datasets = self.get_measurments_datasets_of_type(
            mtype="sample well image")
        
        well_images = []
        for dataset in tqdm(well_datasets, desc="Getting images", unit="dts", leave=False):

            data = get_image_measurement(self.client, dataset, output_dir=self._cache_dir,
                                         use_cache=self._use_cache,
                                         overwrite_existing=self._overwrite)
            if data is not None:
                well_images.append(data)
                
        for image in well_images:
            sample = self.get_sample(image.sample_mfid)
            
            if sample is not None:
                sample.add_measurement(image)
                
        return
    
    # return all datasets of samples in object
    @property
    def samples_datasets(self):
        unique_datasets = []
        seen_datasets = set()
        
        for sample in self:
            for dataset in sample.datasets:
                # Convert dict to a tuple of key-value pairs
                if isinstance(dataset, dict):
                    dataset_key = tuple(sorted(dataset.items()))  # Sorting to ensure consistent order
                else:
                    dataset_key = dataset
                
                if dataset_key not in seen_datasets:
                    seen_datasets.add(dataset_key)
                    unique_datasets.append(dataset)
        
        return unique_datasets

    
    @property
    def samples(self):
        return self._samples
    
    @property
    def nsamples(self):
        return len(self._samples)
    
    # make class iterable
    def __len__(self):
        return len(self.samples)
    
    def get_sample(self, sample_id):
        """Get sample by its identifier."""
        return self._sample_map.get(sample_id)

    def __getitem__(self, index):
        if isinstance(index, str):  # ID lookup
            sample = self._sample_map.get(index)
            if sample is None:
                raise KeyError(f"Sample with ID '{index}' not found.")
            return sample
            
        elif isinstance(index, slice):  # Slice
            sliced_samples = self.samples[index]
            return ThinFilms(samples=sliced_samples, from_crucible=False, 
                             cache_dir=self._cache_dir, use_cache=self._use_cache)
        
        elif isinstance(index, int):  # Integer index
            return self.samples[index]
    
        else:
            raise TypeError("Index must be either a string, slice, or an integer.")

    def __contains__(self, sample):
        return sample in self.samples
    
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.nsamples} TFs)"