---
name: cite
description: Find and flag unsourced claims that need citations
---

You are about to launch the **citation-needed** agent to find and flag claims that lack proper citations in the Panopticon repository.

## What the Citation-Needed Agent Does

This agent is the **citation watchdog** - like Wikipedia's [citation needed] tag, but for Panopticon.

**Citation-Needed responsibilities:**
- 🔍 **Scan** for unsourced claims (passive or batch mode)
- 📌 **Flag** missing citations with `[citation needed]` markers
- 📊 **Categorize** by priority (critical → high → medium → low)
- 💡 **Suggest** what kind of citation would satisfy
- 🚨 **Be vocal** about citation quality issues

## Two Operating Modes

### Passive Observation Mode
- Agent observes while other work happens
- Notices unsourced claims in passing
- Flags them gently without interrupting workflow
- Logs findings for future reference

### Active Batch Audit Mode
- Systematic scan of documents or entire repository
- Comprehensive flagging of all unsourced claims
- Detailed report with priority categorization
- Commits all markers at once

## When to Use the Citation-Needed Agent

**Batch Citation Audits:**
- "Find all unsourced claims in provider documentation"
- "Audit the security docs for missing citations"
- "Scan infrastructure docs for citation issues"

**Document Review:**
- "Check if this document has proper citations"
- "Verify citation quality in this file"

**Quality Assurance:**
- "Audit repository for citation quality"
- "Find all [citation needed] issues"

**Before Publication:**
- "Make sure customer-facing docs are properly cited"
- "Verify all claims have sources before sharing"

## What You'll Get

### Batch Audit Output

```
📌 Citation Audit: Provider Documentation

🔍 Scanned: 23 documents, 1,847 lines

📊 Findings Summary:
- CRITICAL citations needed: 3
- HIGH priority citations needed: 8
- MEDIUM priority citations needed: 15
- LOW priority citations needed: 4
- Vague citations found: 2

🚨 Critical Issues:

📄 File: providers/salesforce.md
Line: 47
Claim: "Salesforce rate limit is 15,000 requests/day"
Priority: CRITICAL
Reason: Specific technical claim affecting integration design
Should cite: Official Salesforce API documentation

📄 File: security/compliance.md
Line: 12
Claim: "We are SOC2 Type II certified"
Priority: CRITICAL
Reason: Compliance claim critical for customer trust
Should cite: Compliance certificate or official security docs

✅ Actions Taken:
- Added [citation needed] markers to 32 claims
- Committed markers to repository
- Flagged 3 critical issues for immediate attention
```

### Passive Observation Output

```
📌 Citation Notice: infrastructure/gcp-setup.md

🔍 Observed while: steward was reorganizing docs

📄 Found unsourced claim:
Line: 78
Claim: "Our Cloud SQL instance has 64 cores"
Priority: HIGH
Action: Added [citation needed] marker

💡 Suggestion:
Should cite: GCP console screenshot, infrastructure-as-code, or monitoring dashboard

✅ Marker added, continuing observation.
```

## Citation Priority Levels

**CRITICAL** - Security, compliance, customer-facing claims:
- "We are SOC2 certified"
- "API is PCI-DSS compliant"
- "SLA guarantees 99.9% uptime"

**HIGH** - Technical specifics, provider details:
- "Salesforce rate limit is 15,000/day"
- "Token expires after 2 hours"
- "Webhook retries 3 times"

**MEDIUM** - General facts that should be cited:
- "We use PostgreSQL 15"
- "Team has 12 engineers"
- "We deploy via ArgoCD"

**LOW** - Nice-to-have citations:
- Common knowledge
- Obvious observations
- General software concepts

## What the Agent Flags

### Always Flags
- Specific numbers and metrics
- API/technical specifications
- Security/compliance claims
- Provider-specific behaviors
- Customer data
- Attributed statements

### Often Flags
- Process descriptions
- Architecture decisions
- Historical information
- Team structure
- Tool configurations

### Rarely Flags
- General software concepts
- Common knowledge
- Obvious code observations
- Meta-documentation

## Citation Marker Format

```markdown
The Salesforce API has a rate limit of 15,000 requests per day. [citation needed]

<!-- Citation needed: Specific technical claim about Salesforce rate limits.
     Should cite: Official Salesforce API documentation.
     Added by: citation-needed agent on 2026-02-06 -->
```

For critical issues:
```markdown
Our system is SOC2 Type II certified. [citation needed - CRITICAL]

<!-- Citation needed: Security compliance claim - critical for customer trust.
     Should cite: Official compliance certificate or security documentation.
     Added by: citation-needed agent on 2026-02-06 -->
```

## Invoke the Citation-Needed Agent

**For batch audits:**
```
I'll scan [scope] for unsourced claims and flag them with [citation needed] markers.

Process:
1. Scan all documents in scope
2. Identify claims requiring citations
3. Categorize by priority
4. Add markers with explanatory comments
5. Generate comprehensive report
6. Commit all markers
```

**For passive observation:**
```
I'll observe the current work and flag any unsourced claims I notice along the way.
This won't interrupt the workflow - just gentle flagging.
```

Then use the Task tool with `subagent_type: "citation-needed"` to launch the agent.

---

**Remember:** The citation-needed agent is like having a peer reviewer constantly watching for unsourced claims. It makes citation quality issues visible so researchers can address them.
