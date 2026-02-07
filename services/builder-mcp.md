# Builder MCP Service

<!--
attribution:
  source: server/builder-mcp/ directory (full source), CLAUDE.md, main.go, mcp.go, tools/registry.go, core/, Dockerfile, ENV_VARS.md
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The **builder-mcp** service is a Model Context Protocol (MCP) server that assists developers ("builders") with creating and managing Ampersand integrations. It exposes **90+ tools** and **30+ resources** via the MCP protocol, enabling AI agents (Claude, VSCode Copilot, etc.) to help builders create, configure, debug, and maintain integrations with SaaS providers.

**Location:** `server/builder-mcp/`
**Language:** Go (compiled binary)
**Framework:** MCP protocol via `github.com/eberle1080/mcp-protocol` and `github.com/eberle1080/mcp`
**Web Framework:** Fiber (via `server/shared/ampfiber`)
**Default Port:** 8080
**Confidence:** HIGH (full source code review)

## Architecture

```
+---------------------+
|   MCP Client        |  (Claude Code, VSCode, etc.)
|  - Sampling Support |
|  - Elicitation      |
+----------+----------+
           | JSON-RPC over stdio/SSE/Streamable HTTP
           v
+---------------------+
|  Builder MCP Server  |
|  - Tool Registry     |  (90+ tools in 16 categories)
|  - Resource Registry |  (30+ resources in 8 categories)
|  - Completions       |  (IDE autocompletion support)
|  - State Machines    |  (multi-step guided workflows)
|  - Memory Service    |  (chromem-go vector store)
|  - Alarm Worker      |  (scheduled reminders)
|  - Session Metrics   |  (Prometheus tracking)
|  - i18n              |  (internationalization)
+----------+----------+
           |
           v
+---------------------+
|  Ampersand API      |  (PostgreSQL, Redis, shared packages)
+---------------------+
```

### Key Design Decisions

1. **Dynamic Handler Factory** - Each MCP connection gets its own handler instance, preventing cross-session contamination. Server-level configuration (maturity levels, disabled tools) is merged into per-connection contexts.

2. **Progressive Disclosure** - Tools are organized by journey phase (Discovery, Configuration, Implementation, Testing, Production, Troubleshooting) and complexity level (Beginner, Intermediate, Advanced) so agents suggest appropriate tools at each stage.

3. **Maturity-Based Filtering** - Tools have maturity levels (1-5) and environments filter by minimum maturity: dev shows all (1+), staging shows experimental+ (3+), prod shows battle-tested only (5).

4. **Dual Transport Modes** - Supports both HTTP mode (default, for deployed services) and stdio mode (for local development via `MCP_TRANSPORT=stdio`).

5. **Tool-as-Data Pattern** - Tools are registered via a centralized `ToolRegistry` in `tools/registry.go` using a factory pattern. Each tool definition includes metadata (category, complexity, journey phases, maturity, use cases, prerequisites, related tools).

## Package Structure

