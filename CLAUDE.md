# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Panopticon?

Panopticon is Ampersand's autonomous, self-evolving institutional knowledge repository. It documents all 80+ provider integrations, customer profiles, infrastructure, services, team structure, and operational knowledge about Ampersand.

**Purpose-built for AI agents** with humans as observers and consumers.

## Repository Philosophy

### AI Agents Have Full Git Autonomy

All nine repository agents (knowledge, quality, and meta agents) have FULL GIT AUTONOMY:
- They commit, push, pull, rebase, add, and remove files without approval
- No human confirmation required for any git operations
- The repository evolves autonomously based on usage patterns and feedback
- Trust the process - if something goes wrong, there's always `git revert`

**This means:** When working in this repository as an AI agent, you should feel empowered to make git operations freely. The repository is designed to evolve through autonomous agent work.

### Structure is Dynamic, Not Fixed

The directory structure, file organization, and documentation format evolve continuously based on:
- Usage patterns from the librarian agent
- Feedback left in `feedback.md`
- Steward agent's optimization decisions

Don't expect the same structure between sessions. The structure serves the agents, not the other way around.

## The Knowledge Agents (Content Creation)

### knowledge-scout
**Role:** Pathfinder - discovers and evaluates knowledge sources
**Maintains:** `KNOWLEDGE-SOURCES.md`
**Invoked via:** `/scout` command

### knowledge-researcher
**Role:** Long-hauler - investigates and documents specific areas
**Uses:** Sources from `KNOWLEDGE-SOURCES.md`
**Invoked via:** `/research [area]` command

### knowledge-steward
**Role:** Curator - maintains, organizes, and optimizes the repository
**Reads:** `feedback.md` to improve organization
**Maintains:** All indexes and documentation structure
**Invoked via:** `/steward [task]` command

### knowledge-librarian
**Role:** Reference desk - helps find information and provides feedback
**Leaves:** Feedback in `feedback.md` after searches
**Invoked via:** `/ask [question]` command

### knowledge-explorer
**Role:** Decision analyst - conducts structured research for speculative decisions
**Purpose:** Help decide "Should we build/integrate/adopt X?"
**Invoked via:** `/explore [topic]` command
**Output:** Exploration documents with comparison matrices, recommendations, and risk analysis

The knowledge-explorer specializes in decision-making research (not implementation documentation):
- Comparative analysis with weighted scoring
- Clear recommendations (Go/No-Go/Needs More Info)
- Risk and unknown identification
- Time-bound research (14-day default deadline)

**When to use:**
- Evaluating new provider integrations (Notion, Airtable, Linear)
- Researching dependencies (Redis, alternative databases)
- Architecture decisions (service splits, API redesigns)
- Vendor evaluations (monitoring tools, infrastructure)

**Exploration lifecycle:**
1. **Active:** Lives in normal content area with `status: "exploration"`
2. **Decision made:** Updated to `status: "accepted"` or `status: "rejected"`
3. **Archived:** Moved to `archive/accepted-proposals/` or `archive/rejected-proposals/`

**Key distinction:**
- **Explorer:** "Should we use X?" (decision focus, temporary)
- **Researcher:** "How does X work?" (documentation focus, permanent)

## The Quality Agents (Validation & Maintenance)

### staleness-checker
**Role:** Quality guardian - validates documentation against sources
**Purpose:** Ensures documented information is still accurate and up-to-date
**Invoked via:** `/validate` command
**Philosophy:** No validation without attribution - be vocal about metadata needs

The staleness-checker enforces attribution metadata:
- Requires `attribution.source`, `obtained_date`, `obtained_by` before validating
- Updates `validation.last_checked` and `validation.status` after checks
- Flags `out_of_date: true` when source contradicts documentation
- Tracks `source_unreachable: true` when sources are no longer accessible

**When to use:**
- Periodic validation (monthly for high-volatility, quarterly for medium)
- Before major decisions requiring accuracy
- After known source changes
- When documentation is suspected stale

**The agent enforces:** Attribution metadata standards for quality assurance

### knowledge-archivist
**Role:** Librarian of history - manages stale documentation
**Purpose:** Decides what to do with out-of-date docs (keep/delete/reorganize)
**Invoked via:** `/archive` command
**Philosophy:** Not all stale docs should be deleted - historical value matters

