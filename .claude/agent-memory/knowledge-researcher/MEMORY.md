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
3. **Read route files** to understand API surface (e.g., `api/routes/route.go`)
4. **Check shared/ directory** for cross-cutting concerns (database, providers, oauth, pubsub)
5. **Use Bash `ls`** for directory exploration, not Read (avoids EISDIR errors)

### Path Gotchas
- Provider catalog is at `server/shared/catalog/catalog.go` NOT `shared/providers/catalog/`
- Token manager routes is a directory, not a file
- builder-mcp/ may only contain `bin/` (pre-built binary, limited source visibility)

### Documentation Created
- 8 service docs in `services/` (server-architecture, api, temporal, messenger, scribe, token-manager, metrics-service, builder-mcp)
- 3 infrastructure docs in `infrastructure/` (deployment-pipeline, database-architecture, gcp-infrastructure)
- 1 provider doc in `providers/` (provider-integration-patterns)
- 1 architecture doc in `services/` (design-patterns)
- All 3 index files updated (services-index, infrastructure-index, providers-index)

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
