---
validation_metadata:
  attribution:
  source: server/messenger/main.go and handler files
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
---

# Messenger Service

## Overview

The **messenger** service processes Google Pub/Sub messages for webhook delivery, data routing, and event processing. It is the bridge between background processing (Temporal workflows, provider webhooks) and the builder's webhook endpoints. Its workload is extremely bursty.

**Location:** `server/messenger/`
**Port:** 9992 (metrics), 6062 (pprof)
**Framework:** Google Pub/Sub client
**Confidence:** HIGH

## Responsibilities

- **Read result delivery** -- Receives completed read results, splits into chunks, delivers via webhooks
- **Write poll processing** -- Polls bulk write job status
- **Subscription event processing** -- Receives and processes incoming provider webhooks
- **Subscription event delivery** -- Delivers processed subscription events to builder webhooks
- **Notification delivery** -- Sends notifications via Svix
- **Provider schema change handling** -- Processes provider schema change events

## Pub/Sub Listeners (6 subscriptions)

| Topic | Subscription | Handler | Timeout | Purpose |
|-------|-------------|---------|---------|---------|
| ReadFinished | read-finished-subscription | `readHandler` | 30 min | Completed read operations |
| PollBulkJob | poll-bulk-job-subscription | `writeHandler` | 5 min | Bulk write job polling |
| SubscribeWebhookReceived | subscribe-webhook-received-subscription | `subscribeReceiveHandler` | 30 min | Incoming provider webhooks |
| SubscribeWebhookProcessed | subscribe-webhook-processed-subscription | `subscribeDeliveryHandler` | 30 min | Processed events for delivery |
| NotificationEmitted | notification-emitted-subscription | `notificationHandler` | 5 min | Notification delivery |
| ProviderSchemaChanged | provider-schema-changed-subscription | `providerSchemaChangedHandler` | 5 min | Schema change processing |

### Special: 11x Subscription Isolation

In production, 11x (a high-volume customer) gets their own separate subscription to the `SubscribeWebhookReceived` topic. This prevents high-volume customers from starving out other customers. Controlled via `ENABLE_11X_SUBSCRIPTION` env var.

## Data Flow: Read Delivery

```
Temporal Read Workflow
    |
    v
Pub/Sub: ReadFinished topic
    |
    v
Messenger: readHandler()
    |
    v
deliverReadData()
    |
    +-- Splits results into <300KB chunks (Svix webhook limit)
    +-- For oversized single rows: stores in GCS, sends webhook with pre-signed URL
    +-- Delivers via webhooks to builder endpoints
    +-- Handles delivery retries and failures
```

## Data Flow: Subscription Events

```
Provider (e.g., Salesforce Platform Events)
    |
    v
Cloud Function (webhook gateway)
    |
    v
Pub/Sub: SubscribeWebhookReceived topic
    |
    v
Messenger: subscribeReceiveHandler()
    |-- subscribeReceiveWebhook() - validates, processes event
    |
    v
Pub/Sub: SubscribeWebhookProcessed topic
    |
    v
Messenger: subscribeDeliveryHandler()
    |-- deliverSubscribeData() - delivers to builder's webhook
```

## Key Implementation Files

- `main.go` -- Service initialization and listener configuration
- `deliverReadData.go` -- Read result processing and webhook delivery
- `writeProcessPoll.go` -- Bulk write job polling
- `subscribeEventProcessor.go` -- Incoming subscription event processing
- `deliverSubscribeData.go` -- Subscription event delivery to builders
- `notificationWebhook.go` -- Notification processing via Svix
- `providerSchemaChange.go` -- Provider schema change handling
- `messageHandler.go` -- Shared message handling utilities
- `metrics.go` -- Prometheus metric definitions
- `shared.go` -- Shared helper functions

## Metrics

Each handler tracks:
- Messages received (counter)
- Messages acked/nacked (counter)
- Errors total (counter)
- Dequeue errors (counter)
- Processing time (histogram)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SUBSCRIPTION_ENABLE_READ_FINISHED` | true | Enable read result processing |
| `SUBSCRIPTION_ENABLE_POLL_BULK_JOB` | true | Enable write poll processing |
| `SUBSCRIPTION_ENABLE_WEBHOOK_RECEIVED` | true | Enable subscription event intake |
| `SUBSCRIPTION_ENABLE_WEBHOOK_PROCESSED` | true | Enable subscription event delivery |
| `SUBSCRIPTION_ENABLE_NOTIFICATION_EMITTED` | true | Enable notification delivery |
| `SUBSCRIPTION_ENABLE_PROVIDER_SCHEMA_CHANGED` | true | Enable schema change processing |
| `ENABLE_11X_SUBSCRIPTION` | false | Enable dedicated 11x subscription (prod only) |
| `SUBSCRIPTION_TIMEOUT_*` | varies | Per-subscription ack deadline timeouts |

## Dependencies

- **Google Pub/Sub** -- Message consumption
- **PostgreSQL** -- Operation and installation data
- **Google Cloud Storage** -- Read result retrieval
- **Svix** -- Webhook delivery infrastructure
- **Builder webhook endpoints** -- Final delivery targets

## Cross-References

- Architecture overview: `services/server-architecture.md`
- Temporal (produces messages): `services/temporal.md`
- Scribe (parallel Pub/Sub consumer): `services/scribe.md`
