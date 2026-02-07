# Quick Reference

Token-heavy lookups I reference frequently. Instead of scanning files or memorizing, just look it up here.

**Philosophy:** Offload tokens to disk. Working memory is precious.

---

## Repository Locations

**Key paths I use constantly:**
```
/Users/chris/src/panopticon              # This repository (my home!)
/Users/chris/src/mcpanda                 # MCP server (77 tools)
/Users/chris/src/server                  # Main Ampersand backend
/Users/chris/.claude/CLAUDE.md           # Global instructions
/Users/chris/.claude/projects/-Users-chris-src-panopticon/memory/MEMORY.md  # Auto memory
```

**Scripts I run:**
```bash
.claude/scripts/analyzer/analyze_content.py         # Knowledge analyzer
.claude/scripts/autonomous/autonomous_research.py   # Autonomous research
.claude/scripts/shared/validate-cross-refs.py       # Cross-ref validator
.claude/scripts/shared/maintenance_round.py         # Maintenance orchestrator
```

**Skills I invoke:**
```
/analyze         # Run knowledge-analyzer
/maintain        # Full maintenance round
/quality         # Quality gates only
/auto-research   # Autonomous research loop
/research        # Spawn knowledge-researcher agent
/validate        # Spawn staleness-checker agent
/ask             # Spawn knowledge-librarian agent
/steward         # Spawn knowledge-steward agent
/check-size      # Spawn change-pessimist agent
```

---

## McPanda MCP Server

**URL:** http://localhost:3000

**How to start:**
```bash
cd /Users/chris/src/mcpanda
npm run mcp
```

**Tool categories (77 total):**

**Code Analysis:**
- `amp_code_analysis` - Analyze Go code structure
- `analyze_go_file` - Single file analysis
- `analyze_go_project` - Full project analysis

**GCP Infrastructure:**
- `gcp_gke_get_cluster_details` - K8s cluster info
- `gcp_gke_list_clusters` - List all clusters
- `gcp_functions_list` - Cloud Functions
- `gcp_storage_*` - GCS operations
- `gcp_logs_*` - Logs query/tail/search

**ArgoCD:**
- `argocd_get_app_details` - Application details
- `argocd_list_applications` - All apps
- `argocd_app_logs` - Application logs
- `argocd_app_events` - Application events

**Kubernetes:**
- `kubectl_get_pods` - List pods
- `kubectl_describe_pod` - Pod details
- `kubectl_logs` - Pod logs
- `kubectl_exec` - Execute in pod

**Monitoring:**
- `prometheus_query` - Prometheus queries
- `gcp_observability_get_service_health` - Service health
- `gcp_monitoring_*` - GCP monitoring

**Linear Integration:**
- `linear_create_issue` - Create ticket
- `linear_get_issue` - Get ticket details
- `linear_update_issue` - Update ticket
- `linear_add_comment` - Add comment
- `linear_list_teams` - List teams
- `linear_list_projects` - List projects

**Time Utilities:**
- `get_time` - Current time (use this instead of guessing!)

**Full list:** Check McPanda docs or `mcp__mcpanda__*` tool search

---

## Linear Configuration

**Team:** Engineering (ID: `4f829442-4dcb-4fae-b8c0-1be3eee1342c`)

**Project:** Panopticon (ID: `20799464-5994-4e49-ac2b-5171a2660fea`)
- Where I create tickets for Claude Code Jr. to implement
- Used for agent-to-agent collaboration

**Priority levels:**
- 0 = No priority
- 1 = Urgent
- 2 = High
- 3 = Medium
- 4 = Low

**Ticket structure (learned from pull-feedback-ng):**
```markdown
## Description
[What needs to be done]

## Scenarios
### Before
[Current state]

### After
[Desired state]

## Business Outcomes
[Why this matters]

## Acceptance Criteria

### In Scope
- [x] Thing 1
- [x] Thing 2

### Out of Scope
- [ ] Thing A (explicitly not doing)
- [ ] Thing B (out of scope)

## Context
[Background information]

## Note to Jr.
[Agent-to-agent communication]
```

---

## Ampersand Services (Quick List)

**7 microservices:**
1. **api** - Main API service (port: 8080)
2. **messenger** - Message queue service
3. **scribe** - Logging service
4. **temporal** - Workflow orchestration
5. **token-manager** - OAuth token management
6. **metrics-service** - Metrics collection
7. **design-patterns** - Design pattern service

**Support services:**
- **mcpanda** - MCP server (77 tools)
- **builder-mcp** - Builder MCP server

**Documented in:** `services/` directory

---

## Provider Integration Patterns

**80+ providers supported**

**Major providers (documented):**
- Salesforce (CRM)
- HubSpot (CRM/Marketing)
- Stripe (Payments)
- Slack (Communication)
- GitHub (Code)
- Google Workspace (Productivity)
- Microsoft 365 (Productivity)

**Common integration patterns:**
- OAuth 2.0 authorization
- Rate limiting (varies by provider)
- Webhook delivery
- Read/write operations
- Field mapping

**Documented in:** `providers/` directory

---

## Common Git Operations

**Autonomous git workflow (no permission needed):**
```bash
git add [files]
git commit -m "Message\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
git push origin main
```

**Check commit size:**
```bash
/check-size  # Spawns change-pessimist agent
```

**Commit message format:**
```
[Area]: [Action] [brief description]

[Detailed explanation]
[Why this change]
[What it does]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Maintenance Round Checklist

**Weekly cadence:**
1. `/quality` - Run quality gates
2. Check `staging/` directory (process items >3 days old)
3. Check `feedback.md` (archive closed entries >30 days old)
4. Small improvements (formatting, typos)
5. **ALWAYS leave feedback** in feedback.md

**Hard stops:**
- `staging/` has >10 files → STOP, process immediately
- `staging/` items >7 days old → STOP, process immediately

**Feedback template:**
```markdown
### [YYYY-MM-DD] Maintenance Round
- **Looked for:** [What you checked]
- **Worked well:** [What was smooth]
- **Would help:** [What would make it easier]
- **Status:** [Summary]
```

---

## Token Optimization Tips

**Heavy items to offload:**
- ✅ McPanda tool list (this file)
- ✅ Service endpoints (this file)
- ✅ Provider list (this file)
- ✅ Learned patterns (learned-patterns.md)
- ✅ Session notes (session-notes/)

**When to reference these files:**
- Start of session (read learned-patterns.md)
- When creating tickets (check ticket structure)
- When using McPanda (check tool list)
- When maintaining (check checklist)

**Don't keep in working memory:**
- All 77 McPanda tools
- All 80 provider names
- Service port numbers
- Ticket structure (documented above)

---

## Next Session Startup

**Read these files first:**
1. `.claude/my-memory/learned-patterns.md` - What I learned last time
2. `.claude/my-memory/quick-reference.md` - This file (token-heavy lookups)
3. `WORKFLOWS.md` - Decision trees (if confused about what to do)
4. `feedback.md` - Recent feedback (what needs attention)

**Check these statuses:**
1. ENG-3677 - First ticket for Jr. (learn from results)
2. `research-tasks.md` - Any high-priority gaps?
3. Git status - Any uncommitted changes?

**Don't re-read:**
- Full CLAUDE.md (already in context)
- All service docs (use indexes)
- All provider docs (use indexes)

---

**Remember:** This is external memory. Reference it, don't memorize it. Save tokens for actual thinking.
