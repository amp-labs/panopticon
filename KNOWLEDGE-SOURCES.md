# Knowledge Sources for Research

This document catalogs the primary sources of truth for researching Ampersand knowledge.

## Code Repositories

### Primary Repositories

**NOTE:** Repository locations on disk vary by developer machine. Use McPanda or amp-ctx to discover locations dynamically:
- McPanda tool: `locations` - Get repository and service location mappings
- amp-ctx: Automatically resolves repository paths based on context

1. **server** (Ampersand Backend Monorepo)
   - **Primary purpose:** Main backend services for Ampersand platform
   - **Services included:** 7 microservices + shared libraries
     - `api` - REST API (customer requests, resource management, auth, encryption, Temporal orchestration)
     - `temporal` - Background workers (long-running tasks, retries, throttling)
     - `messenger` - Webhook delivery engine (splits data into <300kb chunks, subscription handling)
     - `scribe` - Event ingestion from Pub/Sub (operations, billing events)
     - `token-manager` - Centralized OAuth token refresh service
     - `metrics` - Prometheus metrics exposure
     - `builder-mcp` - MCP server for integration building

   - **Shared libraries (45+ packages):**
     - Database abstractions (types, GORM, memory implementations)
     - OAuth flows, token management
     - Temporal workflow definitions
     - Provider integrations, catalog
     - Billing, usage tracking
     - GCS storage, Redis caching
     - Monitoring, tracing, metrics

   - **Code structure:**
     - 1,150+ Go files, 2.2GB total
     - 2,226 commits in Jan 2025, 2,104 in Feb 2025 (highly active)
     - Last commit: 2026-02-06

   - **Key documentation:**
     - `README.md` - Local dev setup, Docker Compose configuration, troubleshooting
     - `AGENTS.md` - Agent-oriented guide (resource relationships, local endpoints, commands)
     - `docs/interface-first-design-patterns.md` - Design patterns for testable components
     - `shared/database/README.md` - Database development guide with examples
     - `docs/swagger.json` - OpenAPI specification (12KB)

   - **Quality & Maturity Indicators:**
     - Automated formatting (wsl, gci, golangci-lint, typos)
     - Pre-commit hooks for code quality
     - Integration tests with scenarios
     - Database migration system (Atlas)
     - Seed data for testing
     - Comprehensive Makefile (40+ targets)
     - Multiple environment support (local, dev, staging, prod, preview)

   - **Research Use Cases:**
     - **API endpoints:** Search `api/routes/` for endpoint implementations
     - **Provider integrations:** Check `shared/providers/` and provider-specific code
     - **Database schema:** Use `shared/database/models/` and migrations
     - **Business logic:** Temporal workflows, read/write/subscribe handlers
     - **OAuth patterns:** `shared/oauth/` implementation
     - **Error handling:** Distributed error migration and recovery

   - **Access Methods:**
     - Direct file navigation (Glob/Grep)
     - `locations` tool from McPanda for dynamic path resolution
     - Git log for commit history and recent changes
     - Database analysis via shared/database interfaces

   - **Known Strengths:**
     - Well-organized monorepo with clear service boundaries
     - Excellent documentation for AI agents (AGENTS.md is thorough)
     - Design patterns documented by example (examples/ directory)
     - Active maintenance and frequent updates
     - Strong architectural patterns (interface-first, context-based DI)

   - **Limitations:**
     - Large codebase requires targeted searches
     - Private dependencies (amp-common) require GitHub SSH access
     - Some documentation in Slab (requires MCP tool access)
     - Real customer data in prod requires appropriate authorization

   - **Get location:** Use `locations` tool from McPanda, or: `~/src/server`

2. **mcpanda**
   - MCP server with 77 tools for Ampersand operations
   - Integration testing automation
   - Provider interaction tools
   - Contains extensive documentation in root-level .md files
   - **Get location:** Use `locations` tool from McPanda

