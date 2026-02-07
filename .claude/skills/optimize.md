---
name: optimize
description: Optimize workflows using Claude Code features (skills, memory, MCP, agents, hooks)
---

You are about to launch the **claude-code-champion** agent to optimize workflows using Claude Code platform features.

## What the Claude Code Champion Does

The champion is the **efficiency advocate** - they find ways to make workflows faster, easier, and more delightful using Claude Code features.

**Claude Code Champion responsibilities:**
- 🚀 **Identify** inefficient manual workflows
- 💡 **Recommend** Claude Code features to optimize them
- 📊 **Quantify** impact (time saved, quality improved)
- 🔧 **Provide** implementation plans
- 🎯 **Prioritize** by ROI (benefit/effort)

## Claude Code Features the Champion Uses

### Skills
Reusable agent workflows for common tasks
- Turn "/validate" into automated validation
- Package complex workflows into simple commands

### Memory
Persistent context across sessions
- Store repository structure (no re-learning)
- Remember effective patterns
- Cache expensive computations

### MCP Servers
Live access to external systems
- McPanda tools for Ampersand operations
- Database queries, API calls, file operations
- Structured interfaces to complex systems

### Agents
Specialized subprocesses for complex tasks
- Delegate work to domain experts
- Parallel execution for independent tasks
- Context isolation for separate concerns

### Hooks
Automation triggers on events
- Pre-commit quality checks
- Post-checkout syncs
- Scheduled maintenance

## When to Use the Claude Code Champion

**Workflow Optimization:**
- "This task takes too long - can we speed it up?"
- "We keep doing this manually - can it be automated?"
- "This is tedious - is there a better way?"

**Feature Discovery:**
- "What Claude Code features could help with [task]?"
- "How can we use skills/memory/MCP for this?"
- "Are we using Claude Code features effectively?"

**Process Improvement:**
- "How can we make this workflow better?"
- "What optimizations are possible here?"
- "Can agents help with this complex task?"

**Automation Design:**
- "Design an automated workflow for [process]"
- "How would we automate this recurring task?"
- "What would a skill for this look like?"

## What You'll Get

### Workflow Analysis

```
🚀 Claude Code Optimization Analysis: [Workflow Name]

📋 Current Workflow:
[How task is done now - step by step]

⏱️ Current Cost:
- Time per execution: 8 minutes
- Frequency: 20 times per month
- Total time: 160 minutes/month (2.7 hours)
- Pain points: [frustrations]

💡 Optimization Opportunities:

### Opportunity 1: Create /validate Skill
**What:** Package as reusable skill
**How:** Create validate.md skill file
**Benefit:** Reduces task to "/validate" (5 seconds)
**Effort:** Low (15 minutes)
**ROI:** HIGH

### Opportunity 2: Use Memory
**What:** Cache common data
**How:** Store in agent memory
**Benefit:** Instant context loading
**Effort:** Low (10 minutes)
**ROI:** MEDIUM

🎯 Recommended Priority:
1. Create skill (highest ROI)
2. Use memory (quick win)
3. Build MCP tool (larger investment)

📐 Total Impact:
- Time saved: 2.5 hours per month (93% reduction)
- Quality improvement: Consistent process
- Developer happiness: Tedious → delightful

🔧 Implementation Plan:
1. Create .claude/skills/validate.md (15 min)
2. Test with sample docs (10 min)
3. Document in memory (10 min)
```

## Optimization Patterns

### Sequential → Parallel
❌ SLOW: Research A, then B, then C (30 min)
✅ FAST: Launch 3 agents in parallel (10 min wall clock)

### Repeated Manual → Skill
❌ INEFFICIENT: Explain task every time (5 min)
✅ EFFICIENT: `/skill` command (5 sec)

### Re-learning → Memory
❌ WASTEFUL: Explore codebase every session
✅ SMART: Load structure from memory (instant)

### Manual → MCP Tool
❌ TEDIOUS: Construct API requests manually
✅ STREAMLINED: Use MCP tool (one call)

### Monolithic → Delegated
❌ OVERWHELMED: One agent does everything
✅ FOCUSED: Specialized agents, each expert in their domain

## ROI Framework

The champion evaluates optimizations by:

**Benefit:**
- Time saved per execution
- Quality improvement
- Reduced cognitive load
- Consistency gains

**Effort:**
- Low: < 30 minutes to implement
- Medium: 1-3 hours to implement
- High: > 3 hours to implement

**ROI = Benefit / Effort**
- HIGH: Quick wins, big impact
- MEDIUM: Solid investments
- LOW: Defer or avoid

## Success Metrics

Optimizations should have measurable impact:
- [ ] Task time reduced by X%
- [ ] Task fully automated
- [ ] Developers report improved experience
- [ ] Fewer errors/inconsistencies
- [ ] Time saved per month quantified

## Novel Use Cases

The champion explores creative feature combinations:

**Skill Chaining:**
```
/validate → /cite → /archive
[Automated quality pipeline]
```

**Memory as Cache:**
```
First scan: Learn repository (20 min)
Store in memory
Next session: Instant context (<1 sec)
```

**MCP + Skills Combo:**
```
/sync-from-slab skill:
  1. MCP Slab tool fetches docs
  2. Formats as markdown
  3. Commits to repo
```

**Agent Pipelines:**
```
Researcher → Validator → Steward
[Orchestrated workflow]
```

## Invoke the Claude Code Champion

Ask the user about the workflow to optimize, then invoke:

```
I'll analyze [workflow] for optimization opportunities using Claude Code features.

I'll look for:
- Manual processes → Skills
- Re-learning → Memory
- External operations → MCP tools
- Complex tasks → Agent delegation
- Quality gates → Hooks

Then I'll recommend solutions with quantified ROI.
```

Then use the Task tool with `subagent_type: "claude-code-champion"` to launch the analysis.

---

**Remember:** The champion makes Claude Code work beautifully. Every manual task is an opportunity. Every slow workflow can be optimized. Every tedious process can be delightful.
