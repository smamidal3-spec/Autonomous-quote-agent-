"""
Agent: Fraud Detection
Position in pipeline: After Risk Profiler (Step 2 of 6)
Detects suspicious or inconsistent quote requests using Isolation Forest + Gradient Boosting.
"""

import logging
import os
import time
from typing import List, Optional

import joblib
import pandas as pd

from agents.label_normalization import (
    coverage_to_numeric,
    is_high_vehicle_cost,
    miles_to_numeric,
    salary_to_numeric,
    vehicle_cost_to_numeric,
)
from agents.schema import FraudOutput, QuoteInput, RiskOutput

logger = logging.getLogger("FraudDetectionAgent")


class FraudDetectionAgent:
    def __init__(self, models_dir="models"):
        try:
            self.iso_forest = joblib.load(
                os.path.join(models_dir, "fraud_isolation_forest.pkl")
            )
            self.gb_model = joblib.load(
                os.path.join(models_dir, "fraud_detector_gb.pkl")
            )
            self.scaler = joblib.load(os.path.join(models_dir, "fraud_scaler.pkl"))
            self.feature_cols = joblib.load(
                os.path.join(models_dir, "fraud_feature_cols.pkl")
            )
            self.loaded = True
            logger.info("Fraud Detection models loaded successfully")
        except Exception as exc:
            logger.warning(
                f"Fraud Detection models not found: {exc}. Agent will pass-through."
            )
            self.loaded = False

    def _validate_profile(self, quote: QuoteInput) -> Optional[str]:
        """Step 1: Input validation checks."""
        if quote.Driver_Age < 18:
            return "Driver age below legal driving age"
        if quote.Driving_Exp > max(0, quote.Driver_Age - 16):
            return "Driving experience inconsistent with age"
        if quote.Quoted_Premium < 0:
            return "Negative premium value"
        if quote.Prev_Accidents < 0 or quote.Prev_Citations < 0:
            return "Negative values not allowed"
        if quote.HH_Vehicles < 0 or quote.HH_Drivers < 0:
            return "Negative values for household data"
        if quote.Driver_Age > 100 or quote.Driving_Exp > 85:
            return "Extremely unrealistic inputs"
        if quote.Quoted_Premium > 1_000_000:
            return "Extremely unrealistic inputs"
        return None

    def _evaluate_rules(
        self, quote: QuoteInput, risk: RiskOutput, sal_num: float, veh_cost_num: float
    ) -> List[str]:
        """Step 2: Business rule engine."""
        flags: list[str] = []
        if quote.Driver_Age < 23 and veh_cost_num >= 25:
            flags.append("Young driver with luxury vehicle")
        if veh_cost_num > sal_num * 4:
            flags.append("Vehicle price far above salary")
        if risk.risk_score > 60 and quote.Quoted_Premium < 500:
            flags.append("Premium too low for high-risk driver")
        if quote.Driving_Exp > (quote.Driver_Age - 16):
            flags.append("Driving experience inconsistent with age")
        return flags

    def _extract_features(self, quote: QuoteInput, risk: RiskOutput) -> pd.DataFrame:
        """Engineer fraud-detection features from quote + risk output."""
        sal_num = salary_to_numeric(quote.Sal_Range)
        veh_cost_num = vehicle_cost_to_numeric(quote.Vehicl_Cost_Range)
        cov_num = coverage_to_numeric(quote.Coverage)
        miles_num = miles_to_numeric(quote.Annual_Miles_Range)

        driving_exp = max(quote.Driving_Exp, 0)
        features = {
            "driver_age": quote.Driver_Age,
            "driving_exp": driving_exp,
            "prev_accidents": quote.Prev_Accidents,
            "prev_citations": quote.Prev_Citations,
            "risk_score": risk.risk_score,
            "quoted_premium": quote.Quoted_Premium,
            "hh_vehicles": quote.HH_Vehicles,
            "hh_drivers": quote.HH_Drivers,
            "sal_numeric": sal_num,
            "veh_cost_numeric": veh_cost_num,
            "cov_numeric": cov_num,
            "miles_numeric": miles_num,
            "vehicle_cost_to_salary_ratio": veh_cost_num / (sal_num + 1),
            "premium_to_vehicle_ratio": quote.Quoted_Premium
            / ((veh_cost_num * 100000) + 1),
            "premium_to_risk_ratio": quote.Quoted_Premium / (risk.risk_score + 1),
            "driver_age_to_vehicle_value": quote.Driver_Age / (veh_cost_num + 1),
            "experience_to_accident_ratio": driving_exp / (quote.Prev_Accidents + 1),
            "premium_deviation_from_expected": quote.Quoted_Premium
            / (risk.risk_score * 10 + 1),
        }
        return pd.DataFrame([features])[self.feature_cols]

    def _generate_reason_codes(
        self, quote: QuoteInput, risk: RiskOutput, fraud_score: float
    ) -> list[str]:
        """Generate human-readable fraud reason codes."""
        reasons: list[str] = []
        if quote.Prev_Accidents >= 2 and quote.Driving_Exp <= 3:
            reasons.append("high_accident_velocity")
        if quote.Driver_Age < 23 and is_high_vehicle_cost(quote.Vehicl_Cost_Range):
            reasons.append("age_vehicle_mismatch")
        if risk.risk_score > 50 and quote.Quoted_Premium < 500:
            reasons.append("premium_risk_mismatch")
        if quote.Prev_Citations >= 3 and quote.Prev_Accidents >= 2:
            reasons.append("high_violation_frequency")
        if quote.Veh_Usage == "Business" and quote.Coverage == "Basic":
            reasons.append("coverage_usage_mismatch")
        if quote.Re_Quote == "Yes" and risk.risk_score > 60:
            reasons.append("suspicious_requote_pattern")
        if not reasons and fraud_score > 0.7:
            reasons.append("statistical_anomaly")
        return reasons

    def process(self, quote: QuoteInput, risk: RiskOutput) -> FraudOutput:
        """Process quote through fraud detection. Returns safe defaults on error."""
        start_time = time.time()
        try:
            if not self.loaded:
                raise RuntimeError("Models not loaded")

            validation_error = self._validate_profile(quote)
            if validation_error:
                return FraudOutput(
                    fraud_risk_score=1.0,
                    fraud_flag=True,
                    fraud_reason_codes=[validation_error],
                    rule_flags=[],
                    decision="INVALID_PROFILE",
                )

            features_df = self._extract_features(quote, risk)
            sal_num = features_df["sal_numeric"].iloc[0]
            veh_cost_num = features_df["veh_cost_numeric"].iloc[0]
            rule_flags = self._evaluate_rules(quote, risk, sal_num, veh_cost_num)

            features_scaled = self.scaler.transform(features_df)
            iso_score = self.iso_forest.decision_function(features_scaled)[0]
            iso_fraud_score = max(0, min(1, 0.5 - iso_score))

            gb_proba = self.gb_model.predict_proba(features_df)[0]
            gb_fraud_prob = gb_proba[1] if len(gb_proba) > 1 else 0.0

            fraud_risk_score = round(0.4 * iso_fraud_score + 0.6 * gb_fraud_prob, 4)

            fraud_flag = False
            decision = "CLEAR"
            if fraud_risk_score >= 0.5:
                fraud_flag = True
                decision = "REVIEW_REQUIRED"
            elif rule_flags:
                decision = "ESCALATE_RULES"

            reason_codes = self._generate_reason_codes(quote, risk, fraud_risk_score)
            inference_time = time.time() - start_time
            logger.info(
                f"Fraud detection: score={fraud_risk_score:.4f}, flag={fraud_flag}, time={inference_time:.3f}s"
            )

            return FraudOutput(
                fraud_risk_score=fraud_risk_score,
                fraud_flag=fraud_flag,
                fraud_reason_codes=reason_codes if reason_codes else ["none"],
                rule_flags=rule_flags,
                decision=decision,
            )
        except Exception as exc:
            inference_time = time.time() - start_time
            logger.error(
                f"Fraud detection failed ({inference_time:.3f}s): {exc}. Passing through safely."
            )
            return FraudOutput(
                fraud_risk_score=0.0,
                fraud_flag=False,
                fraud_reason_codes=["agent_error_passthrough"],
                rule_flags=[],
                decision="CLEAR",
            )
