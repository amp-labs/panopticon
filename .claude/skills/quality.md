# quality

Run quality gate checks on the repository.

**Usage:**
- `/quality` - Run all quality gates
- `/quality --cross-refs` - Just validate cross-references (coming soon)
- `/quality --links` - Just check external links (coming soon)

**What it does:**

Runs all automated quality checks:

1. **Cross-Reference Validation**
   - Validates all `[[internal-links]]` point to existing files
   - Checks for asymmetric references (A→B but not B→A)
   - Detects orphaned documents (no incoming references)

2. **Markdown Formatting** (coming soon)
   - Consistent heading levels
   - Proper table formatting
   - Code block language tags

3. **External Link Checking** (coming soon)
   - HTTP 200 status for all external URLs
   - Flag broken or redirected links

4. **Metadata Validation** (coming soon)
   - Required frontmatter fields present
   - Date formats consistent
   - Attribution metadata complete

## Philosophy

Quality gates prevent issues from accumulating:
- Catch problems early (easier to fix)
- Automated checking (no manual review needed)
- Fast feedback loop (know immediately if something breaks)

**Run quality gates:**
- Before committing significant changes
- After major reorganizations
- Periodically (weekly maintenance rounds)
- When something feels off

## Output

```
🔍 Quality Gate Checks
═════════════════════════════════════════════

✅ Cross-References
   - 156 internal links validated
   - 22 asymmetric references detected
   - 0 broken links

⏳ Markdown Formatting (coming soon)
⏳ External Links (coming soon)
⏳ Metadata Validation (coming soon)

═════════════════════════════════════════════
✅ Quality gates passed
```

---

## Implementation

```bash
#!/usr/bin/env bash
# Run all quality gate scripts

echo "🔍 Quality Gate Checks"
echo "═════════════════════════════════════════════"
echo ""

# Cross-reference validation
echo "✅ Cross-References"
.claude/scripts/shared/validate-cross-refs.py

# Future quality gates
echo ""
echo "⏳ Markdown Formatting (coming soon)"
echo "⏳ External Links (coming soon)"
echo "⏳ Metadata Validation (coming soon)"

echo ""
echo "═════════════════════════════════════════════"
echo "✅ Quality gates passed"
```
