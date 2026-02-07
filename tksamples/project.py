#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 13:09:34 2026

@author: roncofaber
"""

# internal modules
from tksamples import Sample
from tksamples.collection import SampleCollection
from tksamples.graph.graph import build_project_graph

# avoid circular import by importing inside method
# from tksamples import Samples

# Set up logger for this module
import logging
logger = logging.getLogger(__name__)

# networking

#%%

class CrucibleProject(SampleCollection):

    def __init__(self, project_id):

        # internal variables
        self._project_id  = project_id

        # load samples and initialize parent
        samples = self._load_samples()
        super().__init__(samples=samples)

        # build project graph
        self._setup_graph()

        return
    
    def _load_samples(self):
        """Load all samples from the Crucible project."""
        # get all samples and datasets
        dsts_samples  = self._get_project_samples()
        dsts_datasets = self._get_project_datasets()

        # create mapping of datasets with metadata
        dataset_map = {dst["unique_id"]:dst for dst in dsts_datasets}

        # create one sample obj for each sample dataset
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


    def _get_project_samples(self):
        dsts_samples = self.client.list_samples(
            project_id=self.project_id, sample_type=None, limit=999999)
        dsts_samples = sorted(dsts_samples, key=lambda x: x["sample_name"])
        return dsts_samples
        
    def _get_project_datasets(self):
        dsts_datasets = self.client.list_datasets(
            project_id=self.project_id, limit=999999, include_metadata=True)
        return dsts_datasets
    
    def _get_project_graph(self):
        return self.client._request("GET",f"/projects/{self.project_id}/sample_graph")
    
    def _setup_mapping(self):
        """Extend parent mapping with sample type grouping."""
        # Call parent mapping setup
        super()._setup_mapping()

        # group samples by type
        self._samples_by_type = {}
        for sample in self._samples:
            sample_type = sample.sample_type
            if sample_type not in self._samples_by_type:
                self._samples_by_type[sample_type] = []
            self._samples_by_type[sample_type].append(sample)

        return
    
    def _setup_graph(self):
        
        graph = self._get_project_graph()
        
        # assign parent/child relationship
        for edge in graph.get("edges", []):
            
            parent_id = edge["source"]
            child_id  = edge["target"]
            
            parent = self.get_sample(parent_id)
            child  = self.get_sample(child_id)
            
            if parent is not None and child is not None:
                child.add_parent(parent)
            else:
                logger.warn("Graph info inconsistent")
        
        # build graph with networkx
        self._graph = build_project_graph(self.samples)
                
        return
    
    @property
    def project_id(self):
        return self._project_id

    @property
    def graph(self):
        return self._graph

    def get_samples_by_type(self, sample_type):
        """
        Get all samples of a specific type.

        Parameters
        ----------
        sample_type : str
            The sample type to filter by (e.g., "thin film", "solution", etc.)

        Returns
        -------
        list
            List of Sample objects matching the specified type
        """
        return self._samples_by_type.get(sample_type, [])

    def get_samples_collection(self, sample_type):
        """
        Get a Samples collection for a specific sample type.

        Creates a Samples instance containing all samples of the specified type,
        enabling use of measurement loading methods (get_uvvis_data, get_well_images, etc.).

        Parameters
        ----------
        sample_type : str
            The sample type to filter by (e.g., "thin film", "solution", etc.)

        Returns
        -------
        Samples
            A Samples collection instance containing samples of the specified type

        Examples
        --------
        >>> project = CrucibleProject(project_id="10k_perovskites")
        >>> thin_films = project.get_samples_collection("thin film")
        >>> thin_films.get_uvvis_data()
        """
        from tksamples import Samples

        samples_list = self.get_samples_by_type(sample_type)
        return Samples(samples=samples_list, from_crucible=False,
                      project_id=self._project_id, sample_type=sample_type)

    @property
    def sample_types(self):
        """Get list of all unique sample types in the project."""
        return list(self._samples_by_type.keys())