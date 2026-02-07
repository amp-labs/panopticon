#!/usr/bin/env python3
"""
Fix HTML comment metadata to proper YAML frontmatter.

Converts documents with:
  <!--
  attribution:
    source: ...
  -->

To:
  ---
  validation_metadata:
    attribution:
      source: ...
  ---
"""

import sys
import re
from pathlib import Path

def fix_metadata(filepath):
    """Convert HTML comment metadata to YAML frontmatter."""
    content = Path(filepath).read_text()

    # Check if already has frontmatter
    if content.startswith('---'):
        print(f"✓ {filepath}: Already has YAML frontmatter")
        return False

    # Extract HTML comment metadata
    html_comment_pattern = r'<!--\s*(attribution:.*?validation:.*?)\s*-->'
    match = re.search(html_comment_pattern, content, re.DOTALL)

    if not match:
        print(f"⚠ {filepath}: No HTML comment metadata found")
        return False

    metadata_block = match.group(1)

    # Convert to YAML frontmatter
    yaml_frontmatter = f"""---
validation_metadata:
  {metadata_block}
---
"""

    # Replace HTML comment with YAML frontmatter
    new_content = re.sub(
        r'<!--\s*attribution:.*?-->\s*\n*',
        yaml_frontmatter,
        content,
        count=1,
        flags=re.DOTALL
    )

    # Write back
    Path(filepath).write_text(new_content)
    print(f"✅ {filepath}: Converted to YAML frontmatter")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: fix-metadata-format.py <file1> [file2 ...]")
        sys.exit(1)

    fixed_count = 0
    for filepath in sys.argv[1:]:
        if fix_metadata(filepath):
            fixed_count += 1

    print(f"\n{fixed_count} file(s) fixed")

if __name__ == '__main__':
    main()
