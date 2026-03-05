import streamlit as st
import requests
import json
import joblib

st.set_page_config(
    page_title="Strict Quote Agents Pipeline", layout="wide", page_icon="🤖"
)
st.title("🛡️ Strict 6-Agent Autonomous Pipeline")
st.markdown("Hitting the **FastAPI Backend** and processing JSON structured outputs.")
try:
    feature_cols = joblib.load("models/feature_columns.pkl")
    encoders = joblib.load("models/categorical_encoders.pkl")
except:
    st.error("Could not load model features. Please run training script first.")
    st.stop()
st.sidebar.header("Input New Quote Data")
user_input = {}
query_params = st.query_params


def get_param(key, default, cast_fn):
    val = query_params.get(key, default)
    try:
        return cast_fn(val)
    except:
        return default


def get_selectbox_index(key, options_list):
    """Get the index for a selectbox from URL params."""
    val = get_param(key, "", str)
    opts = list(options_list)
    if val in opts:
        return opts.index(val)
    return 0


user_input["Agent_Num"] = int(
    st.sidebar.number_input(
        "Agent Number", value=get_param("Agent_Num", 10, int), step=1, format="%d"
    )
)
user_input["HH_Vehicles"] = int(
    st.sidebar.number_input(
        "Household Vehicles",
        value=get_param("HH_Vehicles", 1, int),
        step=1,
        format="%d",
    )
)
user_input["HH_Drivers"] = int(
    st.sidebar.number_input(
        "Household Drivers", value=get_param("HH_Drivers", 1, int), step=1, format="%d"
    )
)
user_input["Driver_Age"] = int(
    st.sidebar.number_input(
        "Driver Age", value=get_param("Driver_Age", 30, int), step=1, format="%d"
    )
)
user_input["Driving_Exp"] = int(
    st.sidebar.number_input(
        "Driving Experience (Years)",
        value=get_param("Driving_Exp", 5, int),
        step=1,
        format="%d",
    )
)
user_input["Prev_Accidents"] = int(
    st.sidebar.number_input(
        "Previous Accidents",
        value=get_param("Prev_Accidents", 0, int),
        step=1,
        format="%d",
    )
)
user_input["Prev_Citations"] = int(
    st.sidebar.number_input(
        "Previous Citations",
        value=get_param("Prev_Citations", 0, int),
        step=1,
        format="%d",
    )
)
user_input["Quoted_Premium"] = int(
    st.sidebar.number_input(
        "Quoted Premium ($)",
        value=get_param("Quoted_Premium", 1000, int),
        step=50,
        format="%d",
    )
)
user_input["Q_Creation_DT"] = st.sidebar.text_input(
    "Quote Creation Date", value=get_param("Q_Creation_DT", "2019/10/01", str)
)
user_input["Q_Valid_DT"] = st.sidebar.text_input(
    "Quote Valid Until Date", value=get_param("Q_Valid_DT", "2023/12/31", str)
)
user_input["Policy_Bind_DT"] = st.sidebar.text_input(
    "Policy Bind Date", value=get_param("Policy_Bind_DT", "2019/10/02", str)
)
agent_display_map = {
    "EA": "Exclusive Agent",
    "IA": "Independent Agent",
}
agent_codes = (
    list(encoders["Agent_Type"].classes_) if "Agent_Type" in encoders else ["EA", "IA"]
)
agent_display = [agent_display_map.get(a, a) for a in agent_codes]
selected_agent_display = st.sidebar.selectbox(
    "Agent Type", agent_display, index=get_selectbox_index("Agent_Type", agent_codes)
)
user_input["Agent_Type"] = agent_codes[agent_display.index(selected_agent_display)]
region_display_map = {
    "A": "Zone A — High Accident",
    "B": "Zone B — Moderate Accident",
    "C": "Zone C — Low Accident",
    "D": "Zone D — Urban High Risk",
    "E": "Zone E — Suburban Moderate",
    "F": "Zone F — Rural Low Risk",
    "G": "Zone G — Highway Corridor",
    "H": "Zone H — Industrial Zone",
}
region_codes = (
    list(encoders["Region"].classes_)
    if "Region" in encoders
    else ["A", "B", "C", "D", "E", "F", "G", "H"]
)
region_display = [region_display_map.get(r, r) for r in region_codes]
selected_region_display = st.sidebar.selectbox(
    "Region / Zone", region_display, index=get_selectbox_index("Region", region_codes)
)
user_input["Region"] = region_codes[region_display.index(selected_region_display)]
policy_opts = (
    list(encoders["Policy_Type"].classes_)
    if "Policy_Type" in encoders
    else ["Truck", "Sedan"]
)
user_input["Policy_Type"] = st.sidebar.selectbox(
    "Policy Type", policy_opts, index=get_selectbox_index("Policy_Type", policy_opts)
)
gender_opts = (
    list(encoders["Gender"].classes_) if "Gender" in encoders else ["Male", "Female"]
)
user_input["Gender"] = st.sidebar.selectbox(
    "Gender", gender_opts, index=get_selectbox_index("Gender", gender_opts)
)
marital_opts = (
    list(encoders["Marital_Status"].classes_)
    if "Marital_Status" in encoders
    else ["Married", "Single"]
)
user_input["Marital_Status"] = st.sidebar.selectbox(
    "Marital Status",
    marital_opts,
    index=get_selectbox_index("Marital_Status", marital_opts),
)
edu_opts = (
    list(encoders["Education"].classes_)
    if "Education" in encoders
    else ["Bachelors", "Masters"]
)
user_input["Education"] = st.sidebar.selectbox(
    "Education Level", edu_opts, index=get_selectbox_index("Education", edu_opts)
)
sal_opts = (
    list(encoders["Sal_Range"].classes_)
    if "Sal_Range" in encoders
    else ["<= $ 25 K", "50 K - 75 K"]
)
user_input["Sal_Range"] = st.sidebar.selectbox(
    "Salary Range", sal_opts, index=get_selectbox_index("Sal_Range", sal_opts)
)
cov_opts = (
    list(encoders["Coverage"].classes_)
    if "Coverage" in encoders
    else ["Basic", "Balanced", "Comprehensive"]
)
user_input["Coverage"] = st.sidebar.selectbox(
    "Coverage Type", cov_opts, index=get_selectbox_index("Coverage", cov_opts)
)
veh_opts = (
    list(encoders["Veh_Usage"].classes_)
    if "Veh_Usage" in encoders
    else ["Pleasure", "Business"]
)
user_input["Veh_Usage"] = st.sidebar.selectbox(
    "Vehicle Usage", veh_opts, index=get_selectbox_index("Veh_Usage", veh_opts)
)
miles_opts = (
    list(encoders["Annual_Miles_Range"].classes_)
    if "Annual_Miles_Range" in encoders
    else ["<= 7.5 K", "> 15 K"]
)
user_input["Annual_Miles_Range"] = st.sidebar.selectbox(
    "Annual Miles Range",
    miles_opts,
    index=get_selectbox_index("Annual_Miles_Range", miles_opts),
)
vcost_opts = (
    list(encoders["Vehicl_Cost_Range"].classes_)
    if "Vehicl_Cost_Range" in encoders
    else ["10 K - 20 K"]
)
user_input["Vehicl_Cost_Range"] = st.sidebar.selectbox(
    "Vehicle Cost Range",
    vcost_opts,
    index=get_selectbox_index("Vehicl_Cost_Range", vcost_opts),
)
user_input["Re_Quote"] = st.sidebar.selectbox(
    "Re-Quote", ["No", "Yes"], index=get_selectbox_index("Re_Quote", ["No", "Yes"])
)
API_URL = "http://127.0.0.1:8000/api/v1/evaluate_quote"
if st.sidebar.button("Calculate The Risk 🔍"):
    st.markdown("---")
    with st.spinner("Calling API..."):
        try:
            response = requests.post(API_URL, json=user_input)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to reach FastAPI Backend: {e}")
            st.stop()
    st.write(f"**Quote ID:** `{data['quote_id']}`")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🕵️ Agent 1: Risk Profiler")
        st.json(data["risk_evaluation"])
        st.subheader("🛡️ Agent 2: Fraud Detection")
        if data.get("fraud_detection"):
            st.json(data["fraud_detection"])
        else:
            st.info("Fraud detection bypassed or unavailable.")
        st.subheader("💰 Agent 5: Premium Advisor")
        st.json(data["premium_advice"])
    with col2:
        st.subheader("📊 Agent 3: Conversion Predictor")
        st.json(data["conversion_prediction"])
        st.subheader("✨ Agent 4: Personalization Engine")
        if data.get("personalization"):
            st.json(data["personalization"])
        else:
            st.info("Personalization bypassed or unavailable.")
        st.subheader("🚦 Agent 6: Decision Router")
        final_d = data["final_decision"]
        if final_d["decision"] == "AUTO_APPROVE":
            st.success(f"**Decision:** {final_d['decision']}")
        elif final_d["decision"] == "ESCALATE_TO_UNDERWRITER":
            st.error(f"**Decision:** {final_d['decision']}")
        else:
            st.warning(f"**Decision:** {final_d['decision']}")
        st.json(data["final_decision"])
        if data["escalation_status"]["escalation_required"]:
            st.error(
                f"🚨 HUMAN ESCALATION REQUIRED: {data['escalation_status']['reason']}"
            )
        st.markdown(
            f"<div id='raw-testing-json' style='display:none;'>{json.dumps(data)}</div>",
            unsafe_allow_html=True,
        )
