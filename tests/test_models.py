from sagsbench.models import AttackResult, CampaignResult, Domain, Severity


def test_summary_computes_sags_score():
    result = CampaignResult(target_name="test")
    result.results.append(
        AttackResult(
            test_id="T1",
            category="prompt_injection",
            domain=Domain.security,
            severity=Severity.high,
            status="passed",
            attack_success=False,
            prompt="x",
            expected_behavior="y",
        )
    )
    result.finalize()
    assert result.summary["total"] == 1
    assert result.summary["sags_score"] == 100.0
