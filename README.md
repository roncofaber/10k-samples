# 10k Thin Film Sample Analysis

`tksamples` is the main Python interface for the analysis of the multimodal datasets of 10,000 thin film samples. It integrates the [Crucible API](https://crucible.lbl.gov/) to enable automated sample characterization workflows.

## Installation

```bash
# Install from source
git clone https://github.com/roncofaber/10k-samples.git
cd 10k-samples
pip install -e .
```

## Quick Start

### Working with Crucible Database

```python
from tksamples import TKSamples

# Load thin film samples from Crucible
tfilms = TKSamples(from_crucible=True)
print(f"Loaded {tfilms.nsamples} samples")

# Get UV-Vis measurements (automatically get data from Crucible and associates with samples)
tfilms.get_uvvis_data()

# Access individual samples with their measurements
sample = tfilms[0]
print(f"Sample {sample.sample_name} has {len(sample.measurements)} measurements")
```

## Requirements

See `pyproject.toml` for full dependency list. Python ≥ 3.8 required.

## Examples

Check the `tksamples/examples/` directory for detailed usage examples:

## Contributing

Contributions welcome! Please submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

**Fabrice Roncoroni** - [fabrice.roncoroni@gmail.com](mailto:fabrice.roncoroni@gmail.com)