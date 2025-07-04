#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
README.md Synchronization Script for i4h Documentation

This script synchronizes README.md files from the i4h-* repositories into the main
documentation system with proper attribution and image handling.
"""

import argparse
import logging
import os
import re
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Tuple

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ReadmeSynchronizer:
    """Synchronizer that copies README files with proper attribution and image handling"""
    
    def __init__(self, config_path: Path):
        self.config_path: Path = config_path
        self.config: Dict = self._load_config()
        self.base_path: Path = Path(os.getcwd())
        
        # Configuration-driven thresholds
        thresholds = self.config.get('content_thresholds', {})
        self.min_content_length: int = thresholds.get('minimum_length', 500)
        self.critical_threshold: int = thresholds.get('critical_threshold', 100)
        
        # Repository URLs from configuration
        self.repo_urls: Dict[str, str] = self.config.get('repository_urls', {})
        
        # Pre-compiled regex patterns for image path fixing
        self.image_patterns: List[Pattern[str]] = [
            re.compile(r'!\[([^\]]*)\]\(([^)]+)\)'),  # Markdown image syntax: ![alt](path)
            re.compile(r'<img\s+([^>]*\s)?src="([^"]+)"'),  # HTML img tags: <img src="path" ...>
            re.compile(r"<img\s+([^>]*\s)?src='([^']+)'"),  # HTML img tags with single quotes
        ]
        
        # Image file extensions
        self.image_extensions: Tuple[str, ...] = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')
        
        # Statistics tracking
        self.stats: Dict = {
            'processed': 0,
            'warnings': 0,
            'errors': 0,
            'needs_content': []
        }
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _validate_source_repositories(self) -> None:
        """Validate that all configured source repositories exist"""
        missing_repos = []
        
        for repo_name in self.repo_urls.keys():
            repo_path = self.base_path / repo_name
            if not repo_path.exists():
                missing_repos.append(repo_name)
            elif not repo_path.is_dir():
                missing_repos.append(f"{repo_name} (not a directory)")
        
        if missing_repos:
            logger.error("Missing source repositories:")
            for repo in missing_repos:
                logger.error(f"  - {repo}")
            logger.error("Please clone the required repositories before running sync.")
            raise FileNotFoundError(f"Missing repositories: {', '.join(missing_repos)}")
        
        logger.info(f"✓ All {len(self.repo_urls)} source repositories found")
    
    def sync_all(self, dry_run: bool = False, fix_all_images: bool = False) -> None:
        """Synchronize all README files according to configuration"""
        logger.info("Starting README synchronization...")
        
        # Validate source repositories exist
        self._validate_source_repositories()
        
        for repo_config in self.config['repositories']:
            self._sync_repository(repo_config, dry_run)
        
        # Fix all images if requested
        if fix_all_images:
            logger.info("\nFixing images in all markdown files...")
            self._fix_all_images_in_docs(dry_run)
        
        # Generate documentation needs report
        if self.stats['needs_content']:
            self._generate_documentation_needs_report(dry_run)
        elif dry_run:
            logger.info(f"\n[DRY RUN] No documentation needs report needed - all files have sufficient content")
        
        # Print summary
        logger.info(f"\nSynchronization complete!")
        logger.info(f"Files processed: {self.stats['processed']}")
        logger.info(f"Warnings: {self.stats['warnings']}")
        logger.info(f"Errors: {self.stats['errors']}")
        logger.info(f"Files needing content: {len(self.stats['needs_content'])}")
    
    def _sync_repository(self, repo_config: Dict, dry_run: bool) -> None:
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
    
    def _process_readme(self, source: str, target: str, dry_run: bool) -> None:
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
            content = self._fix_image_paths(content, source_path, target_path, dry_run)
            
            # Check if content is minimal
            content_length = len(content.strip())
            needs_documentation = content_length < self.min_content_length
            
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
                logger.info(f"  [DRY RUN] Would write to {target_path}")
            
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
    
    def _fix_image_paths(self, content: str, source_path: Path, target_path: Path, dry_run: bool = False) -> str:
        """Fix relative image paths to work from the target location"""
        
        for i, pattern in enumerate(self.image_patterns):
            for match in pattern.finditer(content):
                if i == 0:  # Markdown syntax: ![alt](path)
                    original_path = match.group(2)
                    full_match = match.group(0)
                else:  # HTML syntax: <img src="path" ...>
                    original_path = match.group(2)
                    full_match = match.group(0)
                
                # Skip URLs and absolute paths
                if original_path.startswith(('http://', 'https://', '/', '#')):
                    continue
                
                # Convert the relative path
                fixed_path = self._convert_relative_path(original_path, source_path, target_path, dry_run)
                
                # Replace in content
                if i == 0:  # Markdown syntax
                    new_match = f'![{match.group(1)}]({fixed_path})'
                else:  # HTML syntax - preserve other attributes
                    new_match = full_match.replace(original_path, fixed_path)
                
                content = content.replace(full_match, new_match)
        
        return content
    
    def _convert_relative_path(self, rel_path: str, source_path: Path, target_path: Path, dry_run: bool = False) -> str:
        """Convert a relative path from source to target location"""
        # Resolve the absolute path from the source file's perspective
        source_dir = source_path.parent
        abs_path = (source_dir / rel_path).resolve()
        
        # Check if it's within the repo
        try:
            rel_to_repo = abs_path.relative_to(self.base_path)
            
            # For any image file, copy it to docs/assets/images
            if abs_path.suffix.lower() in self.image_extensions:
                # Ensure the assets directory exists
                assets_dir = self.base_path / 'docs' / 'assets' / 'images'
                
                if not dry_run:
                    assets_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Copy the image if it exists
                    if abs_path.exists():
                        dest_path = assets_dir / abs_path.name
                        
                        # Only copy if source is newer or dest doesn't exist
                        if not dest_path.exists() or abs_path.stat().st_mtime > dest_path.stat().st_mtime:
                            shutil.copy2(abs_path, dest_path)
                            logger.info(f"Copied image: {abs_path} -> {dest_path}")
                else:
                    if abs_path.exists():
                        dest_path = assets_dir / abs_path.name
                        logger.info(f"  [DRY RUN] Would copy image: {abs_path} -> {dest_path}")
                
                # Calculate relative path from target document to assets
                # Account for MkDocs pretty URLs - the actual HTML will be one level deeper
                # e.g., /how-to/robots/mira-teleoperation.md becomes /how-to/robots/mira-teleoperation/index.html
                
                # For MkDocs, we need to go up one more level
                # Count the depth from docs/ to determine how many levels to go up
                docs_dir = self.base_path / 'docs'
                depth_from_docs = len(target_path.relative_to(docs_dir).parts)
                
                # The actual served page will be one level deeper due to pretty URLs
                # So we need one more '../' than the file structure suggests
                ups = '../' * depth_from_docs
                
                # The path to assets from docs root
                assets_from_docs = f'assets/images/{abs_path.name}'
                
                return ups + assets_from_docs
            
            # For non-image files, calculate relative from target
            target_dir = target_path.parent
            try:
                return str(abs_path.relative_to(target_dir))
            except ValueError:
                # If relative_to fails, fall back to os.path.relpath
                return os.path.relpath(abs_path, target_dir)
            
        except ValueError:
            # Path is outside the repo, return as-is
            return rel_path
    
    def _get_repo_url(self, source_path: Path) -> str:
        """Get the GitHub URL for a source file"""
        relative_path = source_path.relative_to(self.base_path)
        parts = relative_path.parts
        
        if not parts:
            return '#'
        
        repo_name = parts[0]
        base_url = self.repo_urls.get(repo_name)
        
        if not base_url:
            return '#'
        
        if len(parts) > 1:
            file_path = '/'.join(parts[1:])
            return f"{base_url}/blob/main/{file_path}"
        else:
            return base_url
    
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
        except Exception:
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
    
    def _generate_documentation_needs_report(self, dry_run: bool = False) -> None:
        """Generate a report of documentation that needs to be written"""
        report_path = self.base_path / 'docs' / 'documentation-needs-report.md'
        
        content = f"""# Documentation Needs Report

This report lists all README files that need additional content from the engineering team.

Generated: {datetime.now().isoformat()}

## Files Needing Documentation

Total files with minimal content: {len(self.stats['needs_content'])}

| Source File | Target Documentation | Current Length | Status |
|------------|---------------------|----------------|---------|
"""
        
        for item in sorted(self.stats['needs_content'], key=lambda x: x['length']):
            status = "❌ Critical" if item['length'] < self.critical_threshold else "⚠️ Needs Expansion"
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

- **❌ Critical** (< {self.critical_threshold} chars): These files are essentially empty and need immediate attention
- **⚠️ Needs Expansion** (< {self.min_content_length} chars): These files have some content but need significant expansion
"""
        
        # Write report
        if not dry_run:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"\nDocumentation needs report generated: {report_path}")
        else:
            logger.info(f"\n[DRY RUN] Would generate documentation needs report: {report_path}")
            logger.info(f"\n--- Documentation Needs Report (DRY RUN) ---")
            print(content)
            logger.info(f"--- End of Report ---")
    
    def _fix_all_images_in_docs(self, dry_run: bool = False) -> None:
        """Fix broken image references in all markdown files"""
        docs_dir = self.base_path / 'docs'
        
        # Find all markdown files
        markdown_files = list(docs_dir.rglob("*.md"))
        
        # Get source repositories
        source_repos = []
        for repo_name in self.repo_urls.keys():
            repo_path = self.base_path / repo_name
            if repo_path.exists():
                source_repos.append(repo_path)
        
        if not source_repos:
            logger.warning("No source repositories found for image fixing")
            return
        
        logger.info(f"Found {len(markdown_files)} markdown files to check")
        logger.info(f"Source repositories: {', '.join(repo.name for repo in source_repos)}")
        
        total_fixed = 0
        total_changes = 0
        files_processed = 0
        
        for file_path in markdown_files:
            # Skip README files in the docs directory itself
            if file_path.name == "README.md":
                continue
            
            fixed, changes = self._fix_images_in_file(file_path, source_repos, dry_run)
            if fixed > 0:
                total_fixed += fixed
                total_changes += changes
                files_processed += 1
        
        # Summary
        logger.info(f"\nImage fixing summary:")
        logger.info(f"Files checked: {len(markdown_files)}")
        logger.info(f"Files with fixes: {files_processed}")
        logger.info(f"Images fixed: {total_fixed}")
        logger.info(f"References updated: {total_changes}")
    
    def _fix_images_in_file(self, file_path: Path, source_repos: List[Path], dry_run: bool = False) -> Tuple[int, int]:
        """Fix broken image references in a single file"""
        logger.info(f"Checking: {file_path.relative_to(self.base_path / 'docs')}")
        
        # Find image references
        image_refs = self._find_image_references(file_path)
        
        if not image_refs:
            return 0, 0
        
        logger.info(f"  Found {len(image_refs)} image reference(s)")
        
        updates = {}
        fixed = 0
        
        for image_path, line_num in image_refs:
            logger.info(f"  Line {line_num}: {image_path}")
            
            # Find source image
            source_image = self._find_source_image(image_path, source_repos)
            
            if not source_image:
                logger.warning(f"    Source image not found: {os.path.basename(image_path)}")
                continue
            
            logger.info(f"    Found source: {source_image}")
            
            # Determine target path and copy image
            target_path = self.base_path / 'docs' / 'assets' / 'images' / source_image.name
            
            if self._copy_image_to_docs(source_image, target_path, dry_run):
                # Get relative path from file to target
                new_path = self._get_relative_path_for_docs(target_path, file_path)
                updates[image_path] = new_path
                fixed += 1
        
        # Update file with new paths
        changes = self._update_file_image_references(file_path, updates, dry_run)
        
        return fixed, changes
    
    def _find_image_references(self, file_path: Path) -> List[Tuple[str, int]]:
        """Find all image references in a markdown file"""
        image_refs = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for i, pattern in enumerate(self.image_patterns):
                    for match in pattern.finditer(line):
                        if i == 0:  # Markdown syntax: ![alt](path)
                            image_path = match.group(2)
                        else:  # HTML syntax: src="path"
                            image_path = match.group(2)
                        
                        # Skip URLs
                        if image_path.startswith(('http://', 'https://')):
                            continue
                        
                        # Check if it's a broken /assets/ path or relative path that needs fixing
                        if image_path.startswith('/assets/'):
                            # Check if this image actually exists in docs
                            full_path = self.base_path / 'docs' / image_path.lstrip('/')
                            if not full_path.exists():
                                # This is a broken reference - needs fixing
                                image_refs.append((image_path, line_num))
                        else:
                            # This is a relative path that might need fixing
                            image_refs.append((image_path, line_num))
        
        return image_refs
    
    def _find_source_image(self, image_path: str, source_repos: List[Path]) -> Optional[Path]:
        """Find the actual image file in source repositories"""
        # Extract just the filename from the path
        image_filename = os.path.basename(image_path)
        
        # Search in all source repositories
        for repo in source_repos:
            for root, dirs, files in os.walk(repo):
                # Skip hidden directories and common non-image directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
                
                if image_filename in files:
                    return Path(root) / image_filename
        
        return None
    
    def _copy_image_to_docs(self, source: Path, target: Path, dry_run: bool = False) -> bool:
        """Copy image file to docs assets directory"""
        try:
            # Ensure target directory exists
            target.parent.mkdir(parents=True, exist_ok=True)
            
            if not dry_run:
                # Only copy if source is newer or dest doesn't exist
                if not target.exists() or source.stat().st_mtime > target.stat().st_mtime:
                    shutil.copy2(source, target)
                    logger.info(f"    Copied {source.name} to {target}")
            else:
                logger.info(f"    [DRY RUN] Would copy {source.name} to {target}")
            
            return True
        except Exception as e:
            logger.error(f"    Failed to copy {source}: {e}")
            return False
    
    def _get_relative_path_for_docs(self, target_path: Path, doc_file: Path) -> str:
        """Get the correct relative path for the image in documentation"""
        # For MkDocs, we need to go up one more level due to pretty URLs
        # Count the depth from docs/ to determine how many levels to go up
        docs_dir = self.base_path / 'docs'
        depth_from_docs = len(doc_file.relative_to(docs_dir).parts)
        
        # The actual served page will be one level deeper due to pretty URLs
        ups = '../' * depth_from_docs
        
        # The path to assets from docs root
        assets_from_docs = f'assets/images/{target_path.name}'
        
        return ups + assets_from_docs
    
    def _update_file_image_references(self, file_path: Path, updates: Dict[str, str], dry_run: bool = False) -> int:
        """Update image references in a file"""
        if not updates:
            return 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes = 0
        
        # Sort updates by length (longest first) to avoid partial replacements
        sorted_updates = sorted(updates.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_path, new_path in sorted_updates:
            # Count occurrences
            occurrences = content.count(old_path)
            if occurrences > 0:
                content = content.replace(old_path, new_path)
                changes += occurrences
                logger.info(f"    Replaced {occurrences} occurrence(s) of '{old_path}' with '{new_path}'")
        
        if changes > 0 and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return changes


def main() -> int:
    """Main entry point"""
    parser = argparse.ArgumentParser(description='README synchronization to documentation')
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
        '--fix-all-images',
        action='store_true',
        help='Also scan and fix broken images in all markdown files'
    )

    
    args = parser.parse_args()
    
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        return 1
    
    try:
        synchronizer = ReadmeSynchronizer(config_path)
        synchronizer.sync_all(dry_run=args.dry_run, fix_all_images=args.fix_all_images)
        return 0
    except Exception as e:
        logger.error(f"Synchronization failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())