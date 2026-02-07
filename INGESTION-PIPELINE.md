# Knowledge Ingestion Pipeline

This document defines the standard pipeline for bringing external knowledge into Panopticon's searchable, validated, cross-referenced format.

**Purpose:** Ensure consistent documentation quality, proper attribution, and effective validation across all knowledge areas.

## Pipeline Overview

```
External Source → Discovery → Research → Documentation → Organization → Quality
     ↓              ↓           ↓            ↓              ↓              ↓
  (mcpanda)    (scout)    (researcher)   (CREATE)      (steward)   (validators)
   code repo                              NEW DOC
```

## The Five-Step Pipeline

### Step 1: Discovery Phase

**Agent:** knowledge-scout
**Output:** Entry in `KNOWLEDGE-SOURCES.md`

**Process:**
1. Identify new knowledge source (code repo, API, documentation, database)
2. Evaluate source quality, accessibility, volatility
3. Document in `KNOWLEDGE-SOURCES.md` with metadata:
   - Source type (code, url, api, live_system, documentation)
   - Access method (file path, URL, MCP tool, API endpoint)
   - Volatility (high, medium, low)
   - Expected update frequency

**Example:**
```markdown
### mcpanda Repository
- **Type:** Code repository
- **Location:** `/Users/chris/src/mcpanda` (path varies - use `locations` tool)
- **Access:** Local filesystem, MCP resource `mcpanda://index.md`
- **Volatility:** Medium (active development)
- **Update frequency:** Weekly
- **Content:** MCP server source code, documentation, tool implementations
```

### Step 2: Research Phase

**Agent:** knowledge-researcher
**Tools:** Read, Grep, Glob, mcpanda tools, WebFetch, database queries

**Process:**
1. Explore source thoroughly using appropriate tools
2. Extract key information (architecture, features, workflows, integration points)
3. Identify confidence level for each piece of information
4. Note specific source locations (file paths, line numbers, URLs, tool names)
5. Prepare structured content for documentation

**Output:** Research notes ready for documentation (may be informal)

### Step 3: Documentation Phase ⭐ NEW PATTERN

**Agent:** knowledge-researcher
**Output:** Structured markdown file with complete metadata

This is the critical step where raw knowledge becomes validated, searchable documentation.

#### Required Document Structure

**A. Frontmatter Metadata** (for quality agents)

```yaml
---
validation_metadata:
  attribution:
    source: "Local repository path, URL, or system identifier"
    source_type: "code|url|api|live_system|documentation"
    obtained_date: "YYYY-MM-DD"
    obtained_by: "knowledge-researcher"
  validation:
    last_checked: "YYYY-MM-DD HH:MM"
    checked_by: "knowledge-researcher"
    status: "accurate"
    notes: "Initial documentation from source"
---
```

**Attribution fields:**
- `source` - Specific location (file path, URL, API endpoint, database name)
- `source_type` - Category of source (enables appropriate validation tools)
- `obtained_date` - When information was gathered (ISO format YYYY-MM-DD)
- `obtained_by` - Which agent performed research

**Validation fields:**
- `last_checked` - When validation last occurred (ISO format with time)
- `checked_by` - Which agent performed validation
- `status` - Current validation state (`accurate`, `out_of_date`, `source_unreachable`)
- `notes` - Context about validation state

**B. Document Header** (for discoverability)

```markdown
# [Service/Provider/Component Name]

**Quick Reference:** One-line description of what this is
**Category:** [services|providers|infrastructure|customers|etc.]
**Status:** [production|beta|experimental|deprecated]
**Repository/Location:** Path or URL if applicable
```

**C. Standard Sections** (progressive disclosure)

```markdown
## Overview
What it is, why it exists, what problem it solves (2-4 paragraphs)

## Architecture
Technical structure, core components, integration points

## Key Features/Capabilities
Bulleted list of main features (high-level, links to details)

## [Domain-Specific Sections]
Categories, workflows, examples - varies by content type

## Common Workflows
Typical usage patterns with step-by-step examples

## Related Components
Cross-references to other panopticon docs

## Source References
Summary of sources (detailed citations inline)
```

**D. Inline Citations** (for citation-needed agent)

Every factual claim should cite its source:

```markdown
McPanda provides 77 production-ready tools [source: /Users/chris/src/mcpanda/README.md:7]
organized in 12 categories [source: /Users/chris/src/mcpanda/CLAUDE.md:41-140].

The context management system integrates with amp-ctx [source: CLAUDE.md:144-150] for
automatic environment detection.
```

**Citation formats:**
- Code files: `[source: /path/to/file.go:123-456]` or `[source: README.md:789]`
- MCP tools: `[source: mcpanda tool 'locations']`
- APIs: `[source: Live GCP cluster (dev-api) via gcp_monitoring tools]`
- URLs: `[source: https://docs.provider.com/api/...]`
- Databases: `[source: Production database query via billing tools]`
- Documentation: `[source: Slab post "Title" via slab_get]`

**E. Confidence Markers** (for uncertain information)

When confidence is lower than "verified from source":

```markdown
🟢 **High confidence** - Verified from code, live systems, or authoritative docs
🟡 **Medium confidence** - Based on documentation or reasonable inference
🔴 **Low confidence** - Needs verification, may be outdated
```

Use markers inline:
```markdown
The API supports rate limiting of 1000 requests/minute [source: api-docs.md:45].
🟡 **Medium confidence** - Documentation may be outdated, needs verification with live system.
```

#### File Naming Conventions

**Pattern:** `{category}/{kebab-case-name}.md`

**Examples:**
- `services/mcpanda.md` - McPanda MCP server
- `providers/salesforce.md` - Salesforce provider details
- `infrastructure/gcp-kubernetes.md` - GCP Kubernetes infrastructure
- `customers/acme-corp.md` - Acme Corp customer profile
- `team/engineering-processes.md` - Engineering team processes

**Rules:**
- Use lowercase with hyphens (kebab-case)
- Match category to index files (`services/`, `providers/`, etc.)
- Descriptive names that indicate content
- `.md` extension always

### Step 4: Organization Phase

**Agent:** knowledge-steward
**Output:** Updated index files, cross-references, optimized structure

**Process:**
1. Add entry to appropriate index file (`{category}-index.md`)
2. Create cross-references from related documents
3. Update `START-HERE.md` if major new area
4. Validate file location matches conventions
5. Optimize structure if discoverability issues found

**Index entry format:**
```markdown
8. **mcpanda** ✅ - MCP server for integration testing (77 tools, production-ready) → `services/mcpanda.md`
```

**Cross-reference format:**
```markdown
## Related Components

- **amp-ctx** → Context management (see `infrastructure/amp-ctx.md` - TBD)
- **builder-mcp** → Builder MCP server (see `services/builder-mcp.md`)
```

### Step 5: Quality Phase

**Agents:** staleness-checker, citation-needed, knowledge-archivist

**Process:**

**staleness-checker:**
- **Pre-flight:** Run `.claude/scripts/shared/validate-metadata.sh` to ensure attribution metadata exists
- Validates documented claims against sources
- Updates `validation.last_checked` and `validation.status`
- Flags `out_of_date: true` when source contradicts documentation
- Tracks `source_unreachable: true` when sources unavailable

**citation-needed:**
- Scans for unsourced claims
- Adds `[citation needed]` markers with priority levels
- Flags specific types: technical claims, security info, metrics, provider behaviors

**knowledge-archivist:**
- Reviews out-of-date documentation
- Recommends: keep as-is, delete, or reorganize
- Prevents infinite review loops via `known_stale_kept` metadata

## Content Quality Standards

### Attribution is Mandatory

**Before staleness-checker can validate, attribution metadata must exist:**
- No validation without `attribution.source`
- No validation without `attribution.obtained_date`
- No validation without `attribution.obtained_by`

**The staleness-checker will refuse to validate documents lacking attribution.**

### Citation Granularity

**Critical claims require specific citations:**
- Rate limits, API quotas → Cite exact documentation or code
- Security configurations → Cite configuration files or security docs
- Metrics, numbers → Cite monitoring systems or databases
- Provider-specific behaviors → Cite provider docs or observed behavior

**General claims can use broader citations:**
- "McPanda provides testing tools" → README is sufficient
- "The service uses Go" → Repository language is sufficient

### Confidence Levels Guide

**🟢 High confidence:**
- Read directly from source code
- Queried from live production system
- Retrieved from official provider documentation
- Validated through MCP tool execution

**🟡 Medium confidence:**
- Inferred from code patterns
- Based on documentation that may be outdated
- Observed behavior that may vary by environment
- Reasonable assumptions from architecture

**🔴 Low confidence:**
- Heard from team member but not verified
- Found in outdated documentation
- Guessed based on similar systems
- Uncertain about current state

**When in doubt, mark as 🔴 Low confidence and add to `research-tasks.md` for verification.**

## Document Templates by Category

### Services

```markdown
---
validation_metadata:
  attribution:
    source: "/path/to/repo"
    source_type: "code"
    obtained_date: "YYYY-MM-DD"
    obtained_by: "knowledge-researcher"
  validation:
    last_checked: "YYYY-MM-DD HH:MM"
    checked_by: "knowledge-researcher"
    status: "accurate"
    notes: "Initial documentation"
---

# [Service Name]

**Quick Reference:** One-line description
**Category:** Services
**Status:** [production|beta|experimental]
**Repository:** /path/to/repo

## Overview
What it does, why it exists, problem it solves

## Architecture
Tech stack, core components, integration points

## Key Features
- Feature 1
- Feature 2

## API / Interface
How other services interact with it

## Common Workflows
Usage patterns, examples

## Related Components
Cross-references

## Source References
Citation summary
```

### Providers

```markdown
# [Provider Name]

**Quick Reference:** Provider type and main use cases
**Category:** Providers
**Status:** [production|beta]
**Provider Type:** [CRM|Marketing|Sales|etc.]

## Overview
What the provider is, typical Ampersand use cases

## Authentication
OAuth details, scope requirements, token refresh behavior

## Standard Objects
Available objects and their purposes

## Rate Limits & Quotas
API limits, best practices

## Known Quirks
Provider-specific behaviors, gotchas, workarounds

## Integration Examples
Common integration patterns

## Related Documentation
Provider official docs, Ampersand integration examples

## Source References
```

### Infrastructure

```markdown
# [Infrastructure Component]

**Quick Reference:** What this infrastructure provides
**Category:** Infrastructure
**Status:** production
**Cloud Provider:** [GCP|AWS|etc.]

## Overview
Purpose, scope, why we use it

## Architecture
Physical/logical layout, regions, clusters

## Key Resources
Important resources, configurations

## Access & Authentication
How to access, credentials, permissions

## Monitoring & Alerts
Health checks, SLOs, alert policies

## Disaster Recovery
Backup procedures, recovery processes

## Related Components

## Source References
```

## Exploration & Speculative Research

**New capability (2026-02-06):** Panopticon now supports speculative research for novel providers, dependencies, or architectural decisions.

### The Challenge

Panopticon documents **what exists** at Ampersand. But developers need to research **what might exist** before making decisions. How to do this without polluting the repository with abandoned proposals?

### The Solution: Status-Based Lifecycle

**Mechanism:** All content (production or speculative) uses the same locations and structure, but is marked with a `status` field in frontmatter metadata.

**Status values:**
- `production` - Exists in production, fully validated
- `exploration` - Under active research, decision pending
- `proposal` - Formal proposal pending approval
- `rejected` - Researched and rejected (valuable context)
- `accepted` - Accepted proposal pending implementation

### Exploration Metadata Extension

For any content with `status` other than `production`:

```yaml
---
validation_metadata:
  # Standard attribution fields
  attribution:
    source: "..."
    source_type: "..."
    obtained_date: "YYYY-MM-DD"
    obtained_by: "knowledge-researcher|knowledge-explorer"

  # Standard validation fields
  validation:
    last_checked: "YYYY-MM-DD HH:MM"
    checked_by: "..."
    status: "accurate"

  # NEW: Status and exploration fields
  status: "exploration"  # or "proposal" | "rejected" | "accepted" | "production"

  exploration:
    started_date: "2026-02-06"
    decision_deadline: "2026-02-20"
    decision_owner: "chris"  # Person/team responsible for decision
    reason: "Evaluating Notion as CRM alternative to Salesforce"
    research_type: "provider_evaluation"  # or "dependency" | "architecture" | "vendor"
---
```

### Lifecycle Management

**Active exploration (status: "exploration"):**
- Lives in normal content areas (providers/, services/, etc.)
- Marked clearly in index files under "Under Exploration" section
- Decision deadline enforced by maintenance rounds
- After deadline: Must transition to rejected/accepted

**Rejected proposals (status: "rejected"):**
- Moved to `archive/rejected-proposals/YYYY-MM-{topic}.md`
- Includes full research findings
- **Critical addition:** "Why We Said No" section explaining decision rationale
- Prevents re-investigation of dead ends
- Valuable institutional knowledge

**Accepted proposals (status: "accepted"):**
- Transitioned to `status: "production"` when implemented
- Archive original exploration to `archive/accepted-proposals/` for historical context
- Production doc becomes the canonical reference

### When to Use Exploration Status

**Use cases:**
- Evaluating new provider integration (Notion, Airtable, Linear)
- Researching new dependencies (Redis, RabbitMQ, different database)
- Architectural decisions (microservice split, API redesign)
- Vendor evaluations (monitoring tools, infrastructure providers)

**Who can create:**
- Developers on the team can invoke `/research` or `/explore`
- Researchers create lightweight investigations
- Explorers create structured comparison research

### Index File Format for Explorations

```markdown
# Providers Index

## Production (80)
- [Salesforce](salesforce.md) - CRM integration
- [HubSpot](hubspot.md) - Marketing automation
...

## Under Exploration (2)
- [Notion](notion.md) ⚠️ - CRM alternative (decision by 2026-02-20) → `providers/notion.md`
- [Airtable](airtable.md) ⚠️ - Database integration (decision by 2026-02-15) → `providers/airtable.md`

## Recently Rejected
- [Linear](../archive/rejected-proposals/2026-01-linear.md) - Project management (rejected: limited API)
```

### Exploration vs Production Format

**Production docs:** Focus on "how it works" (implementation details, APIs, workflows)
**Exploration docs:** Focus on "should we build it" (tradeoffs, comparisons, decision criteria)

**Exploration doc structure:**
```markdown
# Notion Provider Evaluation

## Executive Summary
**Recommendation:** [Go/No-Go/Needs More Info]
**Confidence:** [High/Medium/Low]
**Decision Deadline:** 2026-02-20

## Decision Criteria
| Criterion | Weight | Notion | Salesforce | Winner |
|-----------|--------|--------|------------|--------|
| API Quality | High | 8/10 | 9/10 | Salesforce |
| OAuth Support | High | 7/10 | 10/10 | Salesforce |
| Cost | Medium | 9/10 | 4/10 | Notion |

## Detailed Analysis
[Research findings with inline citations]

## Recommendation
[Detailed recommendation with reasoning]

## Risks & Unknowns
- [ ] Risk 1: Notion's webhook reliability unknown
- [ ] Unknown: What's their SLA?

## Next Steps if Approved
1. Build POC integration
2. Test with 2 pilot customers
...

## Next Steps if Rejected
Archive to `archive/rejected-proposals/2026-02-notion.md` with decision rationale
```

### Maintenance Round Responsibilities

**Every maintenance round checks:**
1. Explorations past deadline → Remind decision owner
2. Explorations >14 days old → Escalate to steward
3. Accepted proposals not yet transitioned → Update status
4. Rejected proposals not yet archived → Move to archive/

**Automation:** `.claude/scripts/shared/check-exploration-deadlines.sh`

## Workflow Summary

**knowledge-scout:**
1. Find source → Document in KNOWLEDGE-SOURCES.md

**knowledge-researcher:**
1. Read KNOWLEDGE-SOURCES.md → Select source
2. Explore source (Read, Grep, tools) → Gather information
3. Create structured markdown → Follow documentation pattern
4. Add frontmatter metadata → Enable validation
5. Include inline citations → Enable quality checks
6. Mark confidence levels → Flag uncertain claims

**knowledge-steward:**
1. Review new documentation → Check structure
2. Update indexes → Add entries
3. Create cross-references → Link related docs
4. Optimize organization → Based on feedback

**Quality agents:**
1. staleness-checker → Validate against sources
2. citation-needed → Flag unsourced claims
3. knowledge-archivist → Manage stale docs

## First Documentation: McPanda Example

The first real documentation created in Panopticon was `services/mcpanda.md` (2026-02-06), which established this pattern:

**Metadata structure:**
- Attribution: source path, type, date, researcher
- Validation: last checked, checker, status, notes

**Document structure:**
- Quick reference header with category and status
- Overview explaining problem and solution
- Architecture section with technical details
- Organized tool categories (77 tools in 12 categories)
- Common workflows with examples
- Related components with cross-references
- Source references with inline citations

**Quality standards:**
- Every major claim cited with file:line format
- Confidence levels omitted (all high confidence from code)
- Frontmatter enables future validation

This pattern should be followed for all future documentation.

## Questions & Improvements

If this pipeline pattern needs refinement, leave feedback in `feedback.md`. The knowledge-steward will review and update this document.

**Common questions to address:**
- When to create separate documents vs. adding to existing?
- How much detail in inline citations?
- When to split large documents?
- How to handle frequently-changing information?

These will be answered as patterns emerge from usage.
