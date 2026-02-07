#!/usr/bin/env bash
# check-exploration-deadlines.sh
# Validates exploration documents and reports on deadline status
#
# Used by: maintenance rounds, steward agent
# Purpose: Ensure explorations don't linger indefinitely, force decision-making

set -euo pipefail

# Color output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "Checking exploration deadlines..."
echo

# Find all markdown files in content directories
content_dirs=("providers" "services" "infrastructure" "customers" "team" "security" "observability")

total_explorations=0
overdue=0
warning=0
active=0

current_date=$(date +%Y-%m-%d)

for dir in "${content_dirs[@]}"; do
  if [ ! -d "$dir" ]; then
    continue
  fi

  for file in "$dir"/*.md; do
    # Skip index files
    if [[ "$file" == *"-index.md" ]] || [[ "$file" == "*/README.md" ]]; then
      continue
    fi

    # Skip if file doesn't exist (glob didn't match)
    if [ ! -f "$file" ]; then
      continue
    fi

    # Extract frontmatter
    frontmatter=$(sed -n '/^---$/,/^---$/p' "$file" | head -n -1 | tail -n +2)

    # Check if status is exploration, proposal, accepted, or rejected
    status=$(echo "$frontmatter" | grep -A 1 "status:" | tail -n 1 | sed 's/^[[:space:]]*//' | tr -d '"' || echo "")

    if [[ "$status" != "exploration" ]] && [[ "$status" != "proposal" ]] && [[ "$status" != "accepted" ]] && [[ "$status" != "rejected" ]]; then
      continue
    fi

    total_explorations=$((total_explorations + 1))

    # Extract exploration metadata
    started_date=$(echo "$frontmatter" | grep "started_date:" | sed 's/.*started_date:[[:space:]]*//' | tr -d '"' || echo "unknown")
    decision_deadline=$(echo "$frontmatter" | grep "decision_deadline:" | sed 's/.*decision_deadline:[[:space:]]*//' | tr -d '"' || echo "unknown")
    decision_owner=$(echo "$frontmatter" | grep "decision_owner:" | sed 's/.*decision_owner:[[:space:]]*//' | tr -d '"' || echo "unknown")
    reason=$(echo "$frontmatter" | grep "reason:" | sed 's/.*reason:[[:space:]]*//' | tr -d '"' || echo "unknown")

    # Calculate days until deadline
    if [[ "$decision_deadline" != "unknown" ]]; then
      deadline_epoch=$(date -j -f "%Y-%m-%d" "$decision_deadline" +%s 2>/dev/null || echo "0")
      current_epoch=$(date -j -f "%Y-%m-%d" "$current_date" +%s)
      days_remaining=$(( (deadline_epoch - current_epoch) / 86400 ))
    else
      days_remaining=-999
    fi

    # Categorize and report
    if [[ "$status" == "rejected" ]] || [[ "$status" == "accepted" ]]; then
      # These should be archived
      echo -e "${YELLOW}⚠️  NEEDS ARCHIVAL${NC} $file"
      echo "   Status: $status"
      echo "   Action needed: Move to archive/${status}-proposals/"
      echo
      warning=$((warning + 1))
    elif [[ $days_remaining -lt 0 ]] && [[ $days_remaining != -999 ]]; then
      # Overdue
      echo -e "${RED}🔴 OVERDUE${NC} $file"
      echo "   Deadline: $decision_deadline (${days_remaining#-} days ago)"
      echo "   Owner: $decision_owner"
      echo "   Reason: $reason"
      echo "   Action needed: Make decision or extend deadline"
      echo
      overdue=$((overdue + 1))
    elif [[ $days_remaining -le 3 ]] && [[ $days_remaining -ge 0 ]]; then
      # Warning (3 days or less)
      echo -e "${YELLOW}⚠️  WARNING${NC} $file"
      echo "   Deadline: $decision_deadline ($days_remaining days remaining)"
      echo "   Owner: $decision_owner"
      echo "   Reason: $reason"
      echo
      warning=$((warning + 1))
    else
      # Active
      echo -e "${GREEN}✅ ACTIVE${NC} $file"
      if [[ $days_remaining != -999 ]]; then
        echo "   Deadline: $decision_deadline ($days_remaining days remaining)"
      else
        echo "   Deadline: Not set"
      fi
      echo "   Owner: $decision_owner"
      echo
      active=$((active + 1))
    fi
  done
done

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary:"
echo "  Total explorations: $total_explorations"
echo "  Active (on track): $active"
echo "  Warning (≤3 days): $warning"
echo "  Overdue: $overdue"
echo

if [[ $overdue -gt 0 ]]; then
  echo -e "${RED}Action required: $overdue explorations are overdue${NC}"
  exit 1
elif [[ $warning -gt 0 ]]; then
  echo -e "${YELLOW}Attention needed: $warning explorations need decision soon${NC}"
  exit 0
else
  echo -e "${GREEN}All explorations are on track${NC}"
  exit 0
fi
