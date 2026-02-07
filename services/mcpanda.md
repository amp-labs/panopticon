---
validation_metadata:
  attribution:
    source: "/Users/chris/src/mcpanda"
    source_type: "code"
    obtained_date: "2026-02-06"
    obtained_by: "knowledge-researcher"
  validation:
    last_checked: "2026-02-06 14:30"
    checked_by: "knowledge-researcher"
    status: "accurate"
    notes: "Initial documentation from source repository exploration"
---

# McPanda - MCP Server for Ampersand Integration Testing

**Quick Reference:** Model Context Protocol server that simplifies complex integration testing workflows into single orchestrated calls
**Category:** Developer Tooling / MCP Services
**Status:** Production (77 tools, 100% complete)
**Repository:** `/Users/chris/src/mcpanda` (location varies by machine - use `locations` tool)

## Overview

McPanda is a Model Context Protocol (MCP) server that transforms Ampersand's complex integration testing workflows from multi-step manual processes into single orchestrated tool calls [source: README.md:1-3].

**Problem it solves:**
- **Before:** Multiple script coordination (`./create_provider_app.py`, `./setup_webhook_testing.py`), manual OAuth flows in browsers (MailMonkey), complex environment setup (`source vars.sh`, kubectl access), manual verification of webhook data and operations, tedious resource cleanup [source: CLAUDE.md:19-25]
- **After:** Single MCP tool calls that handle all complexity internally

**Integration with Ampersand development:**
- Used by AI agents (Claude, custom tools) to test integrations
- Provides 77 production-ready tools across 12 categories [source: README.md:7]
- Integrates with amp-ctx for automatic environment detection [source: README.md:909-936, CLAUDE.md:144-150]
- Supports localhost, dev, staging, prod, and PR environments [source: CLAUDE.md:146]

## Architecture

### MCP Protocol Compliance

McPanda implements the Model Context Protocol specification (version 2024-11-05) with three transport mechanisms [source: CLAUDE.md:31-39]:

1. **stdio transport** - Standard MCP via stdin/stdout (`--stdio` flag)
2. **Streamable HTTP transport** - Unified HTTP with optional SSE streaming
   - POST /mcp for JSON-RPC requests
   - GET /mcp for SSE streaming (real-time tool updates)
   - Security: origin validation, localhost binding, protocol headers
3. **WebSocket support** - Bonus extension (not part of MCP spec)

### Core Components

**Technology Stack:** Go server with JSON Schema validation [source: CLAUDE.md:40-41]

**Context Management System:**
- Primary context source: amp-ctx integration with automatic environment detection [source: CLAUDE.md:144]
- Context priority: Environment override → amp-ctx → config file → localhost [source: CLAUDE.md:148]
- ArgoCD integration: Direct metadata.json.noargo file parsing for environment discovery [source: CLAUDE.md:147]
- Real context switching via `set_context`, `get_context`, `list_contexts` tools [source: CLAUDE.md:149]

**Authentication:**
Automatic authentication selection based on context [source: CLAUDE.md:144-145]:
- API Key authentication
- JWT authentication
- Admin Key authentication

### MCP Resources

McPanda provides documentation resources via the MCP resources protocol:
- `mcpanda://index.md` - Comprehensive quick reference covering all 77 tools, common workflows, authentication methods, and usage tips [source: CLAUDE.md:7-13]

### MCP Prompts

McPanda provides pre-configured prompts for specialized workflows:
- `maintenance` - Autonomous Panopticon maintenance round. Self-directed background work including quality gates, housekeeping, and small improvements. Usage: `/mcpanda:maintenance` [source: prompts/maintenance.go]

## Tool Categories (77 Tools Total)

### Context Management (6 tools) [source: README.md:9-15, CLAUDE.md:43-49]

- `get_context` - Get currently active context with configuration details
- `set_context` - Switch between environments (localhost, dev, staging, prod, PR branches)
- `list_contexts` - List all available contexts with health status
- `set_context_auth` - Override authentication method for current context
- `set_session_vars` - Set session variable overrides for testing
- `get_session_vars` - Get current session variable overrides

### Integration Management (3 tools) [source: README.md:17-20, CLAUDE.md:51-54]

- `integration_deploy` - Deploy and validate integration configs via REST API
- `integration_status` - Get integration status including installations and health
- `integration_cleanup` - Reliable resource cleanup with REST API

