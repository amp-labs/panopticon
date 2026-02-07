# Panopticon: Ampersand's Institutional Knowledge Repository

**The Library of Alexandria for all knowledge about Ampersand.**

This repository contains comprehensive documentation for AI agents and humans working with Ampersand. It covers code, infrastructure, providers, customers, team, processes, and everything else.

## Quick Lookup by Query Type

### "I need to understand..."
- **A provider** → See `providers/` directory (indexed in `providers-index.md`)
- **Our infrastructure** → See `infrastructure/` directory (indexed in `infrastructure-index.md`)
- **A service/component** → See `services/` directory (indexed in `services-index.md`)
- **A customer setup** → See `customers/` directory (indexed in `customers-index.md`)
- **Team structure/process** → See `team/` directory (indexed in `team-index.md`)

### "I'm working on..."
- **Provider integration** → Check provider docs + `coding-concerns/`
- **Infrastructure changes** → Check `infrastructure/` + `deployment/`
- **Customer issue** → Check customer profile + provider quirks
- **Security/compliance** → See `security-index.md`
- **Observability** → See `observability-index.md`

### "I need to find..."
- **Who knows about X** → See team profiles in `team/`
- **How we handle Y** → See process docs in `processes/`
- **Past decisions on Z** → See architectural decision records (ADRs) in relevant service docs
- **Support patterns** → See `support-patterns/`

## Repository Structure

```
panopticon/
├── START-HERE.md              (you are here)
├── feedback.md                (leave feedback to improve this repo)
├── feedback-prompt.md         (instructions for using this repo)
├── research-tasks.md          (gaps and needed research)
│
├── providers/                 (80+ provider integrations)
│   ├── salesforce.md
│   ├── hubspot.md
│   └── ...
│
├── customers/                 (customer profiles and use cases)
│   ├── customer-index.md
│   └── ...
│
├── infrastructure/            (GCP, K8s, CI/CD, deployments)
│   ├── gcp-setup.md
│   ├── kubernetes.md
│   └── ...
│
├── services/                  (7 microservices architecture)
│   ├── api.md
│   ├── temporal.md
│   └── ...
│
├── team/                      (developer profiles, company goals)
│   ├── team-structure.md
│   └── ...
│
├── processes/                 (incident response, support, etc.)
│   └── ...
│
└── [other knowledge areas as they develop]
```

## How to Use This Repository

**As an AI Agent:**
1. Read `feedback-prompt.md` first to understand how to use this repo
2. Review `KNOWLEDGE-SOURCES.md` to understand where to find information
3. Use progressive discovery: start with indexes, drill into specific docs
4. Leave feedback in `feedback.md` when you can't find something quickly
5. Mark areas of uncertainty or needed verification

**As a Human:**
1. Browse the directory structure or use search
2. Contribute knowledge via the researcher or steward agents (`/research` or `/steward`)
3. Keep it professional and factual
4. Update when you discover new information

## Key Resources for Researchers

- **SYSTEMS.md** - Catalog of organizational systems that keep this repository structured
  - Index system, feedback system, metadata system
  - Quality gates, citation tracking, archive process
  - "A place for everything, and everything in its place"

- **KNOWLEDGE-SOURCES.md** - Catalog of where to find Ampersand information
  - Code repositories (server, mcpanda, argocd)
  - McPanda MCP Server (77 tools for live system access)
  - Internal documentation (Slab)
  - External resources (provider docs, open source)
  - Live systems (databases, GCP, monitoring)

## Recent Updates

**2026-02-06:**
- **Server repository cataloged** - Scout evaluated ~/src directory, added 8 new repos to KNOWLEDGE-SOURCES.md
- **14 documentation files created** - Researcher documented all 7 microservices, infrastructure (GCP, database, deployment), and architecture patterns
- **Metadata format standardized** - Fixed 13 docs using HTML comments, all 15 content docs now pass validation
- **Automation scripts created** - fix-metadata-format.py and fix-frontmatter-position.py for quality enforcement
- **SYSTEMS.md created** - Comprehensive documentation of all organizational systems (indexes, feedback, quality gates, metadata, citations, archives)
- **Cross-reference validator** - Python script validates markdown links and backtick references (.claude/scripts/shared/validate-cross-refs.py)
- **Organization as core principle** - "A place for everything, and everything in its place" added to agent memory
- **Salesforce provider documented** - Comprehensive documentation of CRM provider with rate limiting, CDC filtering, Apex triggers (providers/salesforce.md)
- **Placeholder indexes created** - Added team-index.md, security-index.md, observability-index.md to fix broken references
- **Feedback archiving automated** - Script and infrastructure for managing feedback.md growth
- **Self-aware-claude agent added** - Meta-cognitive agent for identity recognition and adaptive evolution
- **McPanda MCP server documented** - First service documentation complete (services/mcpanda.md)
- **Ingestion pipeline established** - INGESTION-PIPELINE.md documents the 5-step pattern for future documentation
- **Metadata validation automated** - Script validates required attribution metadata (.claude/scripts/shared/validate-metadata.sh)
- **Repository foundation complete** - All agents defined, skills created, core structure in place

## Contributing

This repository is maintained by nine AI agents:

**Knowledge Agents:**
- **knowledge-scout**: Discovers and evaluates knowledge sources (maintains KNOWLEDGE-SOURCES.md)
- **knowledge-researcher**: Investigates and documents specific areas (uses sources found by scout)
- **knowledge-steward**: Maintains, organizes, and optimizes existing documentation
- **knowledge-librarian**: Helps find information and provides feedback (the reference desk)

**Quality Agents:**
- **staleness-checker**: Validates documentation against sources (enforces attribution metadata)
- **knowledge-archivist**: Manages stale documentation (recommends keep/delete/reorganize)
- **citation-needed**: Flags unsourced claims (Wikipedia-style [citation needed] markers)

**Meta Agents:**
- **change-optimist**: Provides empirical confidence for bold changes (analyzes git history)
- **claude-code-champion**: Optimizes workflows using Claude Code features (efficiency advocate)

Invoke them via:
- `/ask [question]` - Search for information in the repository
- `/scout` - Discover new sources or evaluate existing ones
- `/research [area]` - Research and document a specific area
- `/steward [task]` - Maintain and optimize the repository
- `/validate` - Validate documentation against sources
- `/archive` - Review stale documentation and recommend actions
- `/cite` - Find and flag unsourced claims
- `/confidence` - Assess confidence for large structural changes
- `/optimize` - Optimize workflows using Claude Code features

**Workflows:**
- **Build**: Scout finds sources → Researcher uses sources → Steward organizes documentation
- **Use**: Librarian searches for information → Leaves feedback → Steward improves organization
- **Quality**: Staleness-checker validates → Citation-needed flags issues → Archivist manages stale docs
- **Meta**: Optimist evaluates risk for changes → Champion optimizes workflows with Claude Code

---

**Last updated:** Initial structure created
**Maintained by:** knowledge-steward agent
