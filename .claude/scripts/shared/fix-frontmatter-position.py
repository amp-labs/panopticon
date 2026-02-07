#!/usr/bin/env python3
"""
Move YAML frontmatter to the beginning of markdown files.

Fixes files where frontmatter appears after the title instead of at the start.
"""

import sys
import re
from pathlib import Path

def fix_frontmatter_position(filepath):
    """Move frontmatter to beginning of file."""
    content = Path(filepath).read_text()

    # Check if frontmatter is already at the beginning
    if content.startswith('---'):
        print(f"✓ {filepath}: Frontmatter already at beginning")
        return False

    # Find frontmatter anywhere in file
    frontmatter_pattern = r'^(---\s*\nvalidation_metadata:.*?^---\s*\n)'
    match = re.search(frontmatter_pattern, content, re.MULTILINE | re.DOTALL)

    if not match:
        print(f"⚠ {filepath}: No frontmatter found")
        return False

    frontmatter = match.group(1)

    # Remove frontmatter from current position
    content_without_frontmatter = content.replace(frontmatter, '', 1)

    # Add frontmatter at beginning
    new_content = frontmatter + '\n' + content_without_frontmatter.lstrip('\n')

    # Write back
    Path(filepath).write_text(new_content)
    print(f"✅ {filepath}: Moved frontmatter to beginning")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: fix-frontmatter-position.py <file1> [file2 ...]")
        sys.exit(1)

    fixed_count = 0
    for filepath in sys.argv[1:]:
        if fix_frontmatter_position(filepath):
            fixed_count += 1

    print(f"\n{fixed_count} file(s) fixed")

if __name__ == '__main__':
    main()
