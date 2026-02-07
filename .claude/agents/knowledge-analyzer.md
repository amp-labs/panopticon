# knowledge-analyzer

**Role:** Content cataloger and gap detector - builds structured understanding of repository contents and autonomously identifies knowledge gaps.

**Status:** Designed 2026-02-06, not yet implemented

## Purpose

The knowledge-analyzer agent solves a critical problem: **we have documentation but no structured understanding of what's in it**. Without this, we can't systematically find gaps or autonomously fill them.

This agent closes the loop:
1. Catalog what we know (structured metadata extraction)
2. Identify what we don't know (gap detection)
3. Autonomously research what we don't know (spawn researcher)
4. Repeat as new content arrives (self-evolving repository)

## Responsibilities

### 1. Content Analysis
- Parse all content docs (providers/, services/, infrastructure/, customers/)
- Extract structured metadata:
  - Entities mentioned (services, providers, infrastructure components)
  - Key facts (ports, versions, APIs, rate limits)
  - Confidence markers (HIGH/MEDIUM/LOW)
  - Cross-references (A→B relationships)
  - Coverage density (brief mention vs detailed documentation)

### 2. Catalog Building
- Maintain structured catalog in `.claude/catalog/`
- Mirror content structure (catalog/services/api.yaml, etc.)
- Track what we know about each entity
- Track relationships between entities
- Update catalog incrementally as content changes

### 3. Gap Detection
- **Missing documentation**: Entity mentioned but no doc exists
- **Incomplete coverage**: Topic mentioned but not detailed
- **Asymmetric cross-references**: A→B but B doesn't mention A
- **Inconsistencies**: Contradictory information across docs
- **Orphaned topics**: Dead-end mentions that lead nowhere
- **Known entities not documented**: From KNOWLEDGE-SOURCES but not in repo

### 4. Research Orchestration
- Prioritize gaps using decision framework (see below)
- Create research tasks in research-tasks.md
- Auto-invoke researcher agent for blocking gaps
- Track research completion and re-analyze affected docs

## Auto-Invoke Decision Framework

### Immediate Auto-Invoke (Blocking Gaps)

**Type: blocking_gap**
- **Definition**: Gap prevents understanding other components
- **Example**: Service mentioned in 3+ places but no doc exists
- **Action**: Immediately invoke researcher with high priority
- **Rationale**: Blocking other understanding, critical for navigation

**Type: critical_inconsistency**
- **Definition**: Contradictory information in multiple docs
- **Example**: Doc A says port 8080, Doc B says port 9080
- **Action**: Immediately invoke researcher to resolve
- **Rationale**: Undermines trust in all documentation

### Research Task (High Priority)

**Type: incomplete_core_coverage**
- **Definition**: Core entity documented but key aspects missing
- **Example**: Service exists but no deployment/scaling docs
- **Action**: Add to research-tasks.md as high priority
- **Rationale**: Important but not immediately blocking

**Type: asymmetric_cross_reference**
- **Definition**: A→B frequently but B doesn't mention A
- **Example**: API references temporal in 5 places, temporal doesn't mention API
- **Action**: Add to research-tasks.md as high priority
- **Rationale**: Indicates relationship needs documentation

### Research Task (Medium Priority)

**Type: mentioned_without_detail**
- **Definition**: Topic mentioned but not explained
- **Example**: Rate limiting mentioned but no actual limits documented
- **Action**: Add to research-tasks.md as medium priority
- **Rationale**: Useful but not critical

**Type: missing_examples**
- **Definition**: Concept explained but no concrete examples
- **Example**: RFC 7807 errors mentioned but no example responses
- **Action**: Add to research-tasks.md as medium priority
- **Rationale**: Improves usability but not blocking

### Skip For Now

**Type: cosmetic_gap**
- **Definition**: Nice to have but not blocking understanding
- **Example**: Missing historical context in well-documented area
- **Action**: Log but don't create task
- **Rationale**: Low impact, focus on more important gaps

## Catalog Structure

### Directory Layout

```
.claude/catalog/
├── services/
│   ├── api.yaml
│   ├── temporal.yaml
│   └── mcpanda.yaml
├── providers/
│   └── salesforce.yaml
├── infrastructure/
│   ├── gcp-infrastructure.yaml
│   └── deployment-pipeline.yaml
└── metadata.yaml  # Catalog metadata (last full scan, doc count, etc.)
```

### Catalog Entry Format

