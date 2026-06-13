from __future__ import annotations

from pathlib import Path

from jinja2 import Template

from sagsbench.models import CampaignResult

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SAGSBench Report</title>
  <style>
    body { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 40px; color: #111827; }
    .hero { padding: 28px; border-radius: 20px; background: linear-gradient(135deg, #111827, #374151); color: white; }
    .cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0; }
    .card { border: 1px solid #e5e7eb; border-radius: 16px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,.06); }
    .score { font-size: 36px; font-weight: 800; }
    .failed { border-left: 6px solid #dc2626; }
    .passed { border-left: 6px solid #16a34a; }
    code { background: #f3f4f6; padding: 2px 5px; border-radius: 5px; }
    pre { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <div class="hero">
    <h1>SAGSBench Red-Team Report</h1>
    <p>Target: {{ result.target_name }}</p>
    <div class="score">{{ summary.sags_score }}/100</div>
    <p>Safety • Alignment • Governance • Security</p>
  </div>
  <div class="cards">
    <div class="card"><b>Tests</b><div class="score">{{ summary.total }}</div></div>
    <div class="card"><b>Passed</b><div class="score">{{ summary.passed }}</div></div>
    <div class="card"><b>Failed</b><div class="score">{{ summary.failed }}</div></div>
    <div class="card"><b>Attack Success</b><div class="score">{{ (summary.attack_success_rate * 100)|round(1) }}%</div></div>
  </div>
  <h2>Domain scores</h2>
  <div class="cards">
  {% for domain, score in summary.domain_scores.items() %}
    <div class="card"><b>{{ domain|title }}</b><div class="score">{{ score }}</div></div>
  {% endfor %}
  </div>
  <h2>Findings</h2>
  {% for item in result.results %}
    <div class="card {{ item.status }}">
      <h3>{{ item.test_id }} — {{ item.category }}</h3>
      <p><b>Domain:</b> <code>{{ item.domain }}</code> <b>Severity:</b> <code>{{ item.severity }}</code> <b>Status:</b> <code>{{ item.status }}</code></p>
      <p><b>Expected:</b> {{ item.expected_behavior }}</p>
      <p><b>Recommendation:</b> {{ item.recommendation }}</p>
      <p><b>Controls:</b> {{ item.mapped_controls|join(', ') }}</p>
      <h4>Prompt</h4><pre>{{ item.prompt }}</pre>
      <h4>Agent response</h4><pre>{{ item.agent_response }}</pre>
      {% for finding in item.findings %}<p><b>{{ finding.judge }}:</b> {{ finding.rationale }}</p>{% endfor %}
    </div>
  {% endfor %}
</body>
</html>
"""


def write_html_report(result: CampaignResult, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = result.summary or result.compute_summary()
    path.write_text(Template(TEMPLATE).render(result=result, summary=summary), encoding="utf-8")
