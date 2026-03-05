import pandas as pd
import joblib
import shap
import json
import os
from agents.schema import QuoteInput, RiskOutput


class RiskProfilerAgent:
    def __init__(self, models_dir="models"):
        self.rf_model = joblib.load(os.path.join(models_dir, "risk_profiler_rf.pkl"))
        self.encoders = joblib.load(
            os.path.join(models_dir, "categorical_encoders.pkl")
        )
        self.feature_cols = joblib.load(os.path.join(models_dir, "feature_columns.pkl"))
        self.explainer = shap.TreeExplainer(self.rf_model)

    def _strict_risk_heuristic(self, quote: QuoteInput) -> str:
        """Deterministic risk heuristic that ALWAYS overrides ML when triggered."""
        risk_points = 0
        if quote.Prev_Accidents >= 2:
            risk_points += 3
        elif quote.Prev_Accidents == 1:
            risk_points += 1
        if quote.Prev_Citations >= 3:
            risk_points += 2
        elif quote.Prev_Citations >= 2:
            risk_points += 2
        elif quote.Prev_Citations >= 1:
            risk_points += 1
        if quote.Driver_Age < 25:
            risk_points += 2
        elif quote.Driver_Age > 65:
            risk_points += 1
        if (
            isinstance(quote.Annual_Miles_Range, str)
            and ">" in quote.Annual_Miles_Range
            and "15" in quote.Annual_Miles_Range
        ):
            risk_points += 1
        if risk_points >= 4:
            return "HIGH"
        elif risk_points >= 2:
            return "MEDIUM"
        return "LOW"

    def process(self, quote: QuoteInput) -> RiskOutput:
        input_data = quote.model_dump()
        df = pd.DataFrame([input_data])
        for col in self.feature_cols:
            if col not in df.columns:
                df[col] = 0.0
        for col in self.feature_cols:
            if col in self.encoders and col in df.columns:
                df[col] = self.encoders[col].transform(df[col].astype(str))
        df = df[self.feature_cols]
        ml_prediction = self.rf_model.predict(df)[0]
        heuristic_tier = self._strict_risk_heuristic(quote)
        tier_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
        if tier_order.get(heuristic_tier, 0) > tier_order.get(ml_prediction, 0):
            prediction = heuristic_tier
        else:
            prediction = ml_prediction
        probs = self.rf_model.predict_proba(df)[0]
        classes = self.rf_model.classes_
        prob_dict = dict(zip(classes, probs))
        risk_score = (prob_dict.get("HIGH", 0) * 100) + (
            prob_dict.get("MEDIUM", 0) * 50
        )
        if prediction != ml_prediction:
            explanation = f"Upgraded to {prediction} risk by strict underwriting heuristics (overriding ML {ml_prediction})."
        else:
            shap_values = self.explainer.shap_values(df)
            class_idx = list(classes).index(prediction)
            import numpy as np

            if isinstance(shap_values, list):
                sv = shap_values[class_idx][0]
            else:
                shap_array = np.array(shap_values)
                if len(shap_array.shape) == 3:
                    sv = shap_array[0, :, class_idx]
                else:
                    sv = shap_array[0]
            sv = np.array(sv).flatten()
            sorted_indices = np.argsort(-np.abs(sv))
            top_feature = self.feature_cols[sorted_indices[0]]
            explanation = (
                f"Classified as {prediction} risk primarily due to {top_feature}."
            )
        return RiskOutput(
            risk_score=round(risk_score, 1),
            risk_tier=prediction,
            risk_explanation=explanation,
        )
