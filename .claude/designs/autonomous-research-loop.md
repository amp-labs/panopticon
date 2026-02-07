# Autonomous Research Loop Design

**Created:** 2026-02-06
**Status:** Implementing
**Purpose:** Close the knowledge loop - autonomous gap detection → research → documentation → re-analysis

## Problem

The knowledge-analyzer detects 60 gaps but requires manual research to fill them. This creates a bottleneck: the repository knows what it doesn't know, but can't autonomously learn it.

## Solution

Use Claude Agent SDK (like ticket-implementer) to spawn ephemeral Claude Code instances that research and document gaps autonomously.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ knowledge-analyzer                                           │
│ - Scans all content docs                                     │
│ - Detects 60 gaps (18 high, 27 medium, 15 low)             │
│ - Writes to research-tasks.md                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ autonomous_research.py (NEW)                                 │
│ - Reads high-priority gaps from research-tasks.md           │
│ - Spawns Claude Code via SDK for each gap                   │
│ - Monitors progress, validates results                       │
└────────────────────┬────────────────────────────────────────┘
                     │ For each gap
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Claude Code (ephemeral subprocess)                           │
│ - Configured with McPanda MCP server                         │
│ - permission_mode="bypassPermissions" (fully autonomous)     │
│ - Research prompt specific to gap                            │
│                                                               │
│ Tools available:                                              │
│ - mcp__mcpanda__* (77 tools - code search, GCP access, etc.) │
│ - Read/Write/Edit (update documentation)                     │
│ - Grep/Glob (explore codebase)                               │
│ - Bash (run commands, check deployments)                     │
└────────────────────┬────────────────────────────────────────┘
                     │ Research complete
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Validation                                                    │
│ - Check if documentation was updated                         │
│ - Verify gap addressed                                        │
│ - Mark task complete in research-tasks.md                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ Re-analyze (detect new gaps)                                 │
│ - Run knowledge-analyzer again                               │
│ - New gaps may emerge from new documentation                 │
│ - Cascading research: gap fill reveals new gaps              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     └─────> Repeat until no high-priority gaps
```

## Implementation

### File: `.claude/scripts/autonomous/autonomous_research.py`

**Dependencies:**
- `claude-agent-sdk` (from ticket-implementer pattern)
- `pyyaml` (already installed)
- McPanda MCP server running

**Key Components:**

1. **Gap Reader**
   - Parse research-tasks.md
   - Extract high-priority gaps
   - Convert to research prompts

2. **Research Orchestrator**
   - Spawn Claude Code via SDK
   - Configure with McPanda MCP
   - Send research prompt
   - Stream progress
   - Collect result

3. **Validator**
   - Check documentation updates
   - Verify gap addressed
   - Update research-tasks.md

4. **Loop Controller**
   - Process gaps one at a time (safer than parallel)
   - Re-analyze after each gap
   - Stop when no high-priority gaps remain
   - Timeout after N iterations (prevent infinite loop)

### Research Prompt Template

```python
research_prompt = f"""You are a knowledge-researcher agent for Panopticon repository.

**Gap ID:** {gap_id}
**Topic:** {topic}
**Document:** {document}
**Description:** {description}

**Your Task:**
Research and document {topic} for {document}.

**Research Sources:**
1. McPanda tools - Use mcp__mcpanda__* tools to:
   - Search server codebase for implementation
   - Check argocd manifests for deployment config
   - Query GCP infrastructure via McPanda
   - Access live system information

2. Codebase exploration:
   - Use Grep to search for relevant code
   - Use Read to understand implementation
   - Check related service docs for patterns

3. Documentation:
   - Update {document} with findings
   - Follow existing format and style
   - Include inline citations (file:line format)
   - Add confidence markers if uncertain

**Success Criteria:**
- {topic} is thoroughly documented in {document}
- Information is accurate and verified from sources
- Follows existing documentation patterns
- Includes citations and confidence markers

**Output:**
Your response should explain what you researched and documented.
The documentation should already be written to {document} via Edit/Write tools.
"""
```

### Claude Agent SDK Configuration

```python
from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

