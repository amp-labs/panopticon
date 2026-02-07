# Server Repository Evaluation

**Evaluated:** 2026-02-06
**Status:** HIGH-VALUE SOURCE - WELL-MAINTAINED
**Confidence:** High

## Overview
The Ampersand server repository is a Go monorepo containing all backend services and is an excellent knowledge source for:
- Actual implementation details (source of truth)
- Provider integration patterns
- Database and ORM patterns
- OAuth and token management
- Temporal workflow definitions
- API endpoint specifications

## Key Metrics
- **Size:** 1,150+ Go files, 2.2GB
- **Activity:** 2,100+ commits in February 2026 (highly active)
- **Last update:** 2026-02-06
- **Services:** 7 microservices + 45+ shared libraries

## Documentation Quality
- **High quality agent documentation** (AGENTS.md is thorough and AI-aware)
- **Design patterns documented by example** (interface-first patterns)
- **Database guide with reference implementation** (examples/database/widget/)
- **Clear architectural decisions** documented in code
- **READMEs for each major area** (database, docker-compose, examples, scripts)

## Strengths
1. Source of truth for implementation (not secondary documentation)
2. Well-organized with clear separation of concerns
3. Strong architectural patterns (interface-first, context-based DI)
4. Active maintenance and frequent updates
5. Comprehensive documentation for both humans and agents
6. Reference implementations in examples/ directory
7. Makefile with 40+ targets for common tasks
8. Multiple environment support (local, dev, staging, prod)

## Limitations
1. Large codebase requires targeted searches
2. Private dependencies (amp-common) require GitHub SSH access
3. Some architectural details documented in Slab (not in repo)
4. Real customer data in prod requires authorization
5. OpenAPI spec is minimal (12KB, not fully comprehensive)

## Research Workflow Tips
- Start with AGENTS.md for architecture overview
- Use interface-first design patterns guide for understanding system design
- Database README is excellent for understanding data patterns
- git log is useful for understanding implementation decisions
- Examples directory is perfect for learning patterns
- Shared libraries are well-organized by concern

## Best Search Patterns
- Provider code: `shared/providers/`, grep for provider name
- Database patterns: `shared/database/` + `examples/database/`
- API endpoints: `api/routes/` subdirectories
- OAuth patterns: `shared/oauth/`
- Workflow logic: `shared/temporal/`
- Event handling: `scribe/` and `messenger/` services

## Integration with Other Sources
- Complements McPanda tools (live system access)
- Complements Slab (architectural decisions, runbooks)
- Complements argocd repository (deployment details)
- Used by knowledge-researcher for detailed investigation
