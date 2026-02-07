# Services Architecture Index

This index documents Ampersand's 7 microservices architecture plus developer tooling.

## Architecture Overview

- **Server Architecture** - System overview, resource hierarchy, communication patterns, shared libraries, local development setup --> `services/server-architecture.md`
- **Design Patterns** - Interface-first design, context-based DI, lazy singletons, builder mocks, functional options, repository pattern --> `services/design-patterns.md`

## Core Services

| # | Service | Purpose | Communication | Documentation |
|---|---------|---------|---------------|---------------|
| 1 | **api** | REST API server, authentication, routing | HTTP (Fiber), Temporal, Pub/Sub | `services/api.md` |
| 2 | **temporal** | Workflow orchestration (16 task queues) | Temporal SDK, Pub/Sub | `services/temporal.md` |
| 3 | **messenger** | Message delivery and event processing | Pub/Sub (6 listeners), HTTP webhooks | `services/messenger.md` |
| 4 | **scribe** | Database persistence of async events | Pub/Sub (2 listeners), PostgreSQL | `services/scribe.md` |
| 5 | **token-manager** | OAuth token management with sharding | HTTP (Fiber) with mTLS, Redis cache | `services/token-manager.md` |
| 6 | **metrics** | Application metrics collection | PostgreSQL queries, Prometheus exposition | `services/metrics-service.md` |
| 7 | **builder-mcp** | MCP server for builder tooling | MCP protocol | `services/builder-mcp.md` |

## Developer Tooling

8. **mcpanda** - MCP server for integration testing (77 tools, production-ready) --> `services/mcpanda.md`

## Service Communication Summary

```
API <-- HTTP --> Token Manager
API -- Temporal --> Temporal Workers
Temporal -- Pub/Sub --> Messenger, Scribe
Cloud Functions -- Pub/Sub --> Messenger
All Services -- PostgreSQL --> Database
All Services -- Redis --> Cache
Temporal -- GCS --> Storage
```

## Production Deployment

In production, services are fully separated with independent deployments. In dev/preview, the API service collapses api/read/write/proxy into a single pod via `ENABLE_*_ROUTES` environment variables.

See `infrastructure/deployment-pipeline.md` for full deployment details.

## Cross-Cutting Concerns

- Security --> See `security-index.md`
- Observability --> See `observability-index.md`
- Data Flow --> See `data-flow-index.md`
- Testing --> See `testing-patterns.md`
