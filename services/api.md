---
validation_metadata:
  attribution:
    source: server/api/ source code, AGENTS.md, api/routes/route.go (full route listing)
    obtained_date: 2026-02-06
    obtained_by: knowledge-researcher
  validation:
    last_checked: 2026-02-06
    status: current
---

# API Service
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
- `apiKey.go` -- API key management (CRUD + admin creation)
- `builder.go` -- Clerk webhook handler for user lifecycle events (created/updated/deleted)
- `claimedDomains.go` -- Domain claiming for org-level domain registration and validation
- `connection.go` -- OAuth connection management (list, get, update, delete, generate, oauth-update)
- `destination.go` -- Webhook destination management (CRUD)
- `installation.go` -- Installation lifecycle (CRUD + import + pause/unpause + backfill progress)
- `integration.go` -- Integration configuration (CRUD + batch upsert)
- `integration_changes.go` -- Integration change tracking
- `invite.go` -- User invitations (CRUD for org invites + accept)
- `jwtKey.go` -- JWT key management (CRUD + update)
- `metadata.go` -- Object metadata endpoints (get/upsert for installations and connections)
- `metrics.go` -- Prometheus metrics definitions (Svix failures, OAuth callback counters)
- `myInfo.go` -- Authenticated user info endpoint (Clerk-only, returns builder profile and roles)
- `notificationEventTopicRoute.go` -- Notification event topic routing (CRUD)
- `oauth.go` -- OAuth flow endpoints (connect, start, callback)
- `object.go` -- Object metadata queries
- `operation.go` -- Operation status, history, and logs
- `org.go` -- Organization management (CRUD + builders + billing account)
- `project.go` -- Project management (CRUD)
- `providerApp.go` -- Provider app configuration (CRUD)
- `providers.go` -- Provider listing/info (public, no auth required)
- `revision.go` -- Integration revision management (create + hydrated get)
- `svix.go` -- Svix operational webhook handler
- `topic.go` -- Notification topics (CRUD)
- `topicDestinationRoute.go` -- Topic-to-destination routing (CRUD)
- `yamlValidator.go` -- amp.yaml validation (internal)

**Read Routes (`api/routes/read/`)** -- Data reading endpoints:
- `POST /v1/.../objects/*:deliverResults` -- On-demand result delivery
- `POST /v1/.../installations/:id:pause` -- Pause read schedules
- `POST /v1/.../installations/:id:unpause` -- Unpause read schedules
- Triggers Temporal read workflows

**Shared Routes (`api/routes/shared/`)** -- Routes shared across read and write subdomains:
- `POST /v1/.../objects/*` -- On-demand read/write processing
- `GET /v1/generate-upload-url` -- GCS upload URL generation (shared with write)

**Write Routes (`api/routes/write/`)** -- Data writing endpoints:
- `GET /v1/generate-upload-url` -- GCS upload URL generation
- Data transformation and validation via on-demand processing

**Proxy Routes (`api/routes/proxy/`)** -- Third-party API proxying:
- `ALL /*` -- Catch-all proxy handler
- Transparent proxying of requests to provider APIs
- Authenticated via installation's OAuth connection
- Routed via subdomain-based isolation

**SignIn Routes (`api/routes/signin/`)** -- Authentication endpoints:
- `GET /save-cookie/:id` -- Save sign-in cookie for CLI auth flow
- `GET /get-cookie/:id` -- Retrieve sign-in cookie for CLI auth flow

### Subdomain-Based Routing

Routes are organized by subdomain, enabling independent scaling and deployment:

| Subdomain | Purpose | Auth Required |
|-----------|---------|---------------|
| `api` | General platform CRUD operations | Yes (multi-modal) |
| `read` | Data read operations | Yes |
| `write` | Data write operations | Yes |
| `proxy` | Direct provider API requests | Yes |
| `signin` | CLI authentication flows | No |

### URL Structure

```
/v1/...                    -- Public API routes
/internal/v1/...           -- Internal-only routes (ping, build, validate-yaml, fake-alert, admin API key, svix webhook)
/callbacks/v1/...          -- OAuth callback routes
```

### Notable Endpoints (Previously Undocumented)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/v1/my-info` | GET | Clerk only | Returns authenticated user's builder profile and roles |
| `/v1/claimed-domains` | GET, POST | Clerk only | Domain claiming/registration |
| `/v1/orgs/:orgId/claimed-domains` | GET | Org auth | List org's claimed domains |
| `/v1/orgs/:orgId/memberships` | POST | Clerk only | Create org membership |
| `/v1/invites:accept` | POST | Clerk only | Accept org invitation |
| `/v1/.../notification-event-topic-routes` | CRUD | Project auth | Notification event routing |
| `/v1/.../topic-destination-routes` | CRUD | Project auth | Topic-to-destination routing |
| `/v1/.../connections:generate` | POST | Frontend+ | Generate connection |
| `/v1/.../installations:import` | POST | Project auth | Import installation |
| `/v1/.../object-metadata` | PUT | Frontend+ | Upsert object metadata |
| `/v1/.../objects/*/metadata` | GET | Frontend+ | Get object metadata |
| `/v1/webhooks/clerk/builder` | POST | None | Clerk user lifecycle webhook |
| `/v1/webhooks/svix/operational` | POST | None (internal) | Svix operational webhook |
| `/v1/orgs/:orgId/billingAccount` | GET | Org owner | Get billing account |

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
- **Route segregation** -- Different route groups can run as separate pods in production (via subdomain routing)
- **Proxy isolation** -- Proxy requests handled by separate Fiber app to prevent interference
- **Integration resolution** -- Middleware resolves integration by ID or name (automatic for routes with `:integrationId` or `:integrationIdOrName`)
- **RFC 7807 errors** -- All errors returned as Problem Detail JSON (via `shared/problem`)
- **Route deduplication** -- Shared routes (like `generate-upload-url`) registered once across multiple subdomains via `DedupKey`
- **Validated handlers** -- `ampfiber.CreateBodyValidatedHandler[T]` for type-safe request body validation
- **Notification routing** -- Topics -> Event Topic Routes -> Topic Destination Routes pipeline for flexible notification delivery
- **Domain claiming** -- Organization-level domain registration with free email provider filtering (6000+ domains)
- **Clerk webhooks** -- User lifecycle events (created/updated/deleted) received via Svix-verified webhooks

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
