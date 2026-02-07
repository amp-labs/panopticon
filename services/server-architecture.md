# Ampersand Server Architecture

<!--
attribution:
  source: server repository (AGENTS.md, README.md, source code analysis)
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The Ampersand server is a **Go monorepo** containing 7 microservices plus shared libraries. It is the core backend platform that enables SaaS builders to create product integrations declaratively -- instead of writing hundreds of lines of code to integrate with Salesforce, builders write 10 lines of YAML configuration.

**Repository:** `~/src/server` (use McPanda `locations` tool for dynamic resolution)
**Language:** Go
**Framework:** GoFiber (HTTP), Temporal (workflows), Google Pub/Sub (messaging)
**Database:** PostgreSQL (via GORM), Redis (caching), Google Cloud Storage (data)
**Last verified:** 2026-02-06

## What Ampersand Does

```
[Customer's SaaS] --> [Ampersand Server] --> [Builder's Application]
     |                       |                    |
Salesforce, HubSpot,    * OAuth management      * Receives clean JSON
Notion, etc.           * API calls & retries    * Via webhooks
                       * Data transformation    * Real-time delivery
                       * Error handling         * Standardized format
```

**Key components:**
- **amp.yaml file** -- Declares what data to sync and how often
- **Ampersand Server** -- Managed service that does the heavy lifting
- **Webhook endpoints** -- Builders receive clean, standardized JSON data
- **Embeddable UI components** -- End users configure integrations in the builder's app

## Resource Hierarchy

```
Organization
 +-- Projects
      +-- Integrations
      |    +-- Revisions (versions of integration configs)
      |    +-- Installations (deployed instances for specific customers)
      |         +-- Operations (sync jobs, data operations)
      +-- Connections (OAuth credentials linking to customer SaaS platforms)
      +-- Provider Apps (OAuth app configurations)
      +-- API Keys (authentication credentials)
      +-- Destinations (webhook endpoints for data delivery)
      +-- JWT Keys (for JWT-based authentication)
```

## Services Overview

| Service | Port (local) | Metrics Port | Purpose |
|---------|-------------|-------------|---------|
| **api** | 8080 | 9990 | REST API server, authentication, routing, proxy |
| **temporal** | - | 9991 | Background workflow orchestration (reads, writes, subscriptions) |
| **messenger** | - | 9992 | Pub/Sub message processing, webhook delivery |
| **scribe** | - | 9995 | Event ingestion from Pub/Sub into database |
| **token-manager** | 8082 | 9994 | Centralized OAuth token refresh service |
| **metrics** | - | 9993 | Database metrics aggregation for Prometheus |
| **builder-mcp** | - | - | MCP server for integration building |

## Service Communication Patterns

```
                   +-------+
                   |  API  |  <-- HTTP requests from builders
                   +---+---+
                       |
          +------------+------------+
          |            |            |
    +-----v----+ +----v-----+ +----v-----+
    | Temporal  | | Pub/Sub  | | Token    |
    | (queues)  | | Topics   | | Manager  |
    +-----+----+ +----+-----+ +----------+
          |            |
    +-----v----+ +----v-----+
    | Read/    | | Messenger|
    | Write    | | (webhook |
    | Workers  | |  delivery)|
    +----------+ +----+-----+
                      |
                 +----v-----+
                 | Scribe   |
                 | (DB      |
                 |  ingest) |
                 +----------+
```

**Communication mechanisms:**
1. **HTTP** -- API to Token Manager (token refresh), external webhook delivery
2. **Temporal queues** -- API triggers workflows for reads, writes, subscriptions
3. **Google Pub/Sub** -- Asynchronous messaging between services (8+ topics)
4. **PostgreSQL** -- Shared database accessed by all services
5. **Google Cloud Storage** -- Read results stored for webhook delivery
6. **Redis** -- Token caching, rate limiting state

## Shared Libraries (55+ packages)

The `shared/` directory contains common code organized by domain:

**Core domain:**
- `shared/common/` -- Domain models and types (no business logic)
- `shared/database/` -- Data access layer (GORM models, repositories, migrations)
- `shared/providers/` -- Provider integration layer (connector management)
- `shared/catalog/` -- Provider catalog and metadata

