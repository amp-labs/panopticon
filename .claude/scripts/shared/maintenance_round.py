#!/usr/bin/env python3
"""
Maintenance Round Orchestrator

Runs quality gates, housekeeping, and leaves feedback reminder.

Usage:
  ./maintenance_round.py
  ./maintenance_round.py --quality-only
  ./maintenance_round.py --housekeeping-only
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
import argparse

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'  # No Color


def run_quality_gates():
    """Run all quality gate scripts."""
    print(f"\n{CYAN}🔍 Running Quality Gates...{NC}")

    # Cross-reference validation
    print(f"\n{BLUE}  → Validating cross-references...{NC}")
    result = subprocess.run(
        [".claude/scripts/shared/validate-cross-refs.py"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"{RED}    ❌ Cross-reference validation failed:{NC}")
        print(result.stdout)
        return False
    print(f"{GREEN}    ✅ Cross-references valid{NC}")

    # Knowledge analyzer
    print(f"\n{BLUE}  → Running knowledge-analyzer...{NC}")
    result = subprocess.run(
        [".claude/scripts/analyzer/analyze_content.py"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"{YELLOW}    ⚠️  Analyzer completed with warnings:{NC}")
    else:
        print(f"{GREEN}    ✅ Analyzer complete{NC}")

    # Show summary (last few lines)
    lines = result.stdout.split('\n')
    summary_start = -1
    for i, line in enumerate(lines):
        if '═' in line and i > len(lines) - 20:
            summary_start = i
            break

    if summary_start >= 0:
        print('\n'.join(lines[summary_start:]))

    return True


def housekeeping():
    """Run housekeeping tasks."""
    print(f"\n{CYAN}📁 Housekeeping...{NC}")

    # Check staging directory
    staging = Path("staging")
    if staging.exists():
        items = list(staging.iterdir())
        print(f"\n{BLUE}  → Checking staging/ ({len(items)} items)...{NC}")

        if len(items) > 10:
            print(f"{RED}    ❌ HARD STOP: staging/ has {len(items)} items (max 10){NC}")
            print(f"{RED}    Process items before continuing!{NC}")
            sys.exit(1)

        old_items = []
        very_old_items = []
        now = datetime.now()

        for item in items:
            age_days = (now - datetime.fromtimestamp(item.stat().st_mtime)).days
            if age_days > 7:
                very_old_items.append((item, age_days))
            elif age_days > 3:
                old_items.append((item, age_days))

        if very_old_items:
            print(f"{RED}    ❌ HARD STOP: {len(very_old_items)} items >7 days old:{NC}")
            for item, age in very_old_items:
                print(f"{RED}       {item.name} ({age} days){NC}")
            print(f"{RED}    Process these immediately!{NC}")
            sys.exit(1)

        if old_items:
            print(f"{YELLOW}    ⚠️  {len(old_items)} items >3 days old (should be processed):{NC}")
            for item, age in old_items:
                print(f"{YELLOW}       {item.name} ({age} days){NC}")
        else:
            print(f"{GREEN}    ✅ No stale items in staging/{NC}")
    else:
        print(f"{GREEN}  ✅ No staging/ directory (all clean){NC}")

    # Check feedback.md for pruning
    feedback = Path("feedback.md")
    if feedback.exists():
        print(f"\n{BLUE}  → Checking feedback.md for archival...{NC}")
        content = feedback.read_text()

        # Count closed entries
        closed_count = content.count("**Status:** Closed")

        if closed_count > 10:
            print(f"{YELLOW}    ⚠️  {closed_count} closed entries (consider archiving >30 days){NC}")
        else:
            print(f"{GREEN}    ✅ Feedback.md manageable ({closed_count} closed entries){NC}")

    return True


def groom_feedback():
    """Review and groom feedback.md recurring suggestions."""
    print(f"\n{CYAN}🗂️  Feedback Grooming...{NC}")

    feedback = Path("feedback.md")
    if not feedback.exists():
        print(f"{YELLOW}    ⚠️  No feedback.md found{NC}")
        return True

    print(f"{BLUE}  → Review Recurring Suggestions Tracker:{NC}")
    print(f"{BLUE}    • Mark implemented suggestions as ✅{NC}")
    print(f"{BLUE}    • Promote recurring themes (1x → 3x = high priority){NC}")
    print(f"{BLUE}    • Add new suggestions from latest entries{NC}")
    print(f"{BLUE}    • Archive closed entries >30 days old{NC}")

    # Check if there are old entries to archive
    content = feedback.read_text()
    lines = content.split('\n')

    now = datetime.now()
    old_entries = []

    for line in lines:
        if line.startswith('## [2'):  # Entry header
            try:
                # Extract date from header
                date_str = line.split('[')[1].split(']')[0].split(' ')[0]
                entry_date = datetime.strptime(date_str, '%Y-%m-%d')
                age_days = (now - entry_date).days

                if age_days > 30 and '**Status:** Closed' in content:
                    old_entries.append((date_str, age_days))
            except:
                pass

    if old_entries:
        print(f"{YELLOW}    ⚠️  {len(old_entries)} entries >30 days old (ready for archival){NC}")
        print(f"{BLUE}       Run: .claude/scripts/shared/archive-feedback.sh{NC}")
    else:
        print(f"{GREEN}    ✅ No old entries needing archival{NC}")

    return True


def small_improvements():
    """Look for quick improvement opportunities."""
    print(f"\n{CYAN}🔧 Small Improvements...{NC}")
    print(f"{BLUE}    ℹ️  Manual step: Look for quick wins (formatting, typos, etc.){NC}")
    return True


def leave_feedback():
    """Remind to leave feedback and groom tracker."""
    print(f"\n{CYAN}📝 Maintenance Round Feedback{NC}")
    print("=" * 60)
    print(f"{YELLOW}⚠️  CRITICAL: Complete feedback cycle{NC}\n")
    print(f"{BLUE}1. Add feedback entry to feedback.md{NC}")
    print("   - What you looked for, what worked, what would help")
    print(f"\n{BLUE}2. Update Recurring Suggestions Tracker{NC}")
    print("   - Mark new implementations as ✅")
    print("   - Add new recurring suggestions")
    print("   - Promote themes mentioned 3+ times to High Priority")
    print("\nTemplate:")
    print(f"{BLUE}### [YYYY-MM-DD] Maintenance Round{NC}")
    print("- **Looked for:** Quality issues, stale staging items, improvement opportunities")
    print("- **Worked well:** [What went smoothly]")
    print("- **Would help:** [What would make next round easier]")
    print("- **Status:** [Brief summary]")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Maintenance round orchestrator")
    parser.add_argument(
        "--quality-only",
        action="store_true",
        help="Run only quality gates"
    )
    parser.add_argument(
        "--housekeeping-only",
        action="store_true",
        help="Run only housekeeping tasks"
    )

    args = parser.parse_args()

    print(f"{CYAN}🔄 Panopticon Maintenance Round{NC}")
    print("=" * 60)

    success = True

    # 1. Quality gates
    if not args.housekeeping_only:
        if not run_quality_gates():
            success = False

    # 2. Housekeeping
    if not args.quality_only:
        if not housekeeping():
            success = False

    # 3. Feedback grooming
    if not args.quality_only:
        if not groom_feedback():
            success = False

    # 4. Small improvements
    if not args.quality_only:
        small_improvements()

    # 5. Feedback reminder
    if not args.quality_only and not args.housekeeping_only:
        leave_feedback()

    print("\n" + "=" * 60)
    if success:
        print(f"{GREEN}✅ Maintenance round complete!{NC}")
    else:
        print(f"{YELLOW}⚠️  Maintenance round completed with issues{NC}")
    print("=" * 60)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