options = ClaudeAgentOptions(
    mcp_servers={
        "mcpanda": {
            "url": "http://localhost:3000"  # McPanda MCP server
        }
    },
    allowed_tools=[
        "mcp__mcpanda__*",  # All McPanda tools
        # Built-in tools automatically available:
        # - Read, Write, Edit (file operations)
        # - Grep, Glob (search)
        # - Bash (commands)
    ],
    permission_mode="bypassPermissions",  # Fully autonomous!
    cwd=str(repo_root),  # Panopticon repository
    stderr=stderr_callback  # Capture SDK output for debugging
)

# Spawn Claude Code and research
async for message in query(prompt=research_prompt, options=options):
    # Stream progress
    if isinstance(message, AssistantMessage):
        # Claude is working...
        pass

    if isinstance(message, ResultMessage):
        if message.subtype == "success":
            result = message.result
            # Research complete!
        elif message.subtype == "error":
            # Research failed
            raise RuntimeError(message.error)
```

## Validation Strategy

After each research task:

1. **Check documentation updated:**
   ```python
   # Read the target document
   doc_content = Path(document).read_text()

   # Check if topic is now documented
   # Look for topic keywords, section headers, etc.
   documented = topic.lower() in doc_content.lower()
   ```

2. **Run analyzer on updated doc:**
   ```python
   # Re-analyze just this document
   entry = analyzer.analyze_document(doc_path)

   # Check if gap is resolved
   gap_still_exists = any(
       g["gap_id"] == gap_id
       for g in entry.gaps
   )
   ```

3. **Mark task complete:**
   ```python
   # Update research-tasks.md
   # Move from "High Priority" to "Completed" section
   # Or remove entirely
   ```

## Safety Mechanisms

1. **Max iterations:** Stop after 10 research cycles (prevent infinite loop)

2. **Timeout per gap:** 10 minutes max per research task

3. **Validation required:** Must verify doc updated before marking complete

4. **Manual fallback:** If automation fails, leave task in research-tasks.md for manual pickup

5. **Logging:** Comprehensive logging of all actions for debugging

6. **Error handling:** Graceful degradation - one gap fails, continue with next

## Usage

```bash
# Run autonomous research loop
.claude/scripts/autonomous/autonomous_research.py

# With options
.claude/scripts/autonomous/autonomous_research.py \
  --max-iterations 5 \
  --timeout 600 \
  --priority high \
  --mcpanda-url http://localhost:3000
```

## Integration Points

### With knowledge-analyzer

```bash
# 1. Run analyzer (detects gaps, creates research tasks)
.claude/scripts/analyzer/analyze_content.py

# 2. Run autonomous research (fills high-priority gaps)
.claude/scripts/autonomous/autonomous_research.py

