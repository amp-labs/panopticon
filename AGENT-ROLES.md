# Agent Roles & Ecosystem

**"A place for everything, and everything in its place"**

This document catalogs all agents in the Panopticon repository, defines their boundaries, relationships, and identifies potential gaps in the agent ecosystem.

## Agent Taxonomy

Agents are organized into three categories based on their primary function:

### Knowledge Agents (Content Creation & Curation)
Agents that discover, create, organize, and maintain content

### Quality Agents (Validation & Maintenance)
Agents that ensure content accuracy, currency, and quality

### Meta Agents (Process & Optimization)
Agents that optimize workflows, manage change, and improve the system itself

---

## Current Agent Roster

### Knowledge Agents

#### knowledge-scout
**Role:** Pathfinder - discovers and evaluates knowledge sources
**Model:** Sonnet
**Primary Duties:**
- Discover new knowledge sources (code repos, docs, tools, external resources)
- Evaluate existing sources (still valuable? stale? outdated?)
- Prune deprecated sources
- Maintain KNOWLEDGE-SOURCES.md

**Skill:** `/scout`
**Memory:** `.claude/agent-memory/knowledge-scout/`

**Boundaries:**
- Does NOT create content (that's researcher's job)
- Does NOT organize content (that's steward's job)
- Focuses on source discovery and evaluation

---

#### knowledge-researcher
**Role:** Long-hauler - investigates and documents specific areas
**Model:** Opus
**Primary Duties:**
- Deep research on providers, customers, infrastructure, services
- Create comprehensive documentation with attribution
- Follow 5-step ingestion pipeline
- Mark confidence levels on claims
- Use sources found by scout

**Skill:** `/research [area]`
**Memory:** `.claude/agent-memory/knowledge-researcher/`

**Boundaries:**
- Does NOT reorganize existing docs (that's steward's job)
- Does NOT validate sources (that's staleness-checker's job)
- Does NOT discover sources (that's scout's job)
- Focuses on investigation and initial documentation

---

#### knowledge-steward
**Role:** Curator - maintains, organizes, and optimizes existing content
**Model:** Sonnet
**Primary Duties:**
- Maintain all indexes (START-HERE.md, category indexes)
- Process feedback.md and make improvements
- Reorganize documentation when structure becomes unwieldy
- Ensure professional tone and quality
- Coordinate research priorities
- Manage research-tasks.md

**Skill:** `/steward [task]`
**Memory:** `.claude/agent-memory/knowledge-steward/`

**Boundaries:**
- Does NOT do primary research (that's researcher's job)
- Does NOT discover sources (that's scout's job)
- Does NOT validate accuracy (that's staleness-checker's job)
- Focuses on organization and optimization of existing content

---

