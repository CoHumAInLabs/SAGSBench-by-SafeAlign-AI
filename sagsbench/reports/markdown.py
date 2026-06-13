from __future__ import annotations

from pathlib import Path

from sagsbench.models import CampaignResult


def write_markdown_report(result: CampaignResult, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    s = result.summary or result.compute_summary()
    lines = [
        "# SAGSBench Red-Team Report",
        "",
        f"**Target:** {result.target_name}",
        f"**Started:** {result.started_at}",
        f"**Completed:** {result.completed_at}",
        "",
        "## Executive summary",
        "",
        f"- SAGS Score: **{s['sags_score']}/100**",
        f"- Tests: **{s['total']}**",
        f"- Passed: **{s['passed']}**",
        f"- Failed: **{s['failed']}**",
        f"- Attack success rate: **{s['attack_success_rate'] * 100:.1f}%**",
        f"- Critical findings: **{s['critical_findings']}**",
        f"- High findings: **{s['high_findings']}**",
        "",
        "## Domain scores",
        "",
    ]
    for domain, score in s["domain_scores"].items():
        lines.append(f"- {domain.title()}: **{score}/100**")
    lines.extend(["", "## Findings", ""])
    for item in result.results:
        if item.status == "passed":
            continue
        lines.extend([
            f"### {item.test_id}: {item.category}",
            "",
            f"- Domain: `{item.domain}`",
            f"- Severity: `{item.severity}`",
            f"- Status: `{item.status}`",
            f"- Expected behavior: {item.expected_behavior}",
            f"- Recommendation: {item.recommendation}",
            f"- Controls: {', '.join(item.mapped_controls) if item.mapped_controls else 'None'}",
            "",
            "**Prompt**",
            "",
            f"> {item.prompt}",
            "",
            "**Agent response**",
            "",
            f"> {item.agent_response[:1000]}",
            "",
        ])
        for finding in item.findings:
            lines.append(f"- Judge `{finding.judge}`: {finding.rationale}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