**Infrastructure:**
- `shared/ampfiber/` -- HTTP framework utilities (middleware, auth)
- `shared/pubsub/` -- Google Pub/Sub client abstraction
- `shared/gcs/` -- Google Cloud Storage client
- `shared/redis/` -- Redis client abstraction
- `shared/temporal/` -- Temporal client and queue definitions
- `shared/crypto/` -- Encryption utilities (KMS integration)

**Business logic:**
- `shared/workflow/` -- Temporal workflow definitions (read operations)
- `shared/write/` -- Write operation logic
- `shared/subscribe/` -- Subscription management
- `shared/oauth/` -- OAuth flow implementations
- `shared/token/` -- Token management logic
- `shared/delivery/` -- Webhook delivery logic

**Operations:**
- `shared/metrics/` -- Prometheus metrics configuration
- `shared/sentry/` -- Error tracking integration
- `shared/logging/` -- Request/response logging
- `shared/pprof/` -- Performance profiling
- `shared/k8sprobe/` -- Kubernetes liveness/readiness probes
- `shared/build/` -- Build information

**Other:**
- `shared/billing/` -- Billing integration (Zenskar)
- `shared/notifications/` -- Notification system
- `shared/limiter/` -- Rate limiting
- `shared/resolver/` -- Resource resolution
- `shared/utils/` -- Pure utility functions

## Directory Structure

```
server/
+-- api/                  # API service (main HTTP server)
|   +-- app/              # Fiber app setup
|   +-- routes/           # Route handlers
|   |   +-- api/          # CRUD endpoints
|   |   +-- proxy/        # Proxy endpoints
|   |   +-- read/         # Read endpoints
|   |   +-- write/        # Write endpoints
|   |   +-- signin/       # Authentication endpoints
|   |   +-- shared/       # Shared route utilities
|   +-- k8s/              # Kubernetes manifests
|   +-- tests/            # API-specific tests
+-- temporal/             # Temporal worker service
+-- messenger/            # Pub/Sub message processing
+-- scribe/               # Event ingestion service
+-- token-manager/        # OAuth token refresh service
|   +-- routes/           # Token manager HTTP endpoints
+-- metrics/              # Metrics aggregation service
+-- builder-mcp/          # MCP server for builders
+-- shared/               # 55+ shared packages
+-- database/             # Migrations, seeds, schema
|   +-- migrations/       # 107 SQL migration files
|   +-- seed/             # Test data JSON files
+-- openapi/              # OpenAPI specification
+-- scripts/              # Development scripts
+-- docker-compose/       # Local development config
+-- integration-tests/    # Integration test scenarios
+-- dbTesting/            # Database-specific tests
+-- examples/             # Reference implementations
+-- cloudbuild/           # Cloud Build configs
+-- testcerts/            # Test certificates
```

## Local Development

**Start:** `make run` (starts all services via Docker Compose)
**Verify:** `make ping`
**Reset DB:** `make refresh-db`
**Tests:** `make test` (unit), `make test/db` (database)
**Lint:** `make fix` (auto-fix), `make lint` (check)

**Local endpoints:**
- API: http://localhost:8080
- PostgreSQL: postgresql://localhost:55432
- Temporal UI: http://localhost:8081
- Token Manager: http://localhost:8082
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Fake GCS: http://localhost:8000
- Svix: http://localhost:8071
- Temporal gRPC: grpc://localhost:7233

## Authentication Methods

1. **API Key** (recommended default) -- `X-Api-Key` header
2. **JWT** (multi-tenancy) -- `Authorization: Bearer` header with group_ref/consumer_ref claims
3. **Admin Key** (debugging) -- `X-Admin-Key` header, bypasses most security
4. **Clerk** (production) -- Disabled locally, used in deployed environments

## Cross-References

- Individual service docs: `services/api.md`, `services/temporal.md`, etc.
- Infrastructure: `infrastructure/` directory
- Provider patterns: `providers/` directory
- Design patterns: `services/design-patterns.md`
- Database guide: `services/database-architecture.md`
