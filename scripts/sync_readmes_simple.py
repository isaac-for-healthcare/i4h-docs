#!/usr/bin/env python3
"""
Simple README.md Synchronization Script for i4h Documentation

This script synchronizes README.md files from the i4h-* repositories into the main
documentation system without trying to be smart about content extraction.
"""

import os
import yaml
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Minimum content threshold (characters) to determine if documentation is needed
MIN_CONTENT_LENGTH = 500


class SimpleReadmeSynchronizer:
    """Simple synchronizer that copies README files with proper attribution"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()
        self.base_path = Path(os.getcwd())
        self.stats = {
            'processed': 0,
            'warnings': 0,
            'errors': 0,
            'needs_content': []
        }
    
    def _load_config(self) -> dict:
        """Load configuration from YAML file"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def sync_all(self, dry_run: bool = False):
        """Synchronize all README files according to configuration"""
        logger.info("Starting README synchronization...")
        
        for repo_config in self.config['repositories']:
            self._sync_repository(repo_config, dry_run)
        
        # Generate documentation needs report
        if self.stats['needs_content']:
            self._generate_documentation_needs_report()
        
        # Print summary
        logger.info(f"\nSynchronization complete!")
        logger.info(f"Files processed: {self.stats['processed']}")
        logger.info(f"Warnings: {self.stats['warnings']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info(f"Files needing content: {len(self.stats['needs_content'])}")
    
    def _sync_repository(self, repo_config: dict, dry_run: bool):
        """Synchronize README files from a single repository"""
        repo_name = repo_config['name']
        logger.info(f"\nProcessing repository: {repo_name}")
        
        # Process main README
        if 'main_readme' in repo_config:
            self._process_readme(
                repo_config['main_readme']['source'],
                repo_config['main_readme']['target'],
                dry_run
            )
        
        # Process sub-READMEs
        for sub_readme in repo_config.get('sub_readmes', []):
            self._process_readme(
                sub_readme['source'],
                sub_readme['target'],
                dry_run
            )
    
    def _process_readme(self, source: str, target: str, dry_run: bool):
        """Process a single README file"""
        source_path = self.base_path / source
        target_path = self.base_path / target
        
        if not source_path.exists():
            logger.error(f"Source file not found: {source_path}")
            self.stats['errors'] += 1
            return
        
        logger.info(f"Processing: {source} -> {target}")
        
        try:
            # Read source content
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix image paths
            content = self._fix_image_paths(content, source_path, target_path)
            
            # Check if content is minimal
            content_length = len(content.strip())
            needs_documentation = content_length < MIN_CONTENT_LENGTH
            
            # Generate frontmatter
            frontmatter = self._generate_frontmatter(source_path, target_path)
            
            # Generate attribution
            attribution = self._generate_attribution(source_path)
            
            # Add TODO warning if content is minimal
            todo_warning = ""
            if needs_documentation:
                todo_warning = self._generate_todo_warning(source_path, content_length)
                self.stats['needs_content'].append({
                    'source': source,
                    'target': target,
                    'length': content_length
                })
                self.stats['warnings'] += 1
            
            # Combine content
            final_content = f"{frontmatter}\n\n{attribution}\n"
            if todo_warning:
                final_content += f"\n{todo_warning}\n"
            final_content += f"\n{content}"
            
            # Add note at end if content is minimal
            if needs_documentation:
                final_content += f"\n\n---\n\n*Note: This documentation page requires additional content from the engineering team. The current source README file contains only {content_length} characters.*"
            
            if not dry_run:
                # Ensure target directory exists
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write to target
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
            else:
                logger.info(f"  [DRY RUN] Would write {len(final_content)} characters")
            
            self.stats['processed'] += 1
            
        except Exception as e:
            logger.error(f"Failed to process {source_path}: {e}")
            self.stats['errors'] += 1
    
    def _generate_frontmatter(self, source_path: Path, target_path: Path) -> str:
        """Generate YAML frontmatter for the documentation file"""
        relative_source = source_path.relative_to(self.base_path)
        title = self._extract_title_from_path(source_path)
        
        frontmatter = f"""---
title: {title}
source: {relative_source}
---"""
        return frontmatter
    
    def _generate_attribution(self, source_path: Path) -> str:
        """Generate attribution notice for synchronized content"""
        relative_source = source_path.relative_to(self.base_path)
        repo_url = self._get_repo_url(source_path)
        
        return f"""!!! info "Source"
    This content is synchronized from [`{relative_source}`]({repo_url})
    
    To make changes, please edit the source file and run the synchronization script."""
    
    def _generate_todo_warning(self, source_path: Path, content_length: int) -> str:
        """Generate TODO warning for minimal content"""
        relative_source = source_path.relative_to(self.base_path)
        
        return f"""!!! warning "TODO: Documentation Needed"
    This page needs significant content. The source README currently contains only {content_length} characters.
    See the documentation needs report for details on what content is required."""
    
    def _fix_image_paths(self, content: str, source_path: Path, target_path: Path) -> str:
        """Fix relative image paths to work from the target location"""
        import re
        
        # Pattern to match image references in markdown and HTML
        patterns = [
            r'!\[([^\]]*)\]\(([^)]+)\)',  # Markdown image syntax: ![alt](path)
            r'<img\s+([^>]*\s)?src="([^"]+)"',  # HTML img tags: <img src="path" ...>
            r"<img\s+([^>]*\s)?src='([^']+)'",  # HTML img tags with single quotes
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                if pattern.startswith(r'!\['):
                    # Markdown syntax
                    original_path = match.group(2)
                    full_match = match.group(0)
                else:
                    # HTML syntax
                    original_path = match.group(2)
                    full_match = match.group(0)
                
                # Skip URLs and absolute paths
                if original_path.startswith(('http://', 'https://', '/', '#')):
                    continue
                
                # Convert the relative path
                fixed_path = self._convert_relative_path(original_path, source_path, target_path)
                
                # Replace in content
                if pattern.startswith(r'!\['):
                    # Markdown syntax
                    new_match = f'![{match.group(1)}]({fixed_path})'
                else:
                    # HTML syntax - preserve other attributes
                    new_match = full_match.replace(original_path, fixed_path)
                
                content = content.replace(full_match, new_match)
        
        return content
    
    def _convert_relative_path(self, rel_path: str, source_path: Path, target_path: Path) -> str:
        """Convert a relative path from source to target location"""
        # Resolve the absolute path from the source file's perspective
        source_dir = source_path.parent
        abs_path = (source_dir / rel_path).resolve()
        
        # Check if it's within the repo
        try:
            rel_to_repo = abs_path.relative_to(self.base_path)
            
            # For any image file, copy it to docs/assets/images
            if abs_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']:
                # Ensure the assets directory exists
                assets_dir = self.base_path / 'docs' / 'assets' / 'images'
                assets_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy the image if it exists
                if abs_path.exists():
                    import shutil
                    dest_path = assets_dir / abs_path.name
                    
                    # Only copy if source is newer or dest doesn't exist
                    if not dest_path.exists() or abs_path.stat().st_mtime > dest_path.stat().st_mtime:
                        shutil.copy2(abs_path, dest_path)
                        logger.debug(f"Copied image: {abs_path} -> {dest_path}")
                
                # Calculate relative path from target document to assets
                # Account for MkDocs pretty URLs - the actual HTML will be one level deeper
                # e.g., /how-to/robots/mira-teleoperation.md becomes /how-to/robots/mira-teleoperation/index.html
                target_dir = target_path.parent
                
                # For MkDocs, we need to go up one more level
                # Count the depth from docs/ to determine how many levels to go up
                docs_dir = self.base_path / 'docs'
                depth_from_docs = len(target_path.relative_to(docs_dir).parts)
                
                # The actual served page will be one level deeper due to pretty URLs
                # So we need one more '../' than the file structure suggests
                ups = '../' * depth_from_docs
                
                # The path to assets from docs root
                assets_from_docs = 'assets/images/' + abs_path.name
                
                return ups + assets_from_docs
            
            # For non-image files, calculate relative from target
            target_dir = target_path.parent
            return os.path.relpath(abs_path, target_dir)
            
        except ValueError:
            # Path is outside the repo, return as-is
            return rel_path
    
    def _get_repo_url(self, source_path: Path) -> str:
        """Get the GitHub URL for a source file"""
        relative_path = source_path.relative_to(self.base_path)
        parts = relative_path.parts
        
        if parts[0] == 'i4h-asset-catalog':
            base_url = 'https://github.com/isaac-for-healthcare/i4h-asset-catalog'
        elif parts[0] == 'i4h-sensor-simulation':
            base_url = 'https://github.com/isaac-for-healthcare/i4h-sensor-simulation'
        elif parts[0] == 'i4h-workflows':
            base_url = 'https://github.com/isaac-for-healthcare/i4h-workflows'
        else:
            return '#'
        
        file_path = '/'.join(parts[1:])
        return f"{base_url}/blob/main/{file_path}"
    
    def _extract_title_from_path(self, path: Path) -> str:
        """Extract a readable title from file path"""
        # Try to get title from first H1 header
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('# '):
                        # Remove markdown formatting from title
                        title = line[2:].strip()
                        # Remove markdown links - extract just the text
                        title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
                        return title
        except:
            pass
        
        # Fallback to path-based title
        parts = path.relative_to(self.base_path).parts
        
        # Special handling for specific paths
        if len(parts) > 2:
            # Get the parent directory name
            parent = parts[-2]
            if parent == 'scripts':
                # Go one level higher
                if len(parts) > 3:
                    parent = parts[-3]
            
            # Clean up the name
            title = parent.replace('_', ' ').replace('-', ' ').title()
            
            # Add context if it's a README
            if parts[-1] == 'README.md':
                # Don't add redundant "Readme"
                return title
        
        # Default fallback
        return path.parent.name.replace('_', ' ').replace('-', ' ').title()
    
    def _generate_documentation_needs_report(self):
        """Generate a report of documentation that needs to be written"""
        report_path = self.base_path / 'docs' / 'documentation-needs-report.md'
        
        content = """# Documentation Needs Report

This report lists all README files that need additional content from the engineering team.

Generated: {timestamp}

## Files Needing Documentation

Total files with minimal content: {total}

| Source File | Target Documentation | Current Length | Status |
|------------|---------------------|----------------|---------|
""".format(
            timestamp=datetime.now().isoformat(),
            total=len(self.stats['needs_content'])
        )
        
        for item in sorted(self.stats['needs_content'], key=lambda x: x['length']):
            status = "❌ Critical" if item['length'] < 100 else "⚠️ Needs Expansion"
            content += f"| `{item['source']}` | `{item['target']}` | {item['length']} chars | {status} |\n"
        
        content += """

## Action Items

1. Review each file listed above
2. Add comprehensive documentation including:
   - Overview/Introduction
   - Prerequisites/Requirements
   - Installation/Setup instructions
   - Usage examples
   - API reference (if applicable)
   - Troubleshooting guide
   - Links to related documentation

## Priority Guidelines

- **❌ Critical** (< 100 chars): These files are essentially empty and need immediate attention
- **⚠️ Needs Expansion** (< 500 chars): These files have some content but need significant expansion
"""
        
        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"\nDocumentation needs report generated: {report_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Simple README synchronization to documentation')
    parser.add_argument(
        '--config',
        default='scripts/readme-sync-config.yml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        return 1
    
    try:
        synchronizer = SimpleReadmeSynchronizer(config_path)
        synchronizer.sync_all(dry_run=args.dry_run)
        return 0
    except Exception as e:
        logger.error(f"Synchronization failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())