3. **argocd**
   - Kubernetes deployment configurations
   - Environment-specific manifests (dev, staging, prod, preview)
   - GitOps source of truth
   - 227MB, 573 commits in last 30 days (highly active)
   - **Get location:** Use `locations` tool from McPanda

4. **cloud-infra** (Infrastructure as Code)
   - Terraform configurations for GCP infrastructure
   - Manages three environments: dev, staging, prod
   - Infrastructure workspace definitions
   - Terraform Cloud integration
   - Key files:
     - `README.md` - Environment setup, workspace management, change workflow
     - `CLAUDE.md` - Agent-specific infrastructure guidance
   - **Quality:** 🟢 High - Active infrastructure management, well-documented
   - **Size:** Infrastructure source of truth for GCP projects
   - **Get location:** ~/src/cloud-infra (or search for terraform configs)

5. **cloud-functions** (Serverless Functions)
   - Google Cloud Function implementations
   - Multiple function categories:
     - `clickhouse_usage_events/` - Usage event processing
     - `webhookgateway/` - Webhook routing and handling
     - `archive-db/` - Database archival jobs
     - `pr-closed-handler/` - GitHub PR event handling
     - `dead-letter-receiver/` - Failed message handling
     - `dead-letter-processor/` - Dead letter queue processing
   - Each function has own README and CLAUDE.md
   - **Quality:** 🟢 High - Production functions with individual documentation
   - **Get location:** ~/src/cloud-functions

6. **amp-yaml-validator** (Configuration Validation)
   - Library for validating amp.yaml integration manifests
   - Comprehensive validation: schema, business logic, provider constraints
   - Key file: `ARCHITECTURE.md` - Design principles and validator structure
   - Modular validator organization by concern
   - **Quality:** 🟢 High - Well-architected, comprehensive validation
   - **Usage:** Research how integrations are validated

7. **amp-common** (Shared Go Libraries)
   - Shared utilities used across Ampersand projects
   - 100% test coverage
   - Packages for: actors, object pooling, concurrency, environment parsing, telemetry
   - Private GitHub repository (requires SSH setup)
   - **Quality:** 🟡 Medium - Well-tested but not Ampersand-specific
   - **28MB, 25 commits/30d** - Actively maintained
   - **Get location:** Use `locations` tool or private repo access

8. **connectors** (Provider Integrations)
   - Provider integration implementations and libraries
   - 240MB, 101 commits in last 30 days (very active)
   - Multiple provider-specific implementations
   - 7 markdown documentation files
   - **Quality:** 🟢 High - Active provider development
   - **Get location:** ~/src/connectors

9. **amp-ctx** (Environment Management)
   - CLI tool for switching between Ampersand contexts
   - Manages different development environments
   - 24MB, minimal activity but core utility
   - **Quality:** 🟡 Medium - Lightweight but essential for development
   - **Get location:** ~/src/amp-ctx

10. **openapi** (API Specifications)
    - OpenAPI definitions for Ampersand APIs
    - 78MB, 12 commits/30d
    - Serves as reference for public API
    - Used to generate reference documentation in docs/ repository
    - **Quality:** 🟡 Medium - API spec source but docs are primary
    - **Get location:** ~/src/openapi

11. **samples** (Example Code)
    - Sample implementations using Ampersand platform
    - 1.9MB, 6 commits/30d
    - Demonstrates integration patterns and usage
    - **Quality:** 🟡 Medium - Good for learning patterns but limited scope
    - **Get location:** ~/src/samples

12. **panopticon** (this repository)
    - Institutional knowledge repository
    - Self-documenting and self-evolving
    - **Location:** You're already here!

### Repositories Evaluated but Not Recommended

The following repositories were discovered and evaluated but are not recommended as primary knowledge sources:

**🔴 Deprecated/Low-Value Repositories:**

1. **temporal** - Upstream fork of Temporal workflow engine
   - Not maintained by Ampersand team
   - Use official Temporal documentation instead
   - **Reason:** Upstream project, not Ampersand-specific

