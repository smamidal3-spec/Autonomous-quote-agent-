"""
Agent: Customer Personalization
Position in pipeline: After Conversion Predictor (Step 4 of 6)
Recommends insurance plans and add-ons using K-Means customer segmentation.
"""

import pandas as pd
import numpy as np
import joblib
import os
import time
import logging
from agents.schema import (
    QuoteInput,
    RiskOutput,
    ConversionOutput,
    PersonalizationOutput,
)

logger = logging.getLogger("PersonalizationAgent")
ADDON_LABELS = {
    "zero_depreciation": "Zero Depreciation Cover",
    "engine_protection": "Engine Protection",
    "roadside_assistance": "24/7 Roadside Assistance",
    "personal_accident_cover": "Personal Accident Cover",
    "return_to_invoice": "Return to Invoice",
    "consumables_cover": "Consumables Cover",
    "key_replacement": "Key Replacement",
    "ncb_protection": "No-Claim Bonus Protection",
    "tyre_protect": "Tyre Protection",
    "passenger_cover": "Passenger Cover",
}


class CustomerPersonalizationAgent:
    def __init__(self, models_dir="models"):
        try:
            self.kmeans = joblib.load(
                os.path.join(models_dir, "personalization_kmeans.pkl")
            )
            self.scaler = joblib.load(
                os.path.join(models_dir, "personalization_scaler.pkl")
            )
            self.plan_mapper = joblib.load(
                os.path.join(models_dir, "personalization_plan_mapper.pkl")
            )
            self.feature_cols = joblib.load(
                os.path.join(models_dir, "personalization_feature_cols.pkl")
            )
            self.loaded = True
            logger.info("Personalization models loaded successfully")
        except Exception as e:
            logger.warning(
                f"Personalization models not found: {e}. Agent will use defaults."
            )
            self.loaded = False

    def _extract_features(self, quote: QuoteInput, risk: RiskOutput) -> pd.DataFrame:
        """Extract clustering features from quote data."""
        sal_map = {
            "<= ₹ 25 Lakh": 2.5,
            "> ₹ 25 Lakh <= ₹ 40 Lakh": 3.75,
            "> ₹ 40 Lakh <= ₹ 60 Lakh": 6.25,
            "> ₹ 60 Lakh <= ₹ 90 Lakh": 8.75,
            "> ₹ 90 Lakh ": 12.5,
        }
        veh_cost_map = {
            "<= ₹ 10 Lakh": 10,
            "> ₹ 10 Lakh <= ₹ 20 Lakh": 15,
            "> ₹ 20 Lakh <= ₹ 30 Lakh": 25,
            "> ₹ 30 Lakh <= ₹ 40 Lakh": 35,
            "> ₹ 40 Lakh ": 40,
        }
        cov_map = {"Basic": 1, "Balanced": 2, "Enhanced": 3}
        miles_map = {
            "<= 7.5 K": 5,
            "> 7.5 K & <= 15 K": 11,
            "> 15 K & <= 25 K": 20,
            "> 25 K & <= 35 K": 30,
            "> 35 K & <= 45 K": 40,
            "> 45 K & <= 55 K": 50,
            "> 55 K": 60,
        }
        features = {
            "driver_age": quote.Driver_Age,
            "driving_exp": max(quote.Driving_Exp, 0),
            "risk_score": risk.risk_score,
            "sal_numeric": sal_map.get(quote.Sal_Range, 6.25),
            "veh_cost_numeric": veh_cost_map.get(quote.Vehicl_Cost_Range, 15),
            "cov_numeric": cov_map.get(quote.Coverage, 2),
            "miles_numeric": miles_map.get(quote.Annual_Miles_Range, 11),
            "quoted_premium": quote.Quoted_Premium,
            "prev_accidents": quote.Prev_Accidents,
        }
        return pd.DataFrame([features])[self.feature_cols]

    def _enhance_addons(
        self,
        base_addons: list,
        quote: QuoteInput,
        risk: RiskOutput,
        conversion: ConversionOutput,
    ) -> list:
        """Dynamically enhance add-on recommendations based on profile."""
        addons = list(base_addons)
        if quote.Driver_Age < 25 and "personal_accident_cover" not in addons:
            addons.append("personal_accident_cover")
        if (
            quote.Annual_Miles_Range
            in [
                "> 15 K",
                "> 15 K & <= 25 K",
                "> 25 K & <= 35 K",
                "> 35 K & <= 45 K",
                "> 45 K & <= 55 K",
                "> 55 K",
            ]
            and "roadside_assistance" not in addons
        ):
            addons.append("roadside_assistance")
        if quote.Vehicl_Cost_Range in [
            "> 30 K",
            "20 K - 30 K",
            "> ₹30 Lakh",
            "₹20L - ₹30L",
            "> ₹ 30 Lakh <= ₹ 40 Lakh",
            "> ₹ 40 Lakh ",
        ]:
            if "zero_depreciation" not in addons:
                addons.append("zero_depreciation")
            if "engine_protection" not in addons:
                addons.append("engine_protection")
        if conversion.conversion_probability > 70 and "return_to_invoice" not in addons:
            addons.append("return_to_invoice")
        return addons

    def _calc_personalization_score(
        self,
        quote: QuoteInput,
        risk: RiskOutput,
        conversion: ConversionOutput,
        plan_data: dict,
    ) -> float:
        """Calculate how well the recommended plan fits the customer."""
        score = 0.5
        if risk.risk_tier == "HIGH" and plan_data["coverage_level"] in [
            "High",
            "Comprehensive",
        ]:
            score += 0.15
        elif risk.risk_tier == "LOW" and plan_data["coverage_level"] in [
            "Basic",
            "Medium",
        ]:
            score += 0.1
        score += (conversion.conversion_probability / 100) * 0.2
        if quote.Driving_Exp > 10:
            score += 0.05
        if (
            quote.Quoted_Premium < 500
            and plan_data["coverage_level"] == "Comprehensive"
        ):
            score -= 0.1
        return round(min(max(score, 0.1), 1.0), 4)

    def process(
        self, quote: QuoteInput, risk: RiskOutput, conversion: ConversionOutput
    ) -> PersonalizationOutput:
        """Process quote through personalization engine. Returns defaults on error."""
        start_time = time.time()
        try:
            if not self.loaded:
                raise RuntimeError("Models not loaded")
            features_df = self._extract_features(quote, risk)
            features_scaled = self.scaler.transform(features_df)
            segment = self.kmeans.predict(features_scaled)[0]
            plan_data = self.plan_mapper.get(
                segment,
                {
                    "plan": "Balanced Guard",
                    "coverage_level": "Medium",
                    "addons": ["roadside_assistance", "personal_accident_cover"],
                },
            )
            enhanced_addons = self._enhance_addons(
                plan_data["addons"], quote, risk, conversion
            )
            p_score = self._calc_personalization_score(
                quote, risk, conversion, plan_data
            )
            addon_labels = [
                ADDON_LABELS.get(a, a.replace("_", " ").title())
                for a in enhanced_addons
            ]
            inference_time = time.time() - start_time
            logger.info(
                f"Personalization: plan={plan_data['plan']}, segment={segment}, score={p_score}, time={inference_time:.3f}s"
            )
            return PersonalizationOutput(
                recommended_plan=plan_data["plan"],
                coverage_level=plan_data["coverage_level"],
                recommended_addons=addon_labels,
                personalization_score=p_score,
            )
        except Exception as e:
            inference_time = time.time() - start_time
            logger.error(
                f"Personalization failed ({inference_time:.3f}s): {e}. Using defaults."
            )
            return PersonalizationOutput(
                recommended_plan="Standard Cover",
                coverage_level="Medium",
                recommended_addons=[
                    "24/7 Roadside Assistance",
                    "Personal Accident Cover",
                ],
                personalization_score=0.5,
            )
