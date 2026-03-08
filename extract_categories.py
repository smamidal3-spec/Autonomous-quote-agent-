import pandas as pd
import json

df = pd.read_csv("data/use_case_03/USE CASE - 03/Autonomous QUOTE AGENTS.csv")
cat_cols = df.select_dtypes(include="object").columns
res = {
    c: df[c].dropna().unique().tolist()
    for c in cat_cols
    if c not in ["Quote_Num", "Policy_Bind"]
}
with open("categories.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("Categories saved to categories.json")
