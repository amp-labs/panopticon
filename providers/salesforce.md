---
validation_metadata:
  attribution:
    source: "/Users/chris/src/server"
    source_type: "code"
    obtained_date: "2026-02-06"
    obtained_by: "knowledge-researcher"
  validation:
    last_checked: "2026-02-06 20:00"
    checked_by: "knowledge-researcher"
    status: "accurate"
    notes: "Initial documentation from server repository code analysis"
---

# Salesforce - CRM Provider Integration

**Quick Reference:** Enterprise CRM with complex API limits, CDC filtering, and custom Apex trigger support
**Category:** CRM Provider
**Status:** Production (heavily used, special features implemented)
**Complexity:** High (rate limiting, junction limits, CDC filtering, Apex deployments)

## Overview

Salesforce is one of Ampersand's most actively used CRM provider integrations. Workflow analysis shows high activity for core CRM objects (Account, Contact, Lead, Opportunity) with 40%+ of recent workflows involving these objects.

**What makes Salesforce special:**
- **Complex rate limiting** - Per-licensed-user API limits requiring adaptive throttling [source: shared/limiter/defaults.go:177-184]
- **Change Data Capture (CDC) filtering** - Custom field-based filtering for subscription events [source: shared/subscribe/providers/salesforce.go:14-51]
- **Junction limit errors** - Special handling for relationship query limits [source: shared/workflow/read/error.go:166-216]
- **Apex trigger deployment** - Scripts for deploying custom triggers to track field changes [source: scripts/sf-apex-trigger/README.md]

## Rate Limiting & Throttling

### API Limits

Salesforce API limits are **per licensed user**, not per org, making static rate limiting impossible [source: shared/limiter/defaults.go:177-178]. Ampersand implements adaptive throttling instead:

**Adaptive throttling mechanism:**
1. Parse `Sforce-Limit-Info` response header from Salesforce API [source: shared/limiter/throttle.go:127-142]
2. Extract `api-usage` (used/allowed) from header [source: shared/limiter/throttle.go:182]
3. Calculate usage ratio: `ApiUsed / ApiAllowed` [source: shared/limiter/adaptive.go:295]
4. Throttle when ratio exceeds threshold [source: shared/limiter/adaptive.go:294-303]

**Implementation details:**
- Threshold is configurable per installation [source: shared/limiter/threshold.go:15]
- Ampersand monitors usage continuously during read operations
- Automatically backs off when approaching quota limits
- Prevents exceeding Salesforce org limits

**Official Salesforce limits:** https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_api.htm [source: shared/limiter/defaults.go:184]

## Change Data Capture (CDC) Filtering

Salesforce supports advanced subscription filtering using custom fields and Apex triggers.

### Custom Field Filtering

**Example use case:** Filter Lead changes to only include records where `AgentIdentifierChanged__c` field is true [source: shared/subscribe/providers/salesforce.go:36-47]

**Configuration:**
```go
Filters: map[ObjectName]*Filter{
    "Lead": {
        EnrichedFields: []*EnrichedField{
            {Name: "AgentIdentifierChanged__c"},
        },
        FilterExpression: "AgentIdentifierChanged__c = true",
    },
}
```

**Enabling:**
- Environment variable: `ENABLE_SALESFORCE_FILTER=true` [source: shared/subscribe/providers/salesforce.go:32]
- Or specific installation ID: `customer.LeadChangeFilteredInstallationId11x` [source: shared/subscribe/providers/salesforce.go:33]

### Apex Trigger Deployment

Ampersand provides scripts for deploying custom Apex triggers to Salesforce orgs [source: scripts/sf-apex-trigger/].

**What the trigger does:**
- Tracks when specific fields change on objects (e.g., `agentidentifier__c` on Lead)
- Sets a boolean field (`AgentIdentifierChanged__c`) when field changes
- Enables CDC filtering using that boolean field [source: scripts/sf-apex-trigger/README.md:383-389]

