# tksamples

**Thin Film Sample Characterization and Analysis**

`tksamples` is a Python package for characterizing thin film samples through multiple measurement types including UV-Vis spectroscopy, imaging, and other analytical methods.

## Installation

```bash
# Install from source
git clone https://github.com/roncofaber/10k-samples.git
cd 10k-samples
pip install -e .
```

## Quick Start

```python
from tksamples import ThinFilm

# Load thin film sample with automatic measurement retrieval
sample = ThinFilm(uuid="your-sample-uuid", get_measurements=True)
print(f"Sample: {sample.sample_name}")
print(f"Available measurements: {len(sample.measurements)}")

# Access UV-Vis measurement data
uvvis_data = sample.measurements[0]  # First measurement
uvvis_data.plot_sample()
```

### Legacy H5 File Analysis

```python
from tksamples import h5_to_samples

# Load samples from HDF5 file
samples = h5_to_samples("your_data.h5", erange=[320, 650])
print(f"Loaded {len(samples)} samples")

# Analyze first sample
sample = samples[0]
sample.plot_sample()
```

## Requirements

See `requirements.txt` for full dependency list. Python ≥ 3.8 required.

**Core dependencies:**
- h5py ≥ 3.7.0
- numpy ≥ 1.21.0
- scipy ≥ 1.7.0
- matplotlib ≥ 3.5.0
- seaborn ≥ 0.11.0

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