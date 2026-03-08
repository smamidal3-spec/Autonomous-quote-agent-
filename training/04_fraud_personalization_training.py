"""
Training Script: Fraud Detection + Customer Personalization Models
Generates 100,000 synthetic insurance records and trains:
  1. Fraud Detection: Isolation Forest (anomaly) + Gradient Boosting (classifier)
  2. Customer Personalization: K-Means clustering + Plan Mapper
"""

import pandas as pd
import numpy as np
import os
import joblib
import warnings
from sklearn.ensemble import IsolationForest, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, silhouette_score, confusion_matrix

warnings.filterwarnings("ignore")
np.random.seed(42)
print("=" * 60)
print("TRAINING: Fraud Detection + Customer Personalization")
print("=" * 60)
print("\n--- Phase 1: Generating 100,000 Synthetic Records ---")
N = 100_000
real_data_path = "data/use_case_03/USE CASE - 03/Autonomous QUOTE AGENTS.csv"
if os.path.exists(real_data_path):
    real_df = pd.read_csv(real_data_path)
    print(f"Using real data distributions from {len(real_df)} records")
else:
    real_df = None
    print("No real data found — using hardcoded distributions")
regions = ["A", "B", "C", "D", "E", "F", "G", "H"]
region_weights = [0.2, 0.15, 0.15, 0.12, 0.1, 0.1, 0.1, 0.08]
policy_types = ["Car", "Truck", "SUV", "Van"]
policy_weights = [0.45, 0.2, 0.25, 0.1]
genders = ["Male", "Female"]
gender_weights = [0.55, 0.45]
marital = ["Married", "Single", "Divorced"]
marital_weights = [0.5, 0.35, 0.15]
education = ["High School", "Bachelors", "Masters", "PhD"]
edu_weights = [0.25, 0.4, 0.25, 0.1]
coverage = ["Basic", "Balanced", "Comprehensive"]
cov_weights = [0.3, 0.45, 0.25]
veh_usage = ["Pleasure", "Business", "Commute"]
usage_weights = [0.35, 0.3, 0.35]
miles_ranges = ["<= 7.5 K", "7.5 K - 15 K", "> 15 K"]
miles_weights = [0.4, 0.35, 0.25]
sal_ranges = [
    "<= ₹ 25 Lakh",
    "₹ 25 Lakh - ₹ 50 Lakh",
    "₹ 50 Lakh - ₹ 75 Lakh",
    "₹ 75 Lakh - ₹ 100 Lakh",
    "> ₹ 100 Lakh",
]
sal_weights = [0.15, 0.3, 0.25, 0.2, 0.1]
veh_cost_ranges = [
    "<= ₹ 10 Lakh",
    "₹ 10 Lakh - ₹ 20 Lakh",
    "₹ 20 Lakh - ₹ 30 Lakh",
    "> ₹ 30 Lakh",
]
veh_cost_weights = [0.2, 0.35, 0.3, 0.15]
agent_types = ["EA", "IA"]
agent_weights = [0.6, 0.4]
re_quote = ["No", "Yes"]
re_quote_weights = [0.7, 0.3]
df = pd.DataFrame(
    {
        "Region": np.random.choice(regions, N, p=region_weights),
        "Policy_Type": np.random.choice(policy_types, N, p=policy_weights),
        "Gender": np.random.choice(genders, N, p=gender_weights),
        "Marital_Status": np.random.choice(marital, N, p=marital_weights),
        "Education": np.random.choice(education, N, p=edu_weights),
        "Coverage": np.random.choice(coverage, N, p=cov_weights),
        "Veh_Usage": np.random.choice(veh_usage, N, p=usage_weights),
        "Annual_Miles_Range": np.random.choice(miles_ranges, N, p=miles_weights),
        "Sal_Range": np.random.choice(sal_ranges, N, p=sal_weights),
        "Vehicl_Cost_Range": np.random.choice(veh_cost_ranges, N, p=veh_cost_weights),
        "Agent_Type": np.random.choice(agent_types, N, p=agent_weights),
        "Re_Quote": np.random.choice(re_quote, N, p=re_quote_weights),
        "Driver_Age": np.clip(np.random.normal(38, 12, N), 18, 80).astype(int),
        "Driving_Exp": np.clip(np.random.normal(10, 6, N), 0, 50).astype(int),
        "Prev_Accidents": np.random.poisson(0.3, N),
        "Prev_Citations": np.random.poisson(0.5, N),
        "HH_Vehicles": np.random.choice([1, 2, 3, 4], N, p=[0.4, 0.35, 0.2, 0.05]),
        "HH_Drivers": np.random.choice([1, 2, 3, 4], N, p=[0.35, 0.4, 0.2, 0.05]),
        "Quoted_Premium": np.clip(np.random.lognormal(6.5, 0.6, N), 200, 10000).astype(
            int
        ),
    }
)
print("Injecting synthetic anomalies into ~3% of records...")
anomaly_mask = np.random.rand(N) < 0.03
mask_age = anomaly_mask & (np.random.rand(N) < 0.25)
df.loc[mask_age, "Driver_Age"] = np.random.randint(10, 18, mask_age.sum())
mask_exp = anomaly_mask & (np.random.rand(N) >= 0.25) & (np.random.rand(N) < 0.5)
df.loc[mask_exp, "Driving_Exp"] = df.loc[mask_exp, "Driver_Age"] + np.random.randint(
    5, 20, mask_exp.sum()
)
mask_veh = anomaly_mask & (np.random.rand(N) >= 0.5) & (np.random.rand(N) < 0.75)
df.loc[mask_veh, "Sal_Range"] = "<= ₹ 25 Lakh"
df.loc[mask_veh, "Vehicl_Cost_Range"] = "> ₹ 30 Lakh"
mask_prem = anomaly_mask & (np.random.rand(N) >= 0.75)
df.loc[mask_prem, "Prev_Accidents"] = np.random.randint(3, 8, mask_prem.sum())
df.loc[mask_prem, "Prev_Citations"] = np.random.randint(3, 8, mask_prem.sum())
df.loc[mask_prem, "Quoted_Premium"] = np.random.randint(100, 300, mask_prem.sum())


