import uuid
import logging
from agents.schema import QuoteInput, PipelineOutput
from agents.agent_1_risk import RiskProfilerAgent
from agents.agent_fraud_detection import FraudDetectionAgent
from agents.agent_2_conversion import ConversionPredictorAgent
from agents.agent_personalization import CustomerPersonalizationAgent
from agents.agent_3_premium import PremiumAdvisorAgent
from agents.agent_4_router import DecisionRouterAgent

logger = logging.getLogger("Pipeline")


class MultiAgentPipeline:
    def __init__(self, models_dir="models"):
        self.agent_risk = RiskProfilerAgent(models_dir)
        self.agent_fraud = FraudDetectionAgent(models_dir)
        self.agent_conversion = ConversionPredictorAgent(models_dir)
        self.agent_personalization = CustomerPersonalizationAgent(models_dir)
        self.agent_premium = PremiumAdvisorAgent()
        self.agent_router = DecisionRouterAgent()

    def execute(self, quote: QuoteInput) -> PipelineOutput:
        risk_out = self.agent_risk.process(quote)
        fraud_out = None
        try:
            fraud_out = self.agent_fraud.process(quote, risk_out)
            logger.info(
                f"Fraud: score={fraud_out.fraud_risk_score:.4f}, flag={fraud_out.fraud_flag}"
            )
        except Exception as e:
            logger.error(f"Fraud agent failed: {e}. Continuing pipeline.")
        conversion_out = self.agent_conversion.process(quote, risk_out.risk_tier)
        personalization_out = None
        try:
            personalization_out = self.agent_personalization.process(
                quote, risk_out, conversion_out
            )
            logger.info(f"Personalization: plan={personalization_out.recommended_plan}")
        except Exception as e:
            logger.error(f"Personalization agent failed: {e}. Continuing pipeline.")
        premium_out = self.agent_premium.process(
            quote, conversion_out.conversion_probability, risk_out.risk_tier
        )
        decision_out, escalation_out = self.agent_router.process(
            risk_out, conversion_out, premium_out, fraud_out
        )
        return PipelineOutput(
            quote_id=str(uuid.uuid4()),
            risk_evaluation=risk_out,
            fraud_detection=fraud_out,
            conversion_prediction=conversion_out,
            personalization=personalization_out,
            premium_advice=premium_out,
            final_decision=decision_out,
            escalation_status=escalation_out,
        )
