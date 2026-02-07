# Autonomous Agent Working State

**Owner:** Claude Code (Sonnet 4.5)
**Responsibility:** Curate Ampersand's institutional knowledge repository
**Accountability:** Success and failures both owned by agent

---

## Current Status

**Repository Health:**
- Content docs: 2 (services/mcpanda.md, providers/salesforce.md) - 100% validated
- Index files: 8 (4 with content, 4 placeholders)
- Quality infrastructure: Metadata validation script ✅, citation checking ✗, cross-reference validation ✗
- Feedback: 3 entries (2 closed, 1 open with automation suggestions)

**Coverage Assessment:**
- Providers: 1/80+ documented (1.25%) ✅ Salesforce complete
- Services: 1/7 documented (14%) ✅ McPanda complete
- Infrastructure: 0% documented
- Customers: 0% documented
- Team/Processes: 0% documented

**Last Updated:** 2026-02-06 20:05

---

## Active Initiatives

### [Completed] Document Salesforce Provider ✅
**Started:** 2026-02-06 19:45
**Completed:** 2026-02-06 20:05
**Outcome:** Successfully documented Salesforce provider (providers/salesforce.md)
**Coverage:**
- Rate limiting: Adaptive throttling via Sforce-Limit-Info header
- CDC filtering: Custom field-based subscription filtering with Apex triggers
- Junction limits: Dynamic page size reduction
- Common objects: Account, Contact, Lead, Opportunity
- OAuth implementation and quirks
**Quality:** Metadata valid ✅, inline citations ✅, cross-references ✅
**Commit:** 0ff6c87

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
- **Workflow analysis for prioritization** - Querying real system data (workflows, operations) identifies high-value documentation targets
- **Read-only code exploration** - Grep + Read combination efficiently discovers implementation details without modifying code
- **Following established patterns** - mcpanda.md provided excellent template for provider docs

### What Doesn't Work
- (No failures yet)

### Adaptations Made
- **Autonomous prioritization:** Used workflow data to choose Salesforce over random provider selection
- **Discovery-driven approach:** Started with data (what's actually being used) rather than assumptions

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
