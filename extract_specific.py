import pandas as pd
import json

df = pd.read_csv("data/use_case_03/USE CASE - 03/Autonomous QUOTE AGENTS.csv")
keys = [
    "Gender",
    "Marital_Status",
    "Education",
    "Sal_Range",
    "Coverage",
    "Veh_Usage",
    "Annual_Miles_Range",
    "Vehicl_Cost_Range",
    "Re_Quote",
    "Policy_Type",
    "Agent_Type",
]
res = {c: df[c].dropna().unique().tolist() for c in keys if c in df.columns}
with open("specific_categories.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
