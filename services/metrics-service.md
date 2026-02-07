---
validation_metadata:
  attribution:
  source: server/metrics/main.go
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
---

# Metrics Service

## Overview

The **metrics** service is a periodic data collection agent that queries the PostgreSQL database and exposes aggregated metrics to Prometheus. It runs on a configurable tick interval, gathering business-level metrics that cannot be derived from individual service instrumentation.

**Location:** `server/metrics/`
**Port:** 9993 (metrics), 6063 (pprof)
**Framework:** Custom ticker loop
**Confidence:** HIGH

## Responsibilities

- **Database metric collection** -- Queries database for aggregate counts and statistics
- **Prometheus exposure** -- Exposes collected metrics for Prometheus scraping
- **Periodic execution** -- Runs on a configurable interval (default: 60 seconds)

## Architecture

Unlike other services that are event-driven (HTTP or Pub/Sub), the metrics service runs a simple ticker loop:

```
Start
  |
  v
Wait for database quorum
  |
  v
Initialize metrics to zero (avoid missing metrics)
  |
  v
+-> Wait for tick (default 60s)
|   |
|   v
|   collectMetrics()
|   |
|   +-- Query database for counts/aggregates
|   +-- Update Prometheus gauges/counters
|   +-- Track collection duration and errors
|   |
+---+
```

## Metrics Tracked

The service collects metrics at the `collectMetrics()` function level. Specific metrics include database-level aggregate counts for entities like operations, installations, connections, and other business objects.

**Meta-metrics (about the collection process itself):**
- `collectionErrors` -- Counter of failed collection attempts
- `collectionDuration` -- Histogram of collection time, labeled by success/failure

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `METRICS_TICK_DURATION` | 60s | Interval between metric collection runs |

## Why It Exists

While individual services expose their own operational metrics (request counts, latencies, error rates), there are business-level metrics that require database queries:

- Total number of active installations across all projects
- Connection status distribution
- Operation success/failure rates over time
- Usage patterns and trends

These aggregate metrics are too expensive to compute on every Prometheus scrape, so the metrics service pre-computes them on a regular interval.

## Dependencies

- **PostgreSQL** -- Data source for aggregate queries
- **Prometheus** -- Metric exposition target

## Cross-References

- Architecture overview: `services/server-architecture.md`
- Observability: `observability-index.md`