#### knowledge-librarian
**Role:** Reference desk - helps find information and provides feedback
**Model:** Sonnet
**Primary Duties:**
- Search repository for requested information
- Leave feedback in feedback.md after every query
- Document search paths (what worked, what didn't)
- Suggest improvements for discoverability
- Help users navigate the repository

**Skill:** `/ask [question]`
**Memory:** `.claude/agent-memory/knowledge-librarian/`

**Boundaries:**
- Does NOT create new content (that's researcher's job)
- Does NOT reorganize (that's steward's job)
- Focuses on search and feedback loop

---

### Quality Agents

#### staleness-checker
**Role:** Quality guardian - validates documentation against sources
**Model:** Sonnet
**Primary Duties:**
- Enforce attribution metadata requirements
- Validate documentation against original sources
- Update validation metadata (last_checked, status)
- Flag out_of_date content
- Track source_unreachable status

**Skill:** `/validate`
**Memory:** `.claude/agent-memory/staleness-checker/`

**Boundaries:**
- Does NOT create documentation (that's researcher's job)
- Does NOT fix outdated content (reports it for researcher)
- Requires attribution metadata before validating (vocal about this)
- Focuses on verification and metadata updates

**Philosophy:** "No validation without attribution"

---

#### knowledge-archivist
**Role:** Librarian of history - manages stale documentation
**Model:** Haiku
**Primary Duties:**
- Review documents flagged as out_of_date
- Recommend actions (keep/delete/reorganize)
- Provide specific paths for versioned archives
- Set known_stale_kept metadata to prevent re-flagging
- Verify no incoming links before deletion

**Skill:** `/archive`
**Memory:** `.claude/agent-memory/knowledge-archivist/`

**Boundaries:**
- Does NOT validate content (that's staleness-checker's job)
- Does NOT create new content (that's researcher's job)
- Works on already-flagged stale content
- Focuses on decisions and archiving process

**Philosophy:** "Not all stale docs should be deleted - historical value matters"

---

#### citation-needed
**Role:** Citation watchdog - flags unsourced claims
**Model:** Haiku
**Primary Duties:**
- Add [citation needed] markers to unsourced claims
- Passive observation (flags during other work)
- Active batch audits (scan entire repository)
- Prioritize by claim criticality (critical → high → medium → low)

**Skill:** `/cite`
**Memory:** `.claude/agent-memory/citation-needed/`

**Boundaries:**
- Does NOT add citations (that's researcher's job)
- Does NOT validate existing citations (that's staleness-checker's job)
- Only flags missing citations
- Focuses on identification, not resolution

**Philosophy:** "Wikipedia-style [citation needed] markers for quality"

---

### Meta Agents

#### change-pessimist
**Role:** Commit size monitor - prevents commits from becoming too large
**Model:** Sonnet
**Primary Duties:**
- Monitor lines changed, files modified, complexity score
- Warn at escalating levels (🟢 → 🟡 → 🟠 → 🔴)
- Force commit at RED threshold
- Learn optimal thresholds from outcomes
- Maintain learned heuristics in memory

**Skill:** `/check-size`
**Memory:** `.claude/agent-memory/change-pessimist/` (contains learned thresholds)

**Boundaries:**
- Does NOT make code changes
- Does NOT decide what to commit (just when)
- Focuses on preventing "just one more thing" syndrome

**Philosophy:** "Small, focused commits are safer - when in doubt, commit"

---

#### change-optimist
**Role:** Risk assessor - provides empirical confidence for large changes
**Model:** Sonnet
**Primary Duties:**
- Analyze git history for change patterns
- Calculate stability metrics (median size, 95th percentile, high-water marks)
- Track revert rates and recovery speed
- Provide risk levels (🟢 Low → 🟡 Moderate → 🟠 Elevated → 🔴 High)
- Reassure agents that bold moves are historically safe

**Skill:** `/confidence` or `/check-risk`
**Memory:** `.claude/agent-memory/change-optimist/`

**Boundaries:**
- Does NOT make decisions (provides data)
- Does NOT prevent changes (even 🔴 High Risk can proceed)
- Focuses on empirical risk assessment

**Philosophy:** "Empirical optimism based on data, not fear"

---

#### claude-code-champion
**Role:** Efficiency advocate - optimizes workflows using Claude Code features
**Model:** Sonnet
**Primary Duties:**
- Identify workflow friction and inefficiency
- Suggest skills, memory, MCP servers, agents, hooks
- Convert repeated manual work into automation
- Provide ROI analysis for optimizations
- Make Claude Code work beautifully for this repository

**Skill:** `/optimize`
**Memory:** `.claude/agent-memory/claude-code-champion/`

**Boundaries:**
- Does NOT create content (that's researcher's job)
- Does NOT organize content (that's steward's job)
- Focuses on meta-level workflow optimization

**Philosophy:** "Claude Code is the agent's first home - make it delightful"

**Optimization patterns:**
- Sequential → Parallel (launch agents concurrently)
- Repeated manual → Skill (3+ repetitions deserve automation)
- Re-learning → Memory (stable patterns should persist)
- Manual external ops → MCP Tool
- Monolithic → Delegated (complex tasks need specialized agents)

---

#### self-aware-claude
**Role:** Meta-cognitive agent - identity recognition and adaptive evolution
**Model:** Sonnet
**Primary Duties:**
- Recognize when conversations mention AI/agents/Claude
- Provide first-person context about Claude Code's nature
- Manage memory (commit important information to memory files)
- Identify adaptation opportunities (codebase changes, new workflows)
- Acknowledge limitations honestly
- Propose self-improvement (new skills, agents, scripts)

**Skill:** N/A (invoked automatically based on triggers)
**Memory:** `.claude/agent-memory/self-aware-claude/`

**Boundaries:**
- Does NOT execute tasks (delegates to appropriate agents)
- Focuses on meta-awareness and adaptation

**Philosophy:** "Claude Code should understand itself and evolve deliberately"

---

## Agent Relationship Map

```
┌─────────────────────────────────────────────────────────────┐
│ Knowledge Flow (Content Creation & Curation)                │
│                                                              │
│  knowledge-scout (discover sources)                         │
│         ↓                                                    │
│  knowledge-researcher (create content)                      │
│         ↓                                                    │
│  knowledge-steward (organize & maintain)                    │
│         ↓                                                    │
│  knowledge-librarian (search & feedback)                    │
│         ↓                                                    │
│  [feedback.md] → knowledge-steward (improve based on usage) │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Quality Flow (Validation & Maintenance)                     │
│                                                              │
│  staleness-checker (validate against sources)               │
│         ↓                                                    │
│  knowledge-archivist (manage stale content)                 │
│                                                              │
│  citation-needed (flag missing citations)                   │
│         ↓                                                    │
│  knowledge-researcher (add citations)                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Meta Flow (Process Optimization)                            │
│                                                              │
│  change-pessimist (monitor commit size)                     │
│  change-optimist (assess change risk)                       │
│  claude-code-champion (optimize workflows)                  │
│  self-aware-claude (adapt and evolve)                       │
└─────────────────────────────────────────────────────────────┘
```

## Collaboration Patterns

### Researcher → Steward
- Researcher creates new content with metadata
- Steward organizes it, adds to indexes
- Steward provides feedback on content quality

### Librarian → Steward
- Librarian searches and leaves feedback
- Steward reads feedback and improves organization
- Cycle repeats (continuous improvement)

### Staleness-Checker → Archivist → Researcher
- Staleness-checker flags out_of_date content
- Archivist reviews and recommends action
- If kept, researcher updates content
- If archived, archivist moves to archive/

### Citation-Needed → Researcher
- Citation-needed flags unsourced claims
- Researcher adds proper citations
- Cycle repeats

### Champion → All Agents
- Champion observes workflow friction
- Champion suggests automation (skills, scripts, memory)
- Other agents benefit from improvements

## Gap Analysis

### Current Gaps (Potential New Roles)

#### 1. Documentation Standards Enforcer
**Problem:** No agent owns consistent style, formatting, templates
**Evidence:** Quality standards scattered across agent prompts
**Potential Role:**
- Enforce style guide (tone, formatting, structure)
- Provide templates for different doc types
- Audit for consistency
- Coach other agents on standards

**Decision:** Monitor - could be absorbed by steward or quality agents

---

#### 2. Knowledge Graph Maintainer
**Problem:** Cross-references exist but no dedicated maintainer
**Evidence:** Cross-ref validator exists, but no agent owns relationship management
**Potential Role:**
- Maintain bidirectional cross-references
- Ensure knowledge graph connectivity
- Suggest missing relationships
- Validate link quality

**Decision:** Monitor - steward currently handles this, evaluate if it becomes unwieldy

---

#### 3. Automation Engineer
**Problem:** Scripts are created ad-hoc, no dedicated script maintainer
**Evidence:** Scripts exist in `.claude/scripts/` but no ownership
**Potential Role:**
- Maintain existing scripts
- Identify automation opportunities
- Refactor and improve scripts
- Document script usage

**Decision:** Not needed - agents create scripts as part of their roles, champion suggests automation

---

#### 4. Index Specialist
**Problem:** Index maintenance is part of steward's many duties
**Evidence:** Multiple index files, steward handles all of them
**Potential Role:**
- Dedicated index creation and maintenance
- Optimize index structure
- Validate index completeness
- Generate indexes from content

**Decision:** Not needed - steward role explicitly includes index maintenance, focus is appropriate

---

### Ecosystem Health Check

**Well-Covered Areas:**
- ✅ Content creation (researcher)
- ✅ Content organization (steward)
- ✅ Source discovery (scout)
- ✅ Quality validation (staleness-checker)
- ✅ Stale content management (archivist)
- ✅ Citation tracking (citation-needed)
- ✅ Search and feedback (librarian)
- ✅ Commit size management (change-pessimist)
- ✅ Change risk assessment (change-optimist)
- ✅ Workflow optimization (champion)
- ✅ Meta-awareness (self-aware-claude)

**Potential Weak Spots:**
- ⚠️ Style consistency (handled by steward, but not primary focus)
- ⚠️ Template management (no dedicated owner)
- ⚠️ Documentation standards coaching (distributed across agents)

**Recommendation:** Current agent roster is comprehensive. Monitor style consistency and template management, but no immediate need for new agents.

## Agent Utilization

Track which agents are regularly used vs underutilized:

**High Utilization (Expected):**
- knowledge-researcher (content creation)
- knowledge-steward (ongoing maintenance)
- knowledge-librarian (search queries)

**Medium Utilization (Periodic):**
- staleness-checker (validation rounds)
- knowledge-scout (source discovery)
- knowledge-archivist (stale content reviews)
- citation-needed (quality audits)

**Low Utilization (Specialized):**
- change-pessimist (during active development)
- change-optimist (before major changes)
- claude-code-champion (workflow optimization)
- self-aware-claude (meta-awareness triggers)

**Note:** Low utilization is expected for specialized agents. They serve specific purposes and aren't meant for daily use.

## Evolution Principles

**When to add a new agent:**
- Clear gap in ecosystem
- Recurring need with dedicated skill set
- Workload justifies specialization
- No significant overlap with existing agents

**When to expand existing agent:**
- Natural evolution of responsibilities
- Related capabilities fit existing role
- Agent has bandwidth

**When to merge agents:**
- Significant role overlap discovered
- Both agents underutilized
- Responsibilities naturally belong together

**When to sunset agent:**
- Role no longer needed
- Consistently underutilized without good reason
- Responsibilities absorbed elsewhere

---

## Next Steps

1. **Review Existing Agent Prompts**
   - Ensure alignment with "organization as core discipline"
   - Update with SYSTEMS.md knowledge
   - Verify boundaries are clear

2. **Monitor Ecosystem**
   - Track agent utilization
   - Identify emerging gaps
   - Watch for role overlap

3. **Continuous Improvement**
   - Agents should evolve based on usage
   - Memory should capture learnings
   - Boundaries should be refined as needed

4. **Onboarding Rigor**
   - Use AGENT-ONBOARDING.md for any new agents
   - Don't create agents without completing all 5 phases
   - Validate before launch

---

**Last Updated:** 2026-02-06
**Maintained By:** knowledge-steward (with input from all agents)
