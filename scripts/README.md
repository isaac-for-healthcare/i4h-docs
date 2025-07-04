# Documentation Scripts

This directory contains scripts for maintaining the i4h documentation.

## Scripts

### sync_readmes.py
Main script for synchronizing README files from source repositories to documentation.
- **Usage**: 
  - `python scripts/sync_readmes.py` - Sync README files (recommended for CI/CD)
  - `python scripts/sync_readmes.py --dry-run` - Preview changes without modifying files
  - `python scripts/sync_readmes.py --fix-all-images` - Also fix broken images in ALL markdown files (manual repair)
  - `python scripts/sync_readmes.py --fix-all-images --dry-run` - Preview all changes including image fixes
- **Config**: Uses `readme-sync-config.yml`
- **Purpose**: 
  - Copies README content from i4h-* repositories to docs/ with proper attribution headers
  - Fixes image references in synced files automatically
  - Optionally scans and fixes broken image references in all markdown files
  - Locates source images in i4h-* repositories and copies them to docs/assets/images/
  - Updates image references to use correct relative paths
- **Note**: This script runs automatically in CI/CD builds (without --fix-all-images)

### readme-sync-config.yml
Configuration file that maps source README files to documentation pages.
- **Format**: YAML with source/target mappings
- **Used by**: sync_readmes.py
- **Structure**:
  - Maps README files from i4h-* repos to docs/ structure
  - Excludes test directories and placeholder files

## Workflow

1. **Regular Sync**: Run `sync_readmes.py` to pull latest README content and fix images in synced files
2. **Manual Image Repair**: Run `sync_readmes.py --fix-all-images` if you need to fix broken images in manually created documentation files

## Notes

- Always use relative paths for images in markdown files
- The sync process preserves original README content with attribution headers
- Image paths are automatically converted from absolute to relative paths