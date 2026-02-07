---
validation_metadata:
  attribution:
  source: server/cloudbuild.yaml, server/argocd-infrastructure.md, server/README.md
  obtained_date: 2026-02-06
  obtained_by: knowledge-researcher
validation:
  last_checked: 2026-02-06
  status: current
---

# Deployment Pipeline and CI/CD

## Overview

Ampersand uses a GitOps deployment model with Google Cloud Build for CI and ArgoCD for CD. The pipeline follows a "testing onion" philosophy with graduated environments from dev through production.

**Confidence:** HIGH

## The Testing Onion

Each layer costs more but provides more confidence:

1. **Unit tests** (GitHub Actions, seconds, free) -- Fast feedback, no infrastructure
2. **Integration tests** (manual, minutes, cheap) -- Testharness with in-memory deps
3. **Preview environments** (`prs/`, triggered by `/gcbrun`, ~10 min) -- Full stack, ephemeral
4. **Dev** (auto-deploy on merge to main) -- Collapsed services, minimal DB
5. **Staging** (manual promotion from dev) -- Auto-scaling, mid-tier DB
6. **Production** (manual promotion from staging) -- Full separation, 64-core DB

## Build Pipeline (Google Cloud Build)

**Config:** `server/cloudbuild.yaml`
**Registry:** `us-west1-docker.pkg.dev/ampersand-prod/gke-repo/`

### Build Steps

All service images are built **in parallel** for maximum speed:

| Step | Service | Dockerfile |
|------|---------|-----------|
| 0 | api | `api/k8s/Dockerfile` |
| 1 | token-manager | `token-manager/k8s/Dockerfile` |
| 2 | messenger | `messenger/k8s/Dockerfile` |
| 3 | scribe | `scribe/k8s/Dockerfile` |
| 4 | metrics | `metrics/k8s/Dockerfile` |
| 5 | temporal | `temporal/k8s/Dockerfile` |
| 6+ | builder-mcp, ArgoCD updates | Various |

**Image tagging:**
- `$SHORT_SHA` -- Git commit short hash
- `${_IMAGE_TAG}` -- Build parameter (branch name or custom tag)

**Build caching:** Uses pre-built base image `base-builder:refreshed` as Docker cache source.

**Build arguments:**
- `flavor` -- Build flavor (dev/staging/prod)
- `project` -- GCP project ID
- `branch` -- Git branch name
- `build` -- Cloud Build ID

### Trigger: Main Branch

When code is merged to main:
1. Cloud Build triggers automatically
2. All service images built in parallel
3. Images pushed to Artifact Registry
4. ArgoCD manifests in dev/ updated with new commit SHAs
5. ArgoCD auto-syncs dev environment

### Trigger: Preview Environment

When `/gcbrun` is commented on a PR:
1. Cloud Build triggers for the PR branch
2. All service images built
3. ArgoCD `prs/<branch-name>/` directory created/updated
4. Preview environment deployed automatically

## ArgoCD (GitOps)

**Repository:** `~/src/argocd`

### Directory Structure

```
argocd/
+-- dev/                # Dev environment manifests
+-- staging/            # Staging environment manifests
+-- prod/               # Production environment manifests
+-- prs/                # Preview environments (one per active PR)
+-- template/           # Template files for new preview envs
+-- scripts/            # Automation (promote.sh, clean.sh, etc.)
+-- kong/               # Kong API gateway config
+-- outpost/            # Outpost webhook infrastructure
```

### Environment Configuration

Each environment directory contains:
- `*-deployment.yaml` -- Kubernetes Deployment manifests (what ArgoCD reads)
- `*-deployment.yaml.tpl` -- Template files with placeholders
- `*-service.yaml` -- Kubernetes Service definitions
- `*-ingress.yaml` -- Ingress configurations
- `*-prometheus.yaml` -- Prometheus ServiceMonitor configs
- `metadata.json.noargo` -- Deployment metadata (not read by ArgoCD)
- `deploy.log` -- Promotion audit trail

### Template System ("Lazy Man's Templating")

Instead of Helm or Kustomize, Ampersand uses simple sed-based templating:

```bash
# Template file (.tpl)
image: us-west1-docker.pkg.dev/ampersand-prod/gke-repo/api:COMMIT_SHA

# Rendered (.yaml)
cat api-deployment.yaml.tpl | sed "s/COMMIT_SHA/a252dcc/g" > api-deployment.yaml
```

Common placeholders: `COMMIT_SHA`, `NAMESPACE_PLACEHOLDER`, domain prefixes.

## Promotion Flow

**Command:** `make promote/staging` or `make promote/prod`
**Script:** `scripts/promote.sh`

**Rules:**
- Can only promote staging -> prod (not dev -> prod directly)
- Forces graduated rollout: dev -> staging -> prod

**Process:**
1. Read source environment metadata and image tags
2. Render target environment templates with new image SHAs
3. Update target metadata (URLs, DB, context, timestamp)
4. Log promotion details (who, when, before/after SHAs)
5. Git commit (user reviews and pushes)
6. ArgoCD auto-syncs within 5-10 minutes

**Key insight:** Promotion updates image tags in the target's own templates, preserving environment-specific configuration (resource limits, replicas, etc.).

## Preview Environments

**Creation:** `/gcbrun` comment on PR
**Cleanup:** Automatic on PR close (via `auto-clean.sh`)

**Isolation:**
- Own Kubernetes namespace (`pr-<branch-name>`)
- Own PostgreSQL database
- Own DNS entries (`<branch>.dev-api.withampersand.com`)
- Own Pub/Sub topics/subscriptions (via GKE Config Connector CRDs)
- Own Temporal queues, secrets, endpoints

**Shared infrastructure:**
- GCP project and service account
- GKE cluster and node pool
- GCS bucket (keys shouldn't clash)
- Container registry
- Clerk dev environment
- Svix dev environment
- PostgreSQL host (separate databases)
- KMS keyring

## Database Migrations (Production)

```bash
# Dev (usually auto-migrated on merge)
make migrations/gcp/dev

# Staging
make migrations/gcp/staging

# Prod (requires secure password from 1Password)
export PROD_DB_PASSWORD="password-here"
make migrations/gcp/prod
```

**Migration ordering rules:**
- Adding tables/columns/indexes: Migrate first, then deploy
- Deleting tables/columns/indexes: Deploy first, then migrate
- Renaming or type changes: Requires coordination, may need Temporal schedule pause

## Cross-References

- Service architecture: `services/server-architecture.md`
- Database architecture: `infrastructure/database-architecture.md`
- GCP infrastructure: `infrastructure/gcp-infrastructure.md`
