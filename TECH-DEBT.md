# Technical Debt Register

This file tracks known technical debt in the Panopticon repository. Technical debt is code or design that works but will cause problems at scale or during maintenance.

## How to Use This

**Adding debt:**
- Document shortcuts taken during implementation
- Include impact assessment and triggers for addressing
- Estimate cost to fix now vs later

**Reviewing debt:**
- **Weekly**: Check if any triggers have fired
- **Monthly**: Assess if tactical debt is blocking work
- **Quarterly**: Evaluate if implementation debt needs refactoring

**Addressing debt:**
- Update status when addressed
- Move to "Resolved" section with resolution date
- Document lessons learned

## Debt Categories

- **Strategic Debt**: Design decisions that will limit growth (address proactively)
- **Tactical Debt**: Shortcuts that work but aren't elegant (pay down opportunistically)
- **Implementation Debt**: Code that works but is hard to maintain (refactor when touched)

---

## Strategic Debt (Address Before Scale)

### DEBT-001: Catalog linear scan doesn't scale beyond ~100 docs
**Created:** 2026-02-06
**Component:** knowledge-analyzer
**Category:** Performance
**Impact:**
- None at current scale (15 docs)
- Noticeable at 50 docs (~5 second scans)
- Unacceptable at 100+ docs (>10 second scans)

**Triggers:**
- When doc count reaches 50: Investigate incremental analysis
- When doc count reaches 100: Must implement caching/incremental
- When full scan takes >5 seconds: Performance degradation noticed

**Cost to fix now:** 3 hours (design incremental analysis)
**Cost to fix at 100 docs:** 1 week (refactor + migration)

**Decision:** Acceptable now, address at 50 docs
**Owner:** knowledge-analyzer maintenance

---

### DEBT-002: No structured query capability (not a knowledge graph)
**Created:** 2026-02-06
**Component:** knowledge-analyzer catalog
**Category:** Architecture
**Impact:**
- Can't answer complex queries ("all services using temporal")
- Can't do inference ("if A uses B and B uses C, what depends on C?")
- Manual cross-reference analysis required

**Triggers:**
- When librarian requests complex queries
- When steward needs relationship analysis
- When catalog reaches 50+ entities (relationship complexity grows)

**Cost to fix now:** 1-2 weeks (knowledge graph implementation)
**Cost to fix at scale:** 2-3 weeks (migration + graph build)

**Decision:** Catalog sufficient for v1, migrate to graph in v4
**Migration path:** See knowledge-analyzer.md v1→v4 migration

---

## Tactical Debt (Pay Down Opportunistically)

### DEBT-003: knowledge-analyzer catalog has no schema validation
**Created:** 2026-02-06
**Component:** knowledge-analyzer catalog
**Category:** Quality
**Impact:**
- Low (errors caught during development/testing)
- Could cause silent failures if catalog malformed
- Harder to debug when catalog structure changes

**Triggers:**
- First schema-related bug (malformed YAML causes failure)
- When adding new catalog fields (want validation)
- When multiple agents write to catalog (need consistency)

**Cost to fix:** 30 minutes (add pydantic or similar validation)

**Decision:** Ship without validation, add when it becomes a problem
**Owner:** knowledge-analyzer maintenance

---

### DEBT-004: No automated catalog migration
**Created:** 2026-02-06
**Component:** knowledge-analyzer catalog
**Category:** Operations
**Impact:**
- If catalog format changes, manual migration required
- Risk of inconsistent catalog state during migration
- Downtime during major format changes

**Triggers:**
- First catalog format breaking change
- When adding required fields to existing catalogs

**Cost to fix:** 1-2 hours (migration script framework)

**Decision:** Acceptable for v1, add migration tooling when needed
**Owner:** knowledge-analyzer maintenance

---

## Implementation Debt (Refactor When Touched)

### DEBT-005: Gap detection is one large function
**Created:** 2026-02-06
**Component:** knowledge-analyzer gap detection
**Category:** Maintainability
**Impact:**
- Low at current complexity (6 gap types)
- Will become unwieldy at 10+ gap types
- Hard to unit test individual gap types

**Triggers:**
- When adding 7th gap type
- When gap detection logic becomes hard to read
- When bugs appear in specific gap types

