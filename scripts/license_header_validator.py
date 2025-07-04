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
License Header Validation Script

This script validates and adds license headers to Python and shell files in the repository.
It automatically excludes directories defined in the readme-sync-config.yml file.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Optional
import re
import yaml

# License header text
LICENSE_HEADER = """SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

# File type configurations
FILE_TYPE_CONFIGS = {
    'python': {
        'extensions': ['.py'],
        'comment_prefix': '# ',
        'shebang_patterns': [r'^#!.*python.*$'],
    },
    'shell': {
        'extensions': ['.sh', '.bash', '.zsh'],
        'comment_prefix': '# ',
        'shebang_patterns': [r'^#!.*sh.*$', r'^#!.*bash.*$', r'^#!.*zsh.*$'],
    },
}

# Static directories to ignore
STATIC_IGNORE_DIRS = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', 'env', 'site', 'build', 'dist', 'third_party', '.devcontainer', '.vscode'}

# Files to ignore
IGNORE_FILES = {'.gitignore', '.pre-commit-config.yaml', '.coveragerc', '.python-version', 'uv.lock'}


def load_config_excludes() -> Set[str]:
    """Load directory exclusions from readme-sync-config.yml."""
    config_path = Path('scripts/readme-sync-config.yml')
    excludes = set()
    
    if not config_path.exists():
        return excludes
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Extract repository names from the config
        if 'repositories' in config:
            for repo in config['repositories']:
                if 'name' in repo:
                    excludes.add(repo['name'])
        
        # Also check repository_urls section
        if 'repository_urls' in config:
            for repo_name in config['repository_urls'].keys():
                excludes.add(repo_name)
                
    except Exception as e:
        print(f"Warning: Could not load config file {config_path}: {e}")
    
    return excludes


def get_file_type(file_path: Path) -> Optional[str]:
    """Determine the file type based on extension."""
    file_suffix = file_path.suffix.lower()
    
    # Check by extension
    for file_type, config in FILE_TYPE_CONFIGS.items():
        if file_suffix in config['extensions']:
            return file_type
    
    return None


def has_shebang(content: str, file_type: str) -> bool:
    """Check if file has a shebang line."""
    if not content:
        return False
    
    first_line = content.split('\n')[0]
    config = FILE_TYPE_CONFIGS.get(file_type, {})
    shebang_patterns = config.get('shebang_patterns', [])
    
    return any(re.match(pattern, first_line) for pattern in shebang_patterns)


def format_license_header(file_type: str) -> str:
    """Format the license header with appropriate comment prefix."""
    config = FILE_TYPE_CONFIGS.get(file_type, {})
    comment_prefix = config.get('comment_prefix', '# ')
    
    lines = LICENSE_HEADER.split('\n')
    formatted_lines = [comment_prefix + line if line.strip() else comment_prefix.rstrip() 
                      for line in lines]
    
    return '\n'.join(formatted_lines)


def has_license_header(content: str, file_type: str) -> bool:
    """Check if file already has a license header."""
    if not content:
        return False
    
    # Get the comment prefix for this file type
    config = FILE_TYPE_CONFIGS.get(file_type, {})
    comment_prefix = config.get('comment_prefix', '# ')
    
    # Look for commented SPDX license identifier in the first 20 lines
    lines = content.split('\n')[:20]
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(comment_prefix.strip()) and 'SPDX-License-Identifier' in stripped_line:
            return True
    return False


def add_license_header(content: str, file_type: str) -> str:
    """Add license header to file content."""
    if not content:
        return format_license_header(file_type) + '\n'
    
    lines = content.split('\n')
    header_lines = format_license_header(file_type).split('\n')
    
    # Handle shebang lines
    if has_shebang(content, file_type):
        shebang_line = lines[0]
        remaining_lines = lines[1:]
        
        # Add empty line after shebang, then header, then another empty line
        result_lines = [shebang_line, ''] + header_lines + [''] + remaining_lines
    else:
        # Add header at the beginning, then empty line
        result_lines = header_lines + [''] + lines
    
    return '\n'.join(result_lines)


def find_code_files(exclude_dirs: Set[str]) -> List[Path]:
    """Find all code files in the repository."""
    code_files = []
    root_dir = Path('.')
    
    # Combine static ignores with config-based excludes
    all_ignore_dirs = STATIC_IGNORE_DIRS | exclude_dirs
    
    for root, dirs, files in os.walk(root_dir):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in all_ignore_dirs]
        
        for file in files:
            if file in IGNORE_FILES:
                continue
                
            file_path = Path(root) / file
            
            # Skip if it's a symlink
            if file_path.is_symlink():
                continue
                
            # Check if it's a code file
            if get_file_type(file_path):
                code_files.append(file_path)
    
    return sorted(code_files)


def process_file(file_path: Path) -> Dict[str, any]:
    """Process a single file to check/add license header."""
    result = {
        'file': file_path,
        'file_type': get_file_type(file_path),
        'has_header': False,
        'needs_header': False,
        'modified': False,
        'error': None
    }
    
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result['has_header'] = has_license_header(content, result['file_type'])
        result['needs_header'] = not result['has_header']
        
        if result['needs_header']:
            # Add license header
            new_content = add_license_header(content, result['file_type'])
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            result['modified'] = True
    
    except Exception as e:
        result['error'] = str(e)
    
    return result


def main():
    """Main function."""
    # Load exclusions from config
    exclude_dirs = load_config_excludes()
    
    print(f"Target file types: Python (.py), Shell (.sh)")
    print(f"Excluding directories: {', '.join(sorted(exclude_dirs)) if exclude_dirs else 'none'}")
    print()
    
    # Find all code files
    code_files = find_code_files(exclude_dirs)
    
    if not code_files:
        print("No Python or shell files found.")
        return
    
    print(f"Found {len(code_files)} files to process")
    print()
    
    # Process files
    files_with_headers = 0
    files_needing_headers = 0
    files_modified = 0
    files_with_errors = 0
    
    for file_path in code_files:
        result = process_file(file_path)
        
        if result['error']:
            files_with_errors += 1
            print(f"❌ ERROR: {result['file']}: {result['error']}")
        elif result['has_header']:
            files_with_headers += 1
            print(f"✅ HAS HEADER: {result['file']}")
        elif result['needs_header']:
            files_needing_headers += 1
            if result['modified']:
                files_modified += 1
                print(f"✅ ADDED HEADER: {result['file']} ({result['file_type']})")
            else:
                print(f"❌ FAILED TO ADD: {result['file']} ({result['file_type']})")
    
    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {len(code_files)}")
    print(f"Files with headers: {files_with_headers}")
    print(f"Files needing headers: {files_needing_headers}")
    print(f"Files modified: {files_modified}")
    print(f"Files with errors: {files_with_errors}")
    
    # Exit with error code if there were issues
    if files_with_errors > 0:
        sys.exit(1)


if __name__ == '__main__':
    main() 