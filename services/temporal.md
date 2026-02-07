# Temporal Service

<!--
attribution:
  source: server/temporal/main.go, shared/temporal/, shared/workflow/
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
-->

## Overview

The **temporal** service is the background workflow orchestration engine for Ampersand. It runs Temporal workers that handle long-running tasks including data reads, writes, deletes, subscription management, token maintenance, and provider schema watching.

**Location:** `server/temporal/`
**Port:** 9991 (metrics), 6061 (pprof)
**Framework:** Temporal Go SDK
**Confidence:** HIGH

## Responsibilities

- **Data reading** -- Executes scheduled and on-demand read operations from provider APIs
- **Bulk writing** -- Handles async bulk write operations with polling
- **Bulk deleting** -- Handles async bulk delete operations with polling
- **Bulk querying** -- Handles async bulk query operations with polling
- **Subscription management** -- Creates, updates, deletes, and maintains real-time subscriptions
- **Token maintenance** -- Keeps OAuth tokens alive via periodic refresh
- **Invite expiration** -- Expires stale user invitations
- **Schema watching** -- Monitors provider schemas for changes
- **Async writes** -- Handles asynchronous write operations with auto-batching

## Worker Architecture

Each worker is defined as a `workerDefinition` with:
- A Temporal worker instance bound to a specific task queue
- Registered workflows (business logic)
- Registered activities (side-effect operations)

All workers are launched concurrently using `simultaneously.DoCtx()`.

### Task Queues (16 queues)

| Queue | Workflows | Activities | Purpose |
|-------|-----------|------------|---------|
| `ReadQueue` | ProviderReadWorkflow | ProviderReadActivity | Scheduled data reads |
| `ReadOndemandQueue` | ProviderReadWorkflow | ProviderReadActivity | On-demand data reads |
| `BulkWriteQueue` | BulkWriteAsyncWorkflow | BulkWriteAsyncActivity | Async bulk writes |
| `BulkWritePollQueue` | BulkWritePollAsyncWorkflow | DoBulkPollAsync | Poll bulk write jobs |
| `BulkDeleteAsyncQueue` | BulkDeleteAsyncWorkflow | BulkDeleteAsyncActivity | Async bulk deletes |
| `BulkDeletePollAsyncQueue` | BulkDeletePollAsyncWorkflow | BulkDeletePollAsyncActivity | Poll bulk delete jobs |
| `BulkQueryAsyncQueue` | BulkQueryAsyncWorkflow | BulkQueryAsyncActivity | Async bulk queries |
| `BulkQueryAsyncPollQueue` | BulkQueryPollAsyncWorkflow | BulkQueryPollAsyncActivity | Poll bulk query jobs |
| `MaintenanceTasksQueue` | ExpireInvites, KeepAliveWorkflow | ExpireInvitesActivity, KeepAliveActivity | Maintenance tasks |
| `SubscribeInstallationCreatedQueue` | SubscribeInstallationCreatedWorkflow | SubscribeInstallationCreatedActivity | Subscription creation |
| `SubscribeInstallationUpdatedQueue` | SubscribeInstallationUpdatedWorkflow | SubscribeInstallationUpdatedActivity | Subscription updates |
| `SubscribeInstallationDeletedQueue` | SubscribeInstallationDeletedWorkflow | SubscribeInstallationDeletedActivity | Subscription deletion |
| `SubscribeInstallationUnsubscribeQueue` | SubscribeInstallationUnsubscribeWorkflow | SubscribeInstallationUnsubscribeActivity | Unsubscription |
| `SubscribeInstallationMaintenanceQueue` | SubscribeInstallationMaintenanceWorkflow | SubscribeInstallationMaintenanceActivity | Subscription maintenance |
| `AsyncWriteQueue` | AsyncWriteWorkflow, AutoBatchWriteWorkflow | AsyncWriteActivity | Async writes with auto-batching |
| `ProviderMetadataWatchQueue` | ProviderSchemaWatchWorkflow | ProviderSchemaWatchActivity | Schema change detection |

### Key Workflow: ProviderReadWorkflow

Located in `shared/workflow/read/workflow.go`:

1. Creates an operation record in the database
2. Executes provider read activity (calls provider API)
3. Handles pagination and state management
4. Publishes results to Pub/Sub (ReadFinished topic)
5. Results are then picked up by the Messenger service for webhook delivery

**Important:** No retry logic at the workflow level. Retries are done at the activity level. The schedule-level policy decides if it continues after a workflow failure.

## Startup Sequence

1. Configure environment and logging
2. Set up shutdown handlers, Sentry, pprof
3. Configure Prometheus metrics
4. Wait for database quorum
5. Initialize OpenTelemetry tracing
6. Retry connecting to Temporal server (exponential backoff, max 60s)
7. Create all worker definitions
8. Launch all workers concurrently
9. Block until shutdown signal

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TEMPORAL_DEADLOCK_DETECTION_TIMEOUT` | 1 minute | Worker deadlock detection timeout |

## Dependencies

- **Temporal server** -- Workflow orchestration (gRPC connection)
- **PostgreSQL** -- Operation state, read state, installation data
- **Google Cloud Storage** -- Read result storage
- **Google Pub/Sub** -- Publish read-finished events
- **Provider APIs** -- Via connectors library (rate-limited)
- **Token Manager** -- OAuth token refresh for provider API calls

## Key Source Locations

- Worker definitions: `server/temporal/main.go`
- Read workflow: `server/shared/workflow/read/`
- Write workflows: `server/shared/temporal/write/`
- Async write: `server/shared/temporal/writeAsync/`
- Subscription workflows: `server/shared/temporal/subscribeinstallation/`
- Token keep-alive: `server/shared/token/`
- Invite expiry: `server/shared/temporal/invite/`
- Schema watching: `server/shared/temporal/providerschemawatch/`
- Queue definitions: `server/shared/temporal/init.go`

## Cross-References

- Architecture overview: `services/server-architecture.md`
- API service (triggers workflows): `services/api.md`
- Messenger (processes results): `services/messenger.md`
- Provider patterns: See provider documentation
