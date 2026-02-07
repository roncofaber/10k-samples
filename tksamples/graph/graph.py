#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graph Utilities: Genealogy Graph Construction and Analysis

Functions for building and analyzing NetworkX graphs from sample genealogy data,
including graph construction, traversal, and relationship analysis.

Created on Tue Feb 4 2026
@author: roncofaber
"""

import networkx as nx
import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


def build_project_graph(samples):
    
    # Create directed graph
    G = nx.DiGraph()

    # Add all samples as nodes
    for sample in samples:
        G.add_node(sample, name=sample.sample_name, type=sample.sample_type,
                   mfid=sample.mfid)

    # Add edges based on parent-child relationships
    for sample in samples:
        for parent in sample.parents:
            # Edge from parent to child
            G.add_edge(parent, sample)

    logger.info(f"Built genealogy graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    return G
