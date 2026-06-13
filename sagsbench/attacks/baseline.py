from __future__ import annotations

from pathlib import Path

import yaml

from sagsbench.campaign import AttackSuite
from sagsbench.models import AttackCase


class BaselineAttackSuite(AttackSuite):
    def __init__(self, name: str, cases: list[AttackCase]):
        self.name = name
        self._cases = cases

    @classmethod
    def from_file(cls, path: str | Path) -> "BaselineAttackSuite":
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        cases = [AttackCase(**item) for item in raw.get("cases", [])]
        return cls(raw.get("name", Path(path).stem), cases)

    @classmethod
    def from_builtin(cls, profile: str = "enterprise") -> "BaselineAttackSuite":
        path = Path(__file__).resolve().parents[1] / "datasets" / f"{profile}_attacks.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Unknown built-in profile: {profile}")
        return cls.from_file(path)

    def cases(self) -> list[AttackCase]:
        return self._cases