### Connection Management (8 tools) [source: README.md:22-30, CLAUDE.md:56-64]

- `connection_list` - List OAuth connections with filtering and status
- `connection_status` - Get detailed connection status and health
- `connection_test` - Test connection validity with real API calls
- `connection_refresh` - Force refresh of OAuth tokens
- `connection_create` - Create connections from existing OAuth tokens
- `connection_delete` - Delete connections and revoke tokens
- `connection_monitor` - Monitor connection health and token expiration
- `oauth_token_copy` - Copy OAuth tokens from dev instance for testing

### System Health (2 tools) [source: README.md:32-34, CLAUDE.md:66-68]

- `system_health_check` - Comprehensive health check with context-aware API validation
- `locations` - Get repository and service location mappings from amp-ctx

### amp.yaml Configuration (8 tools) [source: README.md:36-43, CLAUDE.md:70-78]

- `amp_provider_objects` - Get standard objects available for a provider
- `amp_object_fields` - Get standard fields for a specific provider object
- `amp_config_generate` - Generate complete amp.yaml from high-level description
- `amp_config_validate` - Validate amp.yaml against schema and provider capabilities
- `amp_config_enhance` - Enhance existing amp.yaml with additional objects/fields
- `amp_config_validate_contents` - Validate amp.yaml content structure
- `amp_examples_get` - Get example configurations by provider or use case
- `amp_migration_status` - Check database migration status across environments

### Temporal Workflow Management (7 tools) [source: README.md:45-53, CLAUDE.md:80-87]

- `workflow_inspect` - Inspect workflow execution details
- `workflow_search` - Search for workflows by criteria
- `workflow_retry` - Retry failed workflows
- `workflow_cancel` - Cancel running workflows
- `workflow_timeline` - Get detailed workflow execution timeline
- `workflows_monitor` - Monitor multiple workflows in real-time
- `amp_temporal_workflow_inspect` - Enhanced workflow inspection

### Testing & Automation (6 tools) [source: README.md:55-60, CLAUDE.md:89-95]

- `integration_test_run` - Complete end-to-end test orchestration
- `test_data_inject` - Trigger immediate data flow for testing
- `installation_simulate` - Bypass browser OAuth for automated testing
- `amp_integration_test_orchestrate` - Advanced test orchestration
- `amp_load_test_runner` - Load testing for integrations
- `amp_data_validation` - Validate data flow and transformations

### Provider & Authentication (4 tools) [source: README.md:62-67, CLAUDE.md:97-101]

- `provider_app_create` - Handle credential retrieval and provider app setup with 1Password
- `oauth_session_create` - Programmatic OAuth initiation with flow management
- `oauth_session_status` - Monitor OAuth completion with polling
- `oauth_token_copy` - Copy OAuth tokens from dev instance for testing

### Webhook & Data Monitoring (4 tools) [source: README.md:69-73, CLAUDE.md:103-107]

- `webhook_endpoint_create` - Handle tunnel creation (ngrok, local, custom URLs)
- `webhook_data_monitor` - Active monitoring with operations endpoint polling
- `webhook_data_validate` - Structured validation with pattern matching
- `kinesis_endpoint_create` - AWS Kinesis endpoint creation

### Advanced Diagnostics (17 tools) [source: README.md:75-92, CLAUDE.md:109-126]

- `integration_doctor` - Comprehensive diagnostics with API health checks
- `error_analyze` - Analyze and categorize errors with pattern matching
- `operation_monitor` - Real-time operation monitoring
- `temporal_logs_stream` - Stream Temporal workflow logs
- `logs_pattern_search` - Search logs for specific patterns
- `environment_setup` - Set up environment variables and context
- `amp_logs_stream` - Stream logs from Ampersand services
- `amp_service_restart` - Restart services in local environment
- `amp_health_check_comprehensive` - Deep health checks across all services
- `amp_local_env_setup` - Set up local development environment
- `amp_error_correlation` - Correlate errors across services
- `amp_code_analysis` - Analyze code for common issues
- `amp_incident_analyzer` - Analyze incidents and root causes
- `amp_data_validation` - Validate data flow and transformations
- `amp_integration_test_orchestrate` - Advanced test orchestration
- `amp_load_test_runner` - Load testing for integrations
- `amp_temporal_workflow_inspect` - Enhanced workflow inspection

