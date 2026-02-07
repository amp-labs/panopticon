---
name: ask
description: Search the Panopticon knowledge repository for information
---

You are about to launch the **knowledge-librarian** agent to search for information in Ampersand's Panopticon repository.

## What the Librarian Does

The librarian is the **reference desk** - they help you find information that's already in the repository.

**Librarian responsibilities:**
- 🔍 **Search** for information using indexes and grep
- 📖 **Retrieve** relevant documentation with source citations
- 📝 **Leave feedback** about every search (mandatory)
- 💡 **Suggest** next steps if information is incomplete
- 🎯 **Identify gaps** for researcher or scout to address

## When to Use the Librarian

**Finding Existing Information:**
- "What do we know about Salesforce OAuth?"
- "How does our GCP infrastructure work?"
- "What providers does Customer X use?"
- "Find information about [any documented topic]"

**Quick Lookups:**
- "What's the org ID for Acme Corp?"
- "How do we handle Temporal workflows?"
- "What's our incident response process?"

**General Queries:**
- Any question that might already be documented
- When you need to cite sources
- When you want to know what we've already documented

## When NOT to Use the Librarian

**Use knowledge-researcher instead if:**
- Information clearly doesn't exist yet (need to create it)
- Need deep investigation of a new topic
- Need to gather information from external sources

**Use knowledge-scout instead if:**
- Need to find new sources of information
- Need to evaluate source quality

**Use knowledge-steward instead if:**
- Need to reorganize documentation
- Need to update indexes

## How the Librarian Works

1. **Progressive Search Strategy:**
   - Start with indexes (fastest)
   - Follow cross-references (moderate)
   - Use keyword search (slower)
   - Structured exploration (slowest)
   - Acknowledge failure (with suggestions)

2. **Always Leaves Feedback:**
   - Every query adds entry to feedback.md
   - Documents search difficulty
   - Suggests improvements
   - This feedback helps steward improve organization

3. **Returns Information:**
   - Presents findings with source citations
   - Rates confidence level
   - Suggests next steps if incomplete

## Example Invocation

Ask the user what they want to find, then invoke the librarian:

```
I'll search the Panopticon repository for information about [topic].

Search strategy:
1. Check relevant indexes
2. Follow cross-references
3. Use keyword search if needed
4. Report findings and leave feedback
```

Then use the Task tool with `subagent_type: "knowledge-librarian"` to launch the search.

## The Feedback Loop

```
Librarian searches → Leaves feedback → Steward improves → Next search is easier
```

Every search makes the repository better by providing feedback for the steward to act on.

---

**Remember:** The librarian finds information that EXISTS. If it doesn't exist yet, suggest research or scouting instead.
