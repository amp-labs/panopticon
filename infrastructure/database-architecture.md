# Database Architecture

<!--
attribution:
  source: server/shared/database/README.md, server/database/, AGENTS.md
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

Ampersand uses PostgreSQL as its primary data store, accessed through GORM (Go ORM). The database architecture follows an interface-first design pattern with three implementation tiers: production (GORM), in-memory (for tests), and mock (for unit tests).

**Database:** PostgreSQL 15
**ORM:** GORM
**Schema Management:** Atlas (migration-based)
**Migrations:** 107+ SQL migration files (as of Feb 2026)
**Confidence:** HIGH

## Database Instances

| Environment | Host | Database | Cores | Notes |
|-------------|------|----------|-------|-------|
| Local | localhost:55432 | ampersand-local-db | Docker | Via Docker Compose |
| Dev | Cloud SQL | ampersand-dev-db | Minimal | Auto-migrated on merge |
| Staging | Cloud SQL | ampersand-stag-db | Mid-tier | Manual promotion |
| Production | Cloud SQL | ampersand-prod-db | 64 cores | Manual promotion |
| Preview | Cloud SQL (dev) | pr-<branch-name> | Shared | Ephemeral |
| Atlas (local) | localhost:55433 | ampersand-local-atlas-db | Docker | Migration generation |

## Repository Pattern (Interface-First)

### Five-Package Structure

```
shared/database/
+-- types/          # Interface definitions
+-- models/         # Data model structs (GORM tags)
+-- gormdb/         # PostgreSQL implementation (production)
+-- memory/         # In-memory implementation (integration tests)
+-- mock/           # Mock builders (unit tests)
+-- *.go            # Public API (factory functions, context injection)
```

### Access Pattern

```go
// Production code -- no configuration needed
repo := database.Connections(ctx)
conn, err := repo.GetById(ctx, projectId, connectionId)

// Test code -- inject mock
mockRepo := mock.NewConnectionBuilder().
    WithGetById(func(ctx context.Context, projectId, connId string) (*Connection, error) {
        return &Connection{ID: connId, Status: "active"}, nil
    }).
    Build()
ctx := database.WithConnectionRepository(context.Background(), mockRepo)
```

### Key Principles

1. **Interface in `types/`** -- Define operations, not implementations
2. **Context injection** -- `database.WithXRepository(ctx, repo)` for DI
3. **Lazy singletons** -- `var instance = lazy.New[T](NewRepository)`
4. **Environment-aware** -- Auto-selects memory impl in tests, GORM in production
5. **Thread-safe memory** -- Uses `maps.NewThreadSafeMap` in memory implementations
6. **Compile-time checks** -- `var _ types.Interface = (*implementation)(nil)`

## Primary Entities

### Organization Hierarchy

```
organizations (Org)
  +-- projects (Project)
       +-- integrations (Integration)
       |    +-- revisions (Revision)
       |    +-- installations (Installation)
       |         +-- operations (Operation)
       +-- connections (Connection)
       +-- provider_apps (ProviderApp)
       +-- api_keys (ApiKey)
       +-- destinations (Destination)
       +-- jwt_keys (JwtKey)
```

### Core Tables

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `organizations` | Top-level entity | id, label, default_team_id |
| `projects` | Contains integrations | id, name, organization_id |
| `integrations` | Defines what data to sync | id, project_id, name, provider |
| `revisions` | Versioned integration configs | id, integration_id |
| `installations` | Customer-specific instances | id, integration_id, group_ref, consumer_ref |
| `operations` | Sync jobs and data ops | id, project_id, integration_id, installation_id, status, type |
| `connections` | OAuth credentials | id, project_id, provider, provider_app_id, status |
| `provider_apps` | OAuth app configs | id, project_id, provider, client_id |
| `api_keys` | Authentication keys | key, project_id, label, active, scopes |
| `destinations` | Webhook endpoints | id, project_id, name, type, metadata |
| `jwt_keys` | JWT verification keys | id, project_id |
| `read_states` | Pagination state | id, project_id, installation_id, object_name, next_page_token |

### Status Enums

**Operation Status:** `pending` -> `running` -> `completed` / `failed`
**Operation Type:** `read`, `write`, `proxy`
**Connection Status:** Various states tracking OAuth connection lifecycle

## Connection Pooling

```go
const (
    defaultMaxIdleConns    = 10
    defaultMaxOpenConns    = 100
    defaultMaxConnLifetime = 1 * time.Minute
)
```

## Schema Management (Atlas)

### Migration Workflow

1. **Change GORM struct** -- Modify model in `shared/database/models/`
2. **Generate migration** -- `make migrations/auto` (reads Go structs, generates SQL)
3. **Regenerate Go code** -- `go generate ./...`
4. **Test locally** -- `make test`

### Migration Commands

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `make refresh-db` | Fresh local start | Drops DB, recreates, runs all migrations, seeds |
| `make migrations/auto` | After changing GORM structs | Generates and applies new migration |
| `make migrations/apply-all` | Production/CI deployment | Applies only pending migrations |
| `make migrations/apply` | Testing one migration | Applies next pending migration only |
| `make migrations/hash` | After merge conflicts in atlas.sum | Recomputes migration checksum |

### Migration File Naming

Format: `YYYYMMDDHHMMSS.sql` (timestamp prefix)
Example: `20260127235159.sql`
Total: 107+ migration files spanning from May 2023 to present.

### Handling Conflicts

If `atlas.sum` has merge conflicts:
1. Merge main into branch
2. Resolve model conflicts
3. Run `make migrations/hash` to recompute checksums

If out-of-order migration error:
- Run `atlas migration rebase`, or
- Delete the earlier-timestamped file, regenerate, and reapply

## Seed Data

**Location:** `database/seed/`
**Format:** JSON files per table (`MODEL_NAME.json`)
**Script:** `database/seed/seed.go`
**Usage:** `make seed` or `make refresh-db` (includes seeding)

Pre-seeded environment variables in `local_vars.sh`:
- `PROJECT_ID` -- Pre-configured test project
- `API_KEY` -- Test API key
- `ADMIN_KEY` -- Test admin key
- `DB_DSN` -- Database connection string

## Remote Database Access

- **Metabase** (`https://ampersand.metabaseapp.com/`) -- Read-only access to dev/staging/prod
- **Cloud SQL Proxy** -- `make proxy/db/dev` for preview env database access
- **Direct connection** -- Via `psql $DB_DSN` with appropriate credentials

## Cross-References

- Server architecture: `services/server-architecture.md`
- Design patterns: `services/design-patterns.md`
- Deployment pipeline: `infrastructure/deployment-pipeline.md`
