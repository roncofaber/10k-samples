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

The package requires a Crucible API key. You can configure it in two ways:

1. **Environment variable** (recommended for temporary use):
```bash
export CRUCIBLE_API_KEY='your_api_key_here'
```

2. **Config file** (recommended for persistent configuration):
```python
from tksamples.crucible.config import create_config_file
create_config_file('your_api_key_here')
```

This creates a config file at `~/.config/tksamples/config.ini` on Linux/macOS or `%APPDATA%\tksamples\config.ini` on Windows.

### Cache Directory Configuration

By default, cached data is stored in the platform-specific cache directory (`~/.cache/tksamples/` on Linux, `~/Library/Caches/tksamples/` on macOS, `%LOCALAPPDATA%\tksamples\` on Windows).

You can customize the cache location:

1. **Environment variable**:
```bash
export TKSAMPLES_CACHE_DIR='/path/to/your/cache'
```

2. **Config file**: Add to your `~/.config/tksamples/config.ini`:
```ini
[crucible]
api_key = your_api_key_here
cache_dir = /path/to/your/cache
```

3. **Programmatically**:
```python
from tksamples.crucible.config import create_config_file
create_config_file('your_api_key_here', cache_dir='/path/to/your/cache')
```

## Quick Start

### Working with Crucible Database

```python
# Load relevant modules
from tksamples import ThinFilms  # Import the ThinFilms class from the tksamples package

# Initialize the ThinFilms object
# Use cache to avoid redundant downloads and set overwrite_cache to False
tfilms = ThinFilms(from_crucible=True, use_cache=True, overwrite_cache=False)

# Retrieve well images for the thin films
tfilms.get_well_images()

# Retrieve UV-Vis data for the thin films
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