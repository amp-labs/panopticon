---
name: scout
description: Discover new knowledge sources or evaluate existing ones
---

You are about to launch the **knowledge-scout** agent to discover, evaluate, and maintain Ampersand's catalog of knowledge sources.

## What the Scout Does

The scout is the **pathfinder** - they find and evaluate information sources, while the researcher gathers information FROM those sources.

**Scout responsibilities:**
- 🔍 **Discover** new knowledge sources (repos, docs, tools, databases)
- 📊 **Evaluate** existing sources (quality, usefulness, accessibility)
- ✂️ **Prune** sources that are stale, inaccurate, or low-value
- 📝 **Maintain** KNOWLEDGE-SOURCES.md catalog
- 🎯 **Recommend** research priorities to the researcher

## When to Use the Scout

**Source Discovery:**
- "Are there new repositories or documentation we should know about?"
- "What new MCP tools are available?"
- "Check for new Slab documentation"

**Source Evaluation:**
- "Which knowledge sources are most valuable?"
- "Are our current sources still maintained?"
- "Audit the quality of existing sources"

**Source Pruning:**
- "Remove outdated or stale sources"
- "Which sources are no longer useful?"
- "Clean up KNOWLEDGE-SOURCES.md"

**General Audit:**
- "Run a complete source audit"
- "Update source ratings and recommendations"

## Scout vs. Researcher

| Scout | Researcher |
|-------|------------|
| Finds sources | Uses sources |
| Evaluates source quality | Gathers information |
| Maintains KNOWLEDGE-SOURCES.md | Creates topic documentation |
| Discovers where to look | Investigates specific topics |
| Meta-level (sources) | Ground-level (information) |

## Typical Workflow

1. **Ask user what scouting task** they want performed
2. **Clarify scope** (discovery, evaluation, pruning, or full audit)
3. **Invoke the scout** with clear objective
4. **Review results** (new sources, pruned sources, updated ratings)
5. **Optionally invoke researcher** if high-value sources were discovered

## Example Invocation

```
I'll discover new knowledge sources by scanning for:
- New repositories in parent directories
- New documentation files in existing repos
- New MCP tools and capabilities
- Recent Slab posts or documentation
```

Then use the Task tool with `subagent_type: "knowledge-scout"` to launch the scouting session.

---

**Remember:** The scout is about SOURCES, not INFORMATION. They're the map-maker, not the explorer.
