#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization: Genealogy Graph Plotting

Functions for visualizing sample genealogy graphs with various layouts
and highlighting options.

Created on Tue Feb 4 2026
@author: roncofaber
"""

import logging

# Set up logger for this module
logger = logging.getLogger(__name__)


def plot_genealogy_graph(graph, figsize=(12, 8), node_size=500, font_size=8,
                         layout='hierarchical', sample_type_colors=None):
    """
    Plot the full genealogy graph.

    Parameters
    ----------
    graph : networkx.DiGraph
        Genealogy graph to plot
    figsize : tuple, optional
        Figure size (width, height) in inches
    node_size : int, optional
        Size of nodes in the plot
    font_size : int, optional
        Font size for node labels
    layout : str, optional
        Layout algorithm: 'hierarchical', 'spring', 'circular', 'kamada_kawai'
    sample_type_colors : dict, optional
        Dictionary mapping sample_type to color (e.g., {'thin film': 'blue', 'PS': 'green', 'SS': 'red'})

    Returns
    -------
    fig, ax
        Matplotlib figure and axis objects
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError(f"Required package not installed: {e}")

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Choose layout
    if layout == 'hierarchical':
        pos = _hierarchical_layout(graph)
    elif layout == 'spring':
        pos = nx.spring_layout(graph, seed=42)
    elif layout == 'circular':
        pos = nx.circular_layout(graph)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(graph)
    else:
        logger.warning(f"Unknown layout '{layout}', using spring layout")
        pos = nx.spring_layout(graph, seed=42)

    # Set node colors by sample type
    if sample_type_colors is None:
        sample_type_colors = {
            'thin film': '#3498db',  # Blue
            'PS': '#2ecc71',          # Green
            'SS': '#e74c3c'           # Red
        }

    node_colors = []
    for node in graph.nodes():
        sample_type = graph.nodes[node].get('type', 'unknown')
        node_colors.append(sample_type_colors.get(sample_type, '#95a5a6'))  # Gray for unknown

    # Draw the graph
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_size, ax=ax)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', arrows=True,
                           arrowsize=10, arrowstyle='->', ax=ax)

    # Add labels (sample names)
    labels = {node: graph.nodes[node].get('name', node[:8]) for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels, font_size=font_size, ax=ax)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=stype)
                      for stype, color in sample_type_colors.items()]
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_title(f"Genealogy Graph ({graph.number_of_nodes()} samples, {graph.number_of_edges()} edges)")
    ax.axis('off')
    plt.tight_layout()

    return fig, ax


