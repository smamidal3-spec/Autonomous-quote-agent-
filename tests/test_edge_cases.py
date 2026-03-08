import os
import pytest
from pprint import pprint
from agents.pipeline import MultiAgentPipeline
from agents.schema import QuoteInput

try:
    pipeline = MultiAgentPipeline(models_dir="models")
except Exception as e:
    pipeline = None


def run_test(name, payload, expected_fraud_flag=True, expected_rule_flag=False):
    assert pipeline is not None, "Pipeline failed to load"
    quote = QuoteInput(**payload)
    result = pipeline.execute(quote)
    is_flagged = False
    has_rules = False
    if result.fraud_detection:
        is_flagged = result.fraud_detection.fraud_flag
        has_rules = len(result.fraud_detection.rule_flags) > 0
    assert (
        is_flagged == expected_fraud_flag
    ), f"{name}: Expected fraud_flag={expected_fraud_flag}, got {is_flagged}"
    assert (
        has_rules == expected_rule_flag
    ), f"{name}: Expected rule_flags presence={expected_rule_flag}, got {has_rules}"


def test_api_edge_cases():
    base_payload = {
        "Agent_Type": "EA",
        "Q_Creation_DT": "2023/10/01",
        "Q_Valid_DT": "2023/12/31",
        "Policy_Bind_DT": "2023/10/02",
        "Region": "A",
        "Agent_Num": 10,
        "Policy_Type": "Truck",
        "HH_Vehicles": 1,
        "HH_Drivers": 1,
        "Driver_Age": 30.0,
        "Driving_Exp": 5,
        "Prev_Accidents": 0,
        "Prev_Citations": 0,
        "Gender": "Male",
        "Marital_Status": "Married",
        "Education": "Bachelors",
        "Sal_Range": "> ₹ 25 Lakh <= ₹ 40 Lakh",
        "Coverage": "Balanced",
        "Veh_Usage": "Business",
        "Annual_Miles_Range": "<= 7.5 K",
        "Vehicl_Cost_Range": "> ₹ 10 Lakh <= ₹ 20 Lakh",
        "Re_Quote": "No",
        "Quoted_Premium": 1000,
    }
    p1 = base_payload.copy()
    p1["Driver_Age"] = 10
    p1["Driving_Exp"] = 0
    run_test("10-Year-Old Driver", p1, expected_fraud_flag=True)
    p2 = base_payload.copy()
    p2["Driver_Age"] = 20
    p2["Driving_Exp"] = 2
    p2["Vehicl_Cost_Range"] = "> ₹ 40 Lakh "
    p2["Sal_Range"] = "<= ₹ 25 Lakh"
    run_test(
        "20-Year-Old Buying ₹50 Lakh Car on Low Salary",
        p2,
        expected_fraud_flag=False,
        expected_rule_flag=True,
    )
    p3 = base_payload.copy()
    p3["Driver_Age"] = 35
    p3["Driving_Exp"] = 0
    p3["Prev_Accidents"] = 5
    run_test("0 Experience, Many Accidents", p3, expected_fraud_flag=True)
    p4 = base_payload.copy()
    p4["Driver_Age"] = 20
    p4["Prev_Accidents"] = 4
    p4["Prev_Citations"] = 4
    p4["Quoted_Premium"] = 150
    run_test("Premium Extremely Low For High Risk", p4, expected_fraud_flag=True)
    run_test(
        "Normal Clean Driver",
        base_payload,
        expected_fraud_flag=False,
        expected_rule_flag=False,
    )
