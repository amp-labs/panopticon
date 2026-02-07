#!/usr/bin/env python3
"""
validate-cross-refs.py

Validates cross-references in markdown files.
Checks if files referenced in markdown links or backtick-wrapped filenames actually exist.

Detects:
  - [text](relative/path.md) format
  - `filename.md` format

Usage: ./validate-cross-refs.py [directory]
  If no argument provided, scans current directory

Note: Some "broken" references are expected:
  - INGESTION-PIPELINE.md contains example paths (acme-corp.md, etc.)
  - Agent documentation (.claude/agents/*.md) contains example references
  - Use judgment to distinguish real broken links from example/template references

Used by: maintenance agents, steward
Useful for: Quality gates, housekeeping rounds, pre-commit checks
"""

import os
import re
import sys
from pathlib import Path

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


def find_markdown_files(directory):
    """Find all markdown files, excluding archive and .git directories."""
    # Files that contain example/template references (not actual cross-refs)
    skip_files = {
        'KNOWLEDGE-SOURCES.md',  # External source catalog
        'INGESTION-PIPELINE.md',  # Documentation with example paths
        'AGENT-ONBOARDING.md',  # Onboarding guide with example references
        'SYSTEMS.md',  # System documentation with template patterns
    }

    for root, dirs, files in os.walk(directory):
        # Exclude archive and .git directories
        dirs[:] = [d for d in dirs if d not in ['archive', '.git']]
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                # Skip documentation files with example references
                if file_path.name in skip_files:
                    continue
                # Skip staging README (contains example filenames)
                if 'staging' in str(file_path) and file_path.name == 'README.md':
                    continue
                # Skip agent documentation (contains references to auto memory pattern)
                if '.claude/agents' in str(file_path):
                    continue
                # Skip agent memory files (contain references to files that will be created)
                if '.claude/agent-memory' in str(file_path):
                    continue
                # Skip personal memory files (may reference non-repo files)
                if '.claude/my-memory' in str(file_path):
                    continue
                # Skip skill documentation (may contain example references)
                if '.claude/skills' in str(file_path):
                    continue
                yield file_path


def extract_backtick_refs(content):
    """Extract backtick-wrapped .md references like `filename.md`."""
    return re.findall(r'`([^`]+\.md)`', content)


def extract_link_refs(content):
    """Extract markdown link references like [text](path.md)."""
    matches = re.findall(r'\]\(([^)]+\.md[^)]*)\)', content)
    # Filter out URLs
    return [m for m in matches if not m.startswith('http://') and not m.startswith('https://')]


def is_template_or_example(ref):
    """Check if reference is a template/example pattern (expected not to exist)."""
    # Template patterns like YYYY-MM-DD, [placeholder], {variable}
    template_patterns = [
        'YYYY', 'MM', 'DD', 'QN',  # Date templates
        '[', '{',  # Placeholder syntax
        '...', 'example', 'sample',  # Example indicators
    ]

    # External repository references (not in this repo)
    external_repos = [
        'server/', 'mcpanda://', 'argocd/',
        '~/.claude/',  # Home directory references
        '/app/',  # Container paths (builder-mcp)
        'ENV_VARS.md',  # External docs
    ]

    # Check for template patterns
    for pattern in template_patterns:
        if pattern in ref:
            return True

    # Check for external repo references
    for repo in external_repos:
        if ref.startswith(repo):
            return True

    return False


def check_ref_exists(ref, file_path, search_dirs):
    """Check if a referenced file exists."""
    # Remove anchor fragments
    ref = ref.split('#')[0]
    if not ref:
        return True

    # Skip template/example references
    if is_template_or_example(ref):
        return True

    ref_path = Path(ref)

    # Check relative to file's directory
    file_dir = file_path.parent
    if (file_dir / ref).exists():
        return True

    # Check in root directory
    if ref_path.exists():
        return True

    # Check in common content directories
    for search_dir in search_dirs:
        if (search_dir / ref).exists():
            return True
        # Also check with basename only
        if (search_dir / ref_path.name).exists():
            return True

    return False


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')

    print(f"🔍 Validating cross-references in: {target}")
    print()

    search_dirs = [
        Path('providers'),
        Path('services'),
        Path('infrastructure'),
        Path('customers'),
        Path('team'),
        Path('processes')
    ]

    broken_refs = []
    checked_files = 0
    total_refs = 0

    for md_file in find_markdown_files(target):
        checked_files += 1
        content = md_file.read_text(errors='ignore')

        # Check backtick references
        for ref in extract_backtick_refs(content):
            total_refs += 1
            if not check_ref_exists(ref, md_file, search_dirs):
                broken_refs.append((md_file, ref, 'backtick'))

        # Check markdown link references
        for ref in extract_link_refs(content):
            total_refs += 1
            if not check_ref_exists(ref, md_file, search_dirs):
                broken_refs.append((md_file, ref, 'link'))

    print("━" * 60)

    if not broken_refs:
        print(f"{GREEN}✅ All cross-references valid{NC}")
        print(f"   Checked {checked_files} markdown files, {total_refs} references")
        return 0
    else:
        print(f"{RED}❌ Found {len(broken_refs)} broken reference(s):{NC}")
        print()
        for file_path, ref, ref_type in broken_refs:
            print(f"{RED}❌ BROKEN{NC} {file_path}")
            if ref_type == 'backtick':
                print(f"   Reference: `{ref}`")
            else:
                print(f"   Reference: [{ref}](...)")
            print()
        print(f"   Checked {checked_files} markdown files, {total_refs} references")
        return 1


if __name__ == '__main__':
    sys.exit(main())