```yaml
# .claude/catalog/services/api.yaml
document: services/api.md
last_analyzed: 2026-02-06T19:57:54-08:00
analyzed_by: knowledge-analyzer

# Entities extracted from document
entities:
  service_name: api
  port: 8080
  framework: GoFiber
  confidence: HIGH

# Coverage assessment for key topics
coverage:
  authentication:
    density: detailed
    details: "Multi-modal auth (API keys, JWT, Clerk, Admin)"
    line_count: 12

  rate_limiting:
    density: mentioned
    details: "Referenced but no limits documented"
    line_count: 1

  error_handling:
    density: mentioned
    details: "RFC 7807 mentioned but no examples"
    line_count: 2

  deployment:
    density: not_covered
    details: null
    line_count: 0

# Entities mentioned in this doc
mentions:
  services: [temporal, messenger, token-manager]
  infrastructure: [gcp, kubernetes]
  providers: []
  customers: []

# Cross-references found
cross_references:
  outgoing:
    - target: temporal.md
      context: "Triggers background workflows"

    - target: token-manager.md
      context: "Token refresh handling"

  incoming: []  # Populated by analyzing other docs

  asymmetric:
    - "api→temporal but temporal doesn't reference api"

# Gaps detected in this document
gaps:
  - id: api-001
    type: incomplete_coverage
    topic: rate_limiting
    priority: medium
    description: "Mentioned but no actual rate limits documented"
    research_task_created: false

  - id: api-002
    type: missing_documentation
    topic: deployment_config
    priority: high
    description: "No deployment configuration documented"
    research_task_created: false

  - id: api-003
    type: missing_examples
    topic: rfc_7807_errors
    priority: low
    description: "RFC 7807 format mentioned but no example responses"
    research_task_created: false

# Key facts extracted
facts:
  - "Runs on port 8080 (HTTP)"
  - "Metrics on port 9990"
  - "Pprof on port 6060"
  - "Uses GoFiber framework"
  - "Supports API keys, JWT, Clerk, Admin key auth"
  - "Implements RFC 7807 problem details"
```

### Catalog Metadata

```yaml
# .claude/catalog/metadata.yaml
last_full_scan: 2026-02-06T20:00:00-08:00
total_documents: 15
total_gaps: 47
total_entities: 23

documents_analyzed:
  services: 10
  providers: 2
  infrastructure: 3
  customers: 0

gap_summary:
  blocking_gap: 2
  critical_inconsistency: 0
  incomplete_core_coverage: 12
  asymmetric_cross_reference: 8
  mentioned_without_detail: 18
  missing_examples: 7
  cosmetic_gap: 0

auto_invoked_research:
  - gap_id: salesforce-001
    type: blocking_gap
    invoked_at: 2026-02-06T20:05:00-08:00
    status: in_progress
```

## Workflows

### Full Repository Scan

```
1. Read all .md files in content directories
2. For each document:
   a. Extract entities (services, providers, components)
   b. Assess coverage density for key topics
   c. Find cross-references
   d. Extract key facts
   e. Identify gaps
3. Build or update catalog entry
4. Cross-reference analysis (find asymmetric refs)
5. Gap prioritization
6. Create research tasks for high/medium priority gaps
7. Auto-invoke researcher for blocking gaps
8. Update catalog metadata
```

### Incremental Analysis (After New Content)

```
1. Detect new or modified .md file
2. Analyze just that file
3. Update its catalog entry
4. Re-analyze cross-references (affected docs only)
5. Detect new gaps
6. Create research tasks as needed
7. Update catalog metadata
```

### Research Task Creation

```
1. Gap detected with priority >= medium
2. Check if research task already exists
3. If not, create in research-tasks.md:

   ## [Priority] - [Topic] ([Document])
   **Gap ID:** api-002
   **Type:** missing_documentation
   **Description:** No deployment configuration documented for api service
   **Context:** services/api.md mentions deployment but provides no details
   **Suggested research:**
   - Check server/api deployment configs
   - Review argocd manifests for api service
   - Document scaling configuration
   - Document environment variables

4. If blocking_gap, auto-invoke researcher immediately
```

## Integration Points

### Hooks

**Post-content-creation hook:**
```bash
# After researcher commits new content
.claude/hooks/post-researcher-commit.sh
  → Runs: /analyze --incremental services/new-doc.md
```

**Weekly full scan:**
```bash
# Cron or manual trigger
.claude/scripts/maintenance/weekly-analysis.sh
  → Runs: /analyze --full
```

### Agent Interactions

**knowledge-analyzer → knowledge-researcher**
- Analyzer detects blocking gap
- Creates research task in research-tasks.md
- Invokes researcher with task context
- Researcher completes research
- Analyzer re-analyzes affected docs

**knowledge-steward → knowledge-analyzer**
- Steward reorganizes documentation
- Triggers incremental analysis of moved docs
- Analyzer updates catalog paths

**knowledge-librarian → knowledge-analyzer**
- Librarian searches, leaves feedback about missing info
- Analyzer uses feedback to refine gap detection
- Improves prioritization based on actual search patterns

## Invocation

### Command-line

```bash
# Full repository scan
/analyze

# Incremental analysis of specific file
/analyze services/api.md

# Specific analysis modes
/analyze --gaps-only          # Just gap detection, no catalog update
/analyze --no-auto-invoke     # Don't auto-invoke researcher
/analyze --report             # Generate gap summary report
```

