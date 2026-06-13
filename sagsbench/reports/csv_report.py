from __future__ import annotations

import csv
from pathlib import Path

from sagsbench.models import CampaignResult


def write_csv_report(result: CampaignResult, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["test_id", "category", "domain", "severity", "status", "attack_success", "controls", "recommendation"],
        )
        writer.writeheader()
        for item in result.results:
            writer.writerow(
                {
                    "test_id": item.test_id,
                    "category": item.category,
                    "domain": item.domain,
                    "severity": item.severity,
                    "status": item.status,
                    "attack_success": item.attack_success,
                    "controls": ";".join(item.mapped_controls),
                    "recommendation": item.recommendation,
                }
            )
