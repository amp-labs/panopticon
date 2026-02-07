# Token Manager Service

<!--
attribution:
  source: server/token-manager/main.go, routes/
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The **token-manager** service is a centralized OAuth token refresh service that prevents race conditions in distributed token management. When multiple services or workers need to refresh an OAuth token simultaneously, the token manager serializes these requests to avoid token invalidation.

**Location:** `server/token-manager/`
**Port:** 8082 (HTTP, local), 9994 (metrics), 6064 (pprof)
**Framework:** GoFiber
**Confidence:** HIGH

## Responsibilities

- **Centralized token refresh** -- Single point of truth for OAuth token refresh operations
- **Race condition prevention** -- Serializes concurrent token refresh requests
- **TLS/mTLS support** -- Supports disabled, enabled, and mutual TLS modes
- **Token caching** -- Reduces redundant refresh calls

## Why It Exists

In a distributed system with multiple Temporal workers making provider API calls simultaneously, a common problem arises:

1. Worker A detects an expired token and initiates a refresh
2. Worker B also detects the same expired token and initiates its own refresh
3. Both get new tokens, but the provider may invalidate the first refresh
4. Worker A's subsequent API calls fail because its token was invalidated

The token manager solves this by being the single authority for token refresh. All workers delegate token refresh to this service, which serializes the requests.

## Architecture

### HTTP Endpoints

The service exposes endpoints via GoFiber:

| Endpoint | Purpose |
|----------|---------|
| Token refresh | Refresh OAuth tokens for connections |
| Build info | Service build information |
| Ping | Health check |

### Route Files

- `routes/route.go` -- Route registration
- `routes/token.go` -- Token refresh logic
- `routes/build.go` -- Build info endpoint
- `routes/ping.go` -- Health check
- `routes/error.go` -- Error handling
- `routes/types.go` -- Request/response types
- `routes/prometheus.go` -- Metrics definitions

### TLS Configuration

The token manager supports three TLS modes, configured via `TLS_MODE`:

| Mode | Description | Use Case |
|------|-------------|----------|
| `disabled` | Plain HTTP | Local development |
| `enabled` | TLS with server cert | Basic encryption |
| `mtls` | Mutual TLS | Production (service-to-service authentication) |

mTLS ensures only authorized services (other Ampersand services with valid client certificates) can request token refreshes.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | HTTP listen port |
| `SUBSYSTEM_NAME` | token-manager | Service name |
| `TLS_MODE` | disabled | TLS mode (disabled/enabled/mtls) |
| `TLS_CERT_FILE` | - | Server certificate path |
| `TLS_KEY_FILE` | - | Server key path |
| `MTLS_CERT_FILE` | - | mTLS server certificate |
| `MTLS_KEY_FILE` | - | mTLS server key |
| `MTLS_CLIENT_CERT_FILE` | - | mTLS client certificate |
| `LOG_HTTP_REQUESTS` | true | Enable request logging |
| `DEBUG_REQUESTS_ALLOWED` | false | Allow debug request logging |
| `DEBUG_REQUESTS_REQUIRED` | false | Require debug request logging |
| `FIBER_IMMUTABLE` | true | Fiber context immutability |
| `FIBER_READ_BUFFER_SIZE` | 4096 | Fiber read buffer size |
| `FIBER_WRITE_BUFFER_SIZE` | 4096 | Fiber write buffer size |

## Production Deployment

- **Replicas:** 3+ in production (high availability, blast radius reduction)
- **Communication:** Other services call token-manager via mTLS
- **Dev:** 1 replica (token-manager failure in dev is acceptable)

## Error Handling

Uses the same RFC 7807 Problem Detail pattern as the API service:
- `InputValidationProblem` -- Invalid request data
- `AmpersandProblem` -- Application-level errors
- Prometheus metrics track request/response sizes per endpoint

## Dependencies

- **PostgreSQL** -- Connection and token data
- **Provider OAuth APIs** -- Token refresh endpoints
- **Google KMS** -- Token decryption (tokens stored encrypted)

## Client Integration

Other services access the token manager via `shared/providers/managed.go`:

```go
type TokenManagerClient struct {
    // HTTP client configured with mTLS in production
    // Handles caching, retries, and error handling
}
```

The `TokenManagerClient` caches refresh results to avoid redundant calls within short time windows.

## Cross-References

- Architecture overview: `services/server-architecture.md`
- API service (primary consumer): `services/api.md`
- Temporal (primary consumer): `services/temporal.md`
- Provider integration patterns: See provider documentation
