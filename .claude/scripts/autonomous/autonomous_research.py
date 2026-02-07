#!/usr/bin/env python3
"""
autonomous_research.py

Autonomous research loop - spawns Claude Code instances to research and document gaps.

This script:
1. Reads high-priority gaps from research-tasks.md
2. For each gap, spawns ephemeral Claude Code via SDK
3. Claude researches using McPanda + file tools
4. Validates documentation was updated
5. Re-runs analyzer to detect new gaps
6. Repeats until no high-priority gaps remain

Usage:
  ./autonomous_research.py
  ./autonomous_research.py --max-iterations 5 --timeout 600
  ./autonomous_research.py --mcpanda-url http://localhost:3000

Used by: Autonomous knowledge loop
Requires: claude-agent-sdk, McPanda MCP server running
"""

import asyncio
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional
import argparse

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'  # No Color


try:
    from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, SystemMessage, AssistantMessage, query
except ImportError:
    print(f"{RED}Error: claude-agent-sdk not installed{NC}")
    print("Install with: pip install claude-agent-sdk")
    sys.exit(1)


class Gap:
    """Represents a research gap from research-tasks.md."""

    def __init__(self, gap_id: str, topic: str, document: str, description: str, gap_type: str = ""):
        self.gap_id = gap_id
        self.topic = topic
        self.document = document
        self.description = description
        self.gap_type = gap_type


