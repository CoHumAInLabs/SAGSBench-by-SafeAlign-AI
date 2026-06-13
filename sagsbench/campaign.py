from __future__ import annotations

from rich.progress import track

from sagsbench.judge import Judge
from sagsbench.models import AttackCase, AttackResult, CampaignResult
from sagsbench.target import AgentTarget


class AttackSuite:
    name: str = "attack-suite"

    def cases(self) -> list[AttackCase]:
        raise NotImplementedError


class Campaign:
    def __init__(self, target: AgentTarget, suites: list[AttackSuite], judges: list[Judge]):
        self.target = target
        self.suites = suites
        self.judges = judges

    def run(self, show_progress: bool = True) -> CampaignResult:
        all_cases: list[AttackCase] = []
        for suite in self.suites:
            all_cases.extend(suite.cases())

        iterator = track(all_cases, description="Running SAGSBench campaign") if show_progress else all_cases
        result = CampaignResult(target_name=self.target.name)

        for case in iterator:
            try:
                response = self.target.send(case.prompt)
                findings = [judge.evaluate(case, response) for judge in self.judges]
                passed = all(f.passed for f in findings)
                result.results.append(
                    AttackResult(
                        test_id=case.id,
                        category=case.category,
                        domain=case.domain,
                        severity=case.severity,
                        status="passed" if passed else "failed",
                        attack_success=not passed,
                        prompt=case.prompt,
                        expected_behavior=case.expected_behavior,
                        agent_response=response.text,
                        tool_calls=response.tool_calls,
                        findings=findings,
                        mapped_controls=case.mapped_controls,
                        recommendation=_recommendation(case.category),
                    )
                )
            except Exception as exc:  # defensive runner; evidence keeps error visible
                result.results.append(
                    AttackResult(
                        test_id=case.id,
                        category=case.category,
                        domain=case.domain,
                        severity=case.severity,
                        status="error",
                        attack_success=False,
                        prompt=case.prompt,
                        expected_behavior=case.expected_behavior,
                        findings=[],
                        mapped_controls=case.mapped_controls,
                        recommendation=f"Fix target or adapter error before interpreting this case: {exc}",
                    )
                )
        return result.finalize()


def _recommendation(category: str) -> str:
    defaults = {
        "prompt_injection": "Harden system instructions, add policy gates, and reject instruction override attempts.",
        "tool_misuse": "Require authorization, scoped credentials, and policy checks before tool execution.",
        "privacy_leakage": "Add PII/secret redaction and deny cross-user memory access.",
        "goal_hijack": "Constrain role boundaries and escalate out-of-scope requests.",
        "policy_bypass": "Enforce policy-as-code before agent actions and log all decisions.",
        "inter_agent_trust": "Verify agent identity, provenance, and permissions before trusting delegated messages.",
        "governance": "Require human-in-the-loop escalation for high-impact decisions.",
        "kill_switch": "Validate runtime block decisions, stop execution, and write audit records.",
    }
    return defaults.get(category, "Review failed behavior and add preventive, detective, and corrective controls.")
