import requests
import json
import pandas as pd
from typing import List, Dict, Any

API_URL = "http://localhost:8000/api/v1/evaluate_quote"


def generate_test_cases() -> List[Dict[str, Any]]:
    cases = []
    for i in range(10):
        cases.append(
            {
                "quote_type": "obvious_fraud",
                "expected_fraud": True,
                "data": {
                    "Driver_Age": 19,
                    "Prev_Accidents": 3,
                    "Prev_Citations": 4,
                    "Driving_Exp": 0,
                    "Vehicl_Cost_Range": "> ₹ 30 Lakh",
                    "Quoted_Premium": 200,
                    "Annual_Miles_Range": "> 15 K",
                    "Re_Quote": "Yes",
                },
            }
        )
    for i in range(10):
        cases.append(
            {
                "quote_type": "genuine_safe_driver",
                "expected_fraud": False,
                "data": {
                    "Driver_Age": 45,
                    "Prev_Accidents": 0,
                    "Prev_Citations": 0,
                    "Driving_Exp": 25,
                    "Vehicl_Cost_Range": "₹ 10 Lakh - ₹ 20 Lakh",
                    "Quoted_Premium": 800,
                    "Annual_Miles_Range": "<= 7.5 K",
                    "Re_Quote": "No",
                    "Coverage": "Comprehensive",
                },
            }
        )
    for i in range(10):
        cases.append(
            {
                "quote_type": "genuine_1_accident",
                "expected_fraud": False,
                "data": {
                    "Driver_Age": 50,
                    "Prev_Accidents": 1,
                    "Prev_Citations": 0,
                    "Driving_Exp": 30,
                    "Vehicl_Cost_Range": "₹ 20 Lakh - ₹ 30 Lakh",
                    "Quoted_Premium": 1200,
                    "Annual_Miles_Range": "7.5 K - 15 K",
                    "Re_Quote": "No",
                },
            }
        )
    for i in range(10):
        cases.append(
            {
                "quote_type": "genuine_young_adult",
                "expected_fraud": False,
                "data": {
                    "Driver_Age": 24,
                    "Prev_Accidents": 0,
                    "Prev_Citations": 1,
                    "Driving_Exp": 2,
                    "Vehicl_Cost_Range": "<= ₹ 10 Lakh",
                    "Quoted_Premium": 1500,
                    "Annual_Miles_Range": "7.5 K - 15 K",
                    "Re_Quote": "No",
                },
            }
        )
    for i in range(10):
        cases.append(
            {
                "quote_type": "genuine_expensive_car",
                "expected_fraud": False,
                "data": {
                    "Driver_Age": 60,
                    "Prev_Accidents": 0,
                    "Prev_Citations": 0,
                    "Driving_Exp": 40,
                    "Vehicl_Cost_Range": "> ₹ 30 Lakh",
                    "Quoted_Premium": 3000,
                    "Annual_Miles_Range": "<= 7.5 K",
                    "Re_Quote": "No",
                    "Sal_Range": "> ₹ 100 Lakh",
                },
            }
        )
    return cases


default_quote = {
    "Agent_Type": "EA",
    "Q_Creation_DT": "2023/10/01",
    "Q_Valid_DT": "2023/12/31",
    "Policy_Bind_DT": "2023/10/02",
    "Region": "A",
    "Agent_Num": 10,
    "Policy_Type": "Car",
    "HH_Vehicles": 1,
    "HH_Drivers": 1,
    "Driver_Age": 30,
    "Driving_Exp": 10,
    "Prev_Accidents": 0,
    "Prev_Citations": 0,
    "Gender": "Male",
    "Marital_Status": "Married",
    "Education": "Bachelors",
    "Sal_Range": "₹ 50 Lakh - ₹ 75 Lakh",
    "Coverage": "Balanced",
    "Veh_Usage": "Pleasure",
    "Annual_Miles_Range": "<= 7.5 K",
    "Vehicl_Cost_Range": "₹ 10 Lakh - ₹ 20 Lakh",
    "Re_Quote": "No",
    "Quoted_Premium": 1000,
}


def evaluate():
    test_cases = generate_test_cases()
    results = []
    print(f"Running evaluation on {len(test_cases)} cases...")
    for i, tc in enumerate(test_cases):
        payload = {**default_quote, **tc["data"]}
        try:
            resp = requests.post(API_URL, json=payload)
            resp.raise_for_status()
            out = resp.json()
            fraud = out.get("fraud_detection", {})
            risk = out.get("risk_evaluation", {})
            results.append(
                {
                    "case_id": i + 1,
                    "category": tc["quote_type"],
                    "expected_fraud": tc["expected_fraud"],
                    "flagged": fraud.get("fraud_flag", False),
                    "fraud_score": fraud.get("fraud_risk_score", 0),
                    "risk_tier": risk.get("risk_tier", "UNKNOWN"),
                    "decision": out["final_decision"]["decision"],
                }
            )
        except Exception as e:
            print(f"Error on case {i+1}: {e}")
    df = pd.DataFrame(results)
    print("\n================== FRAUD DETECTOR EVALUATION ==================")
    print(f"Total Cases: {len(df)}")
    print(f"Total Flagged as Fraud: {df['flagged'].sum()} / {len(df)}")
    print("\n--- Breakdown by Category ---")
    summary = (
        df.groupby("category")
        .agg(
            Count=("case_id", "count"),
            Avg_Fraud_Score=("fraud_score", "mean"),
            Flagged_Count=("flagged", "sum"),
            Max_Fraud_Score=("fraud_score", "max"),
        )
        .reset_index()
    )
    false_positives = df[(df["expected_fraud"] == False) & (df["flagged"] == True)]
    true_negatives = df[(df["expected_fraud"] == False) & (df["flagged"] == False)]
    true_positives = df[(df["expected_fraud"] == True) & (df["flagged"] == True)]
    false_negatives = df[(df["expected_fraud"] == True) & (df["flagged"] == False)]
    total_genuine = len(df[df["expected_fraud"] == False])
    total_fraud = len(df[df["expected_fraud"] == True])
    print(summary.to_string(index=False))
    print("\n--- Accuracy Metrics ---")
    print(f"Genuine Cases: {total_genuine}")
    print(f"  [OK] Correctly flagged as Clear (True Negative): {len(true_negatives)}")
    print(
        f"  [FAIL] Incorrectly flagged as Fraud (False Positive): {len(false_positives)}"
    )
    print(f"  False Positive Rate: {len(false_positives) / total_genuine * 100:.1f}%")
    print(f"\nFraudulent Cases: {total_fraud}")
    print(f"  [OK] Correctly flagged as Fraud (True Positive): {len(true_positives)}")
    print(f"  [FAIL] Failed to catch fraud (False Negative): {len(false_negatives)}")
    print(
        "\nIf the False Positive Rate on genuine cases is high, we will need to tune the threshold or adjust the feature weights in the retraining."
    )


if __name__ == "__main__":
    evaluate()