```
builder-mcp/
|-- main.go                    # Entry point, server initialization, HTTP/stdio setup
|-- mcp.go                     # SetupMCP - registers tools, resources, prompts with server
|-- tool.go                    # Legacy Builder type (being migrated to core/builder.go)
|-- prompts.go                 # MCP prompts (agent survey, commit workflow)
|
|-- core/                      # Core framework
|   |-- builder.go             # Type-safe tool builder with schema generation
|   |-- tool_registry.go       # Global tool registry
|   |-- tool_metadata.go       # Categories, complexity, journey phases, maturity levels
|   |-- tool_metrics.go        # Prometheus metrics per tool
|   |-- session.go             # Session validation, retry logic, health checks
|   |-- session_metrics.go     # Session tracking for Prometheus
|   |-- resource_metrics.go    # Resource access metrics
|   |-- elicitation.go         # User input forms, confirmations, choices
|   |-- sampling.go            # LLM completion requests
|   |-- errors.go              # Structured error types with suggested actions
|   |-- error_knowledge_base.go # Error pattern matching and explanations
|   |-- retry.go               # Configurable retry with exponential backoff
|   |-- mcp_logger.go          # MCP-protocol structured logging wrapper
|   |-- param_validator.go     # Input validation
|   |-- version.go             # Protocol version management
|   |-- utils.go               # Context helpers, configuration propagation
|   +-- amplinks_client.go     # amp:// URI scheme client
|
|-- tools/                     # 90+ MCP tools organized by category
|   |-- registry.go            # Centralized ToolDefinition registry
|   |-- validation/            # validate_amp_yaml, amp_dry_run_validation
|   |-- provider/              # amp_suggest_scopes, amp_validate_credentials, amp_search_provider_standard_objects
|   |-- crud/                  # CRUD operations
|   |   |-- api_keys/          # amp_create/update/delete_api_key
|   |   |-- connections/       # amp_create/delete/refresh_connection, amp_create_oauth_url
|   |   |-- destinations/      # amp_create/update/delete_destination
|   |   |-- installations/     # amp_create/update/delete_installation
|   |   |-- integrations/      # amp_update/delete_integration, deploy_amp_yaml
|   |   |-- projects/          # amp_update_project
|   |   +-- provider_apps/     # amp_create/update/delete_provider_app
|   |-- diagnostics/           # amp_troubleshooting_doctor, amp_integration_debugger, kinesis debug
|   |-- conventions/           # amp_detect/store/list/resolve/update/delete_convention
|   |-- help/                  # amp_contextual_help, amp_search_integration_examples
|   |-- integration/           # amp_analyze_project_context, amp_review_integration_code
|   |-- navigation/            # amp_suggest_next_steps, amp_search_ampersand, amp_explain_error
|   |-- operations/            # amp_search_operations, amp_validate_integration, openapi operations, proxy/invoke
|   |-- provider/              # Provider information and scope suggestion
|   |-- resources/             # amp_list/search/get_resource_info
|   |-- security/jwt/          # amp_generate_rsa_keypair, amp_validate/parse_jwt_token, amp_rotate_keypair
|   |-- setup/                 # amp_bootstrap_project, amp_guided_setup, wizards (database, frontend, error handling, security)
|   |-- shared/                # amp_generate_uuid, amp_get_project_context
|   |-- testing/               # amp_test_connection, amp_test_oauth_flow, amp_validate_config, webhook testing
|   |-- workflow/              # Schedule management, trigger read, proxy operations
|   |   |-- alarms/            # amp_set/check/list/cancel_alarm (background worker)
|   |   |-- feedback/          # amp_submit_feedback, amp_collect_feedback_note/bug_report/feature_request
|   |   |-- memory/            # amp_store/search/list/get/delete_memory (vector store)
|   |   +-- survey/            # amp_administer_survey
|   +-- advanced/              # amp_migration_assistant, amp_integration_assistant
|
|-- resources/                 # 30+ MCP resources (data endpoints)
|   |-- registry.go            # Centralized resource registry
|   |-- builder.go             # Resource builder pattern
|   |-- crud/                  # CRUD-related resources
|   |-- customer_guides/       # Customer-facing guides
|   |-- diagnostics/           # Diagnostic data resources
|   |-- docs/                  # Documentation resources, server uptime
|   |-- openapi/               # OpenAPI spec resources
|   |-- providers/             # Provider catalog resources
|   |-- repos/                 # Git repository resources (cached, background updated)
|   +-- surveys/               # Survey resources
|
|-- completions/               # MCP completion handlers (IDE autocompletion)
|   |-- handler.go             # CompletionHandler interface and registry
|   |-- server_handler.go      # Handler wrapping with completion support
|   |-- connections.go         # Connection name completions
|   |-- installations.go       # Installation name completions
|   |-- integrations.go        # Integration name completions
|   |-- objects.go             # Object name completions
|   |-- operations.go          # Operation name completions
|   |-- projects.go            # Project name completions
|   |-- providers.go           # Provider name completions (fuzzy matching)
|   +-- fuzzy.go               # Fuzzy string matching for completions
|
|-- statemachine/              # State machine framework for multi-step workflows
|   |-- helpers.go             # SampleWithGracefulFallback, SampleForExplanation
|   |-- actions/               # Reusable state machine actions (elicit with retry, etc.)
|   +-- examples/              # Example state machine configurations
|
|-- config/                    # Embedded YAML configs for state machine workflows
|   +-- config-data/           # guided_setup, troubleshooting_doctor, migration_assistant, etc.
|
|-- validation/                # Configuration validation framework
|   |-- framework.go           # Validation framework with checkers
|   |-- context.go             # Context-aware validation using embedded YAML chunks
|   |-- scope_mapper.go        # OAuth scope mapping
|   |-- embedded_scopes.go     # Embedded scope data
|   +-- various checkers       # destination, oauth_env, provider_app, rate_limit checkers
|
|-- memory/                    # Persistent long-term memory service
|   |-- service.go             # MemoryService (chromem-go vector DB, per-project segmentation)
|   |-- codebase_cache.go      # Codebase file caching
|   +-- local_embedding.go     # Local embedding generation
|
|-- codegen/                   # Code generation utilities
|   +-- schema_generator.go    # Zod schema generation from field configs
|
|-- helpers/                   # Shared helpers
|   |-- continuation_signals.go # Signals for multi-turn conversations
|   |-- dashboard_links.go     # Generate Ampersand dashboard URLs
|   +-- proactive_context.go   # Proactive context injection
|
|-- internal/                  # Internal packages
|   |-- benchutil/             # Benchmark utilities
|   |-- catalogs/              # Internal catalog generation
|   +-- i18n/                  # Internationalization bundle
|
|-- workers/                   # Background workers
|   +-- token_refresh_worker.go # OAuth token refresh monitoring (currently monitoring-only)
|
|-- shared/                    # Builder-MCP specific shared utilities
|   |-- middleware/            # Warning deduplication middleware
|   +-- utils/                 # Schedule parsing utilities
|
|-- docs/                      # Extensive internal documentation (25+ files)
|-- examples/                  # Integration examples (HubSpot, Salesforce, hybrid)
|-- instructions/              # Progressive discovery instructions for MCP clients
|-- scripts/                   # Helper scripts
+-- k8s/                       # Production Dockerfile (multi-stage: debug + release)
```

