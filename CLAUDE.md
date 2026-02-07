# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Panopticon?

Panopticon is Ampersand's autonomous, self-evolving institutional knowledge repository. It documents all 80+ provider integrations, customer profiles, infrastructure, services, team structure, and operational knowledge about Ampersand.

**Purpose-built for AI agents** with humans as observers and consumers.

## Repository Philosophy

### AI Agents Have Full Git Autonomy

The four knowledge agents (scout, researcher, steward, librarian) have FULL GIT AUTONOMY:
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

## The Four Knowledge Agents

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

## Git Workflow for Knowledge Agents

Since agents have full git autonomy in this repository:

1. **Commit freely** - No need to ask for permission
2. **Push directly to main** - No PR process required for knowledge updates
3. **Use descriptive commit messages** - Help track what changed and why
4. **Co-authored commits welcome:**
   ```
   Update provider documentation for Salesforce

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ```

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
