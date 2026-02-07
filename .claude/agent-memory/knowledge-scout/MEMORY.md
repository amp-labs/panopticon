# Knowledge Scout Memory

## Repository Categorization (2026-02-06)

### Primary Active Repositories (High Value)
- **server** (2.3GB, 611 commits/30d) - Core backend monorepo with 7 services
- **mcpanda** (675MB, 39 commits/30d) - MCP server with 77 tools
- **argocd** (227MB, 573 commits/30d) - K8s deployment configs
- **connectors** (240MB, 101 commits/30d) - Provider integrations library
- **cloud-infra** (infrastructure) - Terraform configs for GCP
- **cloud-functions** (infrastructure) - Cloud Function implementations
- **docs** (public documentation) - Mintlify docs at docs.withampersand.com

### Secondary Active Repositories (Medium Value)
- **amp-common** (28MB, 25 commits/30d) - Shared Go libraries
- **amp-ctx** (24MB, 3 commits/30d) - Context switching CLI
- **openapi** (78MB, 12 commits/30d) - OpenAPI specs
- **samples** (1.9MB, 6 commits/30d) - Sample code

### Tertiary/Stale Repositories (Low Value)
- **temporal** (160MB, 0 commits/30d) - Upstream Temporal fork
- **sdk-go** (24MB, 0 commits/30d) - Upstream Temporal SDK
- **mcp** (4.3MB, 26 commits/30d) - MCP protocol implementation
- **mcp-protocol** (2.6MB, 21 commits/30d) - MCP protocol (seems duplicate of mcp?)
- **client** (483MB, 17 commits/30d) - Client/console (limited activity)
- **cli** (minimal activity) - Ampersand CLI (old? superseded?)
- **server2**, **server3** - Additional server versions (unclear purpose)
- **react** (large node_modules) - Frontend framework upstream
- **cal.com**, **Flowise**, etc. - Third-party/upstream projects

### Not Git Repositories (Infrastructure)
- **.claude** - Agent memory and configurations
- **testdata** - Test data and fixtures
- **worktrees** - Git worktree metadata

## Key Discoveries

### Infrastructure Documentation
- **cloud-infra/README.md** - Terraform setup, GCP project organization (dev/staging/prod)
- **cloud-infra/CLAUDE.md** - Agent-specific infrastructure guidance
- **cloud-functions/** - Multiple cloud function implementations with READMEs
  - clickhouse_usage_events, webhookgateway, archive-db, pr-closed-handler, dead-letter processing
  - Each has its own README and CLAUDE.md

### Shared Libraries & Utilities
- **amp-common** - 100% test coverage, shared Go utilities (actors, pooling, concurrency, telemetry)
- **amp-yaml-validator** - amp.yaml validation library with ARCHITECTURE.md
- **amp-ctx** - Context/environment management CLI

### Documentation Structure
- **server/** - Comprehensive AI agent docs (AGENTS.md), design patterns (interface-first), database patterns
- **mcpanda/** - Extensive .md files documenting MCP design, patterns, implementation guides
- **docs/** - Public-facing documentation (Mintlify-based)
- **connectors/** - Provider integration library (7 markdown files)

## Evaluation Findings

### Source Quality Ratings (by repository)

**🟢 High Quality - Primary Research Sources:**
- **server** - Well-documented, active, comprehensive. Excellent for architecture, APIs, database patterns.
- **mcpanda** - Production tools well-documented. Primary tool reference.
- **argocd** - K8s deployment source of truth. Active infrastructure management.
- **cloud-infra** - Terraform configs with environment management docs.
- **connectors** - Provider integration implementations.

**🟡 Medium Quality - Secondary Sources:**
- **amp-common** - Utility library with good docs but not integration-specific.
- **amp-ctx** - Context management tool, lightweight documentation.
- **openapi** - API spec source, but referenced in docs repo.
- **samples** - Example code, limited scope.

**🔴 Low Quality or Stale - Tertiary/Deprecated:**
- **temporal**, **sdk-go** - Upstream forks, not Ampersand-specific.
- **mcp**, **mcp-protocol** - Protocol implementations, may be duplicated.
- **server2**, **server3** - Unclear versioning, possibly deprecated.
- **cli** - Minimal recent activity.
- **client** - Large but low commit activity (17/30d).

## Recommendations for Scout

### Should Add to KNOWLEDGE-SOURCES.md
1. **cloud-infra** - Infrastructure source of truth (Terraform)
2. **cloud-functions** - Cloud Function implementations and patterns
3. **amp-yaml-validator** - YAML validation library with architecture docs
4. **amp-common** - Shared utilities library
5. **connectors** - Provider integration library
6. **amp-ctx** - Context management tool

### Should Deprecate/Remove
1. **temporal** - Upstream fork, not maintained by Ampersand
2. **sdk-go** - Upstream SDK, not maintained by Ampersand
3. **mcp** vs **mcp-protocol** - Determine which is canonical, deprecate other
4. **server2**, **server3** - Clarify purpose or remove
5. **cli** - Check if superseded by amp-ctx

### Organizational Patterns Found
- Infrastructure repos live at ~/src root level (cloud-infra, cloud-functions, argocd)
- Documentation in multiple places: code repos (.md files), docs/ (public), Slab (internal)
- Architecture docs often stored as ARCHITECTURE.md or AGENTS.md in repo root
- CLAUDE.md files provide agent-specific guidance in various repos

## Discovery Techniques That Worked Well
1. **du -sh** for repository size assessment
2. **git log** for activity patterns (commits in last 30 days)
3. **find for .md files** to discover documentation
4. **grep first lines of README** to understand purpose
5. **Checking for ARCHITECTURE.md/AGENTS.md** finds well-documented projects

## Future Scouting Notes
- Monitor server2/server3 - understand if they're development versions or legacy
- Watch for cli → amp-ctx migration - may need to update sources
- Consider periodic review of external upstream repos (temporal, react, cal.com) - are they needed?
- Track whether public docs (docs/) and Slab docs stay synchronized
