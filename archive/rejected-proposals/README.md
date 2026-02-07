# Rejected Proposals Archive

This directory contains proposals and explorations that were researched but ultimately rejected.

## Purpose

**Rejected proposals are valuable institutional knowledge:**
- Prevent re-investigation of dead ends
- Document "why we said no"
- Provide context for future similar decisions
- Show what we considered and learned

## What Lives Here

**Content:** Exploration documents with `status: "rejected"` that have been archived after decision

**Examples:**
- Provider evaluations (Notion, Airtable, Linear)
- Dependency evaluations (Redis, alternative databases)
- Architecture proposals (service splits, API redesigns)
- Vendor evaluations (monitoring tools, infrastructure providers)

## File Naming Convention

`YYYY-MM-{topic}.md`

**Examples:**
- `2026-02-notion-provider.md` - Notion provider evaluation (rejected Feb 2026)
- `2026-01-redis-caching.md` - Redis for caching evaluation (rejected Jan 2026)
- `2025-12-api-v2-redesign.md` - API v2 redesign (rejected Dec 2025)

## Required Content

When a proposal is archived as rejected, it MUST include:

### "Why We Said No" Section

```markdown
## Why We Said No

**Decision Date:** YYYY-MM-DD
**Decision Maker:** [Name or Team]

**Key Factors:**
- [Factor 1: e.g., Cost savings didn't justify migration risk]
- [Factor 2: e.g., Existing solution already battle-tested]
- [Factor 3: e.g., Missing critical features we need]

**What Would Change Our Mind:**
- [Condition 1: e.g., Provider adds webhook support for all events]
- [Condition 2: e.g., Cost difference grows to >5x]
- [Condition 3: e.g., Current solution deprecated or unsupported]

**Related Rejected Explorations:**
- [Other similar proposals that were also rejected]
```

## Lifecycle

1. **Active exploration** - Lives in normal content area with `status: "exploration"`
2. **Decision made: rejected** - Status updated to `status: "rejected"`
3. **Archived** - Moved to this directory with "Why We Said No" section added
4. **Index updated** - Moved from "Under Exploration" to "Recently Rejected" section

## Value Over Time

**Short term (0-6 months):**
- Prevents immediate re-investigation
- Fresh context for related decisions

**Medium term (6-18 months):**
- Historical context as teams change
- Reference for "we already looked at that"

**Long term (18+ months):**
- May become outdated as technology evolves
- Candidates for archival pruning if conditions changed

## Maintenance

**Quarterly review:**
- Check if rejection reasons still valid
- Update "what would change our mind" if conditions changed
- Archive to `archive/historical/` if no longer relevant

## Related

- `archive/accepted-proposals/` - Proposals that were accepted and implemented
- `archive/feedback-archive-YYYY-QN.md` - Historical feedback entries
