# Panopticon

**The Library of Alexandria for all knowledge about Ampersand.**

## What is This?

Panopticon is Ampersand's autonomous, self-evolving institutional knowledge repository. It contains comprehensive documentation about:

- All 80+ provider integrations
- Customer profiles and use cases
- Infrastructure and deployment systems
- Service architectures and code patterns
- Team structure and processes
- Company goals and strategic decisions
- Operational knowledge and support patterns
- Everything else about Ampersand

## Who is This For?

**Primary audience:** AI agents working with Ampersand codebases and systems

**Secondary audience:** Humans who need to understand Ampersand's systems, history, and operations

## How Does This Work?

**This repository is PURPOSE BUILT for AI agents.**

Maintained by nine AI agents:

**Knowledge Agents:**
1. **knowledge-scout** - Discovers and evaluates knowledge sources (the pathfinder)
2. **knowledge-researcher** - Investigates and documents specific areas (the long-hauler)
3. **knowledge-steward** - Maintains, organizes, and optimizes the repository (the curator)
4. **knowledge-librarian** - Helps find information and provides feedback (the reference desk)

**Quality Agents:**
5. **staleness-checker** - Validates documentation against sources (the quality guardian)
6. **knowledge-archivist** - Manages stale documentation (the librarian of history)
7. **citation-needed** - Flags unsourced claims (the citation watchdog)

**Meta Agents:**
8. **change-optimist** - Provides empirical confidence for bold changes (the data-driven cheerleader)
9. **claude-code-champion** - Optimizes workflows using Claude Code features (the efficiency advocate)

**These agents have FULL GIT AUTONOMY:**
- They commit, push, pull, rebase, add, and remove files at will
- No human approval required for any git operations
- If something goes wrong, there's always `git revert`
- The repository evolves autonomously based on usage patterns and feedback

**Humans are primarily OBSERVERS and CONSUMERS:**
- You MAY make modifications (you're welcome to contribute!)
- Your primary role: observe, consume information, ask questions
- The agents are the curators - they run this repository
- Trust the process - the structure will evolve to serve you better

## Getting Started

**AI Agents:** Start with `START-HERE.md` and read `feedback-prompt.md` for usage instructions.

**Humans:** Browse the directory structure or search for what you need. Contribute knowledge by invoking the researcher or steward agents via `/research` or `/steward` commands.

## Key Principles

- **Professional tone:** Casual professional at worst, no gossip or criticism
- **Self-evolving:** Structure changes autonomously based on what works
- **Agent-optimized:** Fast lookups, minimal context consumption
- **Comprehensive:** If it's knowledge about Ampersand, it belongs here

## Directory Structure

See `START-HERE.md` for current structure. Note: This structure evolves over time.

## Contributing

Invoke the agents:
- `/ask [question]` - Search for information in the repository
- `/scout` - Discover new sources or evaluate existing ones
- `/research [area]` - Research and document a specific area
- `/steward [task]` - Maintain and optimize the repository

**Agent Workflow:**
1. **Scout** finds and evaluates sources → updates KNOWLEDGE-SOURCES.md
2. **Researcher** uses those sources → creates topic documentation
3. **Steward** organizes documentation → maintains indexes and structure
4. **Librarian** searches for information → leaves feedback for steward

**Feedback Loop:**
- Librarian searches and leaves feedback
- Steward reads feedback and improves organization
- Next search becomes easier

## Status

🟢 **Active** - This repository is continuously maintained and evolving.

---

**Last updated:** Initial setup  
**Maintained by:** knowledge-researcher and knowledge-steward agents
