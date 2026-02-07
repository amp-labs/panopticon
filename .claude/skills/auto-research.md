# auto-research

Trigger the autonomous research loop to fill knowledge gaps.

**Usage:**
- `/auto-research` - Process all high-priority gaps
- `/auto-research --max-iterations 5` - Limit to 5 research cycles (coming soon)
- `/auto-research --gap-id mcpanda-002` - Research specific gap (coming soon)

**What it does:**

Spawns autonomous Claude Code instances to research and document knowledge gaps:

## The Loop

```
1. Read high-priority gaps from research-tasks.md
   ↓
2. For each gap:
   → Spawn Claude Code via SDK
   → Configure with McPanda MCP server (77 tools)
   → Send research prompt with gap context
   → Claude researches using code analysis, GCP tools, docs
   → Claude updates documentation via Edit tool
   ↓
3. Validate documentation was updated
   ↓
4. Re-run analyzer to detect new gaps
   ↓
5. Repeat until no high-priority gaps remain
```

## Research Sources

Each spawned Claude Code instance has access to:
- **McPanda tools**: 77 tools for code analysis, GCP, argocd, kubectl, etc.
- **Codebase**: Can grep, read, analyze implementation
- **File tools**: Can read, write, edit documentation
- **Live systems**: Via McPanda (with appropriate permissions)

## Safety Mechanisms

- **Max iterations**: 10 cycles (prevents infinite loop)
- **Timeout per gap**: 10 minutes max
- **Validation**: Must verify doc updated before marking complete
- **Sequential**: One gap at a time (safer, easier to debug)
- **Error handling**: One gap fails, continue with next

## When to Use

**Good times:**
- After running `/analyze` and seeing high-priority gaps
- When research-tasks.md has 10+ high-priority items
- Periodic knowledge expansion (monthly deep dives)
- When you want autonomous gap-filling without manual work

**Not needed when:**
- Only 1-2 gaps (just use `/research` manually)
- Gaps are complex and need human guidance
- McPanda MCP server not running

## Prerequisites

⚠️ **Requires McPanda MCP server running** at http://localhost:3000

Start McPanda first:
```bash
cd /Users/chris/src/mcpanda
npm run mcp
```

## Output

```
🔍 Autonomous Research Loop Starting
═════════════════════════════════════════════

📋 Iteration 1/10
   Found 18 high-priority gap(s)

🎯 Researching: mcpanda-002 (Deployment - mcpanda)
───────────────────────────────────────────────
   🚀 Spawning Claude Code researcher...
   ✓ MCP servers connected (77 tools available)

   📖 Researching deployment configuration...
      → Calling: mcp__mcpanda__argocd_get_app_details
      → Calling: mcp__mcpanda__gcp_gke_get_cluster_details
      → Updating services/mcpanda.md...

   ✓ Research complete (4m 23s)
   ✓ Documentation updated
   ✓ Gap validated as resolved

🔄 Re-analyzing repository...
   ✓ Gap mcpanda-002 resolved
   ⚠ New gap detected: mcpanda-003

═════════════════════════════════════════════
✅ Autonomous Research Complete!

📊 Summary:
   - Gaps processed: 18
   - Successfully researched: 16
   - Failed (retryable): 2
   - Total time: 1h 12m

📈 Repository growth:
   - Coverage before: 60% detailed
   - Coverage after: 72% detailed
   - Knowledge gain: +12%
```

## Philosophy

**"The repository that teaches itself."**

This closes the autonomous loop:
1. **Catalog** what we know (analyzer)
2. **Identify** what we don't know (gap detection)
3. **Research** what we don't know (autonomous research) ← THIS
4. **Repeat** (self-evolving)

The repository becomes a living knowledge system that continuously improves itself.

---

## Implementation

```bash
#!/usr/bin/env bash
# Trigger autonomous research loop

# Check McPanda is running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "❌ McPanda MCP server not running"
    echo "Start it with: cd /Users/chris/src/mcpanda && npm run mcp"
    exit 1
fi

# Run autonomous research
.claude/scripts/autonomous/autonomous_research.py "$@"
```
