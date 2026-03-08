import pandas as pd
import joblib
import shap
import os
import numpy as np
from agents.schema import QuoteInput, ConversionOutput


class ConversionPredictorAgent:
    def __init__(self, models_dir="models"):
        self.xgb_model = joblib.load(
            os.path.join(models_dir, "conversion_predictor_xgb.pkl")
        )
        self.encoders = joblib.load(
            os.path.join(models_dir, "categorical_encoders.pkl")
        )
        self.risk_encoder = joblib.load(os.path.join(models_dir, "risk_encoder.pkl"))
        self.feature_cols = joblib.load(os.path.join(models_dir, "feature_columns.pkl"))
        self.explainer = shap.TreeExplainer(self.xgb_model)

    def process(self, quote: QuoteInput, risk_tier: str) -> ConversionOutput:
        input_data = quote.model_dump()
        df = pd.DataFrame([input_data])
        for col in self.feature_cols:
            if col not in df.columns and col != "Risk_Tier":
                df[col] = 0.0
        for col in self.feature_cols:
            if col in self.encoders and col in df.columns:
                df[col] = self.encoders[col].transform(df[col].astype(str))
        try:
            encoded_risk = self.risk_encoder.transform([risk_tier])[0]
        except ValueError:
            encoded_risk = 0
        df["Risk_Tier"] = encoded_risk
        xgb_cols = self.feature_cols + ["Risk_Tier"]
        df = df[xgb_cols]
        prob = float(self.xgb_model.predict_proba(df)[0][1] * 100)
        if prob > 70:
            band = "HIGH"
        elif prob > 30:
            band = "MEDIUM"
        else:
            band = "LOW"
        shap_values = self.explainer.shap_values(df)
        import numpy as np

        if isinstance(shap_values, list):
            sv = shap_values[1][0]
        else:
            shap_array = np.array(shap_values)
            if len(shap_array.shape) == 3:
                sv = shap_array[0, :, 1]
            else:
                sv = shap_array[0]
        sv = np.array(sv).flatten()
        sorted_indices = np.argsort(-np.abs(sv))
        top_drivers = [xgb_cols[i] for i in sorted_indices[:3]]
        return ConversionOutput(
            conversion_probability=round(prob, 2),
            conversion_band=band,
            top_conversion_drivers=top_drivers,
        )