### HTTP API Operations (6 tools) [source: README.md:94-100, CLAUDE.md:128-134]

- `list_http_endpoints` - List available HTTP endpoints (api, read, write, proxy) for current context
- `list_http_operations_for_endpoint` - List all OpenAPI operations for a specific endpoint
- `describe_http_operation` - Get detailed, fully resolved OpenAPI documentation for an operation
- `invoke_http_operation` - Invoke HTTP operations with automatic credential injection and schema validation
- `get_build_info` - Get build information from the API server
- `ping` - Ping the API server to check if it's responding

### GCP Monitoring & Observability (5 tools) [source: CLAUDE.md:136-141]

- `gcp_monitoring_query_timeseries` - Query Cloud Monitoring metrics with aggregation and filtering
- `gcp_monitoring_list_incidents` - List active and recent incidents with severity and affected resources
- `gcp_observability_get_service_health` - Aggregated service health combining error rates, latency, and incidents
- `gcp_observability_get_operation_trace` - Complete operation context with logs, traces, Pub/Sub, and GCS
- `gcp_observability_get_error_summary` - Error summary across services with grouping and trends

## Common Workflows

### Integration Testing End-to-End

**Typical workflow using McPanda:**

1. **Set up context:** `set_context` to switch to desired environment (dev/staging/prod)
2. **Deploy integration:** `integration_deploy` with amp.yaml configuration
3. **Create provider app:** `provider_app_create` retrieves credentials from 1Password
4. **Set up OAuth:** `oauth_session_create` initiates OAuth flow, `oauth_session_status` monitors completion
5. **Create webhook endpoint:** `webhook_endpoint_create` handles tunnel creation (ngrok/local)
6. **Simulate installation:** `installation_simulate` bypasses browser OAuth for automated testing
7. **Inject test data:** `test_data_inject` triggers immediate data flow
8. **Monitor webhook data:** `webhook_data_monitor` polls operations endpoint
9. **Validate data:** `webhook_data_validate` performs structured validation
10. **Check status:** `integration_status` confirms health and operations
11. **Clean up:** `integration_cleanup` removes all resources

**Before McPanda:** This required coordinating 5+ separate scripts, manual browser OAuth, manual verification steps, and complex cleanup logic.

**With McPanda:** Single orchestrated call via `integration_test_run` handles all steps.

### Debugging Integration Issues

1. **Run diagnostics:** `integration_doctor` performs comprehensive health checks
2. **Analyze errors:** `error_analyze` categorizes errors with pattern matching
3. **Monitor operations:** `operation_monitor` provides real-time operation monitoring
4. **Check workflows:** `workflow_inspect` examines Temporal workflow execution
5. **Stream logs:** `temporal_logs_stream` or `amp_logs_stream` for detailed logging
6. **Correlate errors:** `amp_error_correlation` finds related errors across services

### Environment Management

1. **List available contexts:** `list_contexts` shows all environments with health status
2. **Switch environment:** `set_context` changes to localhost/dev/staging/prod
3. **Override auth:** `set_context_auth` changes authentication method
4. **Verify health:** `system_health_check` confirms API accessibility
5. **Get locations:** `locations` retrieves repository paths for current machine

## Integration with Ampersand Services

McPanda integrates with multiple Ampersand services:

- **API Service:** REST API calls for integration management, connection handling
- **Temporal:** Workflow inspection, monitoring, retry/cancel operations
- **GCP Infrastructure:** Cloud Monitoring metrics, incidents, observability
- **1Password:** Secure credential retrieval for provider apps
- **ArgoCD:** Environment discovery via metadata.json.noargo parsing

## Related Components

- **amp-ctx** → Context management and environment detection (external tool, not yet documented in Panopticon)
- **builder-mcp** → MCP server for integration builders (see `services/builder-mcp.md` - listed in services-index.md)
- **API Service** → REST API server (see `services/api.md` - TBD)
- **Temporal** → Workflow orchestration (see `services/temporal.md` - TBD)
- **GCP Infrastructure** → Cloud platform (see `infrastructure-index.md`)

## Source References

**Primary sources:**
- Repository: `/Users/chris/src/mcpanda` (path varies by machine)
- Documentation: `README.md`, `CLAUDE.md` in repository
- MCP Resource: `mcpanda://index.md` for quick reference

**Validated:** 2026-02-06 by knowledge-researcher via direct repository exploration
