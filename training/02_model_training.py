import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
import os

print("--- Starting Model Design ---")
data_path = "quote_agents/data/use_case_03/USE CASE - 03/Autonomous QUOTE AGENTS.csv"
df = pd.read_csv(data_path)
print(f"Loaded dataset with {len(df)} rows.")


def calculate_risk(row):
    risk_score = 0
    if pd.notna(row.get("Prior_Insurance")) and row["Prior_Insurance"] == "No":
        risk_score += 2
    if pd.notna(row.get("Premium")):
        if row["Premium"] > 1500:
            return "High"
        elif row["Premium"] > 800:
            return "Medium"
    return "Low"


df["Risk_Tier_Target"] = df.apply(calculate_risk, axis=1)
df["Conversion_Target"] = df["Policy_Bind"].apply(lambda x: 1 if x == "Yes" else 0)
features = df.drop(
    columns=[
        "Quote_Num",
        "Policy_Bind",
        "Risk_Tier_Target",
        "Conversion_Target",
        "Premium",
    ],
    errors="ignore",
)
encoders = {}
for col in features.columns:
    if features[col].dtype == "object":
        le = LabelEncoder()
        features[col] = features[col].astype(str)
        features[col] = le.fit_transform(features[col])
        encoders[col] = le
features = features.fillna(features.median(numeric_only=True))
print("\n--- Training Agent 1: Risk Profiler (Random Forest) ---")
X = features
y_risk = df["Risk_Tier_Target"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y_risk, test_size=0.2, random_state=42
)
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)
acc = rf_model.score(X_test, y_test)
print(f"Risk Profiler Accuracy: {acc:.2f}")
print("\n--- Training Agent 2: Conversion Predictor (XGBoost) ---")
X_conv = features.copy()
risk_encoder = LabelEncoder()
X_conv["Risk_Tier"] = risk_encoder.fit_transform(df["Risk_Tier_Target"])
y_conv = df["Conversion_Target"]
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_conv, y_conv, test_size=0.2, random_state=42
)
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    random_state=42,
    use_label_encoder=False,
    eval_metric="logloss",
)
xgb_model.fit(X_train_c, y_train_c)
acc_c = xgb_model.score(X_test_c, y_test_c)
print(f"Conversion Predictor Accuracy: {acc_c:.2f}")
os.makedirs("quote_agents/models", exist_ok=True)
joblib.dump(rf_model, "quote_agents/models/risk_profiler_rf.pkl")
joblib.dump(xgb_model, "quote_agents/models/conversion_predictor_xgb.pkl")
joblib.dump(encoders, "quote_agents/models/categorical_encoders.pkl")
joblib.dump(risk_encoder, "quote_agents/models/risk_encoder.pkl")
joblib.dump(list(X.columns), "quote_agents/models/feature_columns.pkl")
print("\n✅ Step 5 Complete: Models trained and saved successfully!")
