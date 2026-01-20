#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 13:55:47 2026

@author: roncofaber
"""

# scientific computing
import numpy as np
from scipy.signal import find_peaks

# image recognition
from skimage import color, morphology, transform
from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from skimage.filters import gaussian

#%%

def isolate_carrier(image, threshold=0.31, max_object_size=500,
                    rotate=False):

    """Detect the black holder frame and crop to the central region."""
    image_array = image.copy()
    
    # Convert to grayscale
    gray = color.rgb2gray(image_array)
    
    # Thresholding to detect the black holder (frame)
    binary = gray < threshold
    
    # Remove small objects
    binary = morphology.remove_small_objects(binary, max_size=max_object_size)
    
    # Remove outside area anyway
    left   = np.where(binary.sum(axis=0) >0)[0][0]
    right  = np.where(binary.sum(axis=0) >0)[0][-1]
    top    = np.where(binary.sum(axis=1) >0)[0][0]
    bottom = np.where(binary.sum(axis=1) >0)[0][-1]
    
    image_array = image_array[top:bottom,left:right]
    
    if rotate:
        _, tilt_rad, _ = find_carrier_tilt(image)
        image_array = transform.rotate(image_array, np.rad2deg(tilt_rad))
    
    return image_array



def find_carrier_tilt(image, gaussian_sigma: float = 1.0, canny_sigma: float = 2.0,
                  vertical_angle_tolerance: float = 10.0):


    # --- 1. Pre-processing ---
    image_gray = color.rgb2gray(image)
    image_blurred = gaussian(image_gray, sigma=gaussian_sigma)

    # --- 2. Edge Detection ---
    edges = canny(image_blurred, sigma=canny_sigma, low_threshold=0.1, high_threshold=0.3)

    # --- 3. Line Detection ---
    h_space, h_angles, h_dists = hough_line(edges)
    accum, angles, dists = hough_line_peaks(h_space, h_angles, h_dists, num_peaks=10)

    # --- 4. Filter for the Left Edge ---
    best_line = None
    min_angle_abs = float('inf')

    for angle, dist in zip(angles, dists):
        angle_deg = np.rad2deg(angle)
        # We are looking for an angle close to 0 (vertical)
        if abs(angle_deg) < vertical_angle_tolerance:
            if abs(angle) < min_angle_abs:
                min_angle_abs = abs(angle)
                best_line = (angle, dist)

    if best_line is None:
        return None

    # --- 5. Extract and return results ---
    final_angle_rad, final_dist = best_line
    orientation_deg = np.rad2deg(final_angle_rad)

    return orientation_deg, final_angle_rad, final_dist


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


def carrier2samples(image, threshold=0.31, max_object_size=500, bar_height=20, bar_width=2000,
                     peak_height=0.6, peak_distance=400, middle_start=500, middle_end=3000,
                     cross_size=400, cross_width=20, rotate=False):
    """
    Extract 16 segments from a tray image using cross detection for grid alignment.

    Parameters
    ----------
    image : ndarray
        Input tray image (RGB or grayscale)
    threshold : float, optional
        Threshold for holder detection (default: 0.31)
    max_object_size : int, optional
        Maximum object size for noise removal (default: 500)
    bar_height : int, optional
        Height of horizontal scan bar (default: 20)
    bar_width : int, optional
        Width of horizontal scan bar (default: 2000)
    peak_height : float, optional
        Minimum peak height for detection (default: 0.6)
    peak_distance : int, optional
        Minimum distance between peaks (default: 400)
    middle_start : int, optional
        Start of middle region for peak search (default: 500)
    middle_end : int, optional
        End of middle region for peak search (default: 3000)
    cross_size : int, optional
        Size of cross search area (default: 400)
    cross_width : int, optional
        Width of cross search bar (default: 20)

    Returns
    -------
    segments : list
        List of 16 image segments (4x4 grid)
    segment_info : list
        List of dictionaries with segment metadata
    cropped_image : ndarray
        The cropped and processed image
    grid_lines : dict
        Dictionary with 'x_grid' and 'y_grid' coordinates
    """

    # Step 1: Detect and crop holder
    image = isolate_carrier(image, threshold=threshold,
                            max_object_size=max_object_size, rotate=rotate)

    # Step 3: Convert to grayscale (now on potentially rotated image)
    image_gray = color.rgb2gray(image)

    # Step 4: Find horizontal peaks (rows with samples)
    three_peaks, _ = find_horizontal_peaks(
        image_gray, bar_height=bar_height, bar_width=bar_width,
        peak_height=peak_height, peak_distance=peak_distance,
        middle_start=middle_start, middle_end=middle_end)

    # Step 5: Find cross positions at each y-position
    cross_coordinates = find_cross_peaks_at_y(
        image_gray, three_peaks, cross_size=cross_size, cross_width=cross_width,
        peak_height=peak_height, peak_distance=peak_distance)

    # Step 6: Calculate grid boundaries from cross positions
    y_sorted = sorted(cross_coordinates[:, 1])
    x_sorted = sorted(cross_coordinates[:, 0])

    # Average positions for the 3x3 cross grid
    y_str = int(np.mean(y_sorted[:3]))
    y_mid = int(np.mean(y_sorted[3:6]))
    y_end = int(np.mean(y_sorted[6:9]))

    x_str = int(np.mean(x_sorted[:3]))
    x_mid = int(np.mean(x_sorted[3:6]))
    x_end = int(np.mean(x_sorted[6:9]))

    # Calculate spacing and extrapolate to 4x4 grid
    x_spacing = (x_end - x_str) / 2
    y_spacing = (y_end - y_str) / 2

    x_grid = [
        int(x_str - x_spacing),  # Left boundary
        x_str,                   # First cross column
        x_mid,                   # Middle cross column
        x_end,                   # Right cross column
        int(x_end + x_spacing)   # Right boundary
    ]

    y_grid = [
        int(y_str - y_spacing),  # Top boundary
        y_str,                   # First cross row
        y_mid,                   # Middle cross row
        y_end,                   # Bottom cross row
        int(y_end + y_spacing)   # Bottom boundary
    ]

    # Step 7: Extract 16 segments
    segments = []
    segment_info = []

    for row in range(4):
        for col in range(4):
            # Define boundaries for this segment
            x_start = max(0, x_grid[col])
            x_end = min(image_gray.shape[1], x_grid[col + 1])
            y_start = max(0, y_grid[row])
            y_end = min(image_gray.shape[0], y_grid[row + 1])

            # Extract the segment
            segment = image[y_start:y_end, x_start:x_end]
            segments.append(segment)

            segment_info.append({
                'row': row,
                'col': col,
                'x_range': (x_start, x_end),
                'y_range': (y_start, y_end),
                'shape': segment.shape,
            })

    grid_lines = {'x_grid': x_grid, 'y_grid': y_grid}

    return segments, segment_info, image, grid_lines


def visualize_segmentation(image, segments, segment_info, grid_lines):
    """
    Visualize the segmentation result with grid overlay.

    Parameters
    ----------
    image : ndarray
        Cropped grayscale image
    segments : list
        List of 16 segments
    segment_info : list
        List of segment metadata
    grid_lines : dict
        Grid line coordinates
    """
    import matplotlib.pyplot as plt

    # Main image with grid overlay
    plt.figure(figsize=(12, 8))
    plt.imshow(image, cmap='gray')

    # Draw grid lines
    for x in grid_lines['x_grid']:
        plt.axvline(x=x, color='blue', linestyle='-', alpha=0.7, linewidth=2)
    for y in grid_lines['y_grid']:
        plt.axhline(y=y, color='blue', linestyle='-', alpha=0.7, linewidth=2)

    # Label segments
    for info in segment_info:
        x_center = (info['x_range'][0] + info['x_range'][1]) / 2
        y_center = (info['y_range'][0] + info['y_range'][1]) / 2
        text_color = 'white'
        plt.text(x_center, y_center, f"({info['row']},{info['col']})",
                ha='center', va='center', color=text_color, fontsize=10, fontweight='bold')

    plt.title('4x4 Grid Segmentation using Cross Detection')
    plt.axis('off')
    plt.show()

    # Individual segments
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    fig.suptitle('16 Extracted Segments', fontsize=14)

    for i, (segment, info) in enumerate(zip(segments, segment_info)):
        row, col = info['row'], info['col']
        ax = axes[row, col]

        ax.imshow(segment, cmap='gray')
        ax.set_title(f'({row},{col})', fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.show()