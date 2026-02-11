#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Samples: Thin Film Collection Management

Main container class for managing collections of thin film samples with integrated
Crucible API access for automated data retrieval and measurement association.

Created on Tue Jan 20 11:17:33 2026
@author: roncofaber
"""

import logging

# internal modules
from tksamples.collection import SampleCollection
from tksamples import Sample
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

class Samples(SampleCollection):

    def __init__(self, samples=None, from_crucible=True, cache_dir=None,
                 use_cache=True, overwrite_cache=False, project_id=None,
                 sample_type=None):

        # store internal variables
        self._use_cache = use_cache
        # Use configured cache directory if not specified
        self._cache_dir = cache_dir if cache_dir is not None else str(get_cache_dir())
        self._overwrite = overwrite_cache

        # set up knowledge of sample type
        self._sample_type = sample_type

        # read samples from crucible
        if samples is None and from_crucible:
            samples = self._get_samples_from_crucible(project_id=project_id,
                                                      sample_type=sample_type)

        # Initialize parent class with samples
        super().__init__(samples=samples, project_id=project_id)

        return
    
    def _get_samples_from_crucible(self, project_id=None, sample_type=None):
        
        # list all samples with given name
        dsts_samples = self.client.list_samples(
            project_id=project_id, sample_type=sample_type, limit=999999)
        dsts_samples = sorted(dsts_samples, key=lambda x: x["sample_name"])
        
        # get a map of all datasets in the project with all the data
        dataset_map = self._get_project_datasets(project_id=project_id)
        
        # create a TF obj for each sample dataset
        samples = []
        for dst_sample in dsts_samples:
            
            for dst in dst_sample.get("datasets", []):
                dst.update(dataset_map[dst["unique_id"]])
            
            try:
                tf = Sample(dst_sample)
                samples.append(tf)
            except Exception as e:
                logger.error(f"Failed to create Sample from dataset: {e}")
                logger.debug(f"Dataset details:\n\t- name: {dst_sample.get('dataset_name', 'unknown')}"\
                             "\n\t- id: {dataset.get('unique_id', 'unknown')}")
    
        return samples

    def _get_project_datasets(self, project_id=None):

        # get all project datasets
        all_datasets = self.client.list_datasets(
            project_id=project_id, limit=999999, include_metadata=True)

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
                measurement_datasets.append(dataset)
        
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
                logger.warning("Cannot assign measurement to sample - sample not found")
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

    # return all datasets of samples in object (unique)
    @property
    def samples_datasets(self):
        unique_datasets = []
        seen_datasets = set()
        
        for sample in self:
            for dataset in sample.datasets:
                if dataset["unique_id"] not in seen_datasets:
                    seen_datasets.add(dataset["unique_id"])
                    unique_datasets.append(dataset)
        return unique_datasets

    def get_measurements(self, mtype):
        measurements = []
        for sample in self:
            for measurement in sample.measurements:
                if measurement.mtype == mtype:
                    measurements.append(measurement)
        return measurements

    def _create_sliced_collection(self, sliced_samples):
        """Create a new Samples collection from sliced samples."""
        return Samples(samples=sliced_samples, from_crucible=False,
                       cache_dir=self._cache_dir, use_cache=self._use_cache,
                       overwrite_cache=self._overwrite, project_id=self.project_id,
                       sample_type=self._sample_type)