**Cost to fix:** 1 hour (refactor into gap detector classes)

**Decision:** Acceptable for v1, refactor when extending
**Owner:** knowledge-analyzer implementation

---

### DEBT-006: Cross-reference validation duplicated in two tools
**Created:** 2026-02-06
**Component:** validate-cross-refs.py + knowledge-analyzer
**Category:** Duplication
**Impact:**
- Same logic in two places
- If cross-ref format changes, need to update both
- Inconsistent results possible

**Triggers:**
- When cross-reference logic changes
- When bugs appear in one but not the other

**Cost to fix:** 2 hours (consolidate into shared library)

**Decision:** Acceptable for now, consolidate when it causes issues
**Owner:** Shared scripts maintenance

### DEBT-007: Auto-invoke researcher not fully wired
**Created:** 2026-02-06
**Component:** knowledge-analyzer auto-invoke
**Category:** Implementation
**Impact:**
- Blocking gaps are detected but researcher not auto-spawned
- Manual research task pickup still required
- Autonomous loop not fully closed

**Triggers:**
- When first blocking gap is detected
- When autonomous research becomes priority

**Cost to fix:** 1 hour (wrapper script or agent integration)

**Technical note:**
- Python script can't call Task tool (Claude Code environment only)
- Need wrapper that runs script, reads auto-invoke output, spawns Task
- Or integrate analyzer into agent that can call Task directly

**Decision:** Detection logic is correct, wiring deferred until needed
**Owner:** knowledge-analyzer implementation

---

### DEBT-008: Autonomous research sequential processing
**Created:** 2026-02-06
**Component:** autonomous_research.py
**Category:** Performance
**Impact:**
- Slow at scale (18 gaps × 5min = 90min total)
- Can't parallelize research for faster completion
- Single failure blocks remaining gaps

**Triggers:**
- When gap count > 50 (total time > 4 hours)
- When total research time > 2 hours becomes blocking
- When parallel research would provide significant time savings

**Cost to fix:** 4 hours (parallel orchestration with coordination)

**Technical note:**
- Sequential is safer and easier to debug for v1
- Parallel requires coordination to prevent conflicts
- Would need dependency analysis between gaps
- Retry logic becomes more complex with parallel execution

**Decision:** Sequential acceptable for v1 (18 gaps manageable)
**Owner:** autonomous_research.py implementation

---

### DEBT-009: No cross-gap context sharing
**Created:** 2026-02-06
**Component:** autonomous_research.py
**Category:** Intelligence
**Impact:**
- Duplicate research when gaps have overlapping topics
- Missed connections between related gaps
- Each research task starts from scratch

**Triggers:**
- When gaps have obvious overlap (same service, related concepts)
- When duplicate research is observed in multiple gap results
- When researcher requests shared context mechanism

**Cost to fix:** 8 hours (shared context mechanism + refactor)

**Technical note:**
- Independent tasks are simpler for v1
- Shared context requires persistence between spawned instances
- Would need to track what each gap learned
- Context accumulation could help later gaps benefit from earlier ones

**Decision:** Independent tasks acceptable for v1
**Owner:** autonomous_research.py implementation

---

## Resolved Debt

_(Debt that has been addressed - kept for historical reference)_

**Example format:**
```
### DEBT-XXX: Description
**Resolved:** 2026-02-XX
**Resolution:** What was done to address it
**Lessons learned:** What we learned
```

---

## Debt Review Notes

### 2026-02-06: Initial Debt Register Created
- Created alongside knowledge-analyzer design
- 6 debt items documented upfront (strategic design)
- All debt is acceptable for v1 (ship fast, refine later)
- Triggers clearly defined for when to address each item

**Philosophy:** Ship with known debt, track it explicitly, address when triggered. Don't over-engineer before validating the design works.

### 2026-02-06: Autonomous Research Loop Debt Added
- Added DEBT-008 (sequential processing) and DEBT-009 (no context sharing)
- Both are implementation debt acceptable for v1
- Sequential processing chosen for safety and simplicity (18 gaps manageable)
- Cross-gap context sharing deferred until overlap becomes problematic
- Total debt items: 9 (2 strategic, 1 tactical, 6 implementation)
