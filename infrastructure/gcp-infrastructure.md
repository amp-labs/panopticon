---
validation_metadata:
  attribution:
  source: server/argocd-infrastructure.md, server/README.md, server/cloudbuild.yaml
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
---

# GCP Infrastructure

## Overview

Ampersand runs on Google Cloud Platform (GCP) with GKE for container orchestration, Cloud SQL for managed PostgreSQL, and various GCP services for messaging, storage, and security.

**Region:** us-west1
**Confidence:** HIGH (infrastructure docs), MEDIUM (some specifics inferred)

## GCP Services Used

### Compute

| Service | Purpose | Details |
|---------|---------|--------|
| **GKE** (Google Kubernetes Engine) | Container orchestration | Cluster per environment gradient |
| **Cloud Build** | CI/CD pipeline | Builds Docker images, triggers deployments |
| **Cloud Functions** | Webhook gateway | Receives provider webhooks, publishes to Pub/Sub |

### Data

| Service | Purpose | Details |
|---------|---------|--------|
| **Cloud SQL** (PostgreSQL) | Primary database | 64-core in prod, minimal in dev |
| **Cloud Storage** (GCS) | Object storage | Read results, large data blobs |
| **Pub/Sub** | Asynchronous messaging | 8+ topics for inter-service communication |

### Security

| Service | Purpose | Details |
|---------|---------|--------|
| **Cloud KMS** | Key management | Encryption of OAuth tokens and sensitive data |
| **Secret Manager** | Secret storage | Environment-specific secrets |
| **Config Connector** | GCP resource provisioning | CRDs provision Pub/Sub from Kubernetes |

### Networking

| Service | Purpose | Details |
|---------|---------|--------|
| **Cloud DNS** | Domain management | Environment-specific subdomains |
| **Cloud Load Balancing** | Traffic distribution | Via Kong and GKE ingress |
| **Static IPs** | Fixed endpoints | 3 per prod Kong instance |

### Monitoring

| Service | Purpose | Details |
|---------|---------|--------|
| **Cloud Monitoring** | Infrastructure metrics | GKE, Cloud SQL monitoring |
| **Prometheus** | Application metrics | Self-hosted in GKE |
| **Grafana** | Dashboards | Self-hosted in GKE (local development) |

## Kubernetes Architecture

### Environment Gradient

| Environment | Services | DB Cores | Auto-scaling | Replicas | Alerting |
|-------------|----------|----------|-------------|----------|----------|
| **Production** | Full separation (10 deployments) | 64 | Yes | Multiple | Full (PagerDuty, Slack) |
| **Staging** | Some separation | Mid-tier | Yes | Fewer | Conditional |
| **Dev** | Collapsed (1 API pod handles api/read/write/proxy) | Minimal | No | 1 each | None |
| **Preview** | Collapsed (like dev) | Shared dev DB | No | 1 each | None |

### Production Services (Separate Deployments)

- `api` -- REST API server
- `read` -- Read operation service
- `write` -- Write operation service
- `proxy` -- Proxy service
- `temporal` -- Workflow orchestration
- `messenger` -- Message handling
- `scribe` -- Data writing
- `token-manager` -- OAuth token management (3+ replicas)
- `metrics` -- Metrics collection
- `builder-mcp` -- MCP server

### Service Collapsing (Dev/Preview)

In dev, a single API pod handles traffic for api, read, write, and proxy domains:
- Controlled via environment variables (`ENABLE_*_ROUTES`)
- Ingress routes multiple domains to the same service
- Saves cost while maintaining functional testing

### Kong API Gateway

**Two deployments:**
1. **Internet-facing** -- Public API gateway
2. **Outpost-facing** -- Between Ampersand and Outpost (webhook delivery)

**Production configuration:**
- 3 Kong instances pinned to separate GKE zones
- Each with dedicated static external IP
- DNS round-robin across all 3 IPs
- Pod Disruption Budgets for HA

**What Kong does:**
- Reverse proxy / load balancing to backend services
- Rate limiting / throttling
- Light header transformation
- Prometheus metrics
- Does NOT handle authentication (backend services do this)

## Google Pub/Sub Topics

| Topic | Publisher | Subscriber | Purpose |
|-------|----------|-----------|---------|
| `read-finished` | Temporal | Messenger | Completed read operations |
| `poll-bulk-job` | Temporal | Messenger | Bulk write job status |
| `subscribe-webhook-received` | Cloud Functions | Messenger | Incoming provider webhooks |
| `subscribe-webhook-processed` | Messenger | Messenger | Processed events for delivery |
| `subscribe-async-installation` | API | Temporal | Async installation events |
| `usage-emitted` | Various | Scribe | Billing/usage events |
| `operation-change` | Various | Scribe | Operation status updates |
| `notification-emitted` | Various | Messenger | Notification events |
| `provider-schema-changed` | Temporal | Messenger | Provider schema changes |

## Google Cloud Storage

- **Read results** -- Temporal stores read operation results
- **Large payloads** -- Oversized single rows stored with pre-signed URLs
- **Local emulation** -- Fake GCS server at localhost:8000 for development
- **Local storage** -- Files in `docker-compose/data/` (directories = buckets)

## Webhook Delivery Infrastructure

### Current State (Dual System)

- **Svix** (managed service) -- Handles webhook destinations
- **Outpost** (self-hosted, Hookdeck) -- Handles Kinesis destinations

### Outpost Capabilities

- At-least-once delivery guarantee
- Automatic and manual retries
- Idempotency headers, signatures, timestamp validation
- Multi-tenant support
- Supports: webhooks, SQS, Pub/Sub, Kafka, RabbitMQ, EventBridge

### Future Direction

Considering migration from Svix to Outpost for all delivery, which would consolidate infrastructure and reduce costs.

## Container Registry

- **Location:** `us-west1-docker.pkg.dev/ampersand-prod/gke-repo/`
- **Images:** api, temporal, messenger, scribe, token-manager, metrics, builder-mcp
- **Tagging:** `$SHORT_SHA` (git commit hash)
- **Cache:** Pre-built base image `base-builder:refreshed`

## Cross-References

- Deployment pipeline: `infrastructure/deployment-pipeline.md`
- Database architecture: `infrastructure/database-architecture.md`
- Service architecture: `services/server-architecture.md`
- Observability: `observability-index.md`
