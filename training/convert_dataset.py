import pandas as pd
import os

df = pd.read_csv("data/use_case_03/USE CASE - 03/Autonomous QUOTE AGENTS.csv")


def convert_amount(val):
    if not isinstance(val, str):
        return val
    val = val.replace("$", "₹")
    val = val.replace(" K", " Lakh")
    return val


df["Sal_Range"] = df["Sal_Range"].apply(convert_amount)
df["Vehicl_Cost_Range"] = df["Vehicl_Cost_Range"].apply(convert_amount)
df["Quoted_Premium"] = (df["Quoted_Premium"] * 83).astype(int)
df.to_csv("data/use_case_03/USE CASE - 03/Autonomous QUOTE AGENTS_INR.csv", index=False)
print("Converted to Autonomous QUOTE AGENTS_INR.csv")
