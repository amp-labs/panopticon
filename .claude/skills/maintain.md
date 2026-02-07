# maintain

Run a maintenance round on the Panopticon repository.

**Usage:**
- `/maintain` - Full maintenance round (quality gates + housekeeping + improvements)
- `/maintain --quality-only` - Just run quality gates (coming soon)
- `/maintain --housekeeping-only` - Just housekeeping tasks (coming soon)

**What it does:**

## 1. Quality Gates
- ✅ Validate cross-references (check all `[[links]]` are valid)
- ✅ Run knowledge-analyzer (catalog + gap detection)
- ✅ Check for broken external links (coming soon)
- ✅ Validate markdown formatting (coming soon)

## 2. Housekeeping
- 📁 Process `staging/` directory (move items >3 days old to permanent homes)
  - Hard stop if staging has >10 files or items >7 days old
  - Staging should be temporary chaos, not permanent dumping ground
- 🗑️ Prune `feedback.md` (archive closed entries >30 days old)
  - Moves to `archive/feedback-archive-YYYY-QN.md`
  - Keeps feedback.md focused on recent/actionable items
- 📊 Check if indexes need updating

## 3. Small Improvements
- 🔍 Look for quick wins (formatting consistency, typo fixes, etc.)
- 📝 Update metadata where obviously stale
- 🔗 Fix asymmetric cross-references if found

## 4. Feedback Loop
**CRITICAL:** Always leave feedback at the end of maintenance round:
- What was looked for
- What worked well
- What would make future rounds easier
- Suggestions for improvement

This creates the feedback loop that improves the repository over time.

## Philosophy

Maintenance is about **maintaining order**:
- "A place for everything, and everything in its place"
- Fight entropy through regular rounds
- Small improvements compound over time
- Organization is not overhead - it's the foundation

**Disorganization compounds**: A misplaced file today becomes a knowledge gap tomorrow.

## Output

Summary report showing:
- ✅ Quality gates passed/failed
- 📁 Housekeeping actions taken
- 🔧 Improvements made
- 📝 Feedback entry added

---

## Implementation

```python
#!/usr/bin/env python3
"""
Maintenance round orchestrator
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta

def run_quality_gates():
    """Run all quality gate scripts."""
    print("🔍 Running Quality Gates...")

    # Cross-reference validation
    print("\n  → Validating cross-references...")
    result = subprocess.run(
        [".claude/scripts/shared/validate-cross-refs.py"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"    ❌ Cross-reference validation failed:\n{result.stdout}")
        return False
    print("    ✅ Cross-references valid")

    # Knowledge analyzer
    print("\n  → Running knowledge-analyzer...")
    result = subprocess.run(
        [".claude/scripts/analyzer/analyze_content.py"],
        capture_output=True,
        text=True
    )
    print(result.stdout)

    return True

def housekeeping():
    """Run housekeeping tasks."""
    print("\n📁 Housekeeping...")

    # Check staging directory
    staging = Path("staging")
    if staging.exists():
        items = list(staging.iterdir())
        print(f"\n  → Checking staging/ ({len(items)} items)...")

        if len(items) > 10:
            print(f"    ❌ HARD STOP: staging/ has {len(items)} items (max 10)")
            print("    Process items before continuing!")
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
            print(f"    ❌ HARD STOP: {len(very_old_items)} items >7 days old:")
            for item, age in very_old_items:
                print(f"       {item.name} ({age} days)")
            print("    Process these immediately!")
            sys.exit(1)

        if old_items:
            print(f"    ⚠️  {len(old_items)} items >3 days old (should be processed):")
            for item, age in old_items:
                print(f"       {item.name} ({age} days)")
        else:
            print("    ✅ No stale items in staging/")
    else:
        print("  ✅ No staging/ directory (all clean)")

    # Check feedback.md for pruning
    feedback = Path("feedback.md")
    if feedback.exists():
        print("\n  → Checking feedback.md for archival...")
        # Would implement: scan for closed entries >30 days old
        # For now, just note
        print("    ℹ️  Manual check: Archive closed entries >30 days")

    return True

def small_improvements():
    """Look for quick improvement opportunities."""
    print("\n🔧 Looking for small improvements...")
    print("    ℹ️  Manual step: Check for quick wins")
    return True

def leave_feedback():
    """Remind to leave feedback."""
    print("\n📝 Maintenance Round Feedback")
    print("=" * 60)
    print("⚠️  CRITICAL: Add feedback entry to feedback.md")
    print("\nTemplate:")
    print("### [YYYY-MM-DD] Maintenance Round")
    print("- **Looked for:** Quality issues, stale staging items, improvement opportunities")
    print("- **Worked well:** [What went smoothly]")
    print("- **Would help:** [What would make next round easier]")
    print("- **Status:** [Brief summary]")
    print("=" * 60)

def main():
    print("🔄 Panopticon Maintenance Round")
    print("=" * 60)

    success = True

    # 1. Quality gates
    if not run_quality_gates():
        success = False

    # 2. Housekeeping
    if not housekeeping():
        success = False

    # 3. Small improvements
    small_improvements()

    # 4. Feedback reminder
    leave_feedback()

    print("\n" + "=" * 60)
    if success:
        print("✅ Maintenance round complete!")
    else:
        print("⚠️  Maintenance round completed with issues")
    print("=" * 60)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
```