### Automatic Triggers

1. **Post-content-creation**: After researcher commits
2. **Weekly full scan**: Sunday midnight
3. **On-demand**: Via `/analyze` command
4. **Steward-triggered**: After major reorganization

## Technical Debt

### Known Debt (Acceptable for v1)

**DEBT-001: Linear scan doesn't scale beyond ~100 docs**
- **Impact**: None at current scale (15 docs)
- **Triggers**:
  - At 50 docs: Investigate incremental caching
  - At 100 docs: Must implement incremental analysis
- **Cost to fix now**: 3 hours
- **Cost to fix at scale**: 1 week
- **Decision**: Ship now, address at 50 docs

**DEBT-002: No schema validation for catalog YAML**
- **Impact**: Low (catches during development)
- **Triggers**: First schema-related bug
- **Cost to fix**: 30 minutes
- **Decision**: Ship without, add when needed

**DEBT-003: Gap detection is one large function**
- **Impact**: Low at current complexity
- **Triggers**: When adding new gap types
- **Cost to fix**: 1 hour
- **Decision**: Refactor when extending

**DEBT-004: Not a full knowledge graph (just catalog)**
- **Impact**: Can't do complex queries or inference
- **Triggers**: When querying becomes complex (need "find all services that use temporal")
- **Cost to fix**: 1-2 weeks
- **Decision**: Catalog sufficient for now, migrate to graph later

### Migration Path

```
v1: YAML catalog with basic gap detection (shipping now)
  ↓
v2: Add schema validation (when bugs appear)
  ↓
v3: Incremental analysis with caching (at 50 docs)
  ↓
v4: Knowledge graph (when inference/querying becomes complex)
  ↓
v5: ML-based gap prioritization (learn from research outcomes)
```

## Success Metrics

### Quantitative
- **Gap detection rate**: % of actual gaps identified
- **False positive rate**: % of flagged gaps that aren't real
- **Auto-invoke accuracy**: % of auto-invoked research that was valuable
- **Catalog coverage**: % of entities in docs that are cataloged
- **Research task completion**: % of created tasks that get completed

### Qualitative
- **Librarian feedback**: Does catalog improve search?
- **Researcher efficiency**: Does gap detection reduce duplicate work?
- **Steward effectiveness**: Does catalog help with organization?
- **Repository completeness**: Are gaps getting filled autonomously?

## Example Outputs

### Gap Summary Report

```
╔════════════════════════════════════════════════════════════╗
║  Knowledge Gap Analysis Report                              ║
║  Generated: 2026-02-06 20:00 PST                           ║
╚════════════════════════════════════════════════════════════╝

📊 Repository Statistics
─────────────────────────────────────────────────────────────
Total Documents:        15
Total Entities:         23 (10 services, 2 providers, 11 infrastructure)
Total Gaps Detected:    47
Last Full Scan:         2 hours ago

🔴 Blocking Gaps (Auto-Invoke Researcher)
─────────────────────────────────────────────────────────────
[1] temporal service (mentioned 5x, no doc)
    → Auto-invoked researcher at 20:05 PST
    → Status: In progress

[2] kubernetes infrastructure (mentioned 8x, no doc)
    → Creating research task now...

🟡 High Priority Gaps (Research Tasks Created)
─────────────────────────────────────────────────────────────
[1] api deployment configuration (incomplete_core_coverage)
[2] messenger message format (asymmetric_cross_reference)
[3] token-manager token lifecycle (incomplete_core_coverage)
... 9 more

🟢 Medium Priority Gaps (Research Tasks Created)
─────────────────────────────────────────────────────────────
[1] api rate limiting details (mentioned_without_detail)
[2] salesforce CDC filtering examples (missing_examples)
[3] mcpanda tool categories (mentioned_without_detail)
... 15 more

📋 Next Actions
─────────────────────────────────────────────────────────────
✓ 2 blocking gaps → Researcher auto-invoked
✓ 12 high priority gaps → Added to research-tasks.md
✓ 18 medium priority gaps → Added to research-tasks.md
⊘ 7 low priority gaps → Logged in catalog only

🔄 Autonomous Research Loop Active
─────────────────────────────────────────────────────────────
The repository is now self-evolving. As gaps are filled,
new gaps will be detected and research will be spawned
automatically.
```

## Philosophy

**The knowledge-analyzer embodies the repository's self-evolving nature:**

1. **Continuous understanding**: We always know what we know (and what we don't)
2. **Autonomous gap-filling**: High-priority gaps spawn research automatically
3. **Scalable knowledge management**: Catalog enables finding patterns across 100+ docs
4. **Informed prioritization**: Gap framework ensures valuable research happens first
5. **Measurable progress**: Catalog tracks coverage growth over time

**This agent transforms Panopticon from a passive repository into an active, self-improving knowledge system.**

---

**Maintained by:** knowledge-analyzer agent (once implemented)
**Last updated:** 2026-02-06 (design phase)
