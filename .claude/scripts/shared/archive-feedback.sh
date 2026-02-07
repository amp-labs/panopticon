#!/usr/bin/env bash
# archive-feedback.sh - Archive closed feedback entries older than 30 days
#
# Used by: Maintenance agent (during housekeeping)
# Purpose: Prevents unbounded growth of feedback.md by archiving old closed entries
#
# Usage: ./archive-feedback.sh

set -euo pipefail

FEEDBACK_FILE="feedback.md"
CUTOFF_DATE=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d "30 days ago" +%Y-%m-%d)
CURRENT_QUARTER=$(date +%Y-Q$(($(date +%-m)/3+1)))
ARCHIVE_FILE="archive/feedback-archive-${CURRENT_QUARTER}.md"

echo "Archiving closed feedback entries older than ${CUTOFF_DATE}..."

# Check if feedback.md exists
if [[ ! -f "$FEEDBACK_FILE" ]]; then
    echo "Error: $FEEDBACK_FILE not found"
    exit 1
fi

# Create archive file with header if it doesn't exist
if [[ ! -f "$ARCHIVE_FILE" ]]; then
    cat > "$ARCHIVE_FILE" << 'EOF'
# Archived Feedback Entries

This file contains closed feedback entries archived from feedback.md.

## Archived Entries

EOF
fi

# Temporary files
TEMP_FEEDBACK=$(mktemp)
TEMP_ARCHIVE=$(mktemp)
TEMP_ENTRY=$(mktemp)

# Cleanup on exit
trap "rm -f $TEMP_FEEDBACK $TEMP_ARCHIVE $TEMP_ENTRY" EXIT

# Copy original feedback to temp
cp "$FEEDBACK_FILE" "$TEMP_FEEDBACK"

# Track state
in_entry=0
in_feedback_section=0
entry_date=""
entry_status=""
current_entry=""
archived_count=0

# Read line by line
while IFS= read -r line; do
    # Check if we're in the feedback entries section
    if [[ "$line" == "## Feedback Entries" ]]; then
        in_feedback_section=1
        echo "$line" >> "$TEMP_FEEDBACK.new"
        continue
    fi

    # If not in feedback section, just copy the line
    if [[ $in_feedback_section -eq 0 ]]; then
        echo "$line" >> "$TEMP_FEEDBACK.new"
        continue
    fi

    # Check for entry header: ## [YYYY-MM-DD HH:MM] - Agent Name
    if [[ "$line" =~ ^##\ \[([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        # Save previous entry if it exists
        if [[ -n "$current_entry" ]]; then
            # Check if we should archive this entry
            if [[ "$entry_status" == "Closed"* ]] && [[ "$entry_date" < "$CUTOFF_DATE" ]]; then
                echo "$current_entry" >> "$TEMP_ARCHIVE"
                ((archived_count++))
            else
                echo "$current_entry" >> "$TEMP_FEEDBACK.new"
            fi
        fi

        # Start new entry
        entry_date="${BASH_REMATCH[1]}"
        entry_status=""
        current_entry="$line"
        in_entry=1
        continue
    fi

    # If we're in an entry, accumulate lines
    if [[ $in_entry -eq 1 ]]; then
        current_entry="$current_entry
$line"

        # Check for status line
        if [[ "$line" =~ ^\*\*Status:\*\*\ (.+)$ ]]; then
            entry_status="${BASH_REMATCH[1]}"
        fi

        # Check for entry separator
        if [[ "$line" == "---" ]] || [[ "$line" == "" && "$current_entry" =~ Status ]]; then
            # Entry is complete, will be processed at next header or EOF
            continue
        fi
    else
        # Not in an entry, just copy the line
        echo "$line" >> "$TEMP_FEEDBACK.new"
    fi
done < "$TEMP_FEEDBACK"

# Handle last entry
if [[ -n "$current_entry" ]]; then
    if [[ "$entry_status" == "Closed"* ]] && [[ "$entry_date" < "$CUTOFF_DATE" ]]; then
        echo "$current_entry" >> "$TEMP_ARCHIVE"
        ((archived_count++))
    else
        echo "$current_entry" >> "$TEMP_FEEDBACK.new"
    fi
fi

# If we archived anything, append to archive file and update feedback.md
if [[ $archived_count -gt 0 ]]; then
    echo "" >> "$ARCHIVE_FILE"
    cat "$TEMP_ARCHIVE" >> "$ARCHIVE_FILE"
    mv "$TEMP_FEEDBACK.new" "$FEEDBACK_FILE"
    echo "✅ Archived $archived_count closed entries to $ARCHIVE_FILE"
else
    rm -f "$TEMP_FEEDBACK.new"
    echo "✅ No entries to archive (none older than $CUTOFF_DATE and closed)"
fi