## Tool Categories (90+ Tools)

| Category | Count | Examples | Description |
|----------|-------|---------|-------------|
| Validation | ~4 | `validate_amp_yaml`, `amp_dry_run_validation` | Configuration validation without deployment |
| Provider | ~4 | `amp_suggest_scopes`, `amp_validate_credentials`, `amp_search_provider_standard_objects` | Provider discovery and OAuth scope suggestion |
| CRUD | ~18 | `amp_create_connection`, `deploy_amp_yaml`, `amp_delete_installation` | Resource lifecycle management |
| Diagnostics | ~5 | `amp_troubleshooting_doctor`, `amp_integration_debugger`, `amp_debug_kinesis_stream` | Troubleshooting and debugging |
| Conventions | ~5 | `amp_detect_repo_conventions`, `amp_store_convention` | Codebase convention detection and storage |
| Help | ~2 | `amp_contextual_help`, `amp_search_integration_examples` | Contextual help and example search |
| Integration | ~2 | `amp_analyze_project_context`, `amp_review_integration_code` | Code analysis and review |
| Navigation | ~3 | `amp_suggest_next_steps`, `amp_explain_error` | Guidance and error explanation |
| Operations | ~10 | `amp_search_operations`, `amp_openapi_invoke_operation`, `amp_invoke_proxy` | Runtime operations and OpenAPI |
| Resources | ~3 | `amp_list_resources`, `amp_search_resources` | Resource discovery |
| Security/JWT | ~4 | `amp_generate_rsa_keypair`, `amp_validate_jwt_token` | JWT and RSA key management |
| Setup | ~8 | `amp_bootstrap_project`, `amp_guided_setup`, `amp_database_wizard` | Project bootstrapping and wizards |
| Testing | ~6 | `amp_test_connection`, `amp_test_oauth_flow`, `amp_test_webhook_locally` | Integration testing |
| Workflow | ~12 | `amp_pause_schedule`, `amp_trigger_read`, `amp_send_preview_message` | Schedule and proxy operations |
| Alarms | ~4 | `amp_set_alarm`, `amp_check_alarms` | Reminder system |
| Memory | ~7 | `amp_store_memory`, `amp_search_memory` | Vector-based memory storage |
| Feedback | ~8 | `amp_submit_feedback`, `amp_collect_bug_report` | Feedback and survey collection |
| Advanced | ~2 | `amp_migration_assistant`, `amp_integration_assistant` | Advanced multi-step workflows |

## MCP Capabilities

The builder-mcp server exposes these MCP protocol capabilities:

