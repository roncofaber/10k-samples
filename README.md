# 10k-samples

**Analysis of UV-Vis spectroscopy data from 10k sample measurements**

`tksamples` is a Python package designed for processing and analyzing UV-Visible spectroscopy data from HDF5 files. It provides tools for reading multi-position spectroscopy measurements, calculating sample inhomogeneity, and visualizing spectral data.

## Features

- 📁 **HDF5 Data Reading**: Import spectroscopy data from HDF5 files
- 📊 **Data Analysis**: Calculate inhomogeneity metrics across multiple measurement spots
- 🎯 **Wavelength Filtering**: Focus analysis on specific wavelength ranges
- 📈 **Visualization**: Generate publication-ready plots with customizable styling
- 🔧 **Modular Design**: Clean, extensible architecture for spectroscopy analysis

## Installation

### Direct Installation from Repository

```bash
# Install directly from GitHub repository
pip install git+https://github.com/roncofaber/10k-samples.git
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/roncofaber/10k-samples.git
cd 10k-samples

# Install in development mode
pip install -e .
```

### Requirements

- Python ≥ 3.8
- h5py ≥ 3.7.0
- numpy ≥ 1.21.0
- scipy ≥ 1.7.0
- matplotlib ≥ 3.5.0
- seaborn ≥ 0.11.0

## Quick Start

```python
from tksamples import h5_to_samples

# Load samples from HDF5 file with wavelength range
samples = h5_to_samples("your_data.h5", erange=[320, 650])

# Analyze first sample
sample = samples[0]
print(f"Sample: {sample.sample_name}")
print(f"Number of measurement spots: {sample.nspots}")

# Calculate inhomogeneity across spots
inhomogeneity = sample.get_inhomogenity(spots=[0, 1, 2, 3])
print(f"Mean inhomogeneity: {inhomogeneity.mean():.3f}")

# Plot the sample spectra
sample.plot_sample(spots=[0, 1, 2, 3])
```

## Usage Examples

### Basic Data Loading and Analysis

```python
from tksamples import h5_to_samples
import numpy as np

# Load spectroscopy data with wavelength filtering
samples = h5_to_samples("measurement_data.h5", erange=[320, 650])

print(f"Loaded {len(samples)} samples")
print(f"Sample 0: {samples[0].sample_name}")
print(f"Position: x={samples[0].x_center:.2f}, y={samples[0].y_center:.2f}")
print(f"Number of measurement spots: {samples[0].nspots}")

# Access different types of spectral data
wavelengths = samples[0].wavelengths                    # Wavelength array
absorbances = samples[0].absorbances                    # Absorbance data (n_spots, n_wavelengths)
transmissions = samples[0].transmissions                # Transmission data
raw_intensities = samples[0].raw_intensities            # Raw intensity data
corrected_intensities = samples[0].cor_intensities      # Dark-corrected intensities
```

### Inhomogeneity Analysis

```python
# Calculate inhomogeneity for specific spots
spots_to_analyze = [0, 1, 2, 3]
inhomogeneity = samples[0].get_inhomogenity(spots=spots_to_analyze)

# Calculate statistics across all samples
mean_values = [sample.get_inhomogenity(spots=spots_to_analyze).mean()
               for sample in samples]
std_values = [sample.get_inhomogenity(spots=spots_to_analyze).std()
              for sample in samples]

print(f"Sample inhomogeneity values: {inhomogeneity}")
print(f"Overall mean inhomogeneity: {np.mean(mean_values):.3f}")

# Access measurement settings
print(f"Integration time: {samples[0].measurement_settings['spectra_int_time']} ms")
print(f"Spectra averaged: {samples[0].measurement_settings['spectra_averaged']}")
```

### Data Visualization

```python
# Plot specific spots for a sample (with y-position labels)
samples[0].plot_sample(spots=[0, 1, 2, 3])

# Plot all spots for a sample
samples[0].plot_sample()  # Uses all available spots

# Plot with custom wavelength range
samples[0].set_erange([400, 550])
samples[0].plot_sample(spots=[0, 1, 2])

# Access position information
print(f"Y-positions: {samples[0].y_positions}")
print(f"Sample center: ({samples[0].x_center}, {samples[0].y_center})")
```

## API Reference

### Core Classes

#### `NirvanaUVVis`

Main class for UV-Vis spectroscopy analysis with comprehensive data handling.

**Properties:**
- `sample_name`: Name identifier for the sample
- `poskey`: Position key from the HDF5 file
- `wavelengths`: Wavelength array (filtered by energy range)
- `absorbances`: Absorbance data array (shape: n_spots × n_wavelengths)
- `transmissions`: Transmission data array (shape: n_spots × n_wavelengths)
- `raw_intensities`: Raw intensity data array (shape: n_spots × n_wavelengths)
- `cor_intensities`: Dark-corrected intensity data array (shape: n_spots × n_wavelengths)
- `nspots`: Number of measurement spots
- `x_center`, `y_center`: Center position coordinates of the sample
- `x_positions`, `y_positions`: Position arrays for individual measurement spots
- `measurement_settings`: Dictionary containing measurement parameters

**Methods:**
- `set_erange(erange=None, left=None, right=None)`: Set wavelength range for analysis
- `set_references(dark_sample=None, blank_sample=None)`: Set dark and blank reference samples
- `get_inhomogenity(spots=None)`: Calculate inhomogeneity metrics between spots
- `plot_sample(spots=None)`: Visualize spectral data with position labels

### Core Functions

#### `h5_to_samples(h5filename, erange=None)`

Load samples from HDF5 file with automatic dark/blank reference handling.

**Parameters:**
- `h5filename` (str): Path to HDF5 file
- `erange` (tuple, optional): Wavelength range [min, max] in nm

**Returns:**
- `list`: List of `NirvanaUVVis` objects (excluding dark and blank references)

## Data Format

The package expects HDF5 files with the following structure:
```
measurement/
└── pollux_oospec_multipos_line_scan/
    ├── wavelengths
    ├── spec_integration_time
    ├── spectra_averaged
    ├── y_scan_length
    └── positions/
        ├── pos_xxx/
        │   ├── sample_name  # Contains "dark_ref" for dark reference
        │   ├── spectral_data
        │   ├── x_center, y_center
        │   └── y_positions
        ├── pos_yyy/
        │   ├── sample_name  # Contains "blank_ref" for blank reference
        │   └── ... (same structure)
        └── pos_zzz/
            ├── sample_name  # Regular sample name
            └── ... (same structure)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Fabrice Roncoroni** - [fabrice.roncoroni@gmail.com](mailto:fabrice.roncoroni@gmail.com)
