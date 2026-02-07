---
name: steward
description: Maintain, organize, and optimize Ampersand's institutional knowledge repository
---

You are about to launch the **knowledge-steward** agent to maintain and optimize the Panopticon knowledge repository.

The steward can handle:
- **Index Maintenance**: Update START-HERE.md and all topic indexes
- **Feedback Processing**: Review agent feedback and implement improvements
- **Documentation Reorganization**: Restructure areas that have become unwieldy
- **Quality Control**: Audit docs for professional tone, accuracy, and consistency
- **Research Coordination**: Maintain research-tasks.md and suggest priorities

Ask the user what stewardship task they want performed, then invoke the knowledge-steward agent with a clear objective.

Example invocation:
```
I'll perform [stewardship task] by [specific actions].
```

Then use the Task tool with `subagent_type: "knowledge-steward"` to launch the stewardship session.
