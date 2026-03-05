import streamlit as st
import pandas as pd
import joblib
import os
import shap
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="Autonomous Quote Agents", layout="wide", page_icon="🤖")
st.title("🛡️ Autonomous Quote Agents Pipeline")
st.markdown("Processing Insurance Quotes automatically using a 4-Agent Pipeline.")


@st.cache_resource
def load_assets():
    try:
        rf = joblib.load("models/risk_profiler_rf.pkl")
        xgb = joblib.load("models/conversion_predictor_xgb.pkl")
        encoders = joblib.load("models/categorical_encoders.pkl")
        risk_encoder = joblib.load("models/risk_encoder.pkl")
        feature_cols = joblib.load("models/feature_columns.pkl")
        return rf, xgb, encoders, risk_encoder, feature_cols
    except Exception as e:
        return None, None, None, None, None


rf_model, xgb_model, encoders, risk_encoder, feature_cols = load_assets()
if not rf_model:
    st.error("Models not found! Please run the training script first.")
    st.stop()
st.sidebar.header("Input New Quote Data")
user_input = {}
for col in feature_cols:
    if col in encoders:
        options = list(encoders[col].classes_)
        user_input[col] = st.sidebar.selectbox(f"{col}", options)
    else:
        user_input[col] = st.sidebar.number_input(f"{col}", value=0.0)
quoted_premium = st.sidebar.number_input("Proposed Premium ($)", value=1000.0)
if st.sidebar.button("Run Quote Pipeline 🚀"):
    st.markdown("---")
    input_df = pd.DataFrame([user_input])
    for col in input_df.columns:
        if col in encoders:
            input_df[col] = input_df[col].astype(str)
            try:
                input_df[col] = encoders[col].transform(input_df[col])
            except ValueError:
                input_df[col] = 0
    st.subheader("🕵️ Agent 1: Risk Profiler")
    risk_prediction = rf_model.predict(input_df)[0]
    st.info(f"**Predicted Risk Tier:** {risk_prediction}")
    with st.expander("Show Risk Profiler Reasoning (SHAP)"):
        explainer = shap.TreeExplainer(rf_model)
        shap_values = explainer.shap_values(input_df)
        fig, ax = plt.subplots(figsize=(8, 3))
        if isinstance(shap_values, list):
            sv = shap_values[1][0]
        else:
            sv = shap_values[0]
        shap.bar_plot(sv, feature_names=input_df.columns, show=False)
        st.pyplot(fig)
    st.markdown("---")
    st.subheader("📊 Agent 2: Conversion Predictor")
    input_df_conv = input_df.copy()
    try:
        encoded_risk = risk_encoder.transform([risk_prediction])[0]
    except:
        encoded_risk = 0
    input_df_conv["Risk_Tier"] = encoded_risk
    prob = xgb_model.predict_proba(input_df_conv)[0][1] * 100
    st.metric(label="Likelihood to Bind Policy", value=f"{prob:.1f}%")
    st.markdown("---")
    st.subheader("💰 Agent 3: Premium Advisor")
    recommended_premium = quoted_premium
    advice = "Premium is competitive."
    if prob < 40 and risk_prediction != "High":
        recommended_premium = quoted_premium * 0.90
        advice = "Conversion probability is low for an acceptable risk profile. Suggesting a 10% premium reduction to incentivize binding."
    elif risk_prediction == "High":
        recommended_premium = quoted_premium * 1.25
        advice = "High Risk tier detected. Mandating 25% premium surcharge to offset potential claims."
    st.success(f"**Recommended Action:** {advice}")
    st.write(f"**Suggested Adjusted Premium:** ${recommended_premium:,.2f}")
    st.markdown("---")
    st.subheader("🚦 Agent 4: Decision Router")
    final_decision = "UNKNOWN"
    reason = "UNKNOWN"
    if risk_prediction == "Low" and prob > 70:
        final_decision = "✅ AUTO APPROVE"
        reason = "Low risk profile and high probability of binding."
    elif risk_prediction == "High" or prob < 20:
        final_decision = "🚨 ESCALATE TO HUMAN UNDERWRITER"
        reason = "Outside acceptable autonomous bounds (Risk too high, or likelihood to convert too low)."
    else:
        final_decision = "📞 AGENT FOLLOW-UP"
        reason = (
            "Borderline case. Agent should contact customer with the adjusted premium."
        )
    st.markdown(f"### Ultimate Route: {final_decision}")
    st.write(f"**Routing Logic:** {reason}")
