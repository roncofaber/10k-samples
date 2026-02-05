#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TKSamples: Thin Film Collection Management

Main container class for managing collections of thin film samples with integrated
Crucible API access for automated data retrieval and measurement association.

Created on Tue Jan 20 11:17:33 2026
@author: roncofaber
"""

import logging

# internal modules
from tksamples.core import CruxObj
from tksamples import ThinFilm
from tksamples.crucible.converters import get_uvvis_measurement, get_image_measurement
from tksamples.crucible.config import get_cache_dir

# to not make ppl waiting
from tqdm import tqdm

# Set up logger for this module
logger = logging.getLogger(__name__)

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

    def __init__(self, samples=None, from_crucible=True, cache_dir=None,
                 use_cache=True, overwrite_cache=False, project_id=None,
                 sample_type=None):

        # this class really does not have mfid or creation time...
        super().__init__(mfid="", dtype="main", creation_time="1993-04-01T01:18:00.0000+01:00")

        # store internal variables
        self._use_cache = use_cache
        # Use configured cache directory if not specified
        self._cache_dir = cache_dir if cache_dir is not None else str(get_cache_dir())
        self._overwrite = overwrite_cache
        
        # set up knowledge of project
        self._project_id  = project_id
        self._sample_type = sample_type
        
        # read samples from crucible
        if samples is None and from_crucible:
            samples = self._get_samples_from_crucible(project_id=project_id,
                                                      sample_type=sample_type)

        # store samples
        self._samples = samples
        
        # set up internal structure
        self._setup_mapping()
        
        return
    
    def _get_samples_from_crucible(self, project_id=None, sample_type=None):
        
        # list all datasets
        samples_datasets = self.client.list_samples(
            project_id=project_id, sample_type=sample_type, limit=999999)
        samples_datasets = sorted(samples_datasets, key=lambda x: x["sample_name"])
        
        # create a TF obj for each sample dataset
        samples = []
        for dataset in samples_datasets:
            try:
                tf = ThinFilm(dataset)
                samples.append(tf)
            except Exception as e:
                logger.error(f"Failed to create ThinFilm from dataset: {e}")
                logger.debug(f"Dataset details:\n\t- name: {dataset.get('dataset_name', 'unknown')}\n\t- id: {dataset.get('unique_id', 'unknown')}")
    
        return samples
    
    def _setup_mapping(self):

        # define sample maps for fast lookups
        self._samples_by_id = {sample.unique_id: sample for sample in self._samples}
        self._samples_by_name = {sample.sample_name: sample for sample in self._samples}

        # define dataset map
        self._dataset_map = self._get_project_datasets()

        return
    
    def _get_project_datasets(self):
        
        # get all project datasets
        all_datasets = self.client.list_datasets(
            project_id=self._project_id, limit=999999, include_metadata=True)

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
    
    def _get_measurement_data(self, measurement_type, converter_func, description):
        """
        Generic method to retrieve and associate measurements from Crucible.

        Args:
            measurement_type: The measurement type string for filtering datasets
            converter_func: Function to convert dataset to measurement object(s)
            description: Description for the progress bar
        """
        # Get datasets of the specified type
        datasets = self.get_measurments_datasets_of_type(mtype=measurement_type)

        # Collect measurements from all datasets
        measurements = []
        for dataset in tqdm(datasets, desc=description, unit="dts", leave=False):
            data = converter_func(self.client, dataset, output_dir=self._cache_dir,
                                 use_cache=self._use_cache,
                                 overwrite_existing=self._overwrite)
            if data is not None:
                # Handle both single measurements and lists of measurements
                if isinstance(data, list):
                    measurements.extend(data)
                else:
                    measurements.append(data)

        # Associate measurements with their samples
        for measurement in measurements:
            sample = self.get_sample(sample_id=measurement.sample_mfid,
                                    sample_name=measurement.sample_name)
            if sample is not None:
                sample.add_measurement(measurement)
            else:
                logger.warning(f"Cannot assign measurement to sample - sample not found")
                logger.debug(f"Measurement details - mfid: {measurement.sample_mfid}, name: {measurement.sample_name}, type: {measurement.mtype}")

        return

    def get_uvvis_data(self):
        """Retrieve and associate UV-Vis spectroscopy measurements."""
        self._get_measurement_data(
            measurement_type="pollux_oospec_multipos_line_scan",
            converter_func=get_uvvis_measurement,
            description="Getting UV-Vis"
        )
        return

    def get_well_images(self):
        """Retrieve and associate sample well images."""
        self._get_measurement_data(
            measurement_type="sample well image",
            converter_func=get_image_measurement,
            description="Getting images"
        )
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

    def get_measurements(self, mtype):
        
        measurements = []
        for tf in self:
            for measurement in tf.measurements:
                if measurement.mtype == mtype:
                    measurements.append(measurement)
                    
        return measurements
    
    @property
    def samples(self):
        return self._samples
    
    @property
    def nsamples(self):
        return len(self._samples)
    
    # make class iterable
    def __len__(self):
        return len(self.samples)
    
    def get_sample(self, sample_id=None, sample_name=None):
        """Get sample by its identifier."""

        if sample_id is not None:
            return self._samples_by_id.get(sample_id)
        elif sample_name is not None:
            return self._samples_by_name.get(sample_name)
        else:
            logger.warning("get_sample called without sample_id or sample_name")
            return
        
    def __getitem__(self, index):
        if isinstance(index, str):  # String lookup: try ID first, then name
            sample = self._samples_by_id.get(index)
            if sample is None:
                sample = self._samples_by_name.get(index)
            if sample is None:
                raise KeyError(f"Sample with ID or name '{index}' not found.")
            return sample

        elif isinstance(index, slice):  # Slice
            sliced_samples = self.samples[index]
            return ThinFilms(samples=sliced_samples, from_crucible=False,
                             cache_dir=self._cache_dir, use_cache=self._use_cache,
                             overwrite_cache=self._overwrite, project_id=self._project_id,
                             sample_type=self._sample_type)

        elif isinstance(index, int):  # Integer index
            return self.samples[index]

        else:
            raise TypeError("Index must be either a string, slice, or an integer.")

    def __contains__(self, sample):
        return sample in self.samples
    
    def __repr__(self): #make it pretty
        return f"{self.__class__.__name__}({self.nsamples} TFs)"