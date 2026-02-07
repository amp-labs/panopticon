# Services Architecture Index

This index documents Ampersand's 7 microservices architecture plus developer tooling.

## Core Services

1. **api** - REST API server, authentication, routing (TBD)
2. **temporal** - Workflow orchestration (TBD)
3. **messenger** - Message handling (TBD)
4. **scribe** - _Purpose to be documented_
5. **token-manager** - OAuth token management (TBD)
6. **metrics** - Metrics collection (TBD)
7. **builder-mcp** - MCP server for builders (TBD)

## Developer Tooling

8. **mcpanda** ✅ - MCP server for integration testing (77 tools, production-ready) → `services/mcpanda.md`

## Cross-Cutting Concerns

- Security → See `security-index.md`
- Observability → See `observability-index.md`
- Data Flow → See `data-flow-index.md`
- Testing → See `testing-patterns.md`

---

**Note:** Structure will evolve as services are documented.