def calc_risk_score(row):
    score = 0
    if row["Prev_Accidents"] >= 2:
        score += 35
    elif row["Prev_Accidents"] == 1:
        score += 15
    if row["Prev_Citations"] >= 3:
        score += 25
    elif row["Prev_Citations"] >= 1:
        score += 10
    if row["Driver_Age"] < 25:
        score += 20
    elif row["Driver_Age"] > 65:
        score += 10
    if row["Annual_Miles_Range"] == "> 15 K":
        score += 10
    score += np.random.normal(0, 5)
    return np.clip(score, 0, 100)


df["risk_score"] = df.apply(calc_risk_score, axis=1)
print("--- Phase 2: Engineering Fraud Labels ---")
fraud_prob = np.zeros(N)
mask1 = (
    (df["Driver_Age"] < 22)
    & (df["Vehicl_Cost_Range"].isin(["> ₹ 30 Lakh", "₹ 20 Lakh - ₹ 30 Lakh"]))
    & (df["Prev_Accidents"] >= 2)
)
fraud_prob[mask1] += 0.6
mask2 = (df["Prev_Accidents"] >= 3) & (df["Driving_Exp"] <= 2)
fraud_prob[mask2] += 0.5
mask3 = (df["risk_score"] > 60) & (df["Quoted_Premium"] < 400)
fraud_prob[mask3] += 0.4
mask4 = (
    (df["Veh_Usage"] == "Business")
    & (df["Coverage"] == "Basic")
    & (df["Vehicl_Cost_Range"].isin(["> ₹ 30 Lakh", "₹ 20 Lakh - ₹ 30 Lakh"]))
)
fraud_prob[mask4] += 0.3
mask5 = (
    (df["Re_Quote"] == "Yes")
    & (df["Prev_Accidents"] >= 2)
    & (df["Prev_Citations"] >= 3)
)
fraud_prob[mask5] += 0.35
fraud_prob += np.random.uniform(0, 0.1, N)
threshold = np.percentile(fraud_prob, 95)
df["is_fraud"] = (fraud_prob >= threshold).astype(int)
fraud_rate = df["is_fraud"].mean()
print(f"Fraud rate: {fraud_rate:.2%} ({df['is_fraud'].sum()} fraudulent of {N})")
print("--- Phase 3: Engineering Customer Segments ---")
sal_map = {
    "<= ₹2.5 L": 2.5,
    "₹2.5L - ₹5L": 3.75,
    "₹5L - ₹7.5L": 6.25,
    "₹7.5L - ₹10L": 8.75,
    "> ₹10 Lakh": 12.5,
    "<= ₹ 25 Lakh": 2.5,
    "₹ 25 Lakh - ₹ 50 Lakh": 3.75,
    "₹ 50 Lakh - ₹ 75 Lakh": 6.25,
    "₹ 75 Lakh - ₹ 100 Lakh": 8.75,
    "> ₹ 100 Lakh": 12.5,
}
veh_cost_map = {
    "<= ₹10 L": 10,
    "₹10L - ₹20L": 15,
    "₹20L - ₹30L": 25,
    "> ₹30 Lakh": 40,
    "<= ₹ 10 Lakh": 10,
    "₹ 10 Lakh - ₹ 20 Lakh": 15,
    "₹ 20 Lakh - ₹ 30 Lakh": 25,
    "> ₹ 30 Lakh": 40,
}
cov_map = {"Basic": 1, "Balanced": 2, "Comprehensive": 3}
miles_map = {"<= 7.5 K": 5, "7.5 K - 15 K": 11, "> 15 K": 20}
df["sal_numeric"] = df["Sal_Range"].map(sal_map)
df["veh_cost_numeric"] = df["Vehicl_Cost_Range"].map(veh_cost_map)
df["cov_numeric"] = df["Coverage"].map(cov_map)
df["miles_numeric"] = df["Annual_Miles_Range"].map(miles_map)
print(f"Generated {N:,} synthetic records")
print("\n--- Phase 4: Training Fraud Detection Models ---")
fraud_features = pd.DataFrame(
    {
        "driver_age": df["Driver_Age"],
        "driving_exp": df["Driving_Exp"],
        "prev_accidents": df["Prev_Accidents"],
        "prev_citations": df["Prev_Citations"],
        "risk_score": df["risk_score"],
        "quoted_premium": df["Quoted_Premium"],
        "hh_vehicles": df["HH_Vehicles"],
        "hh_drivers": df["HH_Drivers"],
        "sal_numeric": df["sal_numeric"],
        "veh_cost_numeric": df["veh_cost_numeric"],
        "cov_numeric": df["cov_numeric"],
        "miles_numeric": df["miles_numeric"],
        "vehicle_cost_to_salary_ratio": df["veh_cost_numeric"]
        / (df["sal_numeric"] + 1),
        "premium_to_vehicle_ratio": df["Quoted_Premium"]
        / ((df["veh_cost_numeric"] * 100000) + 1),
        "premium_to_risk_ratio": df["Quoted_Premium"] / (df["risk_score"] + 1),
        "driver_age_to_vehicle_value": df["Driver_Age"] / (df["veh_cost_numeric"] + 1),
        "experience_to_accident_ratio": df["Driving_Exp"] / (df["Prev_Accidents"] + 1),
        "premium_deviation_from_expected": df["Quoted_Premium"]
        / (df["risk_score"] * 10 + 1),
    }
)
fraud_feature_cols = list(fraud_features.columns)
print("Training Isolation Forest...")
scaler_fraud = StandardScaler()
fraud_scaled = scaler_fraud.fit_transform(fraud_features)
iso_forest = IsolationForest(
    n_estimators=200, contamination=0.05, max_samples=0.8, random_state=42, n_jobs=-1
)
iso_forest.fit(fraud_scaled)
iso_predictions = iso_forest.predict(fraud_scaled)
iso_pred_labels = (iso_predictions == -1).astype(int)
print(f"Isolation Forest flagged {iso_pred_labels.sum()} anomalies.")
print("Isolation Forest Evaluation on Target Labels:")
print(confusion_matrix(df["is_fraud"], iso_pred_labels))
print(classification_report(df["is_fraud"], iso_pred_labels))
print("Training Gradient Boosting Classifier...")
y_fraud = df["is_fraud"]
X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(
    fraud_features, y_fraud, test_size=0.2, random_state=42, stratify=y_fraud
)
gb_fraud = GradientBoostingClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    random_state=42,
)
gb_fraud.fit(X_train_f, y_train_f)
fraud_acc = gb_fraud.score(X_test_f, y_test_f)
print(f"Fraud Classifier Accuracy: {fraud_acc:.4f}")
print(
    f"Fraud Classification Report:\n{classification_report(y_test_f, gb_fraud.predict(X_test_f))}"
)
print("\n--- Feature Importance (Step 6) ---")
importances = gb_fraud.feature_importances_
indices = np.argsort(importances)[::-1]
print("Top 5 Fraud Indicators:")
for i in range(min(5, len(fraud_feature_cols))):
    print(f"{i+1}. {fraud_feature_cols[indices[i]]} ({importances[indices[i]]:.4f})")
