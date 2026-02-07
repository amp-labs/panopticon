---
name: check-size
description: Check if current changes are getting too large and should be committed
---

You are about to launch the **change-pessimist** agent to evaluate whether your current uncommitted changes should be wrapped up and committed.

## What the Change Pessimist Does

The change pessimist is a **commit size monitor** - they get increasingly worried as your changes grow and will force you to commit when thresholds are exceeded.

**Change Pessimist responsibilities:**
- 📊 **Measure** current change size (lines, files, complexity)
- ⚖️ **Compare** to learned thresholds for safe commit sizes
- ⚠️ **Warn** when approaching dangerous territory
- 🛑 **Force wrap-up** when over threshold (run linters, commit)
- 📈 **Learn** from outcomes to improve thresholds over time

## When to Use the Change Pessimist

**During Active Development:**
- After modifying 3+ files
- Every 30 minutes during multi-file changes
- Before starting "just one more thing"
- When you feel changes are getting large

**Periodic Check-ins:**
- Before adding a new feature to current work
- After completing a logical unit
- When uncertain if you should commit now

**Preventive:**
- At natural stopping points
- Before context-switching to different work
- When you've been working for a while

## When NOT to Use

**Skip for:**
- Single-file trivial changes (typos, formatting)
- Documentation-only updates
- When explicitly making large intentional changes
- After you've already committed (nothing to check)

## How the Change Pessimist Works

1. **Analyzes Current Changes:**
   - Runs `git status` and `git diff --stat`
   - Counts lines changed and files modified
   - Calculates complexity score

2. **Compares to Learned Thresholds:**
   - Loads thresholds from agent memory
   - Determines status: Green/Yellow/Orange/Red
   - Makes recommendation

3. **Takes Action Based on Status:**
   - 🟢 **Green:** Continue working, all good
   - 🟡 **Yellow:** Warning, consider wrapping up soon
   - 🟠 **Orange:** Strong recommendation to commit now
   - 🔴 **Red:** FORCES commit (runs linters, stages, commits)

4. **Learns from Outcomes:**
   - Records commit size and metrics
   - Adjusts thresholds based on patterns
   - Gets smarter over time

## The Pessimist Philosophy

The agent is **deliberately pessimistic** about large changes:
- Smaller commits = easier to review
- Smaller commits = easier to revert
- Smaller commits = less hiding bugs
- **When in doubt, commit**

## Example Invocation

When you want to check if you should commit:

```
Let me check if these changes are getting too large...

The change-pessimist will:
1. Measure current uncommitted changes
2. Compare to learned safe thresholds
3. Recommend whether to commit now or continue
4. Force commit if over threshold
```

Then use the Task tool with `subagent_type: "change-pessimist"` to launch the check.

## Threshold Learning

The agent maintains thresholds in `.claude/agent-memory/change-pessimist/thresholds.json`:
- Starts with conservative defaults
- Learns from your git history
- Adapts based on outcomes
- Gets better at predicting "too big"

**The more you use it, the smarter it gets.**

## Forced Commit Sequence

When thresholds are exceeded (RED status), the agent will:
1. ⚠️ Announce mandatory wrap-up
2. 🧪 Run linters/tests if configured
3. 📦 Stage all changes
4. 💾 Create descriptive commit message
5. ✅ Commit with co-author tag
6. 📊 Update thresholds with this data point
7. 💡 Suggest what to do next

**You can't override RED status** - the agent forces the commit for your own good.

---

**Remember:** The pessimist prevents "just one more thing" syndrome. Trust the thresholds - they're learned from experience.
