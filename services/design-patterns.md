# Design Patterns and Architectural Decisions

<!--
attribution:
  source: server/docs/interface-first-design-patterns.md, server/AGENTS.md, source code analysis
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The Ampersand server codebase follows several well-documented design patterns that enable testability, maintainability, and clear separation of concerns. This document catalogs the key patterns and conventions.

**Confidence:** HIGH (documented in server's own docs and AGENTS.md)

## Core Design Philosophy

**Interface-First Design** -- Define interfaces before implementations. Every component that interacts with external systems has three implementation tiers:

1. **Production** -- Real external system (GORM, Redis, GCS)
2. **Memory** -- Fast, in-memory simulation (integration tests)
3. **Mock** -- Builder-based controllable mock (unit tests)

This enables:
- Unit tests without external dependencies
- Fast test execution using in-memory implementations
- Flexible dependency injection via `context.Context`
- Zero boilerplate for production code (auto environment detection)

## Pattern Catalog

### 1. Context-Based Dependency Injection

**Where:** Every repository, client, and service abstraction

Instead of constructor injection or global singletons, dependencies flow through `context.Context`:

```go
// Production code -- no setup needed, uses defaults
repo := database.Connections(ctx)

// Test code -- inject custom implementation
ctx := database.WithConnectionRepository(ctx, mockRepo)
repo := database.Connections(ctx)  // Returns mockRepo
```

**Implementation pattern:**
1. Custom type for context key: `type ClientContextKey string`
2. Const key value: `const ClientContextKeyValue ClientContextKey = "client"`
3. Injection: `WithClient(ctx, client)` -- stores in context
4. Accessor: `Client(ctx)` -- checks context first, falls back to singleton
5. Nil safety: `contexts.EnsureContext(ctx)` handles nil context

### 2. Lazy Singleton Pattern

**Where:** All shared infrastructure clients (database, Redis, GCS, Temporal, Pub/Sub)

Expensive resources are initialized on first access, not at startup:

```go
var instance = lazy.New[types.Client](NewClient)

func Client(ctx context.Context) types.Client {
    // Check context-injected instance first
    if client, ok := getInjectedInstance(ctx); ok {
        return client
    }
    // Lazy-initialize singleton on first access
    return instance.Get()
}
```

**Benefits:**
- No init-order dependencies
- Deferred initialization avoids startup latency
- Environment-aware: auto-selects memory impl in tests

### 3. Environment-Aware Defaults

**Where:** All infrastructure abstractions

```go
var wantInMemoryRepository = lazy.New[bool](stage.IsTest)

func NewRepository() types.Repository {
    if wantInMemoryRepository.Get() {
        return memory.NewRepository()  // Tests
    }
    return gormdb.NewRepository()      // Production
}
```

`stage.IsTest()` returns true when running via `go test`, `GO_STAGE=test`, or binary ends with `.test`.

### 4. Builder Pattern for Mocks

**Where:** `shared/database/mock/`, `shared/redis/mock/`, etc.

```go
mockRepo := mock.NewConnectionBuilder().
    WithGetById(func(ctx context.Context, projectId, connId string) (*Connection, error) {
        return &Connection{ID: connId, Status: "active"}, nil
    }).
    Build()
```

**Key characteristics:**
- Only specify methods you need (partial mocking)
- Unimplemented methods return `ErrNotImplemented` (safe defaults)
- Compile-time interface verification
- Method chaining for fluent construction

### 5. Functional Options Pattern

**Where:** Service configuration, Fiber app creation

```go
type Option func(d *defaults)

func WithDefaultReadBufferSize(size int) Option {
    return func(d *defaults) { d.ReadBufferSize = size }
}

func NewFiber(appName string, opts ...Option) *fiber.App {
    dflts := &defaults{ReadBufferSize: defaultReadBufSize}
    for _, opt := range opts { opt(dflts) }
    // ...
}
```

### 6. Repository Pattern

**Where:** `shared/database/`

Every database table has a repository interface in `types/` with implementations in `gormdb/`, `memory/`, and `mock/`:

```go
// types/connection.go
type ConnectionRepository interface {
    GetById(ctx context.Context, projectId, connectionId string) (*Connection, error)
    List(ctx context.Context, projectId string) ([]*Connection, error)
    Create(ctx context.Context, conn *Connection) error
}
```

### 7. Factory Pattern for Providers

**Where:** `shared/providers/providers.go`

```go
func NewDeepProviderAPI(
    ctx context.Context,
    provider providers.Provider,
    projectId string,
    connectionId string,
    rateLimited LimiterToggle,
    authenticated AuthMode,
    module string,
) (*ProviderAPI, error)
```

Complex initialization with multiple configuration options, dependency resolution, and error handling.

### 8. Worker Definition Pattern

**Where:** `temporal/main.go`

```go
type workerDefinition struct {
    worker     types.Worker
    label      string
    workflows  []any
    activities []any
}
```

Workers are registered declaratively, then launched concurrently.

## Error Handling Patterns

### RFC 7807 Problem Details

All API errors return structured JSON:

```go
type AmpersandProblem struct {
    Type     string `json:"type"`     // Error category
    Title    string `json:"title"`    // Human-readable summary
    Status   int    `json:"status"`   // HTTP status code
    Detail   string `json:"detail"`   // Specific description
    Instance string `json:"instance"` // Request identifier
}
```

### Error Wrapping with Context

```go
func NewDeepProviderAPI(ctx context.Context, ...) (*ProviderAPI, error) {
    conn, err := database.GetConnectionWithTokens(ctx, projectId, connectionId)
    if err != nil {
        return nil, fmt.Errorf("error getting connection: %w", err)
    }
    if conn.ProviderApp.Provider != provider {
        return nil, fmt.Errorf("connection does not belong to provider %s: %w",
            provider, ErrInvalidConnection)
    }
}
```

### Sentinel Errors

```go
var (
    ErrInvalidProvider   = errors.New("provider not supported")
    ErrInvalidConnection = errors.New("invalid connection for provider")
    ErrNoToken           = errors.New("no access or refresh token found")
)
```

## Communication Patterns

### Service-to-Service

| Mechanism | Use Case | Example |
|-----------|----------|---------|
| **Temporal queues** | Long-running async work | API triggers read/write workflows |
| **Pub/Sub** | Event-driven processing | Temporal publishes, Messenger/Scribe consume |
| **HTTP (internal)** | Synchronous requests | API calls Token Manager for token refresh |
| **Database** | Shared state | All services read/write PostgreSQL |
| **Redis** | Fast state | OAuth session state, token caching |
| **GCS** | Large data transfer | Read results stored for webhook delivery |

### Asynchronous Processing Pattern

```
1. API receives request
2. API creates database record (operation)
3. API enqueues Temporal workflow
4. Temporal executes workflow activities
5. Activity publishes result to Pub/Sub
6. Messenger processes Pub/Sub message
7. Messenger delivers via webhook
8. Scribe persists status update to database
```

### Route Segregation Pattern

The API service can split routes into separate deployments:

```go
EnableApiRoutes:    env.Bool("ENABLE_API_ROUTES").ValueOrElse(true),
EnableReadRoutes:   env.Bool("ENABLE_READ_ROUTES").ValueOrElse(true),
EnableWriteRoutes:  env.Bool("ENABLE_WRITE_ROUTES").ValueOrElse(true),
EnableProxyRoutes:  env.Bool("ENABLE_PROXY_ROUTE").ValueOrElse(true),
```

In production: separate pods for api, read, write, proxy. In dev: single pod with all routes.

## Code Conventions

### Naming

- **Functions:** `GetInstallationsByGroupRef` (descriptive, action+entity+condition)
- **Conversions:** `NewOrgFromCommon(cOrg)`, `(o *Org) ToCommon()`
- **Constants:** `UPPER_SNAKE_CASE` for route params, `camelCase` for config
- **Enums:** String-typed with const block: `type OperationStatus string`

### File Organization

- One entity per file: `installation.go`, `connection.go`
- Tests alongside: `installation_test.go`
- Package names: lowercase, single words, clear purpose

### Context Handling

- Context always first parameter (except receivers)
- Propagated through all nested calls
- Never stored in structs (passed through function calls)

### Logging

- Use `logger.Get(ctx)` for context-aware logging (automatic trace/request IDs)
- Structured logging with `slog` (key-value pairs)
- `logger.Fatal()` for unrecoverable errors (exits process)

### Linting

- `make fix` -- Auto-fix (wsl, gci, golangci-lint, typos)
- `make lint` -- Check without fixing
- `//nolint:directive` with explanation for justified suppressions
- Pre-commit hook runs `make fix` automatically

## Testing Patterns

| Test Type | Command | Dependencies | Speed |
|-----------|---------|-------------|-------|
| Unit tests | `make test` | None (in-memory) | Fast |
| Database tests | `make test/db` | PostgreSQL (Docker) | Medium |
| End-to-end | `scripts/endToEnd/` | Full stack | Slow |
| Integration | `integration-tests/` | Scenarios | Medium |

**Reference implementation:** `examples/database/widget/` -- Complete example with composite keys, foreign keys, soft deletes, factory functions, and tests.

## Cross-References

- Server architecture: `services/server-architecture.md`
- Database architecture: `infrastructure/database-architecture.md`
- Provider patterns: `providers/provider-integration-patterns.md`