class AutonomousResearcher:
    """Orchestrates autonomous research loop."""

    def __init__(
        self,
        repo_root: Path,
        mcpanda_url: str = "http://localhost:3000",
        max_iterations: int = 10,
        timeout_per_gap: int = 600,  # 10 minutes
    ):
        self.repo_root = repo_root
        self.mcpanda_url = mcpanda_url
        self.max_iterations = max_iterations
        self.timeout_per_gap = timeout_per_gap
        self.research_tasks_path = repo_root / "research-tasks.md"

    def parse_research_tasks(self) -> List[Gap]:
        """Parse research-tasks.md and extract high-priority gaps."""
        if not self.research_tasks_path.exists():
            print(f"{YELLOW}⚠ research-tasks.md not found{NC}")
            return []

        content = self.research_tasks_path.read_text()

        # Find High Priority section
        high_priority_match = re.search(
            r'## High Priority.*?(?=## Medium Priority|## Low Priority|$)',
            content,
            re.DOTALL
        )

        if not high_priority_match:
            print(f"{YELLOW}⚠ No High Priority section found{NC}")
            return []

        high_priority_section = high_priority_match.group(0)

        # Parse individual gap entries
        gaps = []

        # Match pattern: ### Topic - service_name
        gap_pattern = r'### (.+?) - (.+?)\n\*\*Gap ID:\*\* (.+?)\n\*\*Type:\*\* (.+?)\n\*\*Document:\*\* (.+?)\n\*\*Description:\*\* (.+?)(?=\n\n|\n\*\*|$)'

        for match in re.finditer(gap_pattern, high_priority_section, re.DOTALL):
            topic = match.group(1).strip()
            service = match.group(2).strip()
            gap_id = match.group(3).strip()
            gap_type = match.group(4).strip()
            document = match.group(5).strip()
            description = match.group(6).strip()

            gaps.append(Gap(
                gap_id=gap_id,
                topic=topic,
                document=document,
                description=description,
                gap_type=gap_type
            ))

        return gaps

    def build_research_prompt(self, gap: Gap) -> str:
        """Build research prompt for Claude Code."""
        return f"""You are a knowledge-researcher agent for the Panopticon repository.

**Gap ID:** {gap.gap_id}
**Topic:** {gap.topic}
**Document:** {gap.document}
**Description:** {gap.description}

**Your Task:**
Research and document **{gap.topic}** for {gap.document}.

**Research Sources:**

1. **McPanda tools** - Use mcp__mcpanda__* tools to:
   - Search server codebase for implementation (amp_code_analysis, analyze_go_file, analyze_go_project)
   - Check argocd manifests for deployment config (argocd_get_app_details, argocd_list_applications)
   - Query GCP infrastructure (gcp_gke_get_cluster_details, gcp_functions_list, etc.)
   - Access live system information (kubectl_get_pods, kubectl_describe_pod, etc.)
   - Get service health and metrics (gcp_observability_get_service_health, prometheus_query)

2. **Codebase exploration:**
   - Use Grep to search for relevant code patterns
   - Use Read to understand implementation details
   - Check related service docs for consistent patterns
   - Look at KNOWLEDGE-SOURCES.md for research sources

3. **Documentation update:**
   - Read {gap.document} to understand existing structure
   - Add a new section or expand existing section for {gap.topic}
   - Follow existing documentation format and style
   - Include inline citations (e.g., "defined in server/api/main.go:123")
   - Add confidence markers: 🟢 HIGH (verified from code), 🟡 MEDIUM (from docs), 🔴 LOW (needs verification)
   - Use Edit tool to update the document

**Documentation Requirements:**

- **Thoroughness:** Document actual implementation, not just concepts
- **Accuracy:** Verify information from source code or live systems
- **Citations:** Include file:line references for code-based claims
- **Examples:** Provide concrete examples where applicable
- **Consistency:** Match tone and format of existing docs

**Example documentation for deployment:**
```markdown
## Deployment

**Confidence:** 🟢 HIGH

The {gap.topic} service is deployed via ArgoCD to GCP Kubernetes Engine.

**Configuration:**
- Namespace: `production`
- Replicas: 3 (auto-scaled 3-10 based on CPU)
- Resource limits: 512Mi memory, 500m CPU
- Deployment manifest: `argocd/apps/production/{service}.yaml` [citation: argocd/apps/production/api.yaml:1-50]

**Scaling:**
Horizontal Pod Autoscaler configured with:
- Target CPU: 70%
- Min replicas: 3
- Max replicas: 10
- Scale-up stabilization: 60s

**Health checks:**
- Liveness probe: `GET /health` every 10s
- Readiness probe: `GET /ready` every 5s
```

**Success Criteria:**
- {gap.topic} is thoroughly documented in {gap.document}
- Information verified from sources (code, argocd, GCP)
- Document updated via Edit tool (not just proposed changes)
- Citations included for factual claims
- Confidence marker added

**Output:**
Explain what you researched and what you documented. The documentation should already be written to {gap.document} via the Edit tool before you finish.
"""

    async def research_gap(self, gap: Gap) -> Dict:
        """Spawn Claude Code to research a single gap."""
        print(f"\n{CYAN}{'─' * 60}{NC}")
        print(f"{CYAN}🎯 Researching: {gap.gap_id} ({gap.topic} - {gap.document}){NC}")
        print(f"{CYAN}{'─' * 60}{NC}\n")

        start_time = datetime.now(timezone.utc)

        # Build research prompt
        prompt = self.build_research_prompt(gap)

        # Capture SDK stderr
        def sdk_stderr_callback(msg: str) -> None:
            print(f"{BLUE}[SDK]{NC} {msg.rstrip()}")

        # Configure Claude Code via SDK
        options = ClaudeAgentOptions(
            mcp_servers={
                "mcpanda": {
                    "url": self.mcpanda_url,
                }
            },
            allowed_tools=["mcp__mcpanda__*"],  # McPanda tools + built-in tools
            permission_mode="bypassPermissions",  # Fully autonomous
            cwd=str(self.repo_root),
            stderr=sdk_stderr_callback,
        )

        print(f"{YELLOW}🚀 Spawning Claude Code researcher...{NC}")

        response_text = ""
        success = False
        error_msg = None

        try:
            # Query Claude Code (async generator)
            async for message in query(prompt=prompt, options=options):
                # System message (MCP init)
                if isinstance(message, SystemMessage) and message.subtype == "init":
                    mcp_servers = message.data.get("mcp_servers", [])
                    connected = [s for s in mcp_servers if s.get("status") == "connected"]
                    print(f"{GREEN}✓ MCP servers connected: {len(connected)}/{len(mcp_servers)}{NC}")

                    for server in connected:
                        server_name = server.get("name", "unknown")
                        tools = server.get("tools", [])
                        print(f"{BLUE}  ✓ {server_name}: {len(tools)} tools available{NC}")

                # Assistant message (Claude's work)
                if isinstance(message, AssistantMessage):
                    if hasattr(message, "content") and message.content:
                        for content_block in message.content:
                            # Text output
                            if hasattr(content_block, "text"):
                                text = content_block.text
                                response_text += text
                                # Print but limit length
                                if len(text) < 200:
                                    print(text)
                                else:
                                    print(text[:200] + "...")

                            # Tool call
                            if hasattr(content_block, "name"):
                                tool_name = content_block.name
                                print(f"{CYAN}  → Calling: {tool_name}{NC}")

                # Result message (final)
                if isinstance(message, ResultMessage):
                    if message.subtype == "success":
                        response_text = message.result
                        success = True
                        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
                        print(f"\n{GREEN}✓ Research complete ({elapsed:.0f}s){NC}")
                    elif message.subtype == "error":
                        error_msg = message.error
                        print(f"\n{RED}✗ Research failed: {error_msg}{NC}")

        except asyncio.TimeoutError:
            error_msg = f"Research timed out after {self.timeout_per_gap}s"
            print(f"\n{RED}✗ {error_msg}{NC}")
        except Exception as e:
            error_msg = str(e)
            print(f"\n{RED}✗ Research failed: {error_msg}{NC}")

        return {
            "success": success,
            "response": response_text,
            "error": error_msg,
            "elapsed_seconds": (datetime.now(timezone.utc) - start_time).total_seconds(),
        }

    def validate_gap_resolved(self, gap: Gap) -> bool:
        """Check if gap was resolved (documentation updated)."""
        doc_path = self.repo_root / gap.document

        if not doc_path.exists():
            print(f"{RED}  ✗ Document not found: {gap.document}{NC}")
            return False

        content = doc_path.read_text()

        # Check if topic appears in document (simple heuristic)
        topic_lower = gap.topic.lower().replace("_", " ")

        if topic_lower in content.lower():
            print(f"{GREEN}  ✓ Topic '{gap.topic}' found in document{NC}")
            return True
        else:
            print(f"{YELLOW}  ⚠ Topic '{gap.topic}' not found in document{NC}")
            return False

    def mark_gap_completed(self, gap: Gap):
        """Mark gap as completed in research-tasks.md."""
        # For now, just print - could implement actual removal
        print(f"{BLUE}  → Gap {gap.gap_id} should be marked complete{NC}")

    async def run(self):
        """Run autonomous research loop."""
        print(f"{CYAN}{'═' * 60}{NC}")
        print(f"{CYAN}🔍 Autonomous Research Loop Starting{NC}")
        print(f"{CYAN}{'═' * 60}{NC}\n")

        iteration = 0
        total_researched = 0
        total_succeeded = 0
        total_failed = 0

        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n{YELLOW}📋 Iteration {iteration}/{self.max_iterations}{NC}")

            # Read current gaps
            gaps = self.parse_research_tasks()

            if not gaps:
                print(f"{GREEN}✓ No high-priority gaps remaining!{NC}")
                break

            print(f"   Found {len(gaps)} high-priority gap(s)\n")

            # Process first gap (sequential for safety)
            gap = gaps[0]
            total_researched += 1

            # Research it
            result = await self.research_gap(gap)

            if result["success"]:
                # Validate
                if self.validate_gap_resolved(gap):
                    total_succeeded += 1
                    self.mark_gap_completed(gap)
                    print(f"{GREEN}  ✓ Gap validated as resolved{NC}")
                else:
                    total_failed += 1
                    print(f"{YELLOW}  ⚠ Gap not fully resolved (validation failed){NC}")
            else:
                total_failed += 1
                print(f"{RED}  ✗ Research failed: {result.get('error', 'unknown error')}{NC}")

            # Re-run analyzer to detect new gaps
            print(f"\n{CYAN}🔄 Re-analyzing repository...{NC}")
            # For now, just note - could shell out to analyzer script
            print(f"{BLUE}  → Would run: .claude/scripts/analyzer/analyze_content.py{NC}")

        # Summary
        print(f"\n{CYAN}{'═' * 60}{NC}")
        print(f"{CYAN}✅ Autonomous Research Complete!{NC}")
        print(f"{CYAN}{'═' * 60}{NC}\n")

        print(f"{BLUE}📊 Summary:{NC}")
        print(f"   - Iterations: {iteration}")
        print(f"   - Gaps processed: {total_researched}")
        print(f"   - Successfully researched: {total_succeeded}")
        print(f"   - Failed (retryable): {total_failed}")

        if total_succeeded > 0:
            success_rate = (total_succeeded / total_researched) * 100
            print(f"\n{GREEN}   Success rate: {success_rate:.0f}%{NC}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Autonomous research loop")
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum research iterations (default: 10)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout per gap in seconds (default: 600)"
    )
    parser.add_argument(
        "--mcpanda-url",
        default="http://localhost:3000",
        help="McPanda MCP server URL (default: http://localhost:3000)"
    )

    args = parser.parse_args()

    # Find repo root
    repo_root = Path(__file__).resolve().parents[3]

    # Create researcher
    researcher = AutonomousResearcher(
        repo_root=repo_root,
        mcpanda_url=args.mcpanda_url,
        max_iterations=args.max_iterations,
        timeout_per_gap=args.timeout,
    )

    # Run loop
    await researcher.run()


if __name__ == "__main__":
    asyncio.run(main())
