# Documentation Deployment Setup

## Overview

The `deploy-docs.yml` workflow automatically syncs content from source repositories, builds MkDocs documentation, and deploys to GitHub Pages.

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to Pages
3. Under "Source", select "GitHub Actions"

### 2. Push to Main Branch

The workflow will automatically run when you push changes to the main branch. It will:
- Clone the source repositories
- Sync README content
- Build the documentation
- Deploy to GitHub Pages

## How It Works

1. **Trigger**: The workflow runs on:
   - Push to main branch (when docs, scripts, mkdocs.yml, requirements.txt, or README files change)
   - Pull requests (for validation only, no deployment)
   - Manual workflow dispatch

2. **Build Process**:
   - Clones your main repository
   - Clones the three source repositories from isaac-for-healthcare organization
   - Runs the sync script to pull README content
   - Builds the MkDocs site
   - Uploads the built site as an artifact

3. **Deployment**:
   - Only deploys from the main branch
   - Uses GitHub's official Pages deployment action
   - Site will be available at: https://isaac-for-healthcare.github.io/i4h/

## Source Repositories

The documentation pulls content from these repositories:
- `isaac-for-healthcare/i4h-asset-catalog`
- `isaac-for-healthcare/i4h-sensor-simulation`
- `isaac-for-healthcare/i4h-workflows`

## Testing Locally

Before pushing, test the build locally:

```bash
# Clone source repos
git clone https://github.com/isaac-for-healthcare/i4h-asset-catalog.git
git clone https://github.com/isaac-for-healthcare/i4h-sensor-simulation.git
git clone https://github.com/isaac-for-healthcare/i4h-workflows.git

# Install dependencies
pip install -r requirements.txt
pip install pyyaml

# Run sync
python scripts/sync_readmes.py --verbose

# Build and serve
mkdocs build
mkdocs serve
```