# Asset Catalog API Reference

This page documents the actual API implementation for the Isaac for Healthcare Asset Catalog.

## Overview

The asset catalog uses a class-based approach where assets are defined as attributes on a class inheriting from `BaseI4HAssets`. Assets are automatically downloaded when accessed.

## Core API

### BaseI4HAssets Class

The main class for defining and accessing assets:

```python
from i4h_asset_helper import BaseI4HAssets

class BaseI4HAssets:
    """Base class for defining I4H assets as class attributes.
    
    Asset paths should be defined as class attributes pointing to
    paths within the asset catalog (e.g., "Props/ABDPhantom/phantom.usda").
    
    Assets are automatically downloaded when accessed.
    """
```

### Key Functions

#### retrieve_asset

Downloads an asset if not already cached:

```python
def retrieve_asset(
    version: str = "0.2.0",
    download_dir: Optional[str] = None,
    sub_path: Optional[str] = None,
    hash: Optional[str] = None,
    force_download: bool = False,
    verbose: bool = False
) -> str:
    """Retrieve an I4H asset.
    
    Args:
        version: Asset catalog version (default: "0.2.0")
        download_dir: Directory to download assets to
        sub_path: Path within the asset catalog
        hash: Expected SHA256 hash
        force_download: Force re-download even if cached
        verbose: Print download progress
        
    Returns:
        Path to the downloaded asset
    """
```

#### get_i4h_asset_path

Get the remote URL for an asset:

```python
def get_i4h_asset_path(
    version: str = "0.2.0",
    sub_path: Optional[str] = None,
    hash: Optional[str] = None
) -> str:
    """Get the remote path for an I4H asset.
    
    Args:
        version: Asset catalog version
        sub_path: Path within the asset catalog
        hash: Expected SHA256 hash
        
    Returns:
        Full URL to the asset
    """
```

#### get_i4h_local_asset_path

Get the local cache path for an asset:

```python
def get_i4h_local_asset_path(
    version: str = "0.2.0",
    download_dir: Optional[str] = None,
    sub_path: Optional[str] = None,
    hash: Optional[str] = None
) -> str:
    """Get the local path where an asset would be cached.
    
    Args:
        version: Asset catalog version
        download_dir: Directory for downloads
        sub_path: Path within the asset catalog
        hash: Expected SHA256 hash
        
    Returns:
        Local filesystem path
    """
```

## Usage Examples

For comprehensive examples, see [Asset Catalog API - Real Usage Examples](./api-examples.md).

### Basic Usage

```python
from i4h_asset_helper import BaseI4HAssets

class MyAssets(BaseI4HAssets):
    # Define your assets
    phantom = "Props/ABDPhantom/phantom.usda"
    robot = "Robots/dVRK/PSM/psm.usd"
    probe = "Props/ClariusUltrasoundProbe/fixture.usda"

# Create instance and access assets
assets = MyAssets()
phantom_path = assets.phantom  # Downloads automatically
robot_path = assets.robot
```

### Direct Function Usage

```python
from i4h_asset_helper import retrieve_asset

# Download a specific asset
path = retrieve_asset(
    version="0.2.0",
    sub_path="Props/ABDPhantom/phantom.usda",
    verbose=True
)
```

## Command Line Interface

### i4h-asset-retrieve

Command-line tool for downloading assets:

```bash
# Basic usage
i4h-asset-retrieve --version 0.2.0 --sub-path Props/ABDPhantom/phantom.usda

# With custom download directory
i4h-asset-retrieve --version 0.2.0 --sub-path Robots/dVRK/PSM/psm.usd \
    --download-dir /path/to/assets

# Force re-download
i4h-asset-retrieve --version 0.2.0 --sub-path Props/Board/board.usd \
    --force-download

# Verbose output
i4h-asset-retrieve --version 0.2.0 --sub-path Props/Organs/organs.usd \
    --verbose
```

## Environment Variables

The asset catalog respects these environment variables:


- `I4H_ASSET_DIR`: Base directory for asset downloads (default: `~/.cache/i4h/assets`)
- `I4H_ASSET_ENV`: Asset environment (dev/staging/production, default: production)

## Available Versions

Current versions supported:

- `0.2.0` - Latest version (default)
- `0.1.0` - Previous stable release
- `0.1.0ea` - Early access version

## Asset Organization

Assets are organized in four main categories:

- `Policies/` - Pre-trained AI models
- `Props/` - Medical equipment and anatomical models
- `Robots/` - Surgical and medical robots
- `Test/` - Test assets for development

See [Available Assets](../../getting-started/asset-catalog/available-assets.md) for the full list.

## Error Handling

The API will raise exceptions for:

- Network errors during download
- Invalid asset paths
- Checksum mismatches
- Missing dependencies

Example:
```python
try:
    assets = MyAssets()
    path = assets.nonexistent_asset
except AttributeError:
    print("Asset not defined")
except Exception as e:
    print(f"Download failed: {e}")
```

## Integration with Isaac Sim

```python
from i4h_asset_helper import BaseI4HAssets
from omni.isaac.core.utils.stage import add_reference_to_stage

class SimAssets(BaseI4HAssets):
    robot = "Robots/Franka/Collected_panda_assembly/panda_assembly.usda"

assets = SimAssets()
add_reference_to_stage(assets.robot, "/World/Robot")
```

## Best Practices

1. Define all project assets in a single class
2. Use descriptive attribute names
3. Set `I4H_ASSET_DIR` for custom storage locations
4. Handle download errors gracefully
5. Cache asset paths after first access

## Related Documentation

- [Asset Catalog Overview](./overview.md)
- [Complete Asset List](../../getting-started/asset-catalog/available-assets.md)
- [API Examples](./api-examples.md)
- [Helper API Reference](./helper-api.md)