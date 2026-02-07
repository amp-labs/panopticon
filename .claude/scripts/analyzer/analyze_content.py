#!/usr/bin/env python3
"""
analyze_content.py

Knowledge analyzer - builds structured catalog of repository contents and detects gaps.

This script:
1. Parses content docs (providers/, services/, infrastructure/)
2. Extracts entities, facts, coverage density
3. Builds YAML catalog in .claude/catalog/
4. Detects gaps (missing docs, incomplete coverage, asymmetric refs)
5. Creates research tasks in research-tasks.md
6. Auto-invokes researcher for blocking gaps (optional)

Usage:
  ./analyze_content.py                    # Full repository scan
  ./analyze_content.py services/api.md    # Incremental analysis
  ./analyze_content.py --gaps-only        # Just gap detection
  ./analyze_content.py --report           # Generate gap summary

Used by: knowledge-analyzer agent
Invoked via: /analyze command
"""

import os
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'  # No Color


@dataclass
class CoverageInfo:
    """Coverage assessment for a topic."""
    density: str  # detailed, mentioned, not_covered
    details: str
    line_count: int


@dataclass
class Gap:
    """A detected knowledge gap."""
    gap_id: str
    gap_type: str  # blocking_gap, incomplete_coverage, etc.
    topic: str
    priority: str  # blocking, high, medium, low
    description: str
    research_task_created: bool = False


@dataclass
class CatalogEntry:
    """Catalog entry for a document."""
    document: str
    last_analyzed: str
    analyzed_by: str = "knowledge-analyzer"
    entities: Dict = None
    coverage: Dict = None
    mentions: Dict = None
    cross_references: Dict = None
    gaps: List = None
    facts: List = None

    def __post_init__(self):
        if self.entities is None:
            self.entities = {}
        if self.coverage is None:
            self.coverage = {}
        if self.mentions is None:
            self.mentions = {"services": [], "providers": [], "infrastructure": [], "customers": []}
        if self.cross_references is None:
            self.cross_references = {"outgoing": [], "incoming": [], "asymmetric": []}
        if self.gaps is None:
            self.gaps = []
        if self.facts is None:
            self.facts = []


