---
name: explore
description: Structured decision research for novel providers, dependencies, or architectural choices
---

You are about to launch the **knowledge-explorer** agent to conduct decision-making research for a potential integration, dependency, or architectural change.

## What the Explorer Does

The explorer is the **decision analyst** - they research options and provide recommendations on whether to proceed.

**Explorer responsibilities:**
- 🎯 Comparative analysis (Option A vs Option B)
- 📊 Decision criteria and weighted scoring
- 💡 Clear recommendations (Go/No-Go/More Info)
- ⚠️ Risk and unknown identification
- 📅 Time-bound research (14-day default deadline)

## Explorer vs. Researcher

If the user wants to know **"How does X work?"** use `/research` instead.
If the user wants to know **"Should we use X?"** use `/explore`.

| Explorer | Researcher |
|----------|------------|
| Decision focus ("Should we?") | Documentation focus ("How does it work?") |
| Comparison matrices | Technical details |
| Recommendations | Implementation docs |
| status: exploration | status: production |
| Temporary (until decision) | Permanent reference |

## What the Explorer Evaluates

- **Providers**: Should we integrate with Notion? Linear? Airtable?
- **Dependencies**: Should we use Redis? RabbitMQ? Different database?
- **Architecture**: Should we split this service? Redesign this API?
- **Vendors**: Should we use Datadog? New Relic? Self-hosted monitoring?

## Explorer Output

**Document location:** Same as production docs (providers/, services/, etc.) but with `status: "exploration"` in frontmatter

**Document format:**
- Executive Summary with recommendation
- Decision Criteria comparison matrix
- Detailed analysis with pros/cons
- Recommendation with confidence level
- Risks & unknowns
- Implementation path (if approved)
- Archival path (if rejected)

**Lifecycle:**
- Active: Lives in normal location, indexed under "Under Exploration"
- Accepted: Transitioned to production documentation
- Rejected: Moved to `archive/rejected-proposals/` with "Why We Said No" section

## Agent Guidance

See `.claude/agents/knowledge-explorer.md` for full agent specification.

Ask the user what they want to evaluate, then invoke the knowledge-explorer agent with clear scope.

Example invocation:
```
I'll evaluate [topic] by comparing [options] against [criteria] and provide a recommendation by [deadline].
```

Then use the Task tool with `subagent_type: "Explore"` to launch the exploration session.
