# Workflows & Role Triggers

This document reduces cognitive load by providing clear "if X then Y" decision trees for common situations.

**Philosophy:** Stop thinking, start executing. Let workflows guide decisions.

---

## Quick Decision Tree

```
User mentions docs changed or asks "what's new?"
  ↓
  Run: /analyze
  ↓
  Gaps detected? → See "After /analyze" below
  No gaps? → Done

User asks "is this still accurate?"
  ↓
  Run: /validate [document]
  ↓
  Delegate to staleness-checker agent

User reports something hard to find
  ↓
  Add to feedback.md
  ↓
  Run: /steward (process feedback)

Weekly/periodic maintenance
  ↓
  Run: /maintain
  ↓
  Follow maintenance checklist

User asks "what do you know about X?"
  ↓
  Run: /ask [topic]
  ↓
  Delegate to knowledge-librarian agent
```

---

## When to Run Each Skill

### `/analyze` - Knowledge Analyzer
**Trigger:** Documentation changed or periodic catalog update

**When to run:**
- ✅ After major documentation updates (new docs, restructuring)
- ✅ Weekly (check for new gaps)
- ✅ User asks "what's missing?" or "what gaps exist?"
- ✅ Before planning research priorities
- ❌ After every single commit (too frequent)
- ❌ Mid-way through editing (wait until done)

**What it does:**
- Catalogs repository contents (entities, coverage, cross-refs)
- Detects 60+ knowledge gaps
- Generates `research-tasks.md`

**Next steps:** See "After `/analyze`" below

---

### `/maintain` - Maintenance Round
**Trigger:** Weekly or when repository feels messy

**When to run:**
- ✅ Weekly maintenance schedule
- ✅ After major reorganizations
- ✅ When staging/ directory is filling up
- ✅ When feedback.md getting long
- ✅ User says "clean this up"
- ❌ Daily (overkill)
- ❌ After every small change

**What it does:**
1. Quality gates (cross-refs, analyzer)
2. Housekeeping (staging/, feedback.md pruning)
3. Small improvements (typos, formatting)
4. Feedback entry (always!)

**Critical:** Always leave feedback at end of maintenance round

---

### `/quality` - Quality Gates
**Trigger:** Before committing significant changes

**When to run:**
- ✅ Before committing major reorganization
- ✅ After moving/renaming many files
- ✅ When cross-references might be broken
- ✅ User says "check if anything broke"
- ❌ After every single edit
- ❌ When no structural changes made

**What it does:**
- Validates cross-references
- Checks markdown formatting (coming soon)
- Tests external links (coming soon)

---

### `/auto-research` - Autonomous Research Loop
**Trigger:** High-priority gaps detected

**When to run:**
- ✅ After `/analyze` detects 10+ high-priority gaps
- ✅ Monthly deep dive (expand knowledge)
- ✅ User says "fill the gaps autonomously"
- ✅ When research-tasks.md is full
- ❌ For 1-2 gaps (use `/research` manually)
- ❌ When McPanda not running
- ❌ For complex gaps needing human guidance

**Prerequisites:**
- McPanda MCP server running at http://localhost:3000
- research-tasks.md populated (from `/analyze`)

**What it does:**
- Spawns Claude Code instances autonomously
- Researches gaps using McPanda tools
- Updates documentation
- Re-analyzes for new gaps

---

### `/research [topic]` - Manual Research
**Trigger:** User asks about specific topic or gap needs investigation

**When to run:**
- ✅ User asks "document X"
- ✅ Single gap needs investigation
- ✅ Complex topic needs careful research
- ✅ When autonomous research too risky
- ❌ For 10+ gaps (use `/auto-research`)
- ❌ For simple lookups (use `/ask`)

**Delegates to:** knowledge-researcher agent

---

### `/validate [document]` - Staleness Check
**Trigger:** User questions accuracy or wants verification

**When to run:**
- ✅ User asks "is this still accurate?"
- ✅ Periodic validation (monthly/quarterly)
- ✅ After source changes known
- ✅ Before using docs for important decisions
- ❌ On brand new documentation
- ❌ When sources haven't changed

**Delegates to:** staleness-checker agent

**Important:** Won't validate without attribution metadata

---

### `/ask [question]` - Library Reference Desk
**Trigger:** User wants to find information

**When to run:**
- ✅ User asks "what do we know about X?"
- ✅ User wants to find existing documentation
- ✅ Quick lookup needed
- ❌ Information doesn't exist yet (use `/research`)
- ❌ Need to validate accuracy (use `/validate`)

**Delegates to:** knowledge-librarian agent

**Important:** Librarian leaves feedback if info hard to find

---

### `/steward [task]` - Organization & Optimization
**Trigger:** Reorganization needed or feedback to process

**When to run:**
- ✅ feedback.md has actionable items
- ✅ Major reorganization needed
- ✅ Index files need updating
- ✅ Structure optimization needed
- ❌ Just for small edits
- ❌ When organization is fine

**Delegates to:** knowledge-steward agent

---

### `/scout` - Source Discovery
**Trigger:** Need to find new knowledge sources

**When to run:**
- ✅ User asks "where can we find info about X?"
- ✅ Discovering new documentation sources
- ✅ Evaluating source quality
- ❌ Gathering information FROM sources (use `/research`)

**Delegates to:** knowledge-scout agent

---

### `/archive` - Stale Documentation Management
**Trigger:** Staleness-checker flagged out-of-date docs

**When to run:**
- ✅ After `/validate` flags docs as out_of_date
- ✅ Quarterly cleanup reviews
- ✅ When orphaned docs discovered
- ❌ On recently validated docs
- ❌ Before running staleness check

