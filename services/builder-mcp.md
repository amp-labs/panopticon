# Builder MCP Service

<!--
attribution:
  source: server/builder-mcp/ directory, AGENTS.md, argocd-infrastructure.md
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The **builder-mcp** service is an MCP (Model Context Protocol) server that assists builders with creating and managing Ampersand integrations. It provides AI-agent-accessible tools for integration building, configuration, and debugging.

**Location:** `server/builder-mcp/`
**Framework:** MCP protocol
**Confidence:** MEDIUM (limited source visibility -- directory contains `bin/` only, suggesting built binary)

## Responsibilities

- **Integration building assistance** -- Helps builders create amp.yaml configurations
- **Configuration validation** -- Validates integration configurations
- **Provider information** -- Provides provider metadata and capabilities
- **Debugging support** -- Assists with troubleshooting integration issues

## Architecture

The builder-mcp directory in the server repo appears to contain a pre-built binary (`bin/`). The actual MCP tool implementations are likely managed separately or compiled into the binary.

**Note:** This is distinct from **McPanda**, which is a separate MCP server for Ampersand operations/testing (documented in `services/mcpanda.md`). Builder-MCP is specifically for builders creating integrations.

## Deployment

In production environments, builder-mcp is deployed as a separate service with its own endpoint:
- Dev: `https://dev-builder-mcp.withampersand.com`
- Staging: Similar pattern
- Prod: Similar pattern

In dev environments, it runs as a separate deployment (not collapsed into the API pod).

## Available Tools

The builder-mcp server provides tools accessible via the MCP protocol. These include (based on deferred tool listing):

- Integration management (create, update, delete, validate)
- Provider search and information
- Configuration generation and enhancement
- OAuth flow assistance
- Connection management
- Webhook testing and debugging
- Error explanation and handling
- Database schema generation
- Project bootstrapping
- And many more specialized tools

See the McPanda/builder-mcp tool listing in the Panopticon for the full catalog.

## Dependencies

- **PostgreSQL** -- Integration and provider data
- **Provider catalog** -- Provider metadata and capabilities

## Cross-References

- Architecture overview: `services/server-architecture.md`
- McPanda (operations MCP): `services/mcpanda.md`
- Provider integration patterns: See provider documentation
