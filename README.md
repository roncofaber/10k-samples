# 10k Thin Film Sample Analysis

`tksamples` is the main Python interface for the analysis of the multimodal datasets of 10,000 thin film samples. It integrates the [Crucible API](https://crucible.lbl.gov/) to enable automated sample characterization workflows.

## Installation

```bash
# Install from source
git clone https://github.com/roncofaber/10k-samples.git
cd 10k-samples
pip install -e .
```

## Configuration

### Setting up Crucible API Access

`tksamples` uses the [pycrucible](https://github.com/MolecularFoundryCrucible/pycrucible) package for Crucible API access. Configuration is managed through `pycrucible`.

**Recommended: Use the interactive setup wizard**
```bash
crucible config init
```

This will guide you through setting up your API key and other settings.

**Alternative configuration methods:**

1. **Environment variable** (temporary use):
```bash
export CRUCIBLE_API_KEY='your_api_key_here'
```

2. **Programmatic setup**:
```python
from pycrucible.config import create_config_file
create_config_file('your_api_key_here')
```

3. **Manual config file**: Create `~/.config/pycrucible/config.ini`:
```ini
[crucible]
api_key = your_api_key_here
api_url = https://crucible.lbl.gov/testapi
cache_dir = /path/to/your/cache  # optional
orcid_id = 0000-0001-2345-6789   # optional
```

**Get your API key:** https://crucible.lbl.gov/testapi/user_apikey

### Managing Configuration with CLI

View and manage your configuration:

```bash
# Show all settings
crucible config show

# Get a specific value
crucible config get api_key

# Set a value
crucible config set cache_dir ~/.cache/my-cache

# Edit config file directly
crucible config edit
```

### Cache Directory

By default, cached data is stored in `~/.cache/pycrucible/` (Linux/macOS) or `%LOCALAPPDATA%\pycrucible\` (Windows).

Customize cache location:
- Environment variable: `export PYCRUCIBLE_CACHE_DIR='/path/to/cache'`
- Config file: Set `cache_dir` as shown above
- CLI: `crucible config set cache_dir /path/to/cache`

## Quick Start

### Working with Crucible Database

```python
# Load relevant modules
from tksamples import Samples  # Import the Samples class from the tksamples package

# Initialize the Samples object
# Use cache to avoid redundant downloads and set overwrite_cache to False
samples = Samples(from_crucible=True, use_cache=True, overwrite_cache=False)

# Retrieve well images for the thin films
samples.get_well_images()

# Retrieve UV-Vis data for the thin films
samples.get_uvvis_data()

# Access individual samples with their measurements
sample = samples[0]
print(f"Sample {sample.sample_name} has {len(sample.measurements)} measurements")
```

## Requirements

- Python ≥ 3.8
- [pycrucible](https://github.com/MolecularFoundryCrucible/pycrucible) - Crucible API client and configuration management

See `pyproject.toml` for full dependency list.

## Examples

Check the `tksamples/examples/` directory for detailed usage examples:

## Contributing

Contributions welcome! Please submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

**Fabrice Roncoroni** - [fabrice.roncoroni@gmail.com](mailto:fabrice.roncoroni@gmail.com)