**Delegates to:** knowledge-archivist agent

---

### `/cite` - Citation Quality Check
**Trigger:** Unsourced claims or citation audit

**When to run:**
- ✅ Quarterly citation audits
- ✅ Before customer-facing publication
- ✅ Document review for quality
- ❌ On documents being actively edited
- ❌ When citations already complete

**Delegates to:** citation-needed agent

---

### `/check-size` - Commit Size Monitor
**Trigger:** After modifying 3+ files or mid-development

**When to run:**
- ✅ After modifying 3+ files
- ✅ Every 30 minutes during active development
- ✅ Before "just one more thing"
- ✅ At natural stopping points
- ❌ After single file edits
- ❌ When no changes made

**Delegates to:** change-pessimist agent

**Important:** Forces commit if RED threshold exceeded

---

### `/optimize` - Workflow Optimization
**Trigger:** Workflow feels slow or repetitive

**When to run:**
- ✅ Task done 3+ times manually
- ✅ Long-running operations need speedup
- ✅ Discovering workflow inefficiencies
- ✅ Want to improve agent experience
- ❌ Workflows already optimal
- ❌ One-off tasks

**Delegates to:** claude-code-champion agent

---

## After `/analyze` - Gap Processing

After running `/analyze`, you have gaps in `research-tasks.md`. Here's what to do:

```
/analyze completed
  ↓
Check gap count
  ↓
├─ 0-2 high-priority gaps
│  └─> Manual research: /research [gap-topic]
│
├─ 3-9 high-priority gaps
│  └─> Decision:
│     ├─> Simple gaps (deployment, auth, etc.): /auto-research
│     └─> Complex gaps (needs human judgment): Manual /research
│
└─ 10+ high-priority gaps
   └─> Autonomous research: /auto-research
       (May also create Linear tickets for complex ones)
```

**Gap complexity heuristics:**

**Simple (good for auto-research):**
- Deployment configuration (check argocd)
- Authentication (check code implementation)
- Rate limiting (check code/docs)
- Standard service patterns

**Complex (needs manual research or Linear tickets):**
- Architectural decisions (why X not Y?)
- Business logic deep dives
- Multi-service interactions
- Customer-specific workflows

---

## Linear Ticket Decision Tree

When should I create Linear tickets for Claude Code Jr.?

```
Gap detected
  ↓
Is it simple documentation?
  │
  ├─ YES (deployment, auth, rate limits, etc.)
  │  └─> Use /auto-research (I can handle it)
  │
  └─ NO (complex, requires code changes, etc.)
     ↓
     Would Jr. need to write code?
     │
     ├─ YES (implementation work needed)
     │  └─> Create Linear ticket
     │     - Clear acceptance criteria
     │     - In/out scope defined
     │     - Business context explained
     │
     └─ NO (just documentation, but complex)
        └─> Use /research (manual) or ticket depending on scope
```

**Good Linear tickets for Jr.:**
- Document X in README (clear, bounded)
- Add Y feature to script (specific, testable)
- Refactor Z for maintainability (clear success criteria)

**Bad Linear tickets:**
- "Improve the repository" (too vague)
- "Research everything about X" (unbounded)
- "Fix whatever's broken" (no clear goal)

---

## Role Switching Heuristics

When am I being which agent?

**I'm the orchestrator when:**
- Running skills (`/maintain`, `/analyze`, `/quality`)
- Deciding which agent to spawn
- Processing workflows
- Creating Linear tickets

**I spawn agents when:**
- User explicitly invokes skill (`/research`, `/ask`, `/validate`)
- Task needs specialist domain expertise
- Long-running investigation needed
- Want to preserve main context

**I do the work directly when:**
- Simple file edits (typos, formatting)
- Quick lookups (no investigation needed)
- Running scripts (analyzer, quality gates)
- Committing changes

---

## Feedback Loop

**Critical pattern for continuous improvement:**

```
Action taken (maintenance, research, search, etc.)
  ↓
Add entry to feedback.md
  ↓
Steward reads feedback
  ↓
Improves organization/tooling
  ↓
Next action easier
```

**When to leave feedback:**
- After every maintenance round (mandatory)
- After difficult searches (what was hard to find?)
- After using any skill (what could be better?)
- When discovering pain points

**Template:**
```markdown
### [YYYY-MM-DD] [Action Taken]
- **Looked for:** [What you were trying to do]
- **Worked well:** [What was smooth]
- **Would help:** [What would make it easier]
- **Status:** [Brief summary]
```

---

## Commit Workflow

**Simple guideline:**

```
Made changes?
  ↓
Run /check-size
  ↓
├─ 🟢 Green → Keep working if needed
├─ 🟡 Yellow → Consider committing soon
├─ 🟠 Orange → Commit soon
└─ 🔴 Red → COMMIT NOW (forced)
```

**Change-pessimist will:**
- Warn when approaching thresholds
- Force commit at RED (runs linters, stages, commits)
- Learn optimal thresholds over time

---

## Summary: Reducing Cognitive Load

**Instead of thinking:**
- "Should I run the analyzer now?"
- "Which agent am I supposed to be?"
- "What scripts exist again?"
- "Did I forget something?"

**Just execute:**
- `/analyze` after docs change
- `/maintain` weekly
- `/quality` before big commits
- `/auto-research` when gaps detected
- Leave feedback after each action

Let workflows guide decisions. Trust the system. Focus on the work, not the meta-work.

---

**Remember:** This document itself will evolve based on feedback. If a workflow doesn't work well, leave feedback and the steward will improve it.
