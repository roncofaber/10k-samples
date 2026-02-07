#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SampleCollection: Base class for managing collections of samples

Provides common functionality for storing, indexing, and accessing
collections of Sample objects.

Created on Thu Feb  6 2026
@author: roncofaber
"""

import logging
from tksamples.core import CruxObj

# Set up logger for this module
logger = logging.getLogger(__name__)

#%%

class SampleCollection(CruxObj):
    """
    Base class for managing collections of samples.

    Provides common functionality for sample storage, indexing, iteration,
    and lookup operations. Subclasses should implement specific data
    loading and collection-specific methods.
    """

    def __init__(self, samples=None):
        """
        Initialize the sample collection.

        Parameters
        ----------
        samples : list of Sample, optional
            List of Sample objects to store in the collection
        """
        # this class really does not have mfid or creation time...
        super().__init__(mfid="", dtype="main", creation_time="1993-04-01T01:18:00.0000+01:00")

        # store samples
        self._samples = samples if samples is not None else []

        # set up internal structure
        self._setup_mapping()

        return

    def _setup_mapping(self):
        """Create internal mappings for fast sample lookup."""
        # define sample maps for fast lookups
        self._samples_by_id = {sample.unique_id: sample for sample in self._samples}
        self._samples_by_name = {sample.sample_name: sample for sample in self._samples}

        return

    @property
    def samples(self):
        """Get list of all samples in the collection."""
        return self._samples

    @property
    def nsamples(self):
        """Get number of samples in the collection."""
        return len(self._samples)

    def get_sample(self, sample_id=None, sample_name=None):
        """
        Get sample by its identifier.

        Parameters
        ----------
        sample_id : str, optional
            Unique ID of the sample
        sample_name : str, optional
            Name of the sample

        Returns
        -------
        Sample or None
            The matching Sample object, or None if not found
        """
        if sample_id is not None:
            return self._samples_by_id.get(sample_id)
        elif sample_name is not None:
            return self._samples_by_name.get(sample_name)
        else:
            logger.warning("get_sample called without sample_id or sample_name")
            return

    def __len__(self):
        """Return number of samples in the collection."""
        return len(self.samples)

    def __iter__(self):
        """Make the collection iterable."""
        return iter(self._samples)

    def __getitem__(self, index):
        """
        Access samples by index, name, or ID.

        Parameters
        ----------
        index : int, str, or slice
            - int: Access sample by position
            - str: Access sample by ID or name
            - slice: Get a subset of samples

        Returns
        -------
        Sample or collection
            Single Sample for int/str index, or sliced collection for slice
        """
        if isinstance(index, str):  # String lookup: try ID first, then name
            sample = self._samples_by_id.get(index)
            if sample is None:
                sample = self._samples_by_name.get(index)
            if sample is None:
                raise KeyError(f"Sample with ID or name '{index}' not found.")
            return sample

        elif isinstance(index, slice):  # Slice
            sliced_samples = self.samples[index]
            return self._create_sliced_collection(sliced_samples)

        elif isinstance(index, int):  # Integer index
            return self.samples[index]

        else:
            raise TypeError("Index must be either a string, slice, or an integer.")

    def _create_sliced_collection(self, sliced_samples):
        """
        Create a new collection from sliced samples.

        Subclasses should override this method to return the appropriate
        collection type with necessary parameters preserved.

        Parameters
        ----------
        sliced_samples : list
            List of Sample objects from slicing operation

        Returns
        -------
        SampleCollection
            New collection instance with sliced samples
        """
        # Default implementation returns a plain list
        # Subclasses should override to return proper typed collections
        return sliced_samples

    def __contains__(self, sample):
        """Check if a sample is in the collection."""
        return sample in self.samples

    def __repr__(self):
        """Return string representation of the collection."""
        return f"{self.__class__.__name__}({self.nsamples} samples)"
