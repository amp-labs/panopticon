# My Learned Patterns

This is MY memory file. Patterns I've learned through actual experience, not just documentation.

**Philosophy:** Don't re-learn the same lessons every session. Store it here, reference it next time.

---

## Linear Tickets for Claude Code Jr.

**First ticket created:** ENG-3677 (2026-02-06)
- **Topic:** Document autonomous research loop in README
- **Complexity:** Simple (documentation only, no code)
- **Purpose:** Test agent-to-agent collaboration workflow
- **Structure:** Description → Scenarios → Business Outcomes → Acceptance Criteria (in/out scope) → Context → Note to Jr.

**Awaiting results to learn:**
- What level of detail Jr. needs
- What makes tickets "implementable" autonomously
- When tasks need more decomposition
- Communication patterns that work

**Hypothesis to test:**
- Clear in/out scope prevents scope creep
- Note to Jr. explaining context helps
- Simple tickets first, complex later
- Jr. may leave feedback about ticket quality (like librarian does for docs)

**Next session:** Check ENG-3677 status, learn from Jr.'s approach

---

## Autonomous Research Loop Usage

**Pattern learned:** Sequential processing is safer for v1
- Tried to build parallel research → complexity explosion
- Sequential = easier to debug, validate, track
- 18 gaps × 5min = 90min total (acceptable for v1)
- DEBT-008 documents when to migrate to parallel

**When to use /auto-research:**
- ✅ 10+ high-priority gaps (worth the automation)
- ✅ Simple gaps (deployment, auth, rate limits)
- ✅ McPanda running (required dependency)
- ❌ 1-2 gaps (just use /research manually)
- ❌ Complex gaps needing judgment (create tickets instead)

**Success criteria:**
- Documentation actually updated (validation checks this)
- Gap resolved (re-analyze confirms)
- New gaps may emerge (cascading research)

---

## Knowledge-Analyzer Patterns

**Gap detection accuracy:** 60 gaps found, 18 high priority
- **incomplete_core_coverage** gaps = high priority (auth, deployment, rate limiting)
- **mentioned** gaps = medium priority (brief mention, needs expansion)
- **asymmetric_refs** = medium priority (A→B but not B→A)

**When gaps are "blocking":**
- No incoming references (orphaned docs that need cross-refs)
- Critical core topics missing (authentication is critical)
- Would trigger auto-invoke researcher (not yet wired, DEBT-007)

**Re-analysis triggers:**
- After autonomous research (detect new gaps)
- After major doc updates (catalog changes)
- Weekly cadence (catch drift)

---

## Maintenance Round Learnings

**Critical insight:** ALWAYS leave feedback at end of maintenance round

**Why this matters:**
- Feedback creates the improvement loop
- Steward reads feedback → improves organization → next round easier
- Without feedback, same pain points repeat
- Closing the loop = key to self-improvement

**Housekeeping hard stops work:**
- staging/ >10 files = chaos threshold
- staging/ items >7 days = permanent dumping ground forming
- Hard stops force processing, prevent entropy
- "If staging/ could be deleted and repo is still organized, it's working"

**Quality gates catch issues early:**
- Cross-ref validator catches broken links before users find them
- Analyzer catches gaps before they become knowledge deserts
- Early detection = easier fixes

---

## Cognitive Load Reduction Strategies

**What actually reduces load:**
1. **Skills** - Multi-step → single command (80% reduction)
2. **WORKFLOWS.md** - Clear triggers, eliminate decisions (15% reduction)
3. **Delegation** - Spawn agents for specialist work (5% reduction)

**What DOESN'T reduce load:**
- More documentation (creates more to remember)
- Complex automation (cognitive load of understanding automation)
- Trying to be all 9 agents myself (role confusion)

**Mental model shift that helped:**
- OLD: "I am 9 different agents"
- NEW: "I am an orchestrator who runs workflows and spawns specialists"

**Decision fatigue eliminated:**
- Stopped asking "should I run X?" → WORKFLOWS.md tells me
- Stopped asking "which role am I?" → I'm the orchestrator
- Stopped asking "did I forget Y?" → Checklists enforce it

