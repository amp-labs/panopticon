# Infrastructure Index

This index documents Ampersand's infrastructure, deployment systems, and operations.

## Major Components

### Google Cloud Platform
- **GCP Infrastructure** - GKE, Cloud SQL, Pub/Sub, Cloud Functions, KMS, storage, networking --> `infrastructure/gcp-infrastructure.md`

### Kubernetes & Service Mesh
- GKE cluster per environment gradient (prod/staging/dev/preview)
- Kong API Gateway (internet-facing + outpost-facing)
- Service collapsing in dev (single pod handles api/read/write/proxy)
- Pod Disruption Budgets for HA in production
- See `infrastructure/gcp-infrastructure.md` for details

### CI/CD & Deployment
- **Deployment Pipeline** - Cloud Build, ArgoCD GitOps, promotion flow, preview environments --> `infrastructure/deployment-pipeline.md`
- Testing onion: unit -> integration -> preview -> dev -> staging -> prod
- Sed-based templating (not Helm/Kustomize)
- Promotion: dev -> staging -> prod (no skipping)

### Databases
- **Database Architecture** - PostgreSQL via GORM, Atlas migrations, repository pattern, entity hierarchy --> `infrastructure/database-architecture.md`
- PostgreSQL 15, 107+ migrations, 64-core in prod
- Five-package structure: types/models/gormdb/memory/mock

### Message Queues & Pub/Sub

8 primary Pub/Sub topics for inter-service communication:

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

See `infrastructure/gcp-infrastructure.md` for full Pub/Sub details.

### Webhook Delivery
- **Svix** (managed) - Webhook destinations
- **Outpost** (self-hosted, Hookdeck) - Kinesis destinations, at-least-once delivery
- Future: consolidation to Outpost for all delivery

## Environment Gradient

| Environment | Services | DB Cores | Auto-scaling | Alerting |
|-------------|----------|----------|-------------|----------|
| **Production** | Full separation (10 deployments) | 64 | Yes | PagerDuty, Slack |
| **Staging** | Some separation | Mid-tier | Yes | Conditional |
| **Dev** | Collapsed (1 API pod) | Minimal | No | None |
| **Preview** | Collapsed (like dev) | Shared dev DB | No | None |

## Cross-Cutting Concerns

- Services architecture --> See `services-index.md`
- Security --> See `security-index.md`
- Observability --> See `observability-index.md`