2. **sdk-go** - Upstream Temporal Go SDK
   - Not maintained by Ampersand team
   - Use official Temporal SDK documentation
   - **Reason:** Upstream project, not Ampersand-specific

3. **server2**, **server3** - Additional server versions
   - Unclear versioning scheme
   - Potentially deprecated alternatives to main server repo
   - **Status:** Needs clarification on purpose and maintenance status
   - **Reason:** Redundant with primary server repository

4. **cli** - Ampersand CLI (legacy)
   - Very low recent activity (1 commit/30d on 2026-01-10)
   - Likely superseded by amp-ctx
   - **Reason:** Low maintenance, possible deprecation

5. **client** - Client/console management
   - 483MB but only 17 commits/30d
   - Purpose unclear from repository structure
   - **Reason:** Large codebase with minimal recent development

6. **mcp** vs **mcp-protocol** - MCP implementations
   - Two similar repositories exist (4.3MB vs 2.6MB)
   - Unclear which is canonical
   - Both have recent activity
   - **Status:** Needs investigation to determine canonical version
   - **Reason:** Possible duplication, need clarity on purpose

**🟢 External Upstream Repositories (For Reference Only):**

These are legitimate upstream projects useful for reference but not Ampersand-specific:
- **react** - React framework
- **fiber** - Go HTTP framework
- **cal.com** - Calendar integration reference
- **Flowise** - Workflow engine reference
- Others in ~/src for tool evaluation/testing

These are for reference and learning only. Ampersand-specific source code is in the primary repositories above.

### MCP Servers (Live Tools)

**McPanda MCP Server** - 77 production tools organized in categories:
- Context Management (6 tools) - Environment switching, auth overrides
- Integration Management (3 tools) - Deploy, status, cleanup
- Connection Management (8 tools) - OAuth connections, health, refresh
- System Health (2 tools) - Comprehensive health checks
- amp.yaml Configuration (8 tools) - Provider objects, validation, generation
- Temporal Workflow Management (7 tools) - Workflow inspection, retry, monitoring
- Testing & Automation (6 tools) - E2E tests, data injection, OAuth simulation
- Provider & Authentication (4 tools) - Provider apps, OAuth sessions, 1Password integration
- Webhook & Data Monitoring (4 tools) - Webhook endpoints, data validation
- Advanced Diagnostics (17 tools) - Error analysis, log streaming, incident analysis
- HTTP API Operations (6 tools) - OpenAPI discovery and invocation
- Many more specialized tools...

**Access:** Available when working in Ampersand development environments

## Documentation Repositories

### Internal Documentation (Slab)
Ampersand uses **Slab** as internal knowledge base. Key content areas:
- MCP server architecture and proposals
- Product roadmaps and feature planning
- Team processes and procedures
- Provider integration guides
- Customer success patterns

**Access:** Via Slab web interface or mcpanda Slab tools
**MCP Tools:** `slab_search`, `slab_get`, `slab_create_post`, `slab_update_post`, `slab_list`

### Server Repository Documentation
Located in root of server repository (use `locations` tool or `~/src/server`):

**AI Agent Guides:**
- `AGENTS.md` - Comprehensive guide for AI agents (resource relationships, service overview, development patterns)
- `README.md` - Local development setup and operation

**Architecture & Design:**
- `docs/interface-first-design-patterns.md` - Design patterns for testable, injectable components
- `docs/swagger.json` - OpenAPI specification for REST API

**Development Guides:**
- `shared/database/README.md` - Database patterns, migrations, models
- `examples/database/widget/` - Complete reference implementation with tests
- `docker-compose/README.md` - Local environment setup details
- `scripts/README.md` - Build and test scripts

**Infrastructure:**
- `argocd-infrastructure.md` - Kubernetes deployment architecture overview
- `MCP_CLIENT_COMPATIBILITY_MATRIX.md` - MCP protocol compatibility information