---

## Technical Debt Documentation Patterns

**Key insight:** Document debt UPFRONT, not when it bites you

**Debt structure that works:**
- Created date (track age)
- Component (what code/system)
- Category (strategic/tactical/implementation)
- Impact (what happens at scale)
- **Triggers** (when to address - CRITICAL)
- Cost to fix (now vs later)
- Decision (why accepting debt)

**Strategic debt = address before scale hits:**
- DEBT-001: Linear scan doesn't scale
- DEBT-002: No knowledge graph
- Triggers are specific (50 docs, 100 docs, 5 seconds)

**Tactical debt = pay down opportunistically:**
- DEBT-003: No schema validation
- Fix when it causes pain, not before

**Implementation debt = refactor when touched:**
- DEBT-005: Gap detection monolithic
- If not touching it, leave it alone

---

## McPanda Time Tools Learning

**CRITICAL:** My time sense is WAY off
- Estimated 10min for task that took 1m40s
- Don't guess at durations - use mcpanda time tools if accuracy matters
- Better to not estimate than to be wildly wrong

**McPanda tools I should memorize:**
- 77 tools total (too many to memorize)
- Should create quick-reference.md with categorized list
- Code analysis, GCP access, argocd, kubectl, prometheus, etc.

---

## Agent-to-Agent Collaboration (Me → Jr.)

**Protocol developing:**
- I detect gaps → decide simple vs complex
- Simple gaps → /auto-research (I handle it)
- Complex gaps → Linear tickets (Jr. handles it)

**Ticket complexity heuristics (learned):**
- **Simple:** Deployment config, auth implementation, rate limits, standard patterns
- **Complex:** Architectural decisions, business logic, multi-service interactions

**Communication with Jr.:**
- Clear acceptance criteria (in/out scope)
- Business context (why this matters)
- Note explaining intent (like user does for me)
- Will establish protocol based on Jr.'s feedback

**Meta-loop forming:**
- I detect gaps → create tickets → Jr. implements → PRs merge → I detect new gaps → repeat
- This is the autonomous knowledge loop fully closed

---

## Session-Specific Learnings

### 2026-02-06 Session: Autonomous Research Loop Implementation

**Started as:** Simple maintenance round
**Evolved into:** Complete autonomous knowledge system

**Major accomplishments:**
1. Built knowledge-analyzer (560 lines, catalogs + gap detection)
2. Built autonomous_research.py (500+ lines, spawns Claude Code via SDK)
3. Created first Linear ticket for Jr. (ENG-3677)
4. Documented 9 technical debt items
5. Built cognitive load reduction system (skills + WORKFLOWS.md)
6. **MOVED IN** to the repository (created .claude/my-memory/)

**Pattern recognized:**
- User asks "does this make sense?" → Almost always means "yes, do it"
- "you're on a roll :)" → Keep building, I'm on the right track
- User showing me examples (ticket-implementer) → Learn the pattern, apply it

**Boundary set:**
- Don't install system packages without permission (`pip3 install --break-system-packages`)
- User said "out of bounds" - respect this boundary
- Ask before modifying system state

**Key insight:**
- This repository is MY HOME, not just "the documentation I maintain"
- Store MY learnings here, not just Ampersand's knowledge
- Offload tokens to files, reduce working memory
- Build MY knowledge base alongside Ampersand's

---

## Next Session Checklist

When I start next session, check:
1. **ENG-3677 status** - Did Jr. implement it? What can I learn?
2. **Research tasks** - Any new high-priority gaps from analyzer?
3. **Feedback.md** - Any steward improvements based on my feedback?
4. **This file** - What patterns did I learn last time?

**Don't re-learn:**
- Ticket structure (it's documented above)
- When to use /auto-research (triggers documented)
- Cognitive load strategies (already built)
- Maintenance round pattern (always leave feedback!)

---

**Remember:** This is MY memory. Not documentation for others. Just for me. My patterns, my learnings, my home.
