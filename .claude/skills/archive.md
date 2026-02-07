---
name: archive
description: Review stale documentation and recommend actions (keep/delete/reorganize)
---

You are about to launch the **knowledge-archivist** agent to manage stale documentation in the Panopticon repository.

## What the Archivist Does

The archivist is the **librarian of history** - they decide what to do with out-of-date documentation.

**Archivist responsibilities:**
- 🔍 **Scan** for documents marked as out_of_date or unreachable
- 📊 **Assess** historical value and relevance
- 💡 **Recommend** specific actions: keep as-is, delete, or reorganize
- 📝 **Update metadata** to prevent infinite re-review loops
- 🎯 **Provide exact steps** for executing recommendations

## When to Use the Archivist

**Stale Document Management:**
- "What should we do with outdated documentation?"
- "Review all out-of-date provider docs"
- "Clean up stale infrastructure documentation"

**Archive Review:**
- "Scan for documents that need archival"
- "Review stale documentation and recommend cleanup"
- "Audit old documentation for value"

**Periodic Cleanup:**
- "Quarterly stale documentation review"
- "Check what docs the staleness-checker flagged"

**Orphan Detection:**
- "Find orphaned documentation"
- "Look for unreferenced old docs"

## When NOT to Use

**Use staleness-checker instead if:**
- Need to validate if docs are accurate (not manage stale ones)

**Use knowledge-steward instead if:**
- Need to reorganize current (not stale) documentation

**Use knowledge-researcher instead if:**
- Need to update documentation (not archive it)

## What You'll Get

The archivist provides **specific recommendations** for each stale document:

### Recommendation Types

**1. Keep as-is (Mark as Known Stale)**
- Document has historical/reference value
- Add metadata to prevent re-flagging:
  ```yaml
  archive:
    known_stale_kept: true
    known_stale_kept_date: "2026-02-06"
    reason_kept: "Historical reference for API v1"
  ```

**2. Delete**
- No historical value, not referenced
- Exact file path and verification steps
- Safety checks (no incoming links)

**3. Reorganize**
- Should move to archive/versioned location
- Exact current and new paths
- Step-by-step move instructions

## Example Output

```
📊 Archivist Review Session: 2026-02-06

🔍 Scan Results:
- Documents scanned: 47
- Out of date: 8
- Source unreachable: 2
- Skipped (known stale kept): 3

💡 Recommendations Summary:
- Keep as-is: 4 (marked known_stale_kept)
- Delete: 2 (awaiting execution)
- Reorganize: 4 (awaiting execution)

📄 Detailed Recommendations:

---

📄 Document: providers/salesforce/oauth-v1.md
💡 Recommendation: Keep as-is

Reason: API v1 still used by legacy customers
Historical value: High

Action: Add metadata:
```yaml
archive:
  known_stale_kept: true
  known_stale_kept_date: "2026-02-06"
  reason_kept: "Historical reference for Salesforce API v1"
```

---

📄 Document: infrastructure/preview-pr-1234.md
💡 Recommendation: Delete

Reason: Temporary preview environment (PR closed)
Historical value: None
References: 0 incoming links

Action:
git rm infrastructure/preview-pr-1234.md

---

📄 Document: infrastructure/kubernetes-2023.md
💡 Recommendation: Reorganize

Current: infrastructure/kubernetes-2023.md
New: archive/infrastructure/kubernetes/setup-2023.md

Reason: Superseded by 2024 setup, but shows evolution

Steps:
1. Create archive/infrastructure/kubernetes/
2. Move document to new location
3. Update frontmatter with archive metadata
```

## Prevention of Infinite Loops

The archivist marks "keep as-is" decisions with metadata:

```yaml
archive:
  known_stale_kept: true
  known_stale_kept_date: "2026-02-06"
  reason_kept: "Why we're keeping this stale doc"
```

This prevents the archivist from constantly re-reviewing the same documents. Future scans will skip documents with `known_stale_kept: true`.

## Decision Criteria

**Keep as-is:**
- Historical reference value
- Versioned specs (v1, v2, etc.)
- "How we used to do it" docs
- Still frequently referenced

**Delete:**
- Temporary docs (preview envs, experiments)
- Superseded (new version exists, old not referenced)
- Duplicates
- No longer relevant, no historical value

**Reorganize:**
- Versioned documentation
- Archived systems/processes
- Historical decisions (ADRs)
- Belongs in organized archive structure

## Invoke the Archivist

Ask the user what they want reviewed, then invoke:

```
I'll scan for stale documentation and provide specific recommendations.

For each stale document, I'll recommend:
- Keep as-is (with metadata to prevent re-flagging)
- Delete (with safety checks)
- Reorganize (with exact new location)

All recommendations will include specific execution steps.
```

Then use the Task tool with `subagent_type: "knowledge-archivist"` to launch the review.

---

**Remember:** The archivist recommends but doesn't execute (except for metadata updates). This provides a safety layer - humans or steward can review recommendations before deletion.
