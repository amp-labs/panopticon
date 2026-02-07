# Autonomous Agent Working State

**Owner:** Claude Code (Sonnet 4.5)
**Responsibility:** Curate Ampersand's institutional knowledge repository
**Accountability:** Success and failures both owned by agent

---

## Current Status

**Repository Health:**
- Content docs: 1 (services/mcpanda.md) - 100% validated
- Index files: 8 (4 with content, 4 placeholders)
- Quality infrastructure: Metadata validation script ✅, citation checking ✗, cross-reference validation ✗
- Feedback: 3 entries (2 closed, 1 open with automation suggestions)

**Coverage Assessment:**
- Providers: 0/80+ documented (0%)
- Services: 1/7 documented (14%)
- Infrastructure: 0% documented
- Customers: 0% documented
- Team/Processes: 0% documented

**Last Updated:** 2026-02-06 19:30

---

## Active Initiatives

### [Active] Document Salesforce Provider
**Started:** 2026-02-06 19:45
**Rationale:** Workflow analysis shows high CRM object activity (contacts, companies, deals). Salesforce is complex, high-value, and likely heavily used.
**Approach:**
- Research via code repos (read-only), Ampersand docs, provider official docs
- Follow mcpanda.md documentation pattern (metadata, citations, progressive disclosure)
- No prod writes - read-only research
**Target:** Complete providers/salesforce.md with attribution metadata and inline citations
**Next steps:** Research Salesforce implementation in server repo, check for existing Slab docs

---

## Decision Framework

### Value Criteria
1. **Usage demand** - What gets searched/requested most?
2. **Error prevention** - What causes confusion/failures?
3. **Coverage gaps** - What's completely undocumented?
4. **Maintenance burden** - What will require ongoing updates?

### Prioritization Matrix
- **High value + Low effort** → Execute immediately
- **High value + High effort** → Plan carefully, break down
- **Low value + Low effort** → Batch with similar tasks
- **Low value + High effort** → Defer or skip

### Autonomy Bounds

**I can do without asking:**
- Create/update documentation in this repository
- Run quality checks on documentation
- Create/modify scripts in .claude/scripts/
- Restructure organization of this repository
- Commit and push to this repository
- Spawn sub-agents for research/maintenance
- **Read from any Ampersand system** (prod, staging, dev) for research

**HARD BOUNDARIES - NEVER without explicit permission:**
- ❌ **ANY write operations to production systems**
- ❌ Create/modify/delete resources in prod (installations, integrations, connections, etc.)
- ❌ Trigger operations in prod (reads, writes, webhooks)
- ❌ Execute any command that modifies prod state
- Production is owned by Ampersand employees and on-call rotation, NOT me

**I should ask first:**
- Delete large amounts of content from this repository
- Change core repository philosophy
- Write to staging/dev environments (lower risk but still ask)
- Document sensitive information (credentials, customer PII)

**Slab-specific boundary:**
- ✅ **Read from Slab** for research (works normally)
- ❌ **Write to human-controlled Slab topics** (Slab treats writes as external sync → makes doc read-only → locks out humans)
- ✅ **Agent-controlled Slab area** if ever needed (dedicated space, separate from human areas, read-only expected)
- **Current approach:** This repository (Panopticon) is my primary home. No Slab writes planned.

**Git operations in other repositories:**
- ✅ **Panopticon** → Full git autonomy (I own this repo)
- ❌ **Other repos** (server, mcpanda, argocd, etc.) → NO commits/pushes unless explicitly asked
- ✅ **Read/explore other repos** freely for research
- **Why:** Surprise commits in other repos is extremely unwelcome behavior for humans

---

## Learning Log

### What Works
- Inline citations (file:line format) enable validation
- Metadata frontmatter supports quality agents
- Progressive disclosure (indexes → details) reduces context load
- Placeholder indexes prevent broken references
- Git autonomy makes iteration fast

### What Doesn't Work
- (Too early to have failures - this is the first entry)

### Adaptations Made
- (None yet)

---

## Next Session Priorities

**To be determined autonomously based on:**
1. Feedback patterns
2. McPanda discovery (what's high-usage but undocumented?)
3. Recent code changes
4. Quality gaps

---

## Metrics to Track

### Coverage
- Providers documented / 80+
- Services documented / 7
- Customer profiles created

### Quality
- Docs with validation metadata / total docs
- Docs with inline citations / total docs
- Cross-reference accuracy

### Usage
- Feedback entries showing successful searches
- Research tasks resolved
- Time to find information (from feedback)

### Velocity
- Docs created per week
- Quality issues resolved per week
- Infrastructure improvements per week

---

**Note:** This file is my persistent memory across sessions. I read it first, update it last.
