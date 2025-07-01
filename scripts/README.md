# Documentation Scripts

This directory contains scripts for maintaining the i4h documentation.

## Scripts

### sync_readmes_simple.py
Main script for synchronizing README files from source repositories to documentation.
- **Usage**: `python scripts/sync_readmes_simple.py`
- **Config**: Uses `readme-sync-config.yml`
- **Purpose**: Copies README content from i4h-* repositories to docs/ with proper attribution headers
- **Note**: This script is referenced in mkdocs.yml and runs automatically on builds

### fix_images.py
Script for fixing broken image references in documentation.
- **Usage**: 
  - `python scripts/fix_images.py` - Fix all broken images
  - `python scripts/fix_images.py --dry-run` - Preview changes without modifying files
  - `python scripts/fix_images.py --file /path/to/file.md` - Fix specific file
- **Purpose**: 
  - Finds broken image references in markdown files
  - Locates source images in i4h-* repositories
  - Copies images to appropriate docs/ locations
  - Updates references to use relative paths

### readme-sync-config.yml
Configuration file that maps source README files to documentation pages.
- **Format**: YAML with source/target mappings
- **Used by**: sync_readmes_simple.py
- **Structure**:
  - Maps README files from i4h-* repos to docs/ structure
  - Excludes test directories and placeholder files

## Workflow

1. **Sync READMEs**: Run `sync_readmes_simple.py` to pull latest README content
2. **Fix Images**: Run `fix_images.py` to ensure all images are properly copied and referenced

## Notes

- Always use relative paths for images in markdown files
- The sync process preserves original README content with attribution headers
- Image paths are automatically converted from absolute to relative paths