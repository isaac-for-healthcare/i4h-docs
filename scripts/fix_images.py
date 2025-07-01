#!/usr/bin/env python3
"""
Script to automatically fix broken image references in documentation files.

This script:
1. Searches for image references in markdown files
2. Finds the actual image files in source repositories
3. Copies images to the correct documentation directory
4. Updates image paths in the documentation files
"""

import os
import re
import shutil
from pathlib import Path
import argparse
import logging
from typing import List, Tuple, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class ImageFixer:
    """Fixes broken image references in documentation."""
    
    def __init__(self, docs_dir: Path, source_repos: List[Path], dry_run: bool = False):
        self.docs_dir = docs_dir
        self.source_repos = source_repos
        self.dry_run = dry_run
        self.assets_dir = docs_dir / "assets" / "images"
        
        # Ensure assets directory exists
        if not self.dry_run:
            self.assets_dir.mkdir(parents=True, exist_ok=True)
    
    def find_image_references(self, file_path: Path) -> List[Tuple[str, int]]:
        """Find all image references in a markdown file."""
        image_refs = []
        
        # Patterns to match different types of image references
        patterns = [
            r'!\[([^\]]*)\]\(([^)]+)\)',  # Markdown images: ![alt](path)
            r'<img[^>]+src=["\']([^"\']+)["\']',  # HTML img tags
        ]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    matches = re.findall(pattern, line)
                    for match in matches:
                        # Extract the image path
                        if pattern.startswith('!'):  # Markdown pattern
                            image_path = match[1]
                        else:  # HTML pattern
                            image_path = match
                        
                        # Skip URLs
                        if image_path.startswith('http'):
                            continue
                        
                        # Check if it's an /assets/ path and verify the file exists
                        if image_path.startswith('/assets/'):
                            # Check if this image actually exists in docs
                            full_path = self.docs_dir / image_path.lstrip('/')
                            if not full_path.exists():
                                # This is a broken reference - needs fixing
                                image_refs.append((image_path, line_num))
                        else:
                            # This is a relative path that needs to be fixed
                            image_refs.append((image_path, line_num))
        
        return image_refs
    
    def find_source_image(self, image_name: str) -> Optional[Path]:
        """Find the actual image file in source repositories."""
        # Extract just the filename from the path
        image_filename = os.path.basename(image_name)
        
        # Search in all source repositories
        for repo in self.source_repos:
            for root, dirs, files in os.walk(repo):
                # Skip hidden directories and common non-image directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
                
                if image_filename in files:
                    return Path(root) / image_filename
        
        return None
    
    def determine_target_path(self, source_image: Path, doc_file: Path) -> Path:
        """Determine the appropriate target path for an image."""
        # Special handling for tutorial resources
        if 'tutorials/assets' in str(source_image):
            if 'bring_your_own_xr' in str(source_image):
                # Check if this is referenced from a how-to guide
                if 'how-to' in str(doc_file):
                    return self.docs_dir / "how-to" / "assets" / "resources" / source_image.name
                else:
                    return self.docs_dir / "tutorials" / "resources" / source_image.name
        
        # Special handling for sensor simulation docs
        if 'sensor-simulation' in str(source_image) and source_image.parent.name == 'docs':
            return self.docs_dir / "reference" / "sensor-simulation" / "docs" / source_image.name
        
        # Default: main assets/images directory
        return self.assets_dir / source_image.name
    
    def copy_image(self, source: Path, target: Path) -> bool:
        """Copy image file to target location."""
        try:
            # Ensure target directory exists
            target.parent.mkdir(parents=True, exist_ok=True)
            
            if not self.dry_run:
                shutil.copy2(source, target)
                logger.info(f"Copied {source.name} to {target}")
            else:
                logger.info(f"[DRY RUN] Would copy {source.name} to {target}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to copy {source}: {e}")
            return False
    
    def get_relative_image_path(self, image_path: Path, doc_file: Path) -> str:
        """Get the correct relative path for the image in documentation."""
        # Get relative path from the doc file to the image
        try:
            # Calculate relative path from doc file's directory to image
            rel_path = os.path.relpath(image_path, doc_file.parent)
            # Always use forward slashes
            return str(rel_path).replace('\\', '/')
        except ValueError:
            # If can't calculate relative path, return as is
            return str(image_path)
    
    def update_image_references(self, file_path: Path, updates: Dict[str, str]) -> int:
        """Update image references in a file."""
        if not updates:
            return 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # Sort updates by length (longest first) to avoid partial replacements
        sorted_updates = sorted(updates.items(), key=lambda x: len(x[0]), reverse=True)
        
        for old_path, new_path in sorted_updates:
            # Count occurrences
            occurrences = content.count(old_path)
            if occurrences > 0:
                content = content.replace(old_path, new_path)
                changes += occurrences
                logger.info(f"  Replaced {occurrences} occurrence(s) of '{old_path}' with '{new_path}'")
        
        if changes > 0 and not self.dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return changes
    
    def process_file(self, file_path: Path) -> Tuple[int, int]:
        """Process a single markdown file."""
        logger.info(f"\nProcessing: {file_path.relative_to(self.docs_dir)}")
        
        # Find image references
        image_refs = self.find_image_references(file_path)
        
        if not image_refs:
            logger.info("  No broken image references found")
            return 0, 0
        
        logger.info(f"  Found {len(image_refs)} image reference(s)")
        
        updates = {}
        fixed = 0
        
        for image_path, line_num in image_refs:
            logger.info(f"  Line {line_num}: {image_path}")
            
            # Find source image
            source_image = self.find_source_image(image_path)
            
            if not source_image:
                logger.warning(f"    Source image not found: {os.path.basename(image_path)}")
                continue
            
            logger.info(f"    Found source: {source_image}")
            
            # Determine target path
            target_path = self.determine_target_path(source_image, file_path)
            
            # Copy image
            if self.copy_image(source_image, target_path):
                # Get the new path for the documentation
                new_path = self.get_relative_image_path(target_path, file_path)
                updates[image_path] = new_path
                fixed += 1
        
        # Update file with new paths
        changes = self.update_image_references(file_path, updates)
        
        return fixed, changes
    
    def fix_all_images(self, specific_file: Optional[Path] = None) -> None:
        """Fix all image references in documentation."""
        if specific_file:
            files = [specific_file]
        else:
            # Find all markdown files
            files = list(self.docs_dir.rglob("*.md"))
        
        total_fixed = 0
        total_changes = 0
        files_processed = 0
        
        for file_path in files:
            # Skip README files in the docs directory itself
            if file_path.name == "README.md":
                continue
            
            fixed, changes = self.process_file(file_path)
            if fixed > 0:
                total_fixed += fixed
                total_changes += changes
                files_processed += 1
        
        # Summary
        logger.info("\n" + "="*50)
        logger.info("SUMMARY:")
        logger.info(f"Files processed: {len(files)}")
        logger.info(f"Files with fixes: {files_processed}")
        logger.info(f"Images fixed: {total_fixed}")
        logger.info(f"References updated: {total_changes}")
        
        if self.dry_run:
            logger.info("\nThis was a DRY RUN. No files were actually modified.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fix broken image references in documentation files"
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path(__file__).parent.parent / "docs",
        help="Path to documentation directory (default: ../docs)"
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Process only a specific file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    # Define source repositories to search
    base_dir = args.docs_dir.parent
    source_repos = [
        base_dir / "i4h-workflows",
        base_dir / "i4h-sensor-simulation",
        base_dir / "i4h-asset-catalog",
    ]
    
    # Filter out non-existent repos
    source_repos = [repo for repo in source_repos if repo.exists()]
    
    if not source_repos:
        logger.error("No source repositories found!")
        return 1
    
    logger.info(f"Documentation directory: {args.docs_dir}")
    logger.info(f"Source repositories: {', '.join(repo.name for repo in source_repos)}")
    logger.info(f"Dry run: {args.dry_run}")
    
    # Create fixer instance
    fixer = ImageFixer(args.docs_dir, source_repos, args.dry_run)
    
    # Fix images
    fixer.fix_all_images(args.file)
    
    return 0


if __name__ == "__main__":
    exit(main())