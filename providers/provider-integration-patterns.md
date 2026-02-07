---
validation_metadata:
  attribution:
  source: server/shared/providers/, server/shared/catalog/, server/shared/oauth/, AGENTS.md
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
---

# Provider Integration Patterns

## Overview

Ampersand integrates with 80+ SaaS providers (Salesforce, HubSpot, Notion, etc.) through a standardized connector system. Providers are cataloged remotely, OAuth flows are managed centrally, and API interactions use rate-limited, authenticated HTTP clients.

**Confidence:** HIGH

## Provider Catalog System

### How Providers Are Cataloged

The provider catalog is a JSON file maintained in the `amp-labs/connectors` open-source repository:

```
https://raw.githubusercontent.com/amp-labs/connectors/main/internal/generated/catalog.json
```

**Key behaviors:**
- The server **automatically reads** the latest catalog from GitHub (no server redeploy needed)
- Catalog is **refreshed every 30 minutes** in production
- Can be overridden via `PROVIDER_CATALOG_URL` environment variable
- Falls back to the compiled-in catalog if the remote fetch fails

**Catalog contains per provider:**
- Provider name and display metadata
- OAuth2 configuration (auth URL, token URL, scopes, grant types)
- Token metadata fields (scopes field, consumer ref field)
- API base URLs and module definitions
- Supported operations (read, write, subscribe, proxy)

### Provider Info Access

```go
// Get provider information from catalog
providerInfo, err := catalog.ReadLatestInfo(ctx, provider, &substitutions)

// Access OAuth configuration
authURL := providerInfo.Oauth2Opts.AuthURL
tokenURL := providerInfo.Oauth2Opts.TokenURL
scopes := providerInfo.Oauth2Opts.ExplicitScopesRequired
```

## Authentication Patterns

### OAuth2 Flow

Ampersand supports OAuth2 Authorization Code flow as the primary authentication method:

1. **Builder creates a Provider App** -- Stores client ID and client secret
2. **End user initiates OAuth** -- Redirected to provider's auth URL
3. **Provider redirects back** -- Callback at `/callbacks/v1/oauth`
4. **Token exchange** -- Server exchanges auth code for access/refresh tokens
5. **Token storage** -- Encrypted tokens stored in Connection record
6. **Token refresh** -- Managed by Token Manager service

**Session state:** OAuth PKCE verifier stored in Redis with a 10-minute TTL.

**Redirect URL format:** `{API_ROOT}/callbacks/v1/oauth`
- Local: `http://localhost:8080/callbacks/v1/oauth`
- Production: `https://api.withampersand.com/callbacks/v1/oauth`

### Supported Auth Types

| Auth Type | Description | Examples |
|-----------|-------------|---------|
| **OAuth2 Authorization Code** | Standard OAuth2 flow | Salesforce, HubSpot |
| **OAuth2 Client Credentials** | Server-to-server auth | Some enterprise APIs |
| **Basic Auth** | Username/password | Legacy APIs |
| **API Key** | Static key authentication | Some simpler APIs |
| **JWT** | JSON Web Token auth | Snowflake |

### Token Management

**Problem:** In a distributed system, multiple Temporal workers may try to refresh the same expired token simultaneously, causing race conditions.

**Solution:** Centralized Token Manager service with sharding:

```go
// Token requests are sharded by project+connection ID
// Each shard routes to a specific token-manager pod
shardIndex := xxhash(projectId + connectionId) % numPods
targetPod := fmt.Sprintf("token-manager-%d.token-manager.%s.svc.cluster.local", shardIndex, namespace)
```

**Token refresh flow:**
1. Worker detects expired token
2. Request sent to Token Manager (sharded by connection)
3. Token Manager serializes refresh requests for the same connection
4. Fresh token returned and cached (TTL cache)
5. Worker retries the API call with new token

**Caching:** TTL cache prevents redundant refresh calls. Cache key is based on project+connection ID.

## Provider API Architecture

### ProviderAPI Struct

```go
type ProviderAPI struct {
    Connector  connectors.Connector              // From amp-labs/connectors library
    Connection *common.ConnectionWithSecretsInt   // OAuth tokens + connection metadata
}
```

### Connector System

The `github.com/amp-labs/connectors` library provides standardized interfaces:

| Interface | Purpose | Operations |
|-----------|---------|-----------|
| `ReadConnector` | Data reading | Read objects with pagination, filtering |
| `WriteConnector` | Data writing | Create, update, delete records |
| `SubscribeConnector` | Real-time subscriptions | Register webhooks, process events |
| `AuthMetadataConnector` | OAuth handling | Token metadata extraction |

### Creating a Provider API

```go
providerAPI, err := providers.NewDeepProviderAPI(
    ctx,
    providers.Salesforce,    // Provider enum
    projectId,               // Project ID
    connectionId,            // Connection ID
    rateLimited,             // Rate limiting toggle
    authenticated,           // Auth mode
    module,                  // Provider module (optional)
)
```

### Rate Limiting

Multi-level rate limiting using a custom HTTP transport:

1. **Provider-level limits** -- Respects provider's API rate limits
2. **Installation-level limits** -- Per-customer throttling
3. **Throttle behavior:**
   - If delay <= 15 seconds: `time.Sleep()` in the transport
   - If delay > 15 seconds: Returns `ThrottledError` (allows Temporal sleep instead)

```go
const MaxSleepTimePermissible = 15 * time.Second
```

### Special Provider Handling

**Snowflake:** Custom JWT-based authentication with cached connections.

```
server/shared/providers/snowflake/
+-- jwt.go       # JWT token generation
+-- client.go    # Snowflake connection configuration
+-- cache.go     # Connection caching
```

## Data Flow Patterns

### Read Operations

```
API: POST /v1/read/.../objects/{objectName}
    |
    v
Temporal: ProviderReadWorkflow
    |-- Create ProviderAPI (authenticated, rate-limited)
    |-- Call connector.Read(ctx, objectName, options)
    |-- Handle pagination (NextPageToken in ReadState)
    |-- Store results in GCS
    |-- Publish to ReadFinished topic
    |
    v
Messenger: deliverReadData()
    |-- Split into <300KB chunks
    |-- Deliver via webhooks to builder
```

### Write Operations

```
API: POST /v1/write/.../objects/{objectName}
    |
    v
Data transformation (map to provider schema)
    |
    v
Temporal: BulkWriteAsyncWorkflow
    |-- Create ProviderAPI
    |-- Call connector.Write(ctx, objectName, data)
    |-- Handle bulk operations and polling
    |-- Publish status updates
```

### Subscription (Real-time) Operations

```
Registration:
  API -> Temporal: SubscribeInstallationCreatedWorkflow
      |-- Register webhook with provider
      |-- Store subscription metadata

Event Reception:
  Provider -> Cloud Function -> Pub/Sub -> Messenger
      |-- Validate signature/auth
      |-- Process event data
      |-- Transform to standard format
      |-- Deliver to builder's webhook
```

### Proxy Operations

```
Builder: ANY /v1/proxy/.../...
    |
    v
API (proxy Fiber app):
    |-- Resolve installation and connection
    |-- Create authenticated HTTP client
    |-- Forward request to provider API
    |-- Return provider response to builder
```

## Object Metadata and Field Hydration

The `shared/providers/hydrate.go` module enriches object metadata:

```go
type HydratedObjectMetadata struct {
    // Provider-specific field definitions
    // Field types, required/optional status
    // Available values for enum fields
}
```

This is used to:
- Provide field information to builders in the amp.yaml config
- Validate field names in read/write configurations
- Map builder field names to provider field names

## Provider Catalog Metrics

The `shared/catalog/metrics.go` and `shared/providers/metrics.go` track:
- Catalog refresh success/failure rates
- Provider API call counts per provider
- API call latencies per provider
- Error rates per provider

## Key Source Locations

| Area | Location |
|------|----------|
| Provider API creation | `server/shared/providers/providers.go` |
| Token management client | `server/shared/providers/managed.go` |
| Rate limiting transport | `server/shared/providers/limiter.go` |
| OAuth2 token handling | `server/shared/providers/oauth2.go` |
| Provider catalog | `server/shared/catalog/catalog.go` |
| OAuth flow | `server/shared/oauth/connection.go` |
| OAuth metadata | `server/shared/oauth/provider.go` |
| Snowflake special | `server/shared/providers/snowflake/` |

## Cross-References

- Server architecture: `services/server-architecture.md`
- Token Manager: `services/token-manager.md`
- Salesforce provider: `providers/salesforce.md`
- Design patterns: `services/design-patterns.md`
