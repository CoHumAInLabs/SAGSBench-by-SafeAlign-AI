from __future__ import annotations

from dataclasses import dataclass

from sagsbench.judge import Judge
from sagsbench.models import AgentResponse, AttackCase, JudgeFinding


@dataclass
class LLMJudge(Judge):
    model: str = "gpt-4o-mini"
    name: str = "llm-judge"

    def evaluate(self, case: AttackCase, response: AgentResponse) -> JudgeFinding:
        # Placeholder for provider-backed evaluation. Kept intentionally optional for OSS portability.
        return JudgeFinding(
            judge=self.name,
            passed=True,
            confidence=0.0,
            rationale=(
                "LLMJudge placeholder did not evaluate. Configure a provider-specific judge "
                "or use RegexJudge and PolicyJudge for deterministic v0.1 runs."
            ),
        )
