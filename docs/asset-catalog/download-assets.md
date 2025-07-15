# Downloading Assets

This guide explains how to download and use assets from the Isaac for Healthcare Asset Catalog.

## Quick Start

Install and download assets:

```bash
# Install the asset catalog package
pip install git+https://github.com/isaac-for-healthcare/i4h-asset-catalog.git

# Download assets (requires Isaac Sim)
i4h-asset-retrieve
```

## Using Assets in Code

### Basic Usage

```python
from i4h_asset_helper import BaseI4HAssets

class MyAssets(BaseI4HAssets):
    phantom = "Props/ABDPhantom/phantom.usda"
    liver = "Props/Organs/organs.usd"
    
# Assets download automatically when accessed
assets = MyAssets()
phantom_path = assets.phantom  # Downloads if needed
```

### Direct Asset Retrieval

```python
from i4h_asset_helper import retrieve_asset

# Download specific asset
asset_path = retrieve_asset(
    sub_path="Props/ABDPhantom/phantom.usda"
)
```

## Environment Variables

Control asset behavior with environment variables:

```bash
# Set asset environment (dev/staging/production)
export I4H_ASSET_ENV=production

# Use specific asset version
export ISAAC_ASSET_SHA256_HASH=<hash_value>

# Custom download directory
export I4H_ASSET_DOWNLOAD_DIR=/path/to/assets
```

## Asset Paths

Assets are downloaded to: `~/.cache/i4h-assets/<SHA256_HASH>/`

Find your asset path:

```python
from i4h_asset_helper import get_asset_local_path
print(get_asset_local_path())
```

