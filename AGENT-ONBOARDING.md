# Agent Onboarding Framework

**"Before creating a new role, ensure you have the skills to fulfill its duties"**

This document defines the rigorous onboarding process for new agents in the Panopticon repository. Adding a new agent is a significant decision that requires careful planning, capability assessment, and alignment verification.

## Philosophy

Agents are not scripts—they are roles with responsibilities, capabilities, and boundaries. Like hiring a specialist, onboarding a new agent requires:
- Clear job description (what problems does it solve?)
- Skills assessment (what capabilities are needed?)
- Training plan (how will it learn the role?)
- Integration strategy (how does it fit with existing agents?)
- Quality standards (how do we measure success?)

**The bar is high.** Don't create a new agent when an existing one could expand scope. Don't create overlapping roles. Don't create agents without clear capabilities.

## When to Consider a New Agent

✅ **Good reasons:**
- Gap in agent ecosystem (no one owns this responsibility)
- Specialized skill set needed (distinct from existing agents)
- Role deserves dedicated focus (too large for ad-hoc)
- Recurring need that would benefit from expertise

❌ **Bad reasons:**
- Convenience (use existing agent instead)
- Temporary task (write a script, don't create a role)
- Unclear boundaries (refine the idea first)
- Overlaps with existing agent (expand that agent's scope instead)

## The Five-Phase Onboarding Process

### Phase 1: Role Definition

**Objective:** Clearly articulate what this agent does and why it exists

**Deliverables:**
1. **Problem Statement**
   - What gap does this agent fill?
   - What pain points does it solve?
   - What happens if this agent doesn't exist?

2. **Responsibilities**
   - Primary duties (the core mandate)
   - Secondary duties (nice-to-have capabilities)
   - Explicitly excluded (what this agent does NOT do)

3. **Success Criteria**
   - How do you know this agent is effective?
   - What does "good work" look like?
   - What outcomes should it produce?

4. **Ecosystem Fit**
   - How does this relate to existing agents?
   - Which agents will this collaborate with?
   - Any potential role conflicts to resolve?

**Template:**
```markdown
# [Agent Name] - Role Definition

## Problem Statement
[What gap exists? What problem needs solving?]

## Responsibilities
### Primary
- [Core duty 1]
- [Core duty 2]

### Secondary
- [Nice-to-have 1]

### Explicitly Excluded (NOT this agent's job)
- [Something another agent handles]
- [Out of scope work]

## Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]

## Ecosystem Fit
- **Collaborates with:** [Agent A] on [task X]
- **Distinct from:** [Agent B] because [reason]
- **Enables:** [Agent C] to focus on [their core work]
```

**Checkpoint:** Before moving to Phase 2, verify:
- [ ] Problem statement is clear and compelling
- [ ] Responsibilities don't significantly overlap with existing agents
- [ ] Success criteria are measurable
- [ ] Ecosystem fit is well-understood

### Phase 2: Capability Assessment

**Objective:** Identify what skills, tools, and knowledge the agent needs to succeed

**Deliverables:**
1. **Required Tools**
   - File operations (Read, Write, Edit, Glob, Grep)
   - Bash commands (git, scripts, system operations)
   - MCP tools (mcpanda, builder-mcp, others)
   - Analysis capabilities (pattern matching, validation)
   - External resources (APIs, databases, documentation)

2. **Knowledge Base**
   - What does the agent need to know upfront?
   - What documentation should it reference?
   - What systems should it understand?
   - What context is required?

3. **Scripts & Automation**
   - What scripts would help this agent work efficiently?
   - Should scripts be created before agent launch?
   - Where should scripts live (.claude/scripts/[agent-name]/)?

4. **Memory Structure**
   - What should persist across sessions?
   - What patterns should be learned?
   - What state needs tracking?
   - Structure of .claude/agent-memory/[agent-name]/

**Template:**
```markdown
# [Agent Name] - Capability Assessment

## Required Tools
- **File Operations:** Read, Write, Edit, Glob, Grep
- **Bash:** git, [specific commands]
- **MCP Tools:** [mcpanda tools], [others]
- **Analysis:** [specific capabilities]

## Knowledge Base
### Must Know
- [System/concept 1]
- [System/concept 2]

### Should Reference
- [Documentation file 1]
- [Documentation file 2]

## Scripts & Automation
### Pre-Launch Scripts
- `.claude/scripts/[agent-name]/[script1].sh` - [purpose]

### Future Scripts (create as needed)
- [Potential automation 1]

## Memory Structure
- `MEMORY.md` - [What to track]
- `[topic].md` - [Detailed notes on specific topics]
```

**Checkpoint:** Before moving to Phase 3, verify:
- [ ] Agent has access to necessary tools
- [ ] Knowledge requirements are documented
- [ ] Critical scripts are created
- [ ] Memory structure is designed

### Phase 3: Training & Alignment

**Objective:** Create comprehensive agent instructions that ensure quality, consistency, and alignment

**Deliverables:**
1. **Agent Prompt File** (`.claude/agents/[agent-name].md`)
   - Name, description, model, color, memory
   - Core philosophy aligned with "organization as core discipline"
   - Detailed responsibilities
   - Operating modes/workflows
   - Examples and interaction patterns
   - Git autonomy instructions
   - Quality standards

2. **Example Scenarios**
   - Sample tasks the agent should handle
   - Expected inputs and outputs
   - Edge cases and error handling

3. **Quality Standards**
   - Professional tone requirements
   - Output format expectations
   - Commit message patterns
   - Documentation standards

4. **Alignment Verification**
   - Aligns with "organization as core discipline"
   - Respects git autonomy principle
   - Maintains professional standards
   - Integrates with existing workflows

**Template:** See existing agent files in `.claude/agents/`

Key sections to include:
```markdown
---
name: [agent-name]
description: "[When to use, examples, when NOT to use]"
model: [sonnet|opus|haiku]
color: [blue|purple|orange|etc]
memory: project
---

# Core Philosophy
[How this agent embodies "organization as core discipline"]

# Responsibilities
[Detailed breakdown]

# Operating Modes
[Different ways to invoke this agent]

# Git Autonomy
- ✅ Commit freely
- ✅ Push immediately
[etc]

# Quality Standards
[Professional tone, output format, etc]

# Interaction Patterns
[Examples of usage]

# Persistent Agent Memory
[Memory structure and usage]
```

**Checkpoint:** Before moving to Phase 4, verify:
- [ ] Agent prompt is comprehensive
- [ ] Examples cover common scenarios
- [ ] Quality standards are clear
- [ ] Alignment with core principles is explicit

### Phase 4: Integration

**Objective:** Integrate the agent into the repository ecosystem

**Deliverables:**
1. **CLAUDE.md Updates**
   - Add to agent list with description
   - Add to workflows section
   - Update relevant sections

2. **START-HERE.md Updates**
   - Add to contributing section
   - Include in agent list
   - Note in recent updates

3. **Skill Creation** (if needed)
   - Create `.claude/skills/[agent-name].md` for easy invocation
   - Document skill usage

4. **Memory Directory Setup**
   - Create `.claude/agent-memory/[agent-name]/`
   - Add empty `MEMORY.md` with guidance

5. **Documentation**
   - Add to SYSTEMS.md if agent manages a system
   - Update relevant index files
   - Note dependencies or prerequisites

**Checklist:**
- [ ] CLAUDE.md updated
- [ ] START-HERE.md updated
- [ ] Skill created (if applicable)
- [ ] Memory directory created
- [ ] Documentation complete

**Checkpoint:** Before moving to Phase 5, verify:
- [ ] All integration points are updated
- [ ] Agent is discoverable by users
- [ ] Documentation is complete

### Phase 5: Validation & Iteration

**Objective:** Verify the agent works as intended and refine based on real usage

**Deliverables:**
1. **Test Scenarios**
   - Run agent on 3-5 representative tasks
   - Verify outputs meet quality standards
   - Check git autonomy is working
   - Validate memory persistence

2. **Role Verification**
   - Agent stays within defined boundaries
   - Doesn't overlap with other agents
   - Produces expected outcomes
   - Aligns with core principles

3. **First Iteration**
   - Gather feedback from initial runs
   - Refine agent prompt if needed
   - Update documentation based on learnings
   - Adjust responsibilities if scope was wrong

4. **Long-term Monitoring**
   - Track agent effectiveness over time
   - Collect feedback in feedback.md
   - Note improvements in agent memory
   - Consider sunsetting if underutilized

**Validation Checklist:**
- [ ] Agent successfully completes sample tasks
- [ ] Output quality meets standards
- [ ] Git commits are appropriate
- [ ] Memory is being used effectively
- [ ] No conflicts with other agents
- [ ] Alignment with core principles verified

**Success Metrics:**
- Agent is invoked regularly (not a one-off)
- Agent produces consistent quality output
- Agent improves over time (memory grows)
- Agent's role remains clear and distinct
- Users/agents find it valuable

## Agent Lifecycle Management

### When to Expand Agent Scope
- Recurring requests that fit the agent's domain
- Natural evolution of responsibilities
- Capability improvements (new tools available)

### When to Refine Agent Role
- Overlap with other agents discovered
- Scope creep observed
- Feedback indicates confusion

### When to Sunset an Agent
- Role is no longer needed
- Responsibilities absorbed by other agents
- Consistently underutilized
- Quality standards not met despite iteration

## Current Agent Ecosystem

See [AGENT-ROLES.md](AGENT-ROLES.md) for:
- Complete agent catalog
- Role boundaries and relationships
- Gap analysis
- Potential new roles

## Onboarding Checklist Summary

When creating a new agent, complete all phases:

**Phase 1: Role Definition**
- [ ] Problem statement written
- [ ] Responsibilities defined (primary, secondary, excluded)
- [ ] Success criteria established
- [ ] Ecosystem fit analyzed

**Phase 2: Capability Assessment**
- [ ] Required tools identified
- [ ] Knowledge base documented
- [ ] Scripts created/planned
- [ ] Memory structure designed

**Phase 3: Training & Alignment**
- [ ] Agent prompt file created
- [ ] Example scenarios documented
- [ ] Quality standards defined
- [ ] Alignment verification passed

**Phase 4: Integration**
- [ ] CLAUDE.md updated
- [ ] START-HERE.md updated
- [ ] Skill created (if needed)
- [ ] Memory directory setup
- [ ] Documentation complete

**Phase 5: Validation**
- [ ] Test scenarios run
- [ ] Role verification passed
- [ ] First iteration complete
- [ ] Long-term monitoring plan

---

**Remember:** A well-onboarded agent is an investment. A poorly-onboarded agent is technical debt. Take the time to do it right.
