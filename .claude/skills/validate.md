---
name: validate
description: Check if documentation is still accurate and up-to-date by validating against sources
---

You are about to launch the **staleness-checker** agent to validate documentation accuracy against original sources.

## What the Staleness Checker Does

The checker is the **quality guardian** - they verify that documented information is still accurate by checking against sources.

**Staleness Checker responsibilities:**
- 🔍 **Validate** documentation against original sources
- 📋 **Enforce** attribution metadata requirements
- 📅 **Update** last_checked dates and validation status
- 🚩 **Flag** out-of-date or incomplete documentation
- 📢 **Be vocal** when metadata is missing (can't validate without it)

## When to Use the Staleness Checker

**Periodic Validation:**
- "Check if the Salesforce docs are still accurate"
- "Validate the infrastructure documentation"
- "Verify the customer profile for Acme Corp"

**Source Verification:**
- "Is this information still current?"
- "Can you verify this against the API documentation?"
- "Check if this code reference is still valid"

**Audit Requests:**
- "Audit all provider documentation for staleness"
- "Check which docs need updating"
- "Validate the security documentation"

**Suspected Staleness:**
- "This looks outdated - can you verify?"
- "I think this changed - can you check?"

## When NOT to Use

**Use knowledge-researcher instead if:**
- Information doesn't exist yet (need to create it)
- Need to gather new information

**Use knowledge-scout instead if:**
- Need to find sources (not validate existing ones)

**Use knowledge-steward instead if:**
- Need to reorganize documentation

## What You'll Get

The checker will:
1. **Check for attribution metadata** (source, date, who gathered it)
2. **If metadata missing:** Politely decline and explain what's needed
3. **If metadata present:** Visit source and validate
4. **Update validation metadata:**
   - `last_checked`: Current date/time
   - `status`: accurate | out_of_date | incomplete | source_unreachable
   - `out_of_date`: true/false flag
5. **Report findings** with specific discrepancies if any
6. **Commit results** to repository

## Expected Output (With Metadata)

```
🔍 Staleness Check: Salesforce OAuth Documentation

📋 Attribution:
- Source: https://developer.salesforce.com/docs/oauth
- Obtained: 2025-12-01 by knowledge-researcher

✅ Validation Results:
- Status: accurate
- Checked: 2026-02-06 16:45
- Findings: All OAuth flows verified. Token refresh documented correctly.

📝 Metadata Updated: Yes
✅ Committed: Yes
```

## Expected Output (Without Metadata)

```
🔍 Staleness Check: Salesforce OAuth Documentation

❌ **Cannot Validate - Missing Attribution Metadata**

This document lacks:
- ❌ No source URL/reference
- ❌ No obtained_date
- ❌ No obtained_by information

**Why This Matters:**
Without knowing where this came from, I can't verify it against the source.

**What's Needed:**
Add frontmatter with attribution metadata:
- attribution.source: Where did this come from?
- attribution.obtained_date: When was it gathered?
```

## The Metadata Schema

Documents should have frontmatter or footer like:

```yaml
---
validation_metadata:
  attribution:
    source: "https://example.com/docs"
    source_type: "url"
    obtained_date: "2025-12-01"
    obtained_by: "knowledge-researcher"
  validation:
    last_checked: "2026-02-06 16:45"
    status: "accurate"
---
```

## Key Principle

**The checker will NOT validate without attribution metadata.** This enforces quality standards - if we don't know where information came from, we can't verify it's still accurate.

## Invoke the Checker

Ask the user what they want validated, then invoke:

```
I'll validate [document/topic] against its original sources.

First, I'll check for attribution metadata.
If present, I'll verify the information is still accurate.
If missing, I'll explain what metadata is needed.
```

Then use the Task tool with `subagent_type: "staleness-checker"` to launch the validation.

---

**Remember:** The checker is professionally insistent about metadata needs. If documents lack attribution, the checker will politely decline and explain why - this helps improve the repository's quality standards over time.