class KnowledgeAnalyzer:
    """Main analyzer class."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.catalog_dir = repo_root / ".claude" / "catalog"
        self.content_dirs = ["services", "providers", "infrastructure", "customers"]

        # Create catalog directory if it doesn't exist
        self.catalog_dir.mkdir(parents=True, exist_ok=True)
        for dir_name in self.content_dirs:
            (self.catalog_dir / dir_name).mkdir(exist_ok=True)

    def find_content_docs(self) -> List[Path]:
        """Find all content markdown files."""
        docs = []
        for dir_name in self.content_dirs:
            dir_path = self.repo_root / dir_name
            if dir_path.exists():
                for md_file in dir_path.glob("*.md"):
                    # Skip index files
                    if not md_file.name.endswith("-index.md"):
                        docs.append(md_file)
        return sorted(docs)

    def extract_entities(self, content: str, doc_path: Path) -> Dict:
        """Extract entities from document content."""
        entities = {}

        # Extract service name if in services/
        if "services" in doc_path.parts:
            entities["service_name"] = doc_path.stem

        # Extract provider name if in providers/
        if "providers" in doc_path.parts:
            entities["provider_name"] = doc_path.stem

        # Extract port numbers
        port_matches = re.findall(r'[Pp]ort[:\s]+(\d{4,5})', content)
        if port_matches:
            entities["ports"] = list(set(port_matches))

        # Extract framework mentions
        frameworks = ["GoFiber", "Fiber", "Temporal", "React", "Next.js", "Express"]
        for framework in frameworks:
            if framework in content:
                entities["framework"] = framework
                break

        # Extract confidence level
        if "Confidence:** HIGH" in content or "**Confidence:** HIGH" in content:
            entities["confidence"] = "HIGH"
        elif "Confidence:** MEDIUM" in content or "**Confidence:** MEDIUM" in content:
            entities["confidence"] = "MEDIUM"
        elif "Confidence:** LOW" in content or "**Confidence:** LOW" in content:
            entities["confidence"] = "LOW"

        return entities

    def assess_coverage(self, content: str, doc_path: Path) -> Dict[str, CoverageInfo]:
        """Assess coverage density for key topics."""
        coverage = {}

        # Common topics to assess based on document type
        if "services" in doc_path.parts:
            topics = [
                "authentication", "rate_limiting", "error_handling",
                "deployment", "scaling", "monitoring", "testing"
            ]
        elif "providers" in doc_path.parts:
            topics = [
                "oauth", "rate_limiting", "api_versions",
                "webhooks", "data_model", "quirks"
            ]
        elif "infrastructure" in doc_path.parts:
            topics = [
                "deployment", "scaling", "monitoring",
                "security", "disaster_recovery"
            ]
        else:
            topics = []

        for topic in topics:
            # Search for topic mentions (case insensitive)
            pattern = re.compile(re.escape(topic.replace("_", " ")), re.IGNORECASE)
            matches = pattern.findall(content)

            if not matches:
                coverage[topic] = CoverageInfo(
                    density="not_covered",
                    details=None,
                    line_count=0
                )
            else:
                # Count lines discussing this topic (rough heuristic)
                lines = content.split('\n')
                topic_lines = [line for line in lines if pattern.search(line)]
                line_count = len(topic_lines)

                # Assess density based on line count
                if line_count >= 5:
                    density = "detailed"
                elif line_count >= 2:
                    density = "mentioned"
                else:
                    density = "brief"

                # Extract context around first mention
                first_mention_line = topic_lines[0] if topic_lines else ""

                coverage[topic] = CoverageInfo(
                    density=density,
                    details=first_mention_line[:100] if first_mention_line else None,
                    line_count=line_count
                )

        return coverage

    def extract_mentions(self, content: str) -> Dict[str, List[str]]:
        """Extract mentions of other entities."""
        mentions = {
            "services": [],
            "providers": [],
            "infrastructure": [],
            "customers": []
        }

        # Known services (from existing docs)
        services = [
            "api", "temporal", "messenger", "token-manager", "scribe",
            "metrics-service", "mcpanda", "builder-mcp"
        ]
        for service in services:
            if service in content.lower():
                mentions["services"].append(service)

        # Known providers
        providers = ["salesforce", "hubspot", "slack", "notion", "stripe"]
        for provider in providers:
            if provider in content.lower():
                mentions["providers"].append(provider)

        # Infrastructure components
        infra = ["gcp", "kubernetes", "k8s", "docker", "argocd", "postgres", "temporal"]
        for component in infra:
            if component in content.lower():
                mentions["infrastructure"].append(component)

        # Deduplicate
        for key in mentions:
            mentions[key] = sorted(list(set(mentions[key])))

        return mentions

    def extract_cross_references(self, content: str, doc_path: Path) -> Dict[str, List]:
        """Extract cross-references to other docs."""
        refs = {"outgoing": [], "incoming": []}

        # Find markdown links to other docs
        link_pattern = r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)'
        matches = re.findall(link_pattern, content)

        for text, target in matches:
            # Clean up target (remove anchors)
            target = target.split('#')[0]

            # Skip external URLs
            if target.startswith('http'):
                continue

            refs["outgoing"].append({
                "target": target,
                "context": text[:50]
            })

        # Find backtick-wrapped .md references
        backtick_pattern = r'`([^`]+\.md)`'
        backtick_matches = re.findall(backtick_pattern, content)

        for target in backtick_matches:
            if not any(ref["target"] == target for ref in refs["outgoing"]):
                refs["outgoing"].append({
                    "target": target,
                    "context": "backtick reference"
                })

        return refs

    def detect_gaps(self, entry: CatalogEntry, doc_path: Path) -> List[Gap]:
        """Detect knowledge gaps in a document."""
        gaps = []
        gap_counter = 1
        doc_prefix = doc_path.stem

        # Gap type 1: Incomplete coverage
        for topic, cov in entry.coverage.items():
            # cov is already a dict (converted by asdict earlier)
            density = cov.get('density') if isinstance(cov, dict) else cov.density

            if density == "mentioned" or density == "brief":
                gaps.append(Gap(
                    gap_id=f"{doc_prefix}-{gap_counter:03d}",
                    gap_type="mentioned_without_detail",
                    topic=topic,
                    priority="medium",
                    description=f"{topic.replace('_', ' ').title()} mentioned but not detailed"
                ))
                gap_counter += 1
            elif density == "not_covered":
                # Only flag not_covered for important topics
                important_topics = ["authentication", "deployment", "oauth", "rate_limiting"]
                if topic in important_topics:
                    gaps.append(Gap(
                        gap_id=f"{doc_prefix}-{gap_counter:03d}",
                        gap_type="incomplete_core_coverage",
                        topic=topic,
                        priority="high",
                        description=f"{topic.replace('_', ' ').title()} not documented"
                    ))
                    gap_counter += 1

        # Gap type 2: Missing examples (look for "mentioned but no examples" patterns)
        example_keywords = ["example", "e.g.", "for instance", "such as"]
        content_lower = str(entry).lower()

        for topic, cov in entry.coverage.items():
            density = cov.get('density') if isinstance(cov, dict) else cov.density

            if density in ["mentioned", "detailed"]:
                # If topic is mentioned but no examples found
                has_examples = any(keyword in content_lower for keyword in example_keywords)
                if not has_examples and density == "mentioned":
                    gaps.append(Gap(
                        gap_id=f"{doc_prefix}-{gap_counter:03d}",
                        gap_type="missing_examples",
                        topic=topic,
                        priority="low",
                        description=f"{topic.replace('_', ' ').title()} explained but no concrete examples"
                    ))
                    gap_counter += 1

        return gaps

    def analyze_document(self, doc_path: Path) -> CatalogEntry:
        """Analyze a single document."""
        print(f"  📄 Analyzing {doc_path.relative_to(self.repo_root)}...")

        content = doc_path.read_text(errors='ignore')

        entry = CatalogEntry(
            document=str(doc_path.relative_to(self.repo_root)),
            last_analyzed=datetime.now(timezone.utc).isoformat(),
        )

        # Extract components
        entry.entities = self.extract_entities(content, doc_path)
        entry.coverage = {
            topic: asdict(cov)
            for topic, cov in self.assess_coverage(content, doc_path).items()
        }
        entry.mentions = self.extract_mentions(content)
        entry.cross_references = self.extract_cross_references(content, doc_path)

        # Extract key facts (first 5 bullet points or key statements)
        facts = []
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('- '):
                fact = line.strip()[2:]
                if len(fact) > 20 and len(fact) < 150:  # Reasonable fact length
                    facts.append(fact)
                if len(facts) >= 5:
                    break
        entry.facts = facts

        # Detect gaps
        gaps = self.detect_gaps(entry, doc_path)
        entry.gaps = [asdict(gap) for gap in gaps]

        return entry

    def save_catalog_entry(self, entry: CatalogEntry, doc_path: Path):
        """Save catalog entry to YAML file."""
        # Determine catalog path
        relative_path = doc_path.relative_to(self.repo_root)
        catalog_path = self.catalog_dir / relative_path.with_suffix('.yaml')

        # Ensure directory exists
        catalog_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict and save
        entry_dict = asdict(entry)

        with open(catalog_path, 'w') as f:
            yaml.dump(entry_dict, f, default_flow_style=False, sort_keys=False)

        print(f"    ✅ Catalog saved to {catalog_path.relative_to(self.repo_root)}")

    def detect_asymmetric_refs(self, all_entries: Dict[str, CatalogEntry]):
        """Detect asymmetric cross-references across all docs."""
        print(f"\n{CYAN}🔗 Detecting asymmetric cross-references...{NC}")

        # Build reference graph
        ref_graph = defaultdict(list)

        for doc_path, entry in all_entries.items():
            for ref in entry.cross_references.get("outgoing", []):
                target = ref["target"]
                ref_graph[doc_path].append(target)

        # Find asymmetric refs
        asymmetric_count = 0
        for doc_path, entry in all_entries.items():
            asymmetric = []
            for ref in entry.cross_references.get("outgoing", []):
                target = ref["target"]
                # Check if target references back
                if target in all_entries:
                    target_refs = [r["target"] for r in all_entries[target].cross_references.get("outgoing", [])]
                    if doc_path not in target_refs and str(Path(doc_path).name) not in target_refs:
                        asymmetric.append(f"{Path(doc_path).name}→{target} but {target} doesn't reference {Path(doc_path).name}")
                        asymmetric_count += 1

            if asymmetric:
                entry.cross_references["asymmetric"] = asymmetric

        print(f"  Found {asymmetric_count} asymmetric cross-references")

    def generate_gap_report(self, all_entries: Dict[str, CatalogEntry]):
        """Generate and display gap summary report."""
        print(f"\n{'═' * 60}")
        print(f"{CYAN}📊 Knowledge Gap Analysis Report{NC}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}")
        print(f"{'═' * 60}\n")

        # Collect all gaps
        gaps_by_priority = defaultdict(list)
        total_gaps = 0

        for doc_path, entry in all_entries.items():
            for gap in entry.gaps:
                gaps_by_priority[gap["priority"]].append((doc_path, gap))
                total_gaps += 1

        # Repository statistics
        print(f"{BLUE}📈 Repository Statistics{NC}")
        print(f"{'─' * 60}")
        print(f"Total Documents:        {len(all_entries)}")
        total_entities = sum(len(e.entities) for e in all_entries.values())
        print(f"Total Entities:         {total_entities}")
        print(f"Total Gaps Detected:    {total_gaps}")
        print()

        # Gaps by priority
        priority_order = ["blocking", "high", "medium", "low"]
        priority_colors = {
            "blocking": RED,
            "high": YELLOW,
            "medium": BLUE,
            "low": GREEN
        }

        for priority in priority_order:
            if priority not in gaps_by_priority:
                continue

            color = priority_colors[priority]
            gaps = gaps_by_priority[priority]

            print(f"{color}{priority.upper()} Priority Gaps ({len(gaps)}){NC}")
            print(f"{'─' * 60}")

            for doc_path, gap in gaps[:5]:  # Show first 5
                doc_name = Path(doc_path).stem
                print(f"[{gap['gap_id']}] {gap['topic']} ({doc_name})")
                print(f"    {gap['description']}")

            if len(gaps) > 5:
                print(f"... {len(gaps) - 5} more")
            print()

        print(f"{'═' * 60}\n")

    def save_catalog_metadata(self, all_entries: Dict[str, CatalogEntry]):
        """Save catalog metadata summary."""
        metadata = {
            "last_full_scan": datetime.now(timezone.utc).isoformat(),
            "total_documents": len(all_entries),
            "total_gaps": sum(len(e.gaps) for e in all_entries.values()),
            "total_entities": sum(len(e.entities) for e in all_entries.values()),
            "documents_analyzed": {
                "services": len([d for d in all_entries.keys() if "services" in d]),
                "providers": len([d for d in all_entries.keys() if "providers" in d]),
                "infrastructure": len([d for d in all_entries.keys() if "infrastructure" in d]),
                "customers": len([d for d in all_entries.keys() if "customers" in d]),
            }
        }

        metadata_path = self.catalog_dir / "metadata.yaml"
        with open(metadata_path, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False)

        print(f"{GREEN}✅ Catalog metadata saved{NC}")

    def run_full_scan(self):
        """Run full repository scan."""
        print(f"{CYAN}{'═' * 60}{NC}")
        print(f"{CYAN}🔍 Knowledge Analyzer - Full Repository Scan{NC}")
        print(f"{CYAN}{'═' * 60}{NC}\n")

        docs = self.find_content_docs()
        print(f"Found {len(docs)} content documents\n")

        all_entries = {}

        # Analyze each document
        for doc_path in docs:
            entry = self.analyze_document(doc_path)
            self.save_catalog_entry(entry, doc_path)
            all_entries[str(doc_path.relative_to(self.repo_root))] = entry

        # Cross-document analysis
        self.detect_asymmetric_refs(all_entries)

        # Save updated entries with asymmetric refs
        for doc_path_str, entry in all_entries.items():
            doc_path = self.repo_root / doc_path_str
            self.save_catalog_entry(entry, doc_path)

        # Generate report
        self.generate_gap_report(all_entries)

        # Save metadata
        self.save_catalog_metadata(all_entries)

        print(f"\n{GREEN}{'═' * 60}{NC}")
        print(f"{GREEN}✅ Full scan complete!{NC}")
        print(f"{GREEN}{'═' * 60}{NC}\n")


def main():
    """Main entry point."""
    repo_root = Path(__file__).resolve().parents[3]  # Go up from .claude/scripts/analyzer/

    analyzer = KnowledgeAnalyzer(repo_root)

    # Parse arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--help":
            print(__doc__)
            return 0
        elif arg == "--report":
            print("Gap report mode not yet implemented")
            return 1
        elif arg == "--gaps-only":
            print("Gaps-only mode not yet implemented")
            return 1
        else:
            print(f"Incremental analysis mode not yet implemented")
            return 1

    # Default: full scan
    analyzer.run_full_scan()

    return 0


if __name__ == '__main__':
    sys.exit(main())
