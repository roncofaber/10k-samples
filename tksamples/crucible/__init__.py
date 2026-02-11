"""
Crucible API integration module for tksamples

Functions for downloading datasets and measurements from Crucible API.
Separated into client (basic functions) and converters (measurement-dependent).
Also includes configuration management for API keys.
"""

# Configuration functions (no dependencies)
from .config import (
    config,
    get_crucible_api_key,
    get_cache_dir,
    get_orcid_id,
    create_config_file,
    get_config_file_path,
)

# Core client functions (no circular import issues)
from .client import (
    setup_crux_client,
    get_data_from_crux,
    get_links_with_extension,
)

# NOTE: Data conversion functions are NOT imported here to avoid circular imports
# Import get_uvvis_measurement directly from .converters where needed

__all__ = [
    "config",
    "get_crucible_api_key",
    "get_cache_dir",
    "get_orcid_id",
    "create_config_file",
    "get_config_file_path",
    "setup_crux_client",
    "get_data_from_crux",
    "get_links_with_extension",
    # "get_uvvis_measurement",  # Available in .converters but not exported here
]