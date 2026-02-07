#!/usr/bin/env bash
# validate-metadata.sh - Check that documentation has required attribution metadata
#
# Used by: All agents (shared utility)
# Purpose: Validates that documentation files have required frontmatter metadata
#          before staleness-checker can validate them
#
# Usage: ./validate-metadata.sh [file.md]
#        ./validate-metadata.sh (checks all .md files in services/, providers/, infrastructure/)

set -euo pipefail

check_file() {
    local file="$1"
    local errors=0

    # Skip if not a markdown file
    [[ "$file" != *.md ]] && return 0

    # Check for frontmatter
    if ! head -1 "$file" | grep -q "^---$"; then
        echo "❌ $file: Missing frontmatter (no opening ---)"
        return 1
    fi

    # Extract frontmatter
    local frontmatter
    frontmatter=$(awk '/^---$/{if(++c==2) exit} c==1' "$file")

    # Required fields (check for nested YAML structure)
    local required_patterns=(
        "attribution:"
        "source:"
        "obtained_date:"
        "obtained_by:"
    )

    for pattern in "${required_patterns[@]}"; do
        if ! echo "$frontmatter" | grep -q "$pattern"; then
            echo "❌ $file: Missing required field containing: $pattern"
            ((errors++))
        fi
    done

    if [[ $errors -eq 0 ]]; then
        echo "✅ $file: Metadata valid"
        return 0
    else
        return 1
    fi
}

main() {
    if [[ $# -eq 0 ]]; then
        # Check all documentation files
        local exit_code=0
        echo "Validating metadata in documentation files..."
        echo ""

        for dir in services providers infrastructure customers team; do
            if [[ -d "$dir" ]]; then
                for file in "$dir"/*.md; do
                    [[ -f "$file" ]] || continue
                    check_file "$file" || exit_code=1
                done
            fi
        done

        exit $exit_code
    else
        # Check specific file
        check_file "$1"
    fi
}

main "$@"