def plot_ancestry_subgraph(graph, sample_mfid, figsize=(10, 6), node_size=800,
                           font_size=10, highlight_color='#f39c12'):
    """
    Plot the ancestry (all ancestors) of a specific sample.

    Parameters
    ----------
    graph : networkx.DiGraph
        Full genealogy graph
    sample_mfid : str
        MFID of the sample to trace ancestry from
    figsize : tuple, optional
        Figure size (width, height) in inches
    node_size : int, optional
        Size of nodes in the plot
    font_size : int, optional
        Font size for node labels
    highlight_color : str, optional
        Color to highlight the target sample

    Returns
    -------
    fig, ax
        Matplotlib figure and axis objects
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError(f"Required package not installed: {e}")

    # Get all ancestors
    ancestors = nx.ancestors(graph, sample_mfid)

    # Create subgraph with target sample and all ancestors
    nodes_to_include = list(ancestors) + [sample_mfid]
    subgraph = graph.subgraph(nodes_to_include).copy()

    if subgraph.number_of_nodes() == 0:
        logger.warning(f"No ancestors found for sample {sample_mfid}")
        return None, None

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Use hierarchical layout
    pos = _hierarchical_layout(subgraph)

    # Color nodes by sample type, highlight the target
    sample_type_colors = {
        'thin film': '#3498db',
        'PS': '#2ecc71',
        'SS': '#e74c3c'
    }

    node_colors = []
    for node in subgraph.nodes():
        if node == sample_mfid:
            node_colors.append(highlight_color)  # Highlight target
        else:
            sample_type = subgraph.nodes[node].get('type', 'unknown')
            node_colors.append(sample_type_colors.get(sample_type, '#95a5a6'))

    # Draw the graph
    nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=node_size, ax=ax)
    nx.draw_networkx_edges(subgraph, pos, edge_color='gray', arrows=True,
                           arrowsize=15, arrowstyle='->', width=2, ax=ax)

    # Add labels
    labels = {node: subgraph.nodes[node].get('name', node[:8]) for node in subgraph.nodes()}
    nx.draw_networkx_labels(subgraph, pos, labels, font_size=font_size, ax=ax)

    target_name = graph.nodes[sample_mfid].get('name', sample_mfid[:8])
    ax.set_title(f"Ancestry of {target_name}")
    ax.axis('off')
    plt.tight_layout()

    return fig, ax


def plot_lineage_subgraph(graph, sample_mfid, figsize=(10, 8), node_size=800,
                         font_size=10, highlight_color='#f39c12'):
    """
    Plot the full lineage (ancestors and descendants) of a specific sample.

    Parameters
    ----------
    graph : networkx.DiGraph
        Full genealogy graph
    sample_mfid : str
        MFID of the sample to trace lineage from
    figsize : tuple, optional
        Figure size (width, height) in inches
    node_size : int, optional
        Size of nodes in the plot
    font_size : int, optional
        Font size for node labels
    highlight_color : str, optional
        Color to highlight the target sample

    Returns
    -------
    fig, ax
        Matplotlib figure and axis objects
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError(f"Required package not installed: {e}")

    # Get all ancestors and descendants
    ancestors = nx.ancestors(graph, sample_mfid)
    descendants = nx.descendants(graph, sample_mfid)

    # Create subgraph with target sample, ancestors, and descendants
    nodes_to_include = list(ancestors) + [sample_mfid] + list(descendants)
    subgraph = graph.subgraph(nodes_to_include).copy()

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Use hierarchical layout
    pos = _hierarchical_layout(subgraph)

    # Color nodes by sample type, highlight the target
    sample_type_colors = {
        'thin film': '#3498db',
        'PS': '#2ecc71',
        'SS': '#e74c3c'
    }

    node_colors = []
    for node in subgraph.nodes():
        if node == sample_mfid:
            node_colors.append(highlight_color)  # Highlight target
        else:
            sample_type = subgraph.nodes[node].get('type', 'unknown')
            node_colors.append(sample_type_colors.get(sample_type, '#95a5a6'))

    # Draw the graph
    nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=node_size, ax=ax)
    nx.draw_networkx_edges(subgraph, pos, edge_color='gray', arrows=True,
                           arrowsize=15, arrowstyle='->', width=2, ax=ax)

    # Add labels
    labels = {node: subgraph.nodes[node].get('name', node[:8]) for node in subgraph.nodes()}
    nx.draw_networkx_labels(subgraph, pos, labels, font_size=font_size, ax=ax)

    target_name = graph.nodes[sample_mfid].get('name', sample_mfid[:8])
    ax.set_title(f"Full Lineage of {target_name}")
    ax.axis('off')
    plt.tight_layout()

    return fig, ax


def _hierarchical_layout(graph):
    """
    Create a hierarchical layout for a directed acyclic graph.

    Nodes are positioned in layers based on their depth from root nodes.

    Parameters
    ----------
    graph : networkx.DiGraph
        Directed graph

    Returns
    -------
    dict
        Dictionary mapping nodes to (x, y) positions
    """
    try:
        import networkx as nx
    except ImportError:
        raise ImportError("networkx is required")

    # Find all layers (using topological generations)
    layers = {}
    for node in nx.topological_sort(graph):
        # Get the maximum layer of all parents + 1
        parents = list(graph.predecessors(node))
        if not parents:
            layers[node] = 0  # Root node
        else:
            layers[node] = max(layers[p] for p in parents) + 1

    # Group nodes by layer
    layer_nodes = {}
    for node, layer in layers.items():
        if layer not in layer_nodes:
            layer_nodes[layer] = []
        layer_nodes[layer].append(node)

    # Position nodes
    pos = {}
    max_layer = max(layer_nodes.keys()) if layer_nodes else 0

    for layer, nodes in layer_nodes.items():
        y = 1.0 - (layer / max(max_layer, 1))  # Invert so roots are at top
        n_nodes = len(nodes)

        for i, node in enumerate(sorted(nodes)):
            if n_nodes == 1:
                x = 0.5
            else:
                x = i / (n_nodes - 1)
            pos[node] = (x, y)

    return pos