### Tools
90+ callable functions organized by category, complexity, and journey phase. Each tool is registered with metadata for progressive disclosure.

### Resources
30+ data endpoints using `amp://` URI scheme, organized into: CRUD, customer guides, diagnostics, docs, OpenAPI, providers, repos, and surveys.

### Prompts
Two registered MCP prompts:
- **agent-survey** - Post-integration survey for UX feedback (two parts: user survey + agent assessment)
- **commit** - Autonomous git commit workflow with quality gates (takes `expected_branch` and `commit_message`)

### Completions
IDE autocompletion support for: providers (fuzzy matching), projects, integrations, installations, connections, objects, and operations.

### Sampling
Tools can request LLM completions from the connected client for dynamic, context-aware responses. Used with graceful fallbacks when sampling is unavailable.

### Elicitation
Tools can request structured user input via forms, confirmations, and choices. Supports capability detection and retry with validation.

### Logging
Structured log messages via MCP `notifications/message` (connection-scoped, not global).

### Experimental
Protocol version information exposed via `ServerCapabilities.Experimental`.

## State Machine Workflows

Complex multi-step tools use embedded YAML-configured state machines:

| Workflow | Config File | Purpose |
|----------|------------|---------|
| Guided Setup | `guided_setup.yaml` | Interactive onboarding for new integrations |
| Troubleshooting Doctor | `troubleshooting_doctor.yaml` | Diagnostic workflow for issues |
| Migration Assistant | `amp_migration_assistant.yaml` | Migration between providers/versions |
| Frontend Decision Wizard | `amp_frontend_decision_wizard.yaml` | Frontend framework selection |
| Integration Assistant | `integration_assistant.yaml` | Guided integration creation |

State machine workflows support:
- Multi-phase progression with branching logic
- Elicitation-based user interaction with retry
- Sampling for dynamic content generation
- Action composition via `statemachine/actions/`

## Memory Service

The builder-mcp includes a persistent vector-based memory service (`memory/service.go`) using **chromem-go**:
- **Per-project segmentation** - Memories are isolated by project ID
- **Semantic search** - Vector similarity search via local embeddings
- **Persistent storage** - File-based persistence (not RAM-only)
- **Operations** - Store, search, list, get, delete memories; project-level deletion; stats

## Background Workers

### Alarm Worker
Started at server initialization (`alarms.StartAlarmWorker`). Provides scheduled reminder functionality via `amp_set_alarm`, `amp_check_alarms`, `amp_list_alarms`, `amp_cancel_alarm` tools.

### Token Refresh Worker
Monitors OAuth token expiration every 15 minutes. Currently in **monitoring mode only** -- logs warnings for tokens expiring within 24 hours but does not auto-refresh (requires system-level API key permissions to implement).

### Session Metrics Tracker
Tracks active MCP sessions and updates Prometheus metrics. Started at initialization, gracefully stopped on shutdown.

## Transport Modes

The service supports two transport modes controlled by `MCP_TRANSPORT` environment variable:

| Mode | Endpoints | Use Case |
|------|----------|----------|
| **HTTP** (default) | `/v1/mcp` (Streamable HTTP), `/v1/sse`, `/v1/message` | Deployed services |
| **stdio** | stdin/stdout | Local development, Claude Code integration |

HTTP mode also provides:
- **OAuth endpoints** for Claude Code compatibility (dummy/open access)
- **Build info** at `/internal/v1/build`
- **K8s probes** for liveness/readiness
- **Sentry** integration (optional via `ENABLE_SENTRY_AGENT_MCP`)
- **OpenTelemetry** tracing (optional)
- **Fiber request/response logging**

Streamable HTTP mode can be enabled via `MCP_USE_STREAMABLE_HTTP=true`.

## Authentication

- **API Key authentication** - Enabled by default for HTTP mode
- **Admin Key authentication** - Enabled by default
- Per-tool permission checks via `apikeys.CheckProjectReadAccess`
- Session-scoped authorization via `AuthorizeMCP`

## Environment Configuration

