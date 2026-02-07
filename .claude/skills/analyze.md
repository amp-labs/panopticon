# analyze

Run the knowledge-analyzer to catalog repository contents and detect gaps.

**Usage:**
- `/analyze` - Run full repository scan
- `/analyze --report` - Generate gap summary report (coming soon)
- `/analyze --gaps-only` - Just detect gaps, don't update catalog (coming soon)

**What it does:**
1. Scans all content docs (providers/, services/, infrastructure/)
2. Extracts entities, coverage, cross-references
3. Builds structured YAML catalog in `.claude/catalog/`
4. Detects knowledge gaps (missing docs, incomplete coverage, asymmetric refs)
5. Generates gap summary report

**Output:**
- Catalog files: `.claude/catalog/{category}/{doc-name}.yaml`
- Metadata: `.claude/catalog/metadata.yaml`
- Gap report: Displayed in terminal

**Philosophy:**
This closes the self-evolving repository loop:
- Catalog what we know → Identify what we don't know → Research what we don't know → Repeat

---

## Implementation

```bash
#!/usr/bin/env bash
.claude/scripts/analyzer/analyze_content.py "$@"
```
