# Provider Integration Index

This index catalogs all 80+ provider integrations supported by Ampersand.

## How to Use This Index

- Each provider has its own document in `providers/`
- Documentation covers: product capabilities, API quirks, OAuth patterns, coding concerns, operational issues
- Cross-referenced with `coding-concerns/` for technical patterns

## Integration Architecture

- **Provider Integration Patterns** - Catalog system, OAuth flows, token management, rate limiting, data flow patterns --> `providers/provider-integration-patterns.md`

### Key Concepts

- **Provider Catalog**: JSON file from `amp-labs/connectors` repo, auto-refreshed every 30 minutes
- **Authentication**: OAuth2 (Authorization Code, Client Credentials), Basic Auth, API Key, JWT
- **Token Management**: Centralized Token Manager service with xxhash-based sharding
- **Rate Limiting**: Multi-level (provider-level + installation-level), threshold at 15s for Temporal sleep
- **Connectors Library**: `github.com/amp-labs/connectors` provides ReadConnector, WriteConnector, SubscribeConnector interfaces

### Data Flow Patterns

| Operation | Flow |
|-----------|------|
| **Read** | API --> Temporal --> Provider API --> GCS --> Pub/Sub --> Messenger --> Webhook |
| **Write** | API --> Data Transform --> Temporal --> Provider API --> Pub/Sub --> Status Update |
| **Subscribe** | Provider --> Cloud Function --> Pub/Sub --> Messenger --> Webhook |
| **Proxy** | Builder --> API --> Authenticated HTTP --> Provider API --> Response |

## Provider Categories

### CRM Providers
- **Salesforce** - Enterprise CRM with adaptive rate limiting, CDC filtering, Apex trigger support --> `providers/salesforce.md`
- HubSpot (TBD)
- _...more to be documented..._

### Marketing Automation
- _To be documented_

### Customer Support
- _To be documented_

### Other Categories
- _Structure will evolve as providers are documented_

---

**Note:** This index will evolve. The knowledge-steward may reorganize categories based on usage patterns.