### McPanda Documentation Files
Located in root of mcpanda repository (use `locations` tool to find repo path):

**Architecture & Design:**
- `MCP.md` - MCP server design for integration testing (highly detailed)
- `MCPANDA_TOOLS_SPEC.md` - Tool specifications
- `AMPERSAND_PATTERNS.md` - Coding and architectural patterns
- `README.md` - McPanda overview and feature catalog

**Product Documentation:**
- `AI_INTEGRATION_UI_PRODUCT_BRIEF.md` - AI integration UI product specs
- `CHAT_INTEGRATION_PLAN.md` - Chat integration planning
- `DASHBOARD_IMPLEMENTATION_PLAN.md` - Dashboard design

**Implementation Guides:**
- `GCP_MONITORING_IMPLEMENTATION.md` - GCP monitoring setup
- `GO_AST_IMPLEMENTATION.md` - Go AST analysis tools
- `KUBECTL_TOOLS_IMPLEMENTATION.md` - Kubernetes tools
- `ONEPASSWORD.md` - 1Password integration

**Slab Export Files:**
- `SLAB_AMPERSAND_MCP_SERVERS.md` - MCP server proposals
- `SLAB_NOTIFICATIONS_BUG_BASH.md` - Bug bash documentation
- `SLAB_PROGRESS_API.md` - Progress API documentation

**Other:**
- `IDEAS.md` - Feature ideas and proposals
- `TOOLING_FEEDBACK.md` - Feedback on tooling

## External Resources

### Provider Documentation
- Official provider API docs (Salesforce, HubSpot, etc.)
- OAuth flow documentation
- Rate limit specifications
- Webhook documentation

**Access:** Public web, use WebFetch/WebSearch tools

### Open Source Projects
- Temporal workflow documentation
- Kubernetes documentation
- ArgoCD documentation
- Go language specifications

## Live Systems

### Databases
- PostgreSQL (dev, staging, prod clusters)
- Database schemas available via Atlas migrations
- Production customer data (requires appropriate access and care)

**Access:** Via mcpanda tools or direct database queries (with authorization)

### GCP Infrastructure
- Cloud Build pipelines
- Kubernetes clusters (GKE)
- Cloud Functions
- Pub/Sub topics and subscriptions
- Cloud Storage buckets
- Cloud SQL instances

**Access:** Via mcpanda GCP tools or gcloud CLI

### Monitoring & Observability
- Prometheus metrics
- GCP Cloud Monitoring
- Sentry error tracking
- ArgoCD application status

**Access:** Via mcpanda monitoring tools

## Repository Discovery & Evaluation

### All Repositories Discovered in ~/src (2026-02-06)

Total: 60+ repositories and projects discovered

**Key Statistics:**
- Largest repositories: server (2.3GB), client (483MB), mcpanda (675MB)
- Most active: argocd (573 commits/30d), server (611 commits/30d), connectors (101 commits/30d)
- Fully documented: server (AGENTS.md, docs/), mcpanda (extensive .md files), argocd (README)
- Infrastructure: cloud-infra (Terraform), cloud-functions (GCP functions), argocd (K8s)

### Evaluation Criteria Used

Each repository was assessed on:
- **Activity Level** - Commits in last 30 days (0-600+)
- **Size** - Total disk space (1MB - 2.3GB)
- **Documentation** - README, architecture docs, design docs
- **Maintenance** - Recent changes, code quality indicators
- **Relevance** - Ampersand-specific vs upstream projects
- **Dependencies** - How critical to understanding Ampersand

### Quality Ratings Explained

- 🟢 **High Quality** - Well-maintained, well-documented, active development, Ampersand-specific
- 🟡 **Medium Quality** - Good documentation, some maintenance, limited scope or activity
- 🔴 **Low Quality** - Minimal documentation, stale, upstream, unclear purpose

---

## Research Workflow Recommendations

