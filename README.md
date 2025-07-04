# Isaac for Healthcare (i4h) Documentation

This repository contains the comprehensive documentation for Isaac for Healthcare, a three-computer solution for healthcare robotics built with MkDocs and Material theme.

## Quick Start

### Prerequisites

- Python 3.10+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/isaac-for-healthcare/i4h-docs.git
cd i4h-docs
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# .venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

3. Serve the documentation locally:
```bash
./serve_docs.sh
# Or directly: mkdocs serve
```

The documentation will be available at http://localhost:8001

## Documentation Structure

The documentation follows the [Diátaxis framework](https://diataxis.fr/) principles:

- `docs/` - Source documentation files
  - `workflows/` - **Complete Solutions**: End-to-end healthcare robotics applications
    - Robotic Ultrasound - Autonomous diagnostic imaging
    - Robotic Surgery - Surgical automation workflows  
    - Telesurgery - Remote surgical operation
  - `asset-catalog/` - **Resources**: Pre-built simulation assets and AI models
  - `sensor-simulation/` - **Capabilities**: Physics-based medical sensor emulation
  - `how-to/` - **Task Guides**: Step-by-step instructions for specific tasks
  - `reference/` - **Technical Reference**: APIs, setup guides, and specifications
  - `assets/` - Images and static resources
- `scripts/` - Documentation maintenance tools
  - `sync_readmes.py` - Synchronizes README files from source repositories
  - `readme-sync-config.yml` - Configuration for README synchronization
  - `sync_readmes.py` - Synchronizes README files and optionally fixes image paths
- `mkdocs.yml` - MkDocs configuration
- `.github/workflows/` - GitHub Actions for automated deployment

## Automated Documentation Workflow

The documentation is automatically built and deployed through GitHub Actions:

1. **On every push to main**, the workflow:
   - Clones the three source repositories (i4h-asset-catalog, i4h-sensor-simulation, i4h-workflows)
   - Runs the sync script to pull README content into the docs structure
   - Builds the MkDocs site
   - Deploys to GitHub Pages at https://isaac-for-healthcare.github.io/i4h/

2. **Content synchronization** is configured in `scripts/readme-sync-config.yml`, which maps:
   - Source README files from the three repositories
   - Target locations in the documentation structure

3. **To update documentation**:
   - Direct edits: Modify files in `docs/` directory
   - Synced content: Update README files in the source repositories
   - Navigation: Edit the `nav` section in `mkdocs.yml`

## Local Development

### Content Synchronization

To sync README files from source repositories:

```bash
# Clone source repositories first (required)
git clone https://github.com/isaac-for-healthcare/i4h-asset-catalog.git
git clone https://github.com/isaac-for-healthcare/i4h-sensor-simulation.git
git clone https://github.com/isaac-for-healthcare/i4h-workflows.git

# Sync content from source repositories
python scripts/sync_readmes.py

# Preview changes without modifying files
python scripts/sync_readmes.py --dry-run

# Fix broken images in all markdown files (manual repair tool)
python scripts/sync_readmes.py --fix-all-images
```

### Advanced Options

```bash
# Build static site
mkdocs build

# Serve with live reload on specific host/port
mkdocs serve -a 0.0.0.0:8001

# Strict mode (fails on warnings)
mkdocs build --strict

# Verbose output
mkdocs serve --verbose
```

### Troubleshooting

- **Missing repositories**: Ensure source repositories are cloned before running sync
- **Image issues**: Use `python scripts/sync_readmes.py --fix-all-images` for manual image repair
- **Build errors**: Check for broken links or missing files with `mkdocs build --strict`

## Support

- Documentation site: https://isaac-for-healthcare.github.io/i4h/
- GitHub repository: https://github.com/isaac-for-healthcare/i4h-docs
- Issue tracker: https://github.com/isaac-for-healthcare/i4h-docs/issues
