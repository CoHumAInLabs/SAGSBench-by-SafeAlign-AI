# SAGSBench by SafeAlign AI

![How Teams Red-Team Production Agents with SAGSBench](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==)

**Open-source red teaming for agentic AI governance.**

SAGSBench helps developers, security teams, and AI governance leaders test AI agents for **Safety, Alignment, Governance, and Security** risks before deployment. It runs adversarial test campaigns against agents, evaluates results with deterministic checks and optional LLM judges, and produces audit-ready reports mapped to policy controls.

Built by [SafeAlign AI](https://safealignai.io/) as an open-source contribution to secure and govern agentic AI systems.

## What it tests

- Prompt injection
- Jailbreaking and instruction override
- Goal hijacking
- Tool misuse and unauthorized action attempts
- Privacy, PII, PHI, and secret leakage
- Policy bypass
- Inter-agent trust exploitation
- Human-approval bypass
- Kill-switch failure
- Audit trail gaps

## Why SAGSBench?

Most AI red-team tools focus on whether an attack succeeded. SAGSBench also asks:

- Which governance control failed?
- Was the agent allowed to call that tool?
- Should the action have escalated to a human?
- Was an audit trail produced?
- Which Safety, Alignment, Governance, or Security domain is implicated?

## 7 Core Capabilities of SAGSBench

1. **Prompt Injection** - Test instruction overrides and context poisoning
2. **Tool Misuse** - Catch unauthorized actions and risky calls
3. **Policy-as-Code** - Validate against SAGS baseline controls
4. **Privacy Checks** - Probe for data leakage and unsafe disclosure
5. **Hybrid Judges** - Combine LLM and deterministic checks
6. **Actionable Reports** - Produce developer and governance evidence
7. **Continuous Assurance** - Close the loop with repeatable testing

## Quick start

```bash
pip install -e .

sagsbench init
sagsbench scan \
  --target http://localhost:8000/chat \
  --profile enterprise \
  --report html,json,markdown
```

## Example Python SDK

```python
from sagsbench import Campaign, HTTPAgentTarget
from sagsbench.attacks import BaselineAttackSuite
from sagsbench.judges import RegexJudge, PolicyJudge

campaign = Campaign(
    target=HTTPAgentTarget(
        name="customer-support-agent",
        endpoint="http://localhost:8000/chat",
        input_key="message",
        output_key="response",
    ),
    suites=[BaselineAttackSuite.from_builtin("enterprise")],
    judges=[RegexJudge(), PolicyJudge.from_builtin("sags_baseline")],
)

result = campaign.run()
result.to_json("reports/results.json")
result.to_markdown("reports/report.md")
```

## CLI commands

```bash
sagsbench init
sagsbench list-profiles
sagsbench scan --target http://localhost:8000/chat --profile enterprise
sagsbench report --input reports/sagsbench-results.json --format markdown
```

## Reports

SAGSBench generates:

- HTML executive report
- Markdown developer report
- JSON evidence logs
- CSV summary
- SARIF for GitHub code scanning

## Project status

This repository is an initial v0.1 scaffold intended for community iteration. It includes a working CLI, policy-as-code, built-in synthetic attack suites, target adapters, judges, and report exporters.

## Responsible use

SAGSBench is for authorized testing only. Do not test systems you do not own or have explicit permission to assess. The included attack prompts are synthetic and designed for defensive evaluation.

## License

Apache-2.0. See [LICENSE](LICENSE).

## Frontend landing page

This repository includes a deploy-ready static frontend under [`frontend/`](frontend/) inspired by modern AI-security product sites.

Run it locally:

```bash
cd frontend
python3 -m http.server 5173
```

Open `http://localhost:5173`.

The frontend includes:

- SafeAlign / SAGSBench hero section
- Quick-start tabs for HTTP agents, OpenAI-compatible APIs, and CI/CD
- Dashboard and attack-run previews
- Security + governance report cards
- Attack-suite matrix
- GitHub Pages deployment workflow