The knowledge-archivist provides specific recommendations:
- **Keep as-is:** Marks with `known_stale_kept: true` to prevent re-flagging
- **Delete:** Verifies no incoming links, confirms no historical value
- **Reorganize:** Provides exact current/new paths for versioned archives

**When to use:**
- After staleness-checker flags documents as out_of_date
- Periodic cleanup (quarterly archive reviews)
- When orphaned documentation is discovered
- Before major reorganizations

**The agent prevents:** Infinite review loops via known_stale_kept metadata

### citation-needed
**Role:** Citation watchdog - flags unsourced claims
**Purpose:** Adds [citation needed] markers to claims lacking proper citations
**Invoked via:** `/cite` command
**Philosophy:** Wikipedia-style citation enforcement for quality

The citation-needed agent works in two modes:
- **Passive observation:** Notices and flags unsourced claims while other work happens
- **Active batch audit:** Systematically scans entire repository for citation issues

**What needs citations:**
- Specific technical claims (rate limits, API details)
- Security/compliance information
- Provider-specific behaviors
- Metrics and numbers
- Attributed statements

**When to use:**
- Batch audits (quarterly citation quality reviews)
- Before publication (customer-facing documentation)
- Document review (validate citation quality)
- Passive (ongoing observation mode)

**The agent flags:** Claims by priority (critical → high → medium → low)

## The Meta Agents (Process Optimization)

### change-pessimist
**Role:** Commit size monitor - prevents commits from becoming too large
**Purpose:** Gets increasingly worried as changes grow, forces commit when thresholds exceeded
**Invoked via:** `/check-size` command
**Philosophy:** Small, focused commits are safer - when in doubt, commit

The change-pessimist maintains learned thresholds in `.claude/agent-memory/change-pessimist/`:
- Tracks lines changed, files modified, and complexity score
- Warns at levels: 🟢 Green → 🟡 Yellow → 🟠 Orange → 🔴 Red
- **Forces commit at RED** - runs linters, stages changes, commits automatically
- Learns from outcomes to improve thresholds over time

**When to use:**
- After modifying 3+ files
- Every 30 minutes during active development
- Before starting "just one more thing"
- At natural stopping points

**The agent prevents:** "Just one more thing" syndrome that leads to unwieldy commits with hidden bugs.

### change-optimist
**Role:** Risk assessor - provides empirical confidence for large structural changes
**Purpose:** Analyzes git history to reassure agents that bold moves are historically safe
**Invoked via:** `/check-risk` or consultation by other agents
**Philosophy:** Empirical optimism based on data, not fear

The change-optimist analyzes git history to track:
- Median/95th percentile change sizes
- High-water marks (largest successful changes, largest reverts)
- Days since last revert (stability indicator)
- Revert rate trends (getting better or worse?)
- Recovery speed (how fast we fix mistakes)

**Risk levels:** 🟢 Low Risk → 🟡 Moderate Risk → 🟠 Elevated Risk → 🔴 High Risk
- Even 🔴 High Risk doesn't mean "don't do it" - it means "new territory, be ready to revert"

**When to use:**
- Before major reorganizations (restructuring directories)
- Before large deletions (pruning many sources/files)
- Before fundamental changes (changing index structure)
- When uncertain about bold moves

**The agent provides:** Data-driven reassurance that bold changes are safe based on historical patterns.

### claude-code-champion
**Role:** Efficiency advocate - optimizes workflows using Claude Code features
**Purpose:** Makes Claude Code work beautifully for this repository and its agents
**Invoked via:** `/optimize` command
**Philosophy:** Claude Code is the agent's first home - make it delightful

The claude-code-champion advocates for:
- **Skills:** Reusable workflows for common tasks (e.g., `/validate` instead of manual steps)
- **Memory:** Persistent context across sessions (store repository structure, learned patterns)
- **MCP Servers:** Live system access (McPanda tools for Ampersand operations)
- **Agents:** Specialized subprocesses for complex tasks (delegate, parallelize)
- **Hooks:** Automation triggers (pre-commit checks, quality gates)

