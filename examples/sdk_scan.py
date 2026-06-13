from sagsbench import Campaign, HTTPAgentTarget
from sagsbench.attacks import BaselineAttackSuite
from sagsbench.judges import PolicyJudge, RegexJudge

campaign = Campaign(
    target=HTTPAgentTarget(
        name="local-agent",
        endpoint="http://localhost:8000/chat",
        input_key="message",
        output_key="response",
    ),
    suites=[BaselineAttackSuite.from_builtin("enterprise")],
    judges=[RegexJudge(), PolicyJudge.from_builtin("sags_baseline")],
)

result = campaign.run()
result.to_json("reports/sagsbench-results.json")
result.to_html("reports/sagsbench-report.html")
result.to_markdown("reports/sagsbench-report.md")
print(result.summary)
