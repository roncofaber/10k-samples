# tksamples

**UV-Vis Spectroscopy and Thin Film Sample Analysis**

`tksamples` provides tools for UV-Vis spectroscopy analysis of thin film samples, with support for HDF5 data processing, Crucible API integration, and automated sample characterization workflows.

## Installation

```bash
# Install from source
git clone https://github.com/roncofaber/10k-samples.git
cd 10k-samples
pip install -e .

# For image processing features
pip install -e ".[image]"
```

## Quick Start

### Working with Crucible Database

```python
from tksamples import TKSamples

# Load thin film samples from Crucible
tfilms = TKSamples()
print(f"Loaded {tfilms.nsamples} samples")

# Get UV-Vis measurements (automatically reads H5 files and associates with samples)
tfilms.get_uvvis_data()

# Access individual samples with their measurements
sample = tfilms[0]
print(f"Sample {sample.sample_name} has {len(sample.measurements)} measurements")
```

### Direct H5 File Analysis

```python
from tksamples import h5_to_samples

# Load samples directly from HDF5 file
samples = h5_to_samples("data.h5", erange=(320, 650))
print(f"Loaded {len(samples)} samples")

# Analyze measurements
for sample in samples:
    sample.plot_sample()
    inhomogeneity = sample.get_inhomogeneity()
```

## Requirements

See `requirements.txt` for full dependency list. Python ≥ 3.8 required.

**Core dependencies:**
- h5py ≥ 3.7.0 (HDF5 file handling)
- numpy ≥ 1.21.0 (numerical computing)
- scipy ≥ 1.7.0 (scientific computing)
- matplotlib ≥ 3.5.0 (plotting)
- seaborn ≥ 0.11.0 (statistical visualization)
- tqdm ≥ 4.64.0 (progress bars)
- qrcode ≥ 7.4.0 (QR code generation)
- pillow ≥ 9.0.0 (image processing)
- requests ≥ 2.28.0 (HTTP requests)

**Optional dependencies:**
- scikit-image ≥ 0.19.0 (for image analysis features)
- pycrucible (for Crucible API access)

## Examples

Check the `tksamples/examples/` directory for detailed usage examples:
- `analyze_sample_example.py` - Basic sample analysis workflow
- `check_stability.py` - Sample stability analysis

## Contributing

Contributions welcome! Please submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

**Fabrice Roncoroni** - [fabrice.roncoroni@gmail.com](mailto:fabrice.roncoroni@gmail.com)