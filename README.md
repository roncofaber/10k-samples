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

`tksamples` uses the [nano-crucible](https://github.com/MolecularFoundryCrucible/nano-crucible) package for Crucible API access. Configuration is managed through `nano-crucible`.

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
from crucible.config import create_config_file
create_config_file('your_api_key_here')
```

3. **Manual config file**: Create `~/.config/nano-crucible/config.ini`:
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

By default, cached data is stored in `~/.cache/nano-crucible/` (Linux/macOS) or `%LOCALAPPDATA%\nano-crucible\` (Windows).

Customize cache location:
- Environment variable: `export PYCRUCIBLE_CACHE_DIR='/path/to/cache'`
- Config file: Set `cache_dir` as shown above
- CLI: `crucible config set cache_dir /path/to/cache`

## Quick Start

### Working with Crucible Projects

The recommended way to work with samples is through the `CrucibleProject` class, which loads all samples and relationships from a Crucible project.

```python
from tksamples.project import CrucibleProject

# Load a project from Crucible
project_id = "10k_perovskites"
proj = CrucibleProject(project_id)

# Get a collection of samples by type
tfilms = proj.get_samples_collection("thin film")
psolus = proj.get_samples_collection("PS")  # Precursor solutions

# Retrieve measurement data (uses cache by default)
tfilms.get_uvvis_data()    # Load UV-Vis spectroscopy data
tfilms.get_well_images()   # Load sample well images

# Access individual samples
sample = tfilms[0]
print(f"Sample {sample.sample_name} has {len(sample.measurements)} measurements")

# Access samples by name or ID
sample_by_name = tfilms["sample_name"]
sample_by_id = tfilms["unique_id_here"]
```

### Direct Samples Loading (Alternative)

You can also load samples directly without a project:

```python
from tksamples import Samples

# Load all samples of a specific type
tfilms = Samples(
    project_id="10k_perovskites",
    sample_type="thin film",
    from_crucible=True,
    use_cache=True,
    overwrite_cache=False
)

# Retrieve measurement data
tfilms.get_uvvis_data()
tfilms.get_well_images()
```

### Configuring Cache Behavior

Control caching when loading projects or samples:

```python
# Use custom cache directory and disable caching
proj = CrucibleProject(
    project_id="10k_perovskites",
    use_cache=False,               # Don't use cached data
    overwrite_cache=True,          # Overwrite existing cache
    cache_dir="/path/to/cache"     # Custom cache location
)

# Same options work for Samples
tfilms = proj.get_samples_collection("thin film")
# Cache settings are inherited from project
```

## Requirements

- Python ≥ 3.8
- [nano-crucible](https://github.com/MolecularFoundryCrucible/nano-crucible) - Crucible API client and configuration management

See `pyproject.toml` for full dependency list.

## Examples

Check the `tksamples/examples/` directory for detailed usage examples:

## Contributing

Contributions welcome! Please submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

**Fabrice Roncoroni** - [fabrice.roncoroni@gmail.com](mailto:fabrice.roncoroni@gmail.com)