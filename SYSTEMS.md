# Organizational Systems

**"A place for everything, and everything in its place"**

This document catalogs the organizational systems that keep Panopticon structured and useful. These systems fight entropy and make knowledge discoverable.

## Index System

**Purpose:** Enable fast navigation without needing to search

**Files:**
- `START-HERE.md` - Master navigation hub
- `providers-index.md` - 80+ provider integrations
- `services-index.md` - Ampersand services and components
- `infrastructure-index.md` - GCP, K8s, deployments
- `customers-index.md` - Customer profiles
- `team-index.md` - Team structure and roles
- `security-index.md` - Security and compliance
- `observability-index.md` - Monitoring and observability

**Maintenance:**
- Updated when new content docs are added
- Cross-referenced from START-HERE.md
- Validated by cross-reference validator script

## Feedback System

**Purpose:** Create feedback loop from usage to improvement

**Files:**
- `feedback.md` - Active feedback entries
- `archive/feedback-archive-YYYY-QN.md` - Historical feedback by quarter

**Process:**
1. Agents leave feedback after searches (what helped, what didn't)
2. Steward reads feedback and makes improvements
3. Maintenance rounds archive closed entries >30 days old
4. Prevents unbounded growth while preserving history

**Template:**
```markdown
## [YYYY-MM-DD HH:MM] - [Agent Name]
**Query:** What were you looking for?
**Found Quickly:** Yes / Partial / No
**Search Difficulty:** Easy / Moderate / Hard / Failed
**Search Path:** What did you try?
**What Helped:** What made it easy to find?
**What Would Help:** What would have made it easier?
**Suggestions:** Any other improvements?
**Status:** Open / Closed
```

## Research Tracking System

**Purpose:** Track knowledge gaps and prioritize investigation

**Files:**
- `research-tasks.md` - Organized by priority (High, Medium, Low)
- Section for low-confidence claims needing verification

**Process:**
1. Agents note gaps when they can't find information
2. Low-confidence claims (🟡 🔴) get tracked for verification
3. Researcher agent picks up tasks and investigates
4. Completed research gets removed from list

## Metadata System

**Purpose:** Enable quality gates, staleness checking, and source attribution

**Required Frontmatter:**
```yaml
---
category: [service|provider|infrastructure|customer|team|process]
status: [active|deprecated|planned]
attribution:
  source: "Where this information came from"
  obtained_date: "YYYY-MM-DD"
  obtained_by: "[Agent name]"
validation:
  last_checked: "YYYY-MM-DD"
  status: [validated|needs_review|out_of_date]
  checked_by: "[Agent name]"
---
```

**Validation:**
- `.claude/scripts/shared/validate-metadata.sh` checks required fields
- Staleness-checker enforces attribution before validation
- Knowledge-archivist uses validation status for decisions

## Citation System

**Purpose:** Track where information comes from, enable verification

**Patterns:**
- **Inline citations**: `(source: file.go:123)` or `(source: Slab/Provider Docs)`
- **Source references section**: Links to all sources at end of document
- **[citation needed]**: Flagged by citation-needed agent for unsourced claims

**Priority Levels:**
- Critical: Security, compliance, legal information
- High: API limits, technical specifications, provider behaviors
- Medium: Implementation details, architecture decisions
- Low: General information, widely-known facts

## Quality Gate System

**Purpose:** Ensure new content meets standards before proliferating

**Gates:**
1. **Metadata validation** - Required frontmatter present
2. **Cross-reference validation** - Links point to real files
3. **Citation coverage** - Important claims have sources
4. **Staleness checking** - Validated against sources
5. **Index completeness** - Content docs are indexed

**Scripts:**
- `.claude/scripts/shared/validate-metadata.sh` ✅
- `.claude/scripts/shared/validate-cross-refs.py` ✅
- Citation checker (planned)
- Index completeness checker (planned)

**Workflow:**
1. Researcher creates content → includes metadata + citations
2. Maintenance round validates → runs quality gate scripts
3. Issues found → noted in research-tasks.md or feedback.md
4. Pass all gates → content is high quality

## Archive System

**Purpose:** Handle outdated information without deletion

**Structure:**
```
archive/
├── feedback-archive-2026-Q1.md       # Closed feedback entries
├── providers/
│   └── salesforce/
│       └── 2024-api-v1.md            # Historical provider versions
└── [other archived content]
```

**Process:**
1. Staleness-checker flags out_of_date content
2. Knowledge-archivist reviews and recommends action
3. If keeping for historical value → move to archive/ with versioning
4. Update metadata: `known_stale_kept: true` prevents re-flagging
5. Add note in current doc pointing to archived version

## Script Organization System

**Purpose:** Make maintenance tools discoverable and maintainable

**Structure:**
```
.claude/scripts/
├── shared/                    # Used by multiple agents
│   ├── validate-metadata.sh
│   └── validate-cross-refs.py
├── steward/                   # Steward-specific
├── researcher/                # Researcher-specific
├── [agent-name]/             # Other agent-specific scripts
```

**Guidelines:**
- Scripts have header comments (what, who uses it, useful for)
- Executable permissions set (`chmod +x`)
- Shared if used by 2+ agents, agent-specific otherwise
- Move from agent-specific to shared when usage expands

## Cross-Reference System

**Purpose:** Create knowledge graph, enable navigation between related topics

**Patterns:**
- Index files reference content docs
- Content docs reference related content
- Bidirectional references when relevant
- Use `backtick` format for file references or `[text](path)` markdown links

**Validation:**
- `.claude/scripts/shared/validate-cross-refs.py` checks for broken links
- Distinguishes real broken links from example/template references
- Maintenance rounds fix broken references or note for research

## Knowledge Source System

**Purpose:** Catalog where to find Ampersand information

**Files:**
- `KNOWLEDGE-SOURCES.md` - Comprehensive catalog maintained by knowledge-scout

**Categories:**
- Code repositories (server, mcpanda, argocd)
- Live tools (McPanda MCP server - 77 tools)
- Documentation (Slab, mcpanda .md files)
- External resources (provider official docs)
- Live systems (databases, GCP, monitoring)

**Maintenance:**
- Scout agent discovers new sources
- Scout evaluates and prunes stale sources
- Researcher uses sources for investigation

## Ingestion Pipeline

**Purpose:** Standardize how new knowledge enters the repository

**Steps:**
1. Discovery (identify information to document)
2. Creation (write content with metadata + citations)
3. Indexing (add to appropriate index file)
4. Validation (run quality gate scripts)
5. Maintenance (periodic staleness checks)

**Documentation:** See `INGESTION-PIPELINE.md` for detailed process

---

## System Maintenance

**Regular Maintenance Tasks:**
- Run quality gate scripts on new/modified content
- Archive closed feedback entries >30 days old
- Validate cross-references
- Check for orphaned content (docs not in any index)
- Review research-tasks.md priorities
- Verify scripts are documented and executable

**Signs of System Degradation:**
- Broken cross-references accumulating
- Feedback.md growing unbounded
- Content docs without metadata
- Missing index entries
- Stale information not flagged

**Recovery:**
- Maintenance rounds address accumulating issues
- Quality gate scripts catch problems early
- Feedback system identifies systemic issues
- Steward agent makes structural improvements

---

**Philosophy:** These systems are not overhead—they're the foundation that makes knowledge discoverable and useful. Without them, Panopticon becomes a pile of markdown files. With them, it becomes an institutional memory.
