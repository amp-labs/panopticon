# Scribe Service

<!--
attribution:
  source: server/scribe/main.go and handler files
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The **scribe** service ingests operations and billing events from Google Pub/Sub queues into the PostgreSQL database at controlled rates. Its primary purpose is to prevent database overload by acting as a controlled ingestion layer between event producers and the database.

**Location:** `server/scribe/`
**Port:** 9995 (metrics), 6065 (pprof)
**Framework:** Google Pub/Sub client
**Confidence:** HIGH

## Responsibilities

- **Usage event ingestion** -- Persists usage/billing events to the database
- **Operation change tracking** -- Persists operation status changes to the database
- **Rate control** -- Controlled ingestion rate to prevent database overload

## Pub/Sub Listeners (2 subscriptions)

| Topic | Subscription | Handler | Timeout | Purpose |
|-------|-------------|---------|---------|---------|
| UsageEmitted | usage-emitted-subscription | `handleUsageEmitted` | 10 min | Billing/usage events |
| OperationChange | operation-change-subscription | `handleOperationChange` | 10 min | Operation status updates |

## Data Flow

```
Various services emit events
    |
    v
Pub/Sub Topics:
  - UsageEmitted (billing events)
  - OperationChange (operation status)
    |
    v
Scribe Service
    |
    v
processUsageEmitted() / processOperationChange()
    |
    v
PostgreSQL Database
    (controlled write rate)
```

## Why Scribe Exists

Without Scribe, multiple services would write directly to the database for every operation status change and usage event. Under high load (thousands of concurrent read/write operations), this could overwhelm the database connection pool. Scribe acts as a buffer:

1. Events are published to Pub/Sub (fast, non-blocking)
2. Scribe consumes events at a sustainable rate
3. Database writes happen at controlled throughput

## Metrics

Each handler tracks:
- Messages received (counter)
- Messages acked/nacked (counter)
- Errors total (counter)
- Dequeue errors (counter)
- Processing time (histogram)

## Key Implementation Files

- `main.go` -- Service initialization and listener configuration
- Handler files for usage and operation processing
- `messageHandler.go` -- Shared message handling utilities (likely similar pattern to messenger)
- `metrics.go` -- Prometheus metric definitions

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SUBSCRIPTION_TIMEOUT_USAGE_EMITTED` | 10 min | Usage event processing timeout |
| `SUBSCRIPTION_TIMEOUT_OPERATION_CHANGE` | 10 min | Operation change processing timeout |

## Dependencies

- **Google Pub/Sub** -- Message consumption
- **PostgreSQL** -- Write destination for events

## Cross-References

- Architecture overview: `services/server-architecture.md`
- Messenger (parallel Pub/Sub consumer): `services/messenger.md`
- Metrics service: `services/metrics-service.md`
