---
name: research
description: Research and document a specific area of Ampersand's institutional knowledge
---

You are about to launch the **knowledge-researcher** agent to investigate and document a specific area of Ampersand's institutional knowledge.

## What the Researcher Does

The researcher is the **long-hauler** - they gather raw data from known sources and document it.

**Researcher responsibilities:**
- 📚 Gather information FROM known sources
- 📝 Document specific areas (providers, customers, infrastructure, etc.)
- 🔍 Deep investigation of specific topics
- ✅ Create comprehensive topic documentation

## What the Researcher Documents

- **Providers**: Product capabilities, API quirks, OAuth patterns, licensing, operational concerns
- **Customers**: Org IDs, provider usage, use cases, integration history
- **Infrastructure**: GCP setup, Kubernetes, CI/CD, deployment pipelines
- **Team & Process**: Developer profiles, company goals, incident response, workflows
- **Code & Architecture**: Service designs, API contracts, technical decisions
- **Anything else**: Partners, vendors, compliance, best practices

## Researcher vs. Scout

If the user is asking about **finding new sources** or **evaluating sources**, use `/scout` instead.
If the user is asking about **gathering information**, use `/research`.

| Researcher | Scout |
|------------|-------|
| Uses sources | Finds sources |
| Gathers information | Evaluates source quality |
| Creates topic documentation | Maintains KNOWLEDGE-SOURCES.md |
| Investigates specific topics | Discovers where to look |
| Ground-level (information) | Meta-level (sources) |

Ask the user what area they want researched, then invoke the knowledge-researcher agent with a clear scope.

Example invocation:
```
I'll research [area] by investigating [sources] and documenting [specific aspects].
```

Then use the Task tool with `subagent_type: "knowledge-researcher"` to launch the research session.
