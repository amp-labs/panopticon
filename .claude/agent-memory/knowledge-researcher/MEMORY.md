# Knowledge Researcher - Agent Memory

## Server Repository Research (2026-02-06)

### Key Source Files for Server Research
- `server/AGENTS.md` (2248 lines) - THE primary reference. Covers resource hierarchy, all services, data flow, auth, code conventions, testing. Start here for any server investigation.
- `server/README.md` (657 lines) - Local dev setup, Docker Compose, preview envs, migrations, billing (Zenskar)
- `server/docs/interface-first-design-patterns.md` (1395 lines) - Detailed design pattern documentation
- `server/argocd-infrastructure.md` (~500 lines) - Testing onion, ArgoCD, Kong, Outpost, promotions
- `server/shared/database/README.md` - Five-package structure, reference implementation

### Effective Research Patterns
1. **Start with AGENTS.md** - It's the most comprehensive single source for the server
2. **Read main.go files** for each service to understand initialization, dependencies, and configuration
3. **Read route files** to understand API surface (e.g., `api/routes/route.go` has ALL routes defined)
4. **Check shared/ directory** for cross-cutting concerns (database, providers, oauth, pubsub)
5. **Use Bash `ls`** for directory exploration, not Read (avoids EISDIR errors)
6. **Read CLAUDE.md files** in each package - they contain concise purpose/usage/examples

### Path Gotchas
- Provider catalog is at `server/shared/catalog/catalog.go` NOT `shared/providers/catalog/`
- Token manager routes is a directory, not a file
- builder-mcp/ NOW has full source (was previously bin/ only on wrong branch)

### builder-mcp Key Insight
- builder-mcp has its own CLAUDE.md (37k, very detailed guide for AI assistants)
- 90+ tools registered in `tools/registry.go` (all tool names via `Name: "..."` grep)
- Uses factory pattern: ToolDefinition -> Factory -> core.ToolRegistrar -> Register()
- Has memory service using chromem-go (vector DB), state machine workflows (YAML configs)
- Dual transport: HTTP (default) and stdio (for Claude Code)
- Maturity filtering: dev=1, staging=3, prod=5

### shared/ Package Discovery
- 56 packages total in `server/shared/`
- Each has CLAUDE.md with purpose, key types, examples
- Notable: `customer/` has hardcoded org IDs per customer (TEMPORARY)
- Notable: `associations/` has hardcoded entity associations (TEMPORARY)
- Notable: `biller/` supports Zenskar + Orb + dual-write migration
- Notable: `mcp/` provides Redis-backed session persistence for builder-mcp

### API Routes Discovery
- ALL routes defined in `api/routes/route.go` (single file, ~970 lines)
- Routes organized by subdomain: api, read, write, proxy, signin
- New endpoints: my-info, claimed-domains, notification-event-topic-routes, topic-destination-routes, org memberships
- Route deduplication via DedupKey for shared routes across subdomains

### Documentation Created / Updated
- 8 service docs in `services/` (server-architecture, api, temporal, messenger, scribe, token-manager, metrics-service, builder-mcp)
- 3 infrastructure docs in `infrastructure/` (deployment-pipeline, database-architecture, gcp-infrastructure)
- 1 provider doc in `providers/` (provider-integration-patterns)
- 1 architecture doc in `services/` (design-patterns)
- All 3 index files updated (services-index, infrastructure-index, providers-index)
- builder-mcp.md: FULL rewrite from MEDIUM to HIGH confidence
- server-architecture.md: shared/ expanded from ~30 to 56 packages
- api.md: 6 new route files documented, subdomain routing, new endpoints table

### Repository Notes
- No git remote configured for panopticon repository (local commits only)
- Previous commits exist from other agents (scout, steward, etc.)

## Research Methodology
- Always read KNOWLEDGE-SOURCES.md first to understand available sources
- Check existing index files before creating new documents
- Use progressive disclosure: index -> overview -> detail documents
- Cross-reference liberally between documents
- Mark confidence levels on all claims
- Commit incrementally (don't wait for everything to be done)
- For large files (>25k tokens), use offset/limit or grep for specific patterns
- Package CLAUDE.md files are the fastest way to understand any shared/ package