**Deployment flow:**
1. Get OAuth credentials from Ampersand API [source: scripts/sf-apex-trigger/README.md:159-162]
2. Package Apex trigger with metadata into zip [source: scripts/sf-apex-trigger/README.md:163]
3. Deploy via Salesforce Metadata API (SOAP) [source: scripts/sf-apex-trigger/README.md:164-169]
4. Poll deployment status until complete [source: scripts/sf-apex-trigger/README.md:170]
5. Verify via Tooling API [source: scripts/sf-apex-trigger/README.md:172]

**Key scripts:**
- `scripts/sf-apex-trigger/deploy/main.go` - Deploy Apex trigger
- `scripts/sf-apex-trigger/limits/main.go` - Fetch Salesforce org limits

## Junction Limit Errors

Salesforce has a limit on junction IDs (relationship query results) that can cause read operations to fail.

**Error handling:**
- Detect junction limit errors automatically [source: shared/workflow/read/error.go:187]
- Reduce page size to stay under junction limit [source: shared/workflow/read/error.go:166]
- Minimum page size enforced to prevent infinite loops [source: shared/workflow/read/error.go:216]

**Pattern:**
```
Read operation → Junction limit error
→ Reduce page size → Retry with smaller batch
→ Continue until below minimum page size
→ Return error if still failing
```

[source: shared/workflow/read/listReader.go:175]

## Common Objects Synced

Based on workflow analysis and seed data:

**Core CRM objects:**
- **Account** - Company/organization records [source: database/seed/revision.salesforce.content.json:8]
- **Contact** - Person records associated with accounts [source: database/seed/revision.salesforce.content.json:31]
- **Lead** - Prospective customers
- **Opportunity** - Sales pipeline records

**Configuration:**
- Objects use standard Salesforce field names (lowercase: `account`, `contact`)
- Support for required fields, optional fields, and field mappings [source: database/seed/revision.salesforce.content.json:11-29]
- Schedule: Typically every 15 minutes (`*/15 * * * *`) [source: database/seed/revision.salesforce.content.json:10]

## OAuth & Authentication

Salesforce uses standard OAuth 2.0 with some Ampersand-specific handling:

**OAuth provider implementation:**
- Standard OAuth2 flow [source: shared/providers/oauth2.go]
- Token refresh handled by Ampersand
- Instance URL discovery from OAuth response
- Support for sandbox and production orgs

**Connection verification:**
- Verification params for Salesforce subscriptions [source: shared/subscribe/providers/salesforce.go:14-22]

## Related Components

- **Connectors library:** `github.com/amp-labs/connectors/providers/salesforce` - Salesforce-specific connector implementation [source: shared/subscribe/providers/salesforce.go:8]
- **Rate limiter:** `shared/limiter/` - Adaptive throttling based on Sforce-Limit-Info header
- **Read workflow:** `shared/workflow/read/` - Junction limit error handling
- **Temporal workflows:** Read, write, subscribe workflows for Salesforce operations

## Known Quirks

1. **Rate limits are per-user, not per-org** - Cannot set static rate limits, must use adaptive throttling
2. **Junction limit errors** - Relationship queries can hit limits, require dynamic page size reduction
3. **CDC requires custom fields** - Advanced filtering needs custom boolean fields + Apex triggers
4. **API version sensitivity** - Scripts use Salesforce API v61.0 [source: scripts/sf-apex-trigger/README.md:425]

## Configuration Examples

See seed data for production-tested configurations:
- `/Users/chris/src/server/database/seed/revision.salesforce.content.json` - Full revision example
- `/Users/chris/src/server/database/seed/config.salesforce.content.json` - Installation config example

## Testing & Debugging

**End-to-end test script:**
- `scripts/endToEnd/salesforce.go` - Salesforce-specific E2E tests

**Deployment tools:**
- Check Salesforce org limits: `go run ./scripts/sf-apex-trigger/limits/main.go`
- Deploy Apex triggers: `go run ./scripts/sf-apex-trigger/deploy/main.go`

---

**See also:**
- providers-index.md for other CRM providers
- services/temporal.md for workflow orchestration details
- infrastructure/rate-limiting.md (TBD) for general rate limiting architecture
