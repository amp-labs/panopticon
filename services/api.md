# API Service

<!--
attribution:
  source: server/api/ source code, AGENTS.md
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The **api** service is the primary HTTP server handling customer requests, authentication, resource management, and orchestrating Temporal workflows. It is the main entry point for all builder interactions with the Ampersand platform.

**Location:** `server/api/`
**Port:** 8080 (HTTP), 9990 (metrics), 6060 (pprof)
**Framework:** GoFiber
**Confidence:** HIGH

## Responsibilities

- **HTTP request handling** -- REST API for all CRUD operations on Ampersand resources
- **Authentication** -- Multi-modal auth (API keys, JWT, Clerk, Admin keys)
- **Route segregation** -- Separate API, Proxy, Read, Write, and SignIn route groups
- **Proxy service** -- Third-party API proxying (routed via `X-Amp-Request-Type: proxy` header)
- **Temporal orchestration** -- Triggers background workflows for read/write operations
- **Request validation** -- Input validation and RFC 7807 problem detail error responses

## Architecture

### Entry Point (`api/main.go`)

The main function:
1. Configures environment (startup.ConfigureEnvironment)
2. Sets up logging, Sentry, pprof, OpenTelemetry
3. Waits for database quorum
4. Initializes Temporal client
5. Creates Fiber app with auth configuration
6. Configures Kubernetes probe service
7. Starts HTTP listener

### Fiber App Setup (`api/app/`)

The Fiber app is configured with:
- **Multiple auth methods** -- Each can be independently enabled/disabled via env vars
- **Route groups** -- API, Read, Write, Proxy, SignIn (each independently toggleable)
- **Proxy isolation** -- Proxy requests routed to separate Fiber app via `X-Amp-Request-Type` header
- **Middleware** -- Request logging, OpenTelemetry tracing, metrics, CORS

### Route Groups

**API Routes (`api/routes/api/`)** -- Standard CRUD operations:
- `apiKey.go` -- API key management
- `connection.go` -- OAuth connection management
- `destination.go` -- Webhook destination management
- `installation.go` -- Installation lifecycle
- `integration.go` -- Integration configuration
- `integration_changes.go` -- Integration change tracking
- `invite.go` -- User invitations
- `jwtKey.go` -- JWT key management
- `metadata.go` -- Metadata endpoints
- `oauth.go` -- OAuth flow endpoints
- `object.go` -- Object metadata
- `operation.go` -- Operation status and history
- `org.go` -- Organization management
- `project.go` -- Project management
- `providerApp.go` -- Provider app configuration
- `providers.go` -- Provider listing/info
- `revision.go` -- Integration revision management
- `svix.go` -- Svix webhook management
- `topic.go` -- Notification topics
- `yamlValidator.go` -- amp.yaml validation

**Read Routes (`api/routes/read/`)** -- Data reading endpoints:
- `POST /v1/read/projects/{projectId}/integrations/{integrationId}/objects/{objectName}`
- Triggers Temporal read workflows
- Supports sync and async modes

**Write Routes (`api/routes/write/`)** -- Data writing endpoints:
- `POST /v1/write/projects/{projectId}/integrations/{integrationId}/objects/{objectName}`
- Data transformation and validation
- Bulk write support via Temporal workflows

**Proxy Routes (`api/routes/proxy/`)** -- Third-party API proxying:
- Transparent proxying of requests to provider APIs
- Authenticated via installation's OAuth connection
- Identified via `X-Amp-Request-Type: proxy` header

**SignIn Routes (`api/routes/signin/`)** -- Authentication endpoints:
- OAuth callback handling (`/callbacks/v1/oauth`)

### URL Structure

```
/v1/...                    -- Public API routes
/internal/v1/...           -- Internal-only routes
/callbacks/v1/...          -- OAuth callback routes
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | HTTP listen port |
| `SUBSYSTEM_NAME` | api | Service name |
| `ENABLE_API_ROUTES` | true | Enable CRUD API routes |
| `ENABLE_READ_ROUTES` | true | Enable read operation routes |
| `ENABLE_WRITE_ROUTES` | true | Enable write operation routes |
| `ENABLE_SIGNIN_ROUTES` | true | Enable authentication routes |
| `ENABLE_PROXY_ROUTE` | true | Enable proxy routes |
| `API_KEY_AUTH_DISABLED` | false | Disable API key auth |
| `ADMIN_KEY_AUTH_DISABLED` | false | Disable admin key auth |
| `JWT_TOKEN_AUTH_DISABLED` | false | Disable JWT auth |
| `CLERK_AUTH_DISABLED` | false | Disable Clerk auth |
| `LOCAL_USE_HTTPS` | false | Enable HTTPS locally |

## Dependencies

- **PostgreSQL** -- Primary data store (via shared/database)
- **Temporal** -- Workflow orchestration (read/write/subscribe)
- **Redis** -- Token caching, rate limiting
- **Google KMS** -- Encryption of sensitive data
- **Clerk** -- Production authentication (disabled locally)
- **Svix** -- Webhook delivery infrastructure

## Key Patterns

- **Multi-auth middleware** -- Each auth method checked in priority order
- **Route segregation** -- Different route groups can run as separate pods in production
- **Proxy isolation** -- Proxy requests handled by separate Fiber app to prevent interference
- **Integration resolution** -- Middleware resolves integration by ID or name
- **RFC 7807 errors** -- All errors returned as Problem Detail JSON

## Production Deployment

In production, the API service can be split into separate deployments:
- **api** -- Standard CRUD operations
- **read** -- Read operation endpoints (separate scaling)
- **write** -- Write operation endpoints (separate scaling)
- **proxy** -- Proxy endpoints (separate scaling)

This is controlled via environment variables that enable/disable route groups, with ingress routing traffic to the appropriate deployment.

## Cross-References

- Architecture overview: `services/server-architecture.md`
- Design patterns: `services/design-patterns.md`
- Token Manager: `services/token-manager.md`
- Temporal workflows: `services/temporal.md`