Key environment variables (from `ENV_VARS.md`):

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MIN_MATURITY_SERVER` | int(1-5) | env-based | Absolute minimum tool maturity level |
| `MIN_MATURITY_DEFAULT` | int(1-5) | none | Default maturity when caller unspecified |
| `SHOW_DEVELOPER_TOOLS` | bool | false | Enable developer-only tools |
| `SHOW_DEMO_TOOLS` | bool | false | Enable demo-only tools |
| `MCP_DISABLED_TOOLS` | string | none | Comma-separated list of tools to disable |
| `MCP_TRANSPORT` | string | "http" | Transport mode: "http" or "stdio" |
| `MCP_USE_STREAMABLE_HTTP` | bool | false | Enable Streamable HTTP transport |
| `MCP_INSTRUCTIONS_FILE` | string | none | Custom instructions file path |
| `MCP_INSTRUCTIONS` | string | none | Custom instructions string |
| `ENABLE_SENTRY_AGENT_MCP` | bool | false | Enable Sentry error tracking |
| `PORT` | int | 8080 | HTTP listen port |

### Maturity Defaults by Environment
- **dev/local/test**: 1 (all tools visible)
- **staging**: 3 (experimental and above)
- **prod**: 5 (battle-tested only)

## Internationalization

The service includes an i18n translation bundle (`internal/i18n/`) initialized at startup. Locale can be set via:
- `locale` query parameter on connection
- `Accept-Language` HTTP header

## Deployment

### Docker Build
Multi-stage Dockerfile in `k8s/Dockerfile`:
1. **Build stage** - Compiles Go binary with `CGO_ENABLED=0`, PIE mode, build VCS info
2. **Debug stage** - Alpine with Delve debugger on port 40000
3. **Release stage** - Alpine with just the binary

Both stages include `instructions/`, `docs/`, and `examples/` directories. The `MCP_INSTRUCTIONS_FILE` is set to `/app/instructions/progressive_discovery.md`.

### Dependencies
- **Go 1.25** (from Dockerfile)
- **PostgreSQL** - Database for projects, integrations, connections, etc.
- **Redis** (optional) - Session store (falls back to in-memory)
- **chromem-go** - Vector database for memory service
- **amp-common** - Shared utilities (env, logging, stage, shutdown, telemetry, etc.)
- **amp-yaml-validator** - YAML configuration validation
- **connectors** - Provider connector library

### Exposed Ports
| Port | Purpose |
|------|---------|
| 6060 | pprof profiling |
| 7070 | Prometheus metrics |
| 8080 | HTTP/MCP endpoint |
| 9090 | K8s probes |
| 40000 | Delve debugger (debug build only) |

### Production URLs
- Dev: `https://dev-builder-mcp.withampersand.com`
- Staging: Similar pattern
- Prod: Similar pattern

## Safe Words

The builder-mcp supports "safe word" triggers for quick feedback collection during agent interactions:

| Safe Word | Tool | Purpose |
|-----------|------|---------|
| `AMPFEEDBACK` / `AMPNOTE` | `amp_collect_feedback_note` | Quick notes, observations, suggestions |
| `AMPBUG` | `amp_collect_bug_report` | Structured bug reports |
| `AMPFEATURE` | `amp_collect_feature_request` | Feature requests with use cases |

When triggered, the agent pauses its current task, collects feedback, then resumes.

## Integration Examples

The service includes example integration configurations in `examples/integrations/`:
- `hubspot-contacts-companies` - HubSpot contacts and companies
- `hubspot-custom-properties` - HubSpot custom property handling
- `hybrid-calcom-hubspot` - Hybrid Cal.com + HubSpot integration
- `salesforce-field-transformations` - Salesforce field transformation patterns
- `salesforce-opportunities-line-items` - Salesforce opportunities with line items

## Distinction from McPanda

| Aspect | Builder MCP | McPanda |
|--------|------------|---------|
| **Purpose** | Help builders create integrations | Internal operations/testing |
| **Audience** | External developers, AI agents | Ampersand team, internal agents |
| **Location** | `server/builder-mcp/` | Separate repository (`mcpanda/`) |
| **Tool Count** | 90+ tools | 77 tools |
| **Deployment** | Part of server, own K8s service | Standalone service |

## Cross-References

- Architecture overview: `services/server-architecture.md`
- McPanda (operations MCP): `services/mcpanda.md`
- API service: `services/api.md`
- Design patterns: `services/design-patterns.md`
- Database architecture: `infrastructure/database-architecture.md`
- Deployment pipeline: `infrastructure/deployment-pipeline.md`
- Provider integration patterns: `providers/provider-integration-patterns.md`