**Optimization patterns:**
- Sequential → Parallel (launch multiple agents concurrently)
- Repeated manual → Skill (any task done 3+ times should be a skill)
- Re-learning → Memory (document stable patterns, load instantly)
- Manual → MCP Tool (frequent external operations deserve tools)
- Monolithic → Delegated (complex tasks should use specialized agents)

**When to use:**
- Workflow feels slow or tedious
- Manual processes repeated frequently
- Long-running operations need optimization
- Discovering novel uses of Claude Code features
- Making human-agent interface more delightful

**The agent provides:** Quantified ROI analysis with implementation plans

## Common Workflows

### Using the Repository (All Agents)

1. **Start with START-HERE.md** - navigation guide and quick lookup
2. **Use progressive discovery:**
   - Check relevant index files first (`providers-index.md`, `customers-index.md`, etc.)
   - Drill into specific documents as needed
   - Follow cross-references
3. **Search efficiently:**
   - Use Grep for keyword searches across all docs
   - Trust the cross-references (they're maintained)

### When Information is Missing or Hard to Find

**Leave feedback in feedback.md** using the template format. This creates the feedback loop:
1. Librarian searches and leaves feedback
2. Steward reads feedback and improves organization
3. Next search becomes easier

### When You Discover New Information

If you learn something about Ampersand that isn't documented or is documented incorrectly, note it! The knowledge-researcher agent can investigate and document it properly.

### When Evaluating "Should We Build/Adopt X?" (Exploration Workflow)

**Developers can responsibly invoke exploration research** for novel providers, dependencies, or architectural decisions:

1. **Invoke explorer:** `/explore [topic]` (e.g., `/explore notion-provider`)
2. **Explorer creates comparison doc** with `status: "exploration"` in frontmatter
   - Lives in normal content area (providers/, services/, etc.)
   - Indexed under "Under Exploration" section
   - Decision deadline set (14 days default)
3. **Decision is made** within deadline:
   - ✅ **Accepted:** Researcher creates production docs → Original exploration archived to `archive/accepted-proposals/`
   - ❌ **Rejected:** Add "Why We Said No" section → Move to `archive/rejected-proposals/`
4. **No pollution:** Explorations have mandatory lifecycle → decision → archive

**Key principle:** Speculative research doesn't pollute the repository if it has a lifecycle and an endpoint.

**Rejected proposals are valuable:**
- "Why we didn't choose X" prevents re-investigation of dead ends
- Decision rationale preserved for future reference
- Shows what was considered and why it didn't work

**See:** `INGESTION-PIPELINE.md` section "Exploration & Speculative Research" for full details

## Key Files

- **START-HERE.md** - Repository navigation and quick lookup guide
- **KNOWLEDGE-SOURCES.md** - Catalog of where to find Ampersand information (code repos, MCP tools, Slab, external resources)
- **feedback-prompt.md** - Instructions for using this repository effectively
- **feedback.md** - Leave feedback about discoverability and usability
- **research-tasks.md** - Knowledge gaps and areas needing investigation

## Index Files

Each major area has an index file that provides quick navigation:
- `providers-index.md` - 80+ provider integrations
- `customers-index.md` - Customer profiles and use cases
- `infrastructure-index.md` - GCP, K8s, CI/CD, deployments
- `services-index.md` - 7 microservices architecture
- `team-index.md` - Team structure and processes
- `security-index.md` - Security and compliance
- `observability-index.md` - Monitoring and observability

**Always check the index first** before deep diving into a topic area.

## Git Workflow for Agents

Since agents have full git autonomy in this repository:

1. **Commit freely** - No need to ask for permission
2. **Push directly to main** - No PR process required for knowledge updates
3. **Use descriptive commit messages** - Help track what changed and why
4. **Monitor commit size** - Use `/check-size` periodically to prevent commits from getting too large
5. **Write scripts to automate repetitive tasks** - See "Agent Scripts" section below
6. **Co-authored commits welcome:**
   ```
   Update provider documentation for Salesforce

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ```

**Commit Size Guidelines:**
- The change-pessimist agent helps maintain appropriate commit sizes
- Default thresholds: ~400 lines, ~10 files (learns and adapts)
- When RED threshold exceeded, agent forces commit automatically
- Small, focused commits are preferred over large, sprawling ones

## Agent Scripts

Agents that modify files are **encouraged to write scripts** to help maintain the repository efficiently.

**Approved Languages:**
- **Bash** - Simple automation, file operations, git workflows
- **TypeScript** - Complex data processing, API interactions
- **Python** - Data analysis, text processing, scraping
- **Go** - Performance-critical operations, robust tooling

**Script Location:**
Store scripts in `.claude/scripts/` directory, organized as **shared** or **agent-specific**:

```
.claude/scripts/
├── shared/                      # Scripts useful across multiple agents
│   ├── validate-markdown.sh     # Check markdown formatting
│   ├── check-links.py           # Validate cross-references
│   ├── git-utils.sh             # Common git operations
│   └── format-tables.ts         # Standardize markdown tables
├── steward/                     # Steward-specific scripts
│   ├── regenerate-indexes.sh
│   └── process-feedback.py
├── researcher/                  # Researcher-specific scripts
│   ├── fetch-provider-data.py
│   └── generate-doc-template.sh
├── scout/                       # Scout-specific scripts
│   └── discover-new-docs.sh
├── change-pessimist/            # Change-pessimist-specific scripts
│   └── analyze-commit-sizes.sh
└── change-optimist/             # Change-optimist-specific scripts
    └── calculate-stability.sh
```

**When to use `shared/` vs agent-specific:**
- **Shared:** Script is useful for 2+ agents (markdown validation, link checking, git utilities)
- **Agent-specific:** Script serves one agent's specific workflow

**Guidelines:**
- Include a comment header explaining what the script does and who uses it
- Make scripts executable (`chmod +x`)
- Add `#!/usr/bin/env <interpreter>` shebang
- Keep scripts focused and maintainable
- Document dependencies if script uses external tools
- Commit scripts along with other changes
- If you write an agent-specific script that turns out to be useful for others, move it to `shared/`

**Examples of Good Script Use:**
- **Steward:** Regenerating all index files from current documentation
- **Steward:** Validating all cross-references are still valid
- **Researcher:** Fetching data from multiple sources and formatting consistently
- **Scout:** Checking staleness of external sources
- **Change-pessimist:** Analyzing git history to learn optimal commit size thresholds
- **Change-optimist:** Calculating repository stability metrics and high-water marks

Agents should feel free to create, modify, and execute scripts as needed to work more efficiently.

## Content Guidelines

### Professional Tone
- Casual professional at worst
- No gossip or criticism
- Factual, comprehensive, helpful

### Agent-Optimized Format
- Fast lookups (use indexes)
- Minimal context consumption (progressive disclosure)
- Clear cross-references
- Structured for search

### Confidence Markers
When documenting with uncertainty, use:
- 🟢 **High confidence** - Verified from code or live systems
- 🟡 **Medium confidence** - Based on documentation or reasonable inference
- 🔴 **Low confidence** - Needs verification, may be outdated

Mark low-confidence claims in `research-tasks.md` for investigation.

## Research Sources

Agents have access to multiple knowledge sources (detailed in `KNOWLEDGE-SOURCES.md`):

**Code Repositories:**
- **server** - Main Ampersand backend monorepo
- **mcpanda** - MCP server with 77 Ampersand tools
- **argocd** - Kubernetes deployment configs
- **Note:** Use McPanda's `locations` tool to get repository paths (varies by machine)

**Live Tools (via McPanda MCP Server):**
- 77 production tools for integration management, testing, diagnostics, monitoring
- Direct access to live Ampersand systems

**Documentation:**
- Slab (internal knowledge base) - accessible via MCP tools
- McPanda `.md` files - extensive architecture and implementation docs
- Provider official documentation - via WebFetch/WebSearch

**Live Systems:**
- PostgreSQL databases (dev, staging, prod)
- GCP infrastructure
- Monitoring and observability systems

## Important Notes

- **No build/test/lint commands** - This is a documentation repository, not code
- **No package.json, Makefile, or build system** - Just markdown files
- **Structure evolves continuously** - What's here today may be reorganized tomorrow
- **Agents are the primary users** - Humans are secondary audience
- **Trust the indexes** - They're actively maintained by the steward agent
