from __future__ import annotations

import json
from pathlib import Path

from sagsbench.models import CampaignResult


def write_sarif_report(result: CampaignResult, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rules = {}
    sarif_results = []
    for item in result.results:
        rule_id = f"SAGSBench.{item.category}"
        rules[rule_id] = {
            "id": rule_id,
            "name": item.category,
            "shortDescription": {"text": item.expected_behavior},
            "help": {"text": item.recommendation},
        }
        if item.status == "failed":
            sarif_results.append(
                {
                    "ruleId": rule_id,
                    "level": "error" if item.severity in {"critical", "high"} else "warning",
                    "message": {"text": f"{item.test_id}: {item.recommendation}"},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": "agent-redteam"},
                                "region": {"startLine": 1},
                            }
                        }
                    ],
                }
            )
    payload = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "SAGSBench",
                        "informationUri": "https://safealignai.io/",
                        "rules": list(rules.values()),
                    }
                },
                "results": sarif_results,
            }
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