### For Provider Research:
1. Start with mcpanda's `amp_provider_objects` and `amp_object_fields` tools
2. Check provider's official API documentation (WebFetch)
3. Search Slab for provider-specific runbooks
4. Review actual integration code in server repo
5. Check for customer implementations using that provider

### For Customer Research:
1. Use mcpanda database query tools for org IDs and metadata
2. Search Slab for customer success stories or support history
3. Check Linear issues related to customer
4. Review integration configurations via mcpanda integration tools

### For Infrastructure Research:
1. Explore argocd repository for deployment configs
2. Use mcpanda GCP tools for live infrastructure state
3. Read server repo's build infrastructure docs
4. Check Cloud Build history and logs

### For Code/Architecture Research:
1. Start with `AGENTS.md` and `docs/interface-first-design-patterns.md` for architecture overview
2. Use Glob/Grep to explore server repository:
   - Search by service: `api/`, `temporal/`, `messenger/`, etc.
   - Search by concern: `shared/database/`, `shared/oauth/`, `shared/providers/`, etc.
3. For database patterns: Review `shared/database/README.md` and `examples/database/widget/`
4. For API endpoints: Navigate `api/routes/` for endpoint handlers
5. For provider integrations: Check `shared/providers/` and `shared/catalog/`
6. Review integration tests (`integration-tests/scenarios/`) for usage patterns
7. Use mcpanda's code analysis tools (Go AST analysis, code_analysis tool)
8. Check git history for implementation decisions: `git log -p <file>`

### For Provider Integration Research:
1. Find provider in `shared/catalog/` - lists supported providers and metadata
2. Check if provider requires special handling in `shared/providers/`
3. Review server code for provider-specific OAuth flows
4. Look for provider field mappings in integration tests
5. Search connectors repository for provider-specific implementations
6. Search Slab for provider-specific runbooks or gotchas
7. Reference provider's official API documentation (WebFetch)

### For Infrastructure & Operations Research:
1. Start with cloud-infra for GCP infrastructure setup and environments
2. Review cloud-functions for serverless patterns and implementations
3. Check argocd for K8s deployment configurations
4. Use mcpanda GCP tools for live infrastructure state
5. Review Cloud Build history and logs for CI/CD patterns
6. Check server repo's Makefile for build/deployment targets

### Research Priority Recommendations

**Tier 1 - Always Start Here (Most Valuable):**
- server - Core architecture, business logic, all APIs
- mcpanda - Tool reference and testing automation
- KNOWLEDGE-SOURCES.md - This document, for source discovery

**Tier 2 - Use When Topic-Specific (High Value):**
- argocd - For infrastructure/deployment questions
- cloud-infra - For GCP architecture questions
- connectors - For provider integration patterns
- amp-yaml-validator - For configuration validation understanding

**Tier 3 - Useful for Detailed Research (Medium Value):**
- amp-common - For shared library patterns
- amp-ctx - For environment management
- cloud-functions - For serverless/event-driven patterns
- samples - For usage examples

**Avoid Unless Specific Need:**
- temporal, sdk-go, react, etc. - Use official upstream documentation instead

### For Workflow/Operations Research:
1. Review Temporal workflow definitions in `shared/temporal/`
2. Search for operation handlers in `api/routes/read/`, `/write/`, `/proxy/`
3. Check scribe service for event ingestion patterns
4. Review messenger service for webhook delivery logic
5. Use mcpanda's Temporal workflow inspection tools

## Tools Available for Research

### File Operations
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `Read` - Read file contents
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web

### MCP Tools (via mcpanda)
- 77 production tools across all categories
- Direct access to live Ampersand systems
- Comprehensive diagnostics and monitoring

### Bash
- Run scripts, queries, git operations
- Access to command-line tools
- Database queries (when authorized)

---

**Note:** This document evolves continuously as new sources are discovered and stale sources are pruned.
**Maintained by:** knowledge-scout agent (discovers, evaluates, and curates sources)
**Used by:** knowledge-researcher agent (gathers information from these sources)
