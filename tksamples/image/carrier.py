#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 13:55:47 2026

@author: roncofaber
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from skimage import color, filters, measure, morphology
import skimage

def crop_image(original_image, labeled_image, label):
    """Crop image to bounding box of specified label region."""
    # Create a binary mask for region
    mask = labeled_image == label
    
    # Find the bounding box of region
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # Crop the original image to the bounding box
    cropped_image = original_image[rmin:rmax+1, cmin:cmax+1]
    
    return cropped_image


def detect_and_crop_holder(image, threshold=0.31, max_object_size=500):
    """Detect the black holder frame and crop to the central region."""
    image_array = image.copy()
    
    # Convert to grayscale
    gray = color.rgb2gray(image_array)
    
    # Thresholding to detect the black holder (frame)
    binary = gray < threshold
    
    # Remove small objects
    binary = morphology.remove_small_objects(binary, max_size=max_object_size)
    
    # Label connected components
    labeled = measure.label(binary)
    
    # Find the properties of the labeled regions
    properties = measure.regionprops(labeled)
    
    # Assume the largest contour is the black holder (frame)
    largest_region = max(properties, key=lambda r: r.area)
    
    # Create a mask for the largest region (the frame)
    frame_mask = np.zeros_like(gray, dtype=bool)
    frame_mask[labeled == largest_region.label] = True
    
    # Label again to find central object
    labeled_binary = measure.label(frame_mask)
    
    # Flood fill from center
    h, w = labeled_binary.shape
    flooded = skimage.segmentation.flood_fill(labeled_binary, (h//2, w//2), new_value=67)
    
    cropped_image = crop_image(image_array, flooded, 67)
    
    return cropped_image


def find_horizontal_peaks(gray_image, bar_height=20, bar_width=2000, 
                          peak_height=0.6, peak_distance=400,
                          middle_start=500, middle_end=3000):
    """
    Slide a horizontal bar along y-axis and find the 3 middle peaks.
    
    Returns:
        three_peaks: array of y-positions of the 3 peaks
        intensity_diffs: full intensity difference array
    """
    height, width = gray_image.shape
    
    # Center x position
    x_center = width // 2
    bar_x_start = max(0, x_center - bar_width // 2)
    bar_x_end = min(width, x_center + bar_width // 2)
    
    # Array to store intensity differences
    intensity_diffs = []
    
    # Slide the bar along y-axis
    for y in range(height - bar_height + 1):
        # Extract the region where the bar would be
        bar_region = gray_image[y:y+bar_height, bar_x_start:bar_x_end]
        
        # Calculate mean absolute difference from white
        diff = np.mean(np.abs(bar_region.astype(float) - 1))
        
        intensity_diffs.append(diff)
    
    intensity_diffs = 1 - np.array(intensity_diffs)
    
    # Find all peaks in the data
    peaks, _ = find_peaks(intensity_diffs, height=peak_height, distance=peak_distance)
    
    # Filter peaks to only those in the middle region
    middle_peaks = peaks[(peaks >= middle_start) & (peaks <= middle_end)]
    
    # Sort by height and take the top 3
    peak_heights = intensity_diffs[middle_peaks]
    top_3_indices = np.argsort(peak_heights)[-3:]
    three_peaks = middle_peaks[top_3_indices]
    three_peaks = np.sort(three_peaks)  # Sort by position
    
    return three_peaks, intensity_diffs


def create_cross_mask(size=400, width=20):
    """Create a cross mask with specified size and arm width."""
    mask = np.zeros((size, size), dtype=bool)
    center = size // 2
    half_width = width // 2
    
    # Make cross black (0.0) - inverted so cross is darker
    mask[:, center-half_width:center+half_width] = True
    mask[center-half_width:center+half_width, :] = True
    
    return mask


def find_cross_peaks_at_y(gray_image, y_positions, cross_size=400, cross_width=20,
                          peak_height=0.6, peak_distance=100):
    """
    Slide a cross mask along x-axis at specified y-positions and find the top 3 cross peaks per y-position.
    Returns up to 3 crosses at each y-position (similar to how find_horizontal_peaks works for y-axis).

    Args:
        gray_image: grayscale image
        y_positions: array of y-coordinates where to slide the cross
        cross_size: size of the cross mask
        cross_width: width of cross arms in pixels
        peak_height: minimum peak height
        peak_distance: minimum distance between peaks

    Returns:
        cross_coordinates: list of (x, y) coordinates for up to 3 crosses per y-position
        all_results: list of intensity arrays for visualization
    """
    # Create the cross mask (white cross on black background)
    cross_mask = create_cross_mask(cross_size, cross_width)
    mask_height, mask_width = cross_mask.shape
    half_height = mask_height // 2
    half_width = mask_width // 2

    # Store results for each peak
    all_results = []
    cross_coordinates = []

    for peak_y in y_positions:
        intensity_x = []

        # Determine y range for the cross (centered at peak_y)
        y_start = peak_y - half_height
        y_end = peak_y + half_height

        # Skip if cross doesn't fit in image
        if y_start < 0 or y_end > gray_image.shape[0]:
            print(f"Warning: Cross at y={peak_y} doesn't fit in image, skipping")
            continue

        # Slide the cross along x-axis
        for x in range(gray_image.shape[1] - mask_width + 1):
            x_start = x
            x_end = x + mask_width

            # Extract the region where cross would be placed
            region = gray_image[y_start:y_end, x_start:x_end]

            # Calculate mean absolute difference (same strategy as horizontal bar)
            diff = np.mean(np.abs(region.astype(float) - 1)[cross_mask])

            intensity_x.append(diff)

        # Convert to numpy array and invert (same as horizontal bar: 1 - diff)
        intensity_x = 1 - np.array(intensity_x)
        all_results.append(intensity_x)

        # Find peaks in the intensity array
        peaks_x, _ = find_peaks(intensity_x, height=peak_height, distance=peak_distance)

        # Get intensity scores for all peaks at this y-position
        crosses_at_this_y = []
        for peak_idx in peaks_x:
            x_coord = peak_idx + half_width  # Add half_width to get center position
            intensity_score = intensity_x[peak_idx]
            crosses_at_this_y.append((x_coord, peak_y, intensity_score))

        # Sort by intensity score (highest first) and take top 3 for this y-position
        crosses_at_this_y.sort(key=lambda x: x[2], reverse=True)
        top_3_at_this_y = crosses_at_this_y[:3]

        # Add the top 3 crosses at this y-position to the final list
        for x_coord, y_coord, _ in top_3_at_this_y:
            cross_coordinates.append((x_coord, y_coord))
    
    cross_coordinates = np.array(cross_coordinates)
            
    sorted_indices = np.lexsort((cross_coordinates[:, 0], cross_coordinates[:, 1]))
    sorted_coordinates = cross_coordinates[sorted_indices]

    return sorted_coordinates



def visualize_cross_peaks(all_results, y_positions, cross_coordinates):
    """Visualize the cross sweep results."""
    fig, axes = plt.subplots(len(all_results), 1, figsize=(10, 3*len(all_results)))
    if len(all_results) == 1:
        axes = [axes]
    
    for i, (intensity_x, peak_y) in enumerate(zip(all_results, y_positions)):
        axes[i].plot(intensity_x)
        
        # Mark peaks for this y position
        peaks_at_y = [x for x, y in cross_coordinates if y == peak_y]
        if peaks_at_y:
            # Convert x coordinates back to indices for plotting
            cross_size = 400  # Should match the parameter used
            half_width = cross_size // 2
            peak_indices = [x - half_width for x in peaks_at_y]
            axes[i].plot(peak_indices, intensity_x[peak_indices], "rx", markersize=10, label='Detected crosses')
        
        axes[i].set_title(f'Cross sweep at y={peak_y}')
        axes[i].set_xlabel('X position')
        axes[i].set_ylabel('Intensity')
        axes[i].legend()
    
    plt.tight_layout()
    plt.show()

def visualize_horizontal_peaks(intensity_diffs, three_peaks):
    """Visualize the horizontal bar sweep results."""
    plt.figure(figsize=(10, 4))
    plt.plot(intensity_diffs)
    plt.plot(three_peaks, intensity_diffs[three_peaks], "rx", markersize=10, label='Detected peaks')
    plt.xlabel("Y position")
    plt.ylabel("Intensity")
    plt.title("Horizontal Bar Sweep")
    plt.legend()
    plt.show()