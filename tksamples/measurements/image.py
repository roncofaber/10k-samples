#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:44:31 2026

@author: roncofaber
"""

# image stuff
from PIL import Image
import matplotlib.pyplot as plt

# internal modules
from tksamples.measurements.measurement import Measurement

#%%

class TFImage(Measurement):
    
    def __init__(self, image=None, dataset=None):
        
        # Get sample info
        scientific_metadata = dataset.get("scientific_metadata")["scientific_metadata"]
        
        
        # initialize measurement
        super().__init__(
            dataset = dataset,
            sample_name = scientific_metadata["sample_name"],
            sample_mfid = scientific_metadata["sample_mfid"],
            measurement_type = "Image"
            )
        
        self.dataset = dataset
        self.image = Image.open(image)
        
        return
    
    def view(self, console=False):
        """Display the image associated with the instance."""
        
        # Check if self.image exists and is valid for display
        if hasattr(self, 'image') and self.image is not None:
            plt.figure(figsize=(3, 3))  # Set figure size to 4x4 inches
            plt.imshow(self.image, cmap='gray')  # Adjust colormap as needed
            plt.axis('off')  # Turn off axes for a cleaner look
            
            if console:
                plt.show()  # Show the plot inline
            else:
                plt.show(block=True)  # Open a separate window
                
        else:
            print("No image to display.")