# Research Tasks

This file tracks knowledge gaps, low-confidence claims, and areas needing investigation by the knowledge-researcher agent.

## How This Works

- **Knowledge-steward** identifies gaps from feedback and marks items here
- **Knowledge-researcher** picks up tasks and investigates them
- **Completed research** gets removed from this list
- **Format can evolve** based on what works best

## High Priority
_(Tasks that impact multiple agents or critical workflows)_

### CONSOLIDATED: Cross-Cutting Service Concerns
**Gap ID:** services-cross-cutting-001
**Type:** systematic_gap
**Scope:** All service documentation
**Created:** 2026-02-06 (consolidated from 23+ individual tasks)

**Pattern identified:** Knowledge-analyzer generated 23+ individual tasks for Authentication, Rate Limiting, and Deployment across 8 services. These are cross-cutting concerns that should be documented systematically, not per-service.

**Recommended approach:**
1. **Create infrastructure/service-patterns.md** covering:
   - Standard authentication patterns used across services
   - Rate limiting implementation (global vs per-service)
   - Deployment patterns and argocd configuration structure
   - Service-to-service authentication
   - Common middleware and security layers

2. **Update individual service docs** to reference the patterns doc:
   - "Authentication: See [service-patterns.md](../infrastructure/service-patterns.md#authentication)"
   - Note service-specific deviations from standard patterns

3. **Research sources:**
   - server/shared/ for common middleware
   - argocd/ for deployment patterns
   - server/*/auth.go (or equivalent) for auth implementations
   - Rate limiting middleware in server/shared/

**Benefits:**
- Reduces duplication (write once, reference many times)
- Easier to maintain (update patterns doc vs 8 service docs)
- Shows architectural consistency across services
- Highlights actual deviations (which are interesting)

**Affected services:**
- api, builder-mcp, design-patterns, mcpanda, messenger, metrics-service, scribe, temporal, token-manager

**Priority:** High - this is foundational knowledge about Ampersand's service architecture

## Medium Priority
_(Useful but not blocking)_

### Deployment - database-architecture
**Gap ID:** database-architecture-001
**Description:** Deployment mentioned but not detailed
**Document:** infrastructure/database-architecture.md

### Scaling - deployment-pipeline
**Gap ID:** deployment-pipeline-001
**Description:** Scaling mentioned but not detailed
**Document:** infrastructure/deployment-pipeline.md

### Scaling - gcp-infrastructure
**Gap ID:** gcp-infrastructure-001
**Description:** Scaling mentioned but not detailed
**Document:** infrastructure/gcp-infrastructure.md

### Monitoring - gcp-infrastructure
**Gap ID:** gcp-infrastructure-002
**Description:** Monitoring mentioned but not detailed
**Document:** infrastructure/gcp-infrastructure.md

### Security - gcp-infrastructure
**Gap ID:** gcp-infrastructure-003
**Description:** Security mentioned but not detailed
**Document:** infrastructure/gcp-infrastructure.md

### Rate Limiting - provider-integration-patterns
**Gap ID:** provider-integration-patterns-001
**Description:** Rate Limiting mentioned but not detailed
**Document:** providers/provider-integration-patterns.md

### Webhooks - provider-integration-patterns
**Gap ID:** provider-integration-patterns-002
**Description:** Webhooks mentioned but not detailed
**Document:** providers/provider-integration-patterns.md

### Quirks - salesforce
**Gap ID:** salesforce-001
**Description:** Quirks mentioned but not detailed
**Document:** providers/salesforce.md

### Rate Limiting - api
**Gap ID:** api-001
**Description:** Rate Limiting mentioned but not detailed
**Document:** services/api.md

### Deployment - api
**Gap ID:** api-002
**Description:** Deployment mentioned but not detailed
**Document:** services/api.md

_...and 17 more medium priority gaps (see catalog for details)_

## Low Priority / Nice to Have

_(Interesting but not urgent)_

## Low-Confidence Claims Needing Verification

_(Documented with 🟡 or 🔴 markers, need verification)_

---

**Note:** This is a living document. Priorities shift, new gaps emerge, and the structure can change as needed.
