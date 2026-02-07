# Staging Directory

**"Quick capture now, thoughtful organization later"**

This is the chaos zone—a temporary landing area for information that hasn't yet been organized.

## Purpose

When information arrives suddenly (user dumps a lot of context, quick notes from a meeting, partial research, rough drafts), you need a place to put it WITHOUT blocking on "where does this permanently belong?"

Staging solves this:
- ✅ Capture information immediately (don't lose it)
- ✅ Don't block on organization decisions
- ✅ Process and organize later, thoughtfully
- ✅ Prevent "half-organized" files from polluting main directories

## What Goes in Staging

**Good candidates:**
- Quick notes that need expansion
- Partial research needing more investigation
- Information dumps needing categorization
- Rough drafts before quality review
- Files where permanent location is unclear
- Multiple related items that arrived together

**Bad candidates:**
- Finished, well-structured documentation (goes directly to permanent home)
- Single clear facts (just add to existing doc)
- Obvious category placement (providers/salesforce.md, not staging)

## File Naming in Staging

Use descriptive names that help future processing:

```
YYYY-MM-DD-topic-description.md
```

Examples:
- `2026-02-06-salesforce-api-quirks-notes.md`
- `2026-02-06-customer-acme-integration-dump.md`
- `2026-02-06-gcp-infrastructure-partial.md`
- `2026-02-06-linear-tickets-batch.md`

Include date so you know how long items have been sitting.

## Processing Workflow

**During Maintenance Rounds:**

1. **Review staging/** directory
   - Scan for files that have been sitting >3 days
   - Prioritize by age and importance

2. **Process each file:**
   - Expand/improve content if needed
   - Determine proper permanent location
   - Rename following category conventions
   - Move to permanent home
   - Update relevant indexes
   - Delete staging file

3. **Commit:**
   - Stage the moved/organized file
   - Commit with message: "Process staging: [topic] → [final location]"

**Maximum staging time:** Files shouldn't sit in staging for >7 days. If something has been in staging for a week, either:
- Process it (organize and move)
- Delete it (wasn't important enough)
- Move it to research-tasks.md (needs more investigation)

## Example Flow

**Capture Phase:**
```bash
# User dumps Salesforce OAuth info
cat > staging/2026-02-06-salesforce-oauth-dump.md <<EOF
Quick notes from debugging Salesforce OAuth:
- Refresh tokens expire after 90 days
- Must use instance URL from token response
- Login URLs differ: test.salesforce.com vs login.salesforce.com
...
EOF
```

**Processing Phase (later maintenance round):**
```bash
# Review staging
ls -la staging/

# Process the file
# 1. Expand notes into proper documentation
# 2. Add frontmatter metadata
# 3. Add citations
# 4. Move to permanent location
mv staging/2026-02-06-salesforce-oauth-dump.md providers/salesforce-oauth.md

# Update index
# (add entry to providers-index.md)

# Commit
git add providers/salesforce-oauth.md providers-index.md
git commit -m "Process staging: Salesforce OAuth notes → providers/salesforce-oauth.md"
```

## Maintenance Rules

**Keep staging clean:**
- Don't let it become a permanent dumping ground
- Process items regularly (every maintenance round)
- If staging has >10 files, that's a red flag (needs processing session)
- If files are >7 days old, that's a red flag (prioritize processing)

**Processing is part of housekeeping:**
- Every maintenance round should check staging/
- Older items get priority
- Quick wins (easy to organize) get processed first
- Complex items may spawn research tasks

## Scripts for Staging Management

Potential automation (create as needed):

**`.claude/scripts/shared/staging-report.sh`**
- List staging files by age
- Flag items >7 days old
- Count total items
- Suggest processing priorities

**`.claude/scripts/steward/process-staging-item.sh`**
- Interactive script to process one staging file
- Prompts for category, proper name, location
- Moves file and updates indexes
- Commits the change

## When NOT to Use Staging

**Skip staging when:**
- Information has obvious permanent home (put it there directly)
- File is already well-organized (no staging needed)
- Quick addition to existing doc (just edit the doc)
- Clear category and proper structure (follow ingestion pipeline directly)

**Use staging when:**
- Unclear where this belongs
- Needs more work before permanent placement
- Information dump that needs untangling
- Multiple related items arriving together
- Time pressure (capture now, organize later)

## Critical Guardrails

⚠️ **DANGER: Staging can become an excuse for poor organization**

Staging is ONLY useful if you maintain discipline:

**The Rules:**
1. **Process regularly** - Every maintenance round MUST check staging/
2. **7-day maximum** - Nothing sits in staging for >7 days
3. **10-file limit** - If staging has >10 files, stop and process immediately
4. **Default to direct placement** - Staging is the exception, not the norm
5. **No "staging mentality" in main dirs** - Main directories stay clean and organized

**Red Flags (staging is failing):**
- Staging has >10 files
- Files in staging for >7 days
- Using staging for things with obvious homes
- Main directories getting messy because "staging will handle it"
- Staging becoming permanent dumping ground

**Recovery:**
- Dedicate a maintenance session to clearing staging
- Review and tighten staging criteria
- Consider if staging is being misused
- Ensure main directories aren't degrading

**Remember:** Staging exists to PREVENT chaos, not to ENABLE it. If staging is making the repository messier, you're using it wrong.

---

**Philosophy:** Staging is the pressure valve that keeps the main directories clean. It lets you be responsive (capture everything) while also being thoughtful (organize properly). Process staging regularly and it serves you well. Neglect staging and it becomes technical debt.

**The test:** Can you remove staging/ entirely and the repository is still perfectly organized? If yes, staging is working. If no, you're relying on staging as a crutch.

**Last Updated:** 2026-02-06