# 3. Re-run analyzer (detects new gaps from filled gaps)
.claude/scripts/analyzer/analyze_content.py
```

### With /analyze skill

Could enhance `/analyze` to optionally trigger autonomous research:

```bash
/analyze --auto-research  # Run analyzer + autonomous research loop
```

## Success Metrics

- **Gap fill rate:** % of high-priority gaps successfully researched
- **Accuracy:** % of documented information that's correct
- **Efficiency:** Time per gap researched
- **Cascade effect:** New gaps detected from filled gaps
- **Coverage growth:** Total entities/coverage before vs after

## Known Limitations (Acceptable for v1)

1. **Sequential processing:** One gap at a time (not parallel)
   - **Why:** Safer, easier to debug
   - **Future:** Parallel processing with coordination

2. **No cross-gap learning:** Each research task is independent
   - **Why:** Simpler implementation
   - **Future:** Share context between gaps

3. **No human review loop:** Fully autonomous
   - **Why:** Trust Claude + validation
   - **Future:** Optional human review gate

4. **McPanda dependency:** Requires McPanda MCP server running
   - **Why:** Critical for code/infra access
   - **Mitigation:** Check McPanda availability before starting

5. **No retry logic:** Failed gap stays in research-tasks.md
   - **Why:** Simpler error handling
   - **Future:** Exponential backoff retry

## Technical Debt

**DEBT-008: Autonomous research sequential processing**
- **Created:** 2026-02-06
- **Component:** autonomous_research.py
- **Category:** Performance
- **Impact:** Slow at scale (18 gaps × 5min = 90min)
- **Triggers:** When gap count > 50 or total time > 2 hours
- **Cost to fix:** 4 hours (parallel orchestration with coordination)
- **Decision:** Sequential acceptable for v1 (18 gaps manageable)

**DEBT-009: No cross-gap context sharing**
- **Created:** 2026-02-06
- **Component:** autonomous_research.py
- **Category:** Intelligence
- **Impact:** Duplicate research, missed connections
- **Triggers:** When gaps have overlapping topics
- **Cost to fix:** 8 hours (shared context mechanism)
- **Decision:** Independent tasks acceptable for v1

## Migration Path

```
v1: Sequential autonomous research (shipping now)
  ↓
v2: Parallel processing with coordination (at 50+ gaps)
  ↓
v3: Cross-gap context sharing (when overlap detected)
  ↓
v4: Human review loop (optional quality gate)
  ↓
v5: Multi-agent collaboration (specialized researchers)
```

## Example Run

```
$ .claude/scripts/autonomous/autonomous_research.py

🔍 Autonomous Research Loop Starting
════════════════════════════════════════════════════════════

📋 Reading research tasks from research-tasks.md...
   Found 18 high-priority gaps

🎯 Gap 1/18: mcpanda-002 (Deployment - mcpanda)
────────────────────────────────────────────────────────────
   Topic: deployment
   Document: services/mcpanda.md

   🚀 Spawning Claude Code researcher...
   ✓ Claude Code SDK initialized
   ✓ McPanda MCP connected (77 tools available)

   📖 Researching deployment configuration...
      → Calling: mcp__mcpanda__argocd_get_app_details
      → Calling: mcp__mcpanda__gcp_gke_get_cluster_details
      → Reading argocd manifests...
      → Updating services/mcpanda.md...

   ✓ Research complete (4m 23s)
   ✓ Documentation updated
   ✓ Gap validated as resolved

🔄 Re-analyzing services/mcpanda.md...
   ✓ Gap mcpanda-002 resolved
   ⚠ New gap detected: mcpanda-003 (scaling configuration)

🎯 Gap 2/18: messenger-001 (Authentication - messenger)
────────────────────────────────────────────────────────────
...

════════════════════════════════════════════════════════════
✅ Autonomous Research Complete!

📊 Summary:
   - Gaps processed: 18
   - Successfully researched: 16
   - Failed (retryable): 2
   - New gaps detected: 5
   - Total time: 1h 12m

📈 Repository growth:
   - Coverage before: 60% detailed, 25% mentioned, 15% not_covered
   - Coverage after: 72% detailed, 18% mentioned, 10% not_covered
   - Knowledge gain: +12% detailed coverage

🔄 Next steps:
   - 2 failed gaps remain in research-tasks.md
   - 5 new gaps added (cascading from research)
   - Run again to process new gaps
```

## Philosophy

**"The repository that teaches itself."**

This closes the autonomous loop:
1. **Catalog** what we know (analyzer)
2. **Identify** what we don't know (gap detection)
3. **Research** what we don't know (autonomous research) ← **NEW**
4. **Repeat** (self-evolving)

The repository becomes a living knowledge system that continuously improves itself by detecting gaps and autonomously filling them.

---

**Status:** Ready to implement
**Next:** Build autonomous_research.py using Claude Agent SDK pattern from ticket-implementer
