from agents.agent_4_router import DecisionRouterAgent
from agents.schema import (
    ConversionOutput,
    DecisionOutput,
    EscalationOutput,
    FraudOutput,
    PremiumOutput,
    RiskOutput,
)


def _run_router(
    risk_tier: str,
    conversion_probability: float,
    conversion_band: str,
    premium_issue: bool,
    fraud: FraudOutput | None = None,
) -> tuple[DecisionOutput, EscalationOutput]:
    router = DecisionRouterAgent()
    risk = RiskOutput(risk_score=45.0, risk_tier=risk_tier, risk_explanation="test")
    conversion = ConversionOutput(
        conversion_probability=conversion_probability,
        conversion_band=conversion_band,
        top_conversion_drivers=["Driver_Age"],
    )
    premium = PremiumOutput(
        premium_issue=premium_issue,
        recommended_premium_range=[1000.0, 1200.0],
        recommendation_reason="test",
    )
    return router.process(risk, conversion, premium, fraud)


def test_router_auto_approve_for_low_risk_high_conversion() -> None:
    decision, escalation = _run_router("LOW", 85.0, "HIGH", False)
    assert decision.decision == "AUTO_APPROVE"
    assert escalation.escalation_required is False


def test_router_escalates_when_fraud_flagged() -> None:
    fraud = FraudOutput(
        fraud_risk_score=0.9,
        fraud_flag=True,
        fraud_reason_codes=["statistical_anomaly"],
        rule_flags=[],
        decision="REVIEW_REQUIRED",
    )
    decision, escalation = _run_router("LOW", 80.0, "HIGH", False, fraud)
    assert decision.decision == "ESCALATE_TO_UNDERWRITER"
    assert escalation.escalation_required is True


def test_router_follow_up_for_medium_conversion() -> None:
    decision, escalation = _run_router("LOW", 45.0, "MEDIUM", False)
    assert decision.decision == "FOLLOW_UP_AGENT"
    assert escalation.escalation_required is False
