from typing import Optional
from agents.schema import (
    RiskOutput,
    ConversionOutput,
    PremiumOutput,
    FraudOutput,
    DecisionOutput,
    EscalationOutput,
    RoutingExplanation,
)


class DecisionRouterAgent:
    def process(
        self,
        risk: RiskOutput,
        conversion: ConversionOutput,
        premium: PremiumOutput,
        fraud: Optional[FraudOutput] = None,
    ) -> tuple[DecisionOutput, EscalationOutput]:
        confidence = 1.0
        decision = "UNKNOWN"
        reason = []
        risk_f = f"Risk Tier is {risk.risk_tier}"
        conv_f = f"Conversion Probability is {conversion.conversion_probability}%"
        prem_f = (
            "Premium issue detected" if premium.premium_issue else "Premium is fine"
        )
        explanation = RoutingExplanation(
            risk_factor=risk_f, conversion_driver=conv_f, premium_issue=prem_f
        )
        if fraud and fraud.fraud_flag:
            decision = "ESCALATE_TO_UNDERWRITER"
            confidence = 0.3
            fraud_reasons = ", ".join(fraud.fraud_reason_codes)
            reason.append(
                f"Fraud flag triggered (score: {fraud.fraud_risk_score:.2f}). Reason codes: {fraud_reasons}."
            )
        elif fraud and fraud.rule_flags:
            decision = "ESCALATE_TO_UNDERWRITER"
            confidence = 0.4
            rule_texts = ", ".join(fraud.rule_flags)
            reason.append(f"Underwriting rules triggered: {rule_texts}.")
        elif risk.risk_tier == "HIGH" or conversion.conversion_probability < 20:
            decision = "ESCALATE_TO_UNDERWRITER"
            confidence = 0.4
            reason.append("High risk profile or extremely low conversion.")
        elif conversion.conversion_band == "MEDIUM" or premium.premium_issue:
            decision = "FOLLOW_UP_AGENT"
            confidence = 0.75
            reason.append(
                "Borderline conversion or premium adjustment needed. Agent intervention required."
            )
        elif risk.risk_tier == "LOW" and conversion.conversion_band == "HIGH":
            decision = "AUTO_APPROVE"
            confidence = 0.95
            reason.append("Low risk and high conversion. Safe to auto-approve.")
        else:
            decision = "FOLLOW_UP_AGENT"
            confidence = 0.6
            reason.append("Fallback to agent review.")
        if (
            fraud
            and fraud.fraud_risk_score > 0.3
            and decision != "ESCALATE_TO_UNDERWRITER"
        ):
            confidence *= 0.8
            reason.append(
                f"Fraud risk noted ({fraud.fraud_risk_score:.2f}) — confidence reduced."
            )
        decision_out = DecisionOutput(
            decision=decision,
            confidence_score=round(confidence, 2),
            decision_explanation=" ".join(reason),
            detailed_explanation=explanation,
        )
        escalation_req = False
        esc_reason = "None"
        if fraud and fraud.fraud_flag:
            escalation_req = True
            esc_reason = f"Fraud detected (score: {fraud.fraud_risk_score:.2f}). Immediate underwriter review required."
        elif fraud and hasattr(fraud, "rule_flags") and fraud.rule_flags:
            escalation_req = True
            esc_reason = f"Underwriting rules triggered: {', '.join(fraud.rule_flags)}. Underwriter review required."
        elif confidence < 0.6:
            escalation_req = True
            esc_reason = "System confidence dropped below 0.6 threshold."
        elif risk.risk_tier == "HIGH":
            escalation_req = True
            esc_reason = "High risk profile mandates escalation."
        elif risk.risk_tier == "MEDIUM" and premium.premium_issue:
            escalation_req = True
            esc_reason = "Medium risk with premium discrepancy triggers escalation."
        escalation_out = EscalationOutput(
            escalation_required=escalation_req, reason=esc_reason
        )
        return decision_out, escalation_out