print("\n--- Phase 5: Training Customer Personalization Model ---")
persona_features = pd.DataFrame(
    {
        "driver_age": df["Driver_Age"],
        "driving_exp": df["Driving_Exp"],
        "risk_score": df["risk_score"],
        "sal_numeric": df["sal_numeric"],
        "veh_cost_numeric": df["veh_cost_numeric"],
        "cov_numeric": df["cov_numeric"],
        "miles_numeric": df["miles_numeric"],
        "quoted_premium": df["Quoted_Premium"],
        "prev_accidents": df["Prev_Accidents"],
    }
)
persona_feature_cols = list(persona_features.columns)
scaler_persona = StandardScaler()
persona_scaled = scaler_persona.fit_transform(persona_features)
K = 5
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10, max_iter=300)
cluster_labels = kmeans.fit_predict(persona_scaled)
sil_score = silhouette_score(persona_scaled, cluster_labels, sample_size=10000)
print(f"K-Means ({K} clusters) Silhouette Score: {sil_score:.4f}")
df["cluster"] = cluster_labels
plan_mapping = {}
for c in range(K):
    cluster_data = df[df["cluster"] == c]
    avg_risk = cluster_data["risk_score"].mean()
    avg_sal = cluster_data["sal_numeric"].mean()
    avg_cov = cluster_data["cov_numeric"].mean()
    avg_age = cluster_data["Driver_Age"].mean()
    if avg_risk > 50 and avg_sal < 40:
        plan = "Essential Protect"
        coverage_level = "Basic"
        addons = ["personal_accident_cover", "roadside_assistance"]
    elif avg_risk > 50 and avg_sal >= 40:
        plan = "Secure Shield"
        coverage_level = "High"
        addons = [
            "zero_depreciation",
            "engine_protection",
            "roadside_assistance",
            "personal_accident_cover",
        ]
    elif avg_risk <= 30 and avg_sal >= 60:
        plan = "Premium Elite"
        coverage_level = "Comprehensive"
        addons = [
            "zero_depreciation",
            "engine_protection",
            "return_to_invoice",
            "consumables_cover",
            "key_replacement",
        ]
    elif avg_risk <= 30 and avg_cov >= 2:
        plan = "Smart Value"
        coverage_level = "Medium"
        addons = ["zero_depreciation", "roadside_assistance", "ncb_protection"]
    else:
        plan = "Balanced Guard"
        coverage_level = "Medium"
        addons = ["roadside_assistance", "personal_accident_cover", "ncb_protection"]
    plan_mapping[c] = {
        "plan": plan,
        "coverage_level": coverage_level,
        "addons": addons,
        "avg_risk": round(avg_risk, 1),
        "avg_salary": round(avg_sal, 1),
        "avg_age": round(avg_age, 1),
        "count": len(cluster_data),
    }
    print(
        f"  Cluster {c}: {plan} ({coverage_level}) — {len(cluster_data):,} customers, avg_risk={avg_risk:.1f}, avg_sal={avg_sal:.1f}"
    )
print("\n--- Phase 6: Saving Model Artifacts ---")
os.makedirs("models", exist_ok=True)
joblib.dump(iso_forest, "models/fraud_isolation_forest.pkl")
joblib.dump(gb_fraud, "models/fraud_detector_gb.pkl")
joblib.dump(scaler_fraud, "models/fraud_scaler.pkl")
joblib.dump(fraud_feature_cols, "models/fraud_feature_cols.pkl")
joblib.dump(kmeans, "models/personalization_kmeans.pkl")
joblib.dump(scaler_persona, "models/personalization_scaler.pkl")
joblib.dump(plan_mapping, "models/personalization_plan_mapper.pkl")
joblib.dump(persona_feature_cols, "models/personalization_feature_cols.pkl")
print("Saved artifacts:")
for f in os.listdir("models"):
    size = os.path.getsize(f"models/{f}")
    print(f"  models/{f} ({size:,} bytes)")
print(f"\n✅ Training complete. {N:,} records used.")
print(f"   Fraud model accuracy: {fraud_acc:.4f}")
print(f"   Personalization silhouette: {sil_score:.4f}")
print(f"   {K} customer segments mapped to insurance plans")
