# Accepted Proposals Archive

This directory contains proposals and explorations that were accepted and subsequently implemented.

## Purpose

**Accepted proposals are historical context:**
- Show what decisions were made and why
- Document the research that informed implementation
- Provide context for "why did we choose X?"
- Trace evolution of the system over time

## What Lives Here

**Content:** Exploration documents with `status: "accepted"` that have been archived after implementation

**Examples:**
- Provider integrations that were researched and then built
- Dependencies that were evaluated and then adopted
- Architecture changes that were proposed and then implemented
- Vendor selections that were researched and then chosen

## File Naming Convention

`YYYY-MM-{topic}.md`

**Examples:**
- `2026-02-salesforce-provider.md` - Salesforce provider evaluation (accepted Feb 2026, now in production)
- `2026-01-temporal-workflows.md` - Temporal adoption (accepted Jan 2026, now core infrastructure)
- `2025-12-kubernetes-migration.md` - K8s migration (accepted Dec 2025, completed)

## Lifecycle

1. **Active exploration** - Lives in normal content area with `status: "exploration"`
2. **Decision made: accepted** - Status updated to `status: "accepted"`
3. **Implementation begins** - Proposal guides implementation
4. **Implementation complete** - Production documentation created
5. **Archived** - Original exploration moved to this directory for historical context

## Relationship to Production Docs

**This archive:** Historical decision-making research (comparative analysis, tradeoffs, recommendations)
**Production docs:** Current implementation details (how it works, how to use it, technical reference)

**Example:**
- `archive/accepted-proposals/2026-01-salesforce-provider.md` - Original evaluation research
- `providers/salesforce.md` - Current production documentation

Both exist because they serve different purposes:
- Archive: "Why we chose Salesforce over Notion" (decision context)
- Production: "How Salesforce integration works" (operational reference)

## When to Archive

**Trigger:** When production documentation is created and validated

**Process:**
1. knowledge-researcher creates production doc (e.g., `providers/salesforce.md`)
2. Production doc has `status: "production"` in frontmatter
3. Original exploration moved from content area to this archive
4. Index updated to move from "Under Exploration" to "Production"
5. Cross-reference added: production doc mentions original evaluation in archive

## Value Over Time

**Short term (0-6 months):**
- Context for team members who weren't involved in decision
- Reference for similar upcoming decisions

**Medium term (6-18 months):**
- Historical context as teams change
- "What were we thinking when we chose X?"

**Long term (18+ months):**
- System evolution history
- Lessons learned for future decisions
- Comparison data may be outdated, but decision rationale remains valuable

## Archive Content

Archived accepted proposals should include:

### Decision Summary (added when archived)

```markdown
## Decision Summary

**Decision Date:** YYYY-MM-DD
**Decision Maker:** [Name or Team]
**Implementation Date:** YYYY-MM-DD (when went to production)

**Key Factors in Acceptance:**
- [Factor 1: e.g., Superior API quality vs alternatives]
- [Factor 2: e.g., Better cost structure for our use case]
- [Factor 3: e.g., Existing team experience]

**Production Documentation:**
See [current documentation](../../providers/salesforce.md) for implementation details

**Lessons Learned:**
- [Lesson 1: e.g., API integration took 2 weeks vs 3-week estimate]
- [Lesson 2: e.g., OAuth complexity higher than expected]
- [Lesson 3: e.g., Rate limits required additional optimization]
```

## Maintenance

**Annual review:**
- Check if production docs still reference archive entries
- Update cross-references if production docs moved/renamed
- Prune if no longer valuable (very old decisions for deprecated systems)

## Related

- `archive/rejected-proposals/` - Proposals that were researched but rejected
- `providers/`, `services/`, `infrastructure/` - Current production documentation
- `INGESTION-PIPELINE.md` - Documentation lifecycle explanation
