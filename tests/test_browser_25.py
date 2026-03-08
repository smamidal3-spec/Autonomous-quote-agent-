import json
import urllib.parse
from playwright.sync_api import sync_playwright
import pytest


def test_ui_profiles_end_to_end():
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_up = sock.connect_ex(("127.0.0.1", 8501)) == 0
    sock.close()
    if not is_up:
        pytest.skip("Streamlit dashboard is not running on port 8501")
    with open("tests/synthetic_data.json", "r") as f:
        profiles = json.load(f)
    print(f"\n🌐 Starting Automated Browser UI Tests for {len(profiles)} Profiles...\n")
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for i, profile in enumerate(profiles):
            name = profile["Profile_Name"]
            params = {
                "Prev_Accidents": profile["Prev_Accidents"],
                "Prev_Citations": profile["Prev_Citations"],
                "Driving_Exp": profile["Driving_Exp"],
                "Driver_Age": profile["Driver_Age"],
                "Veh_Usage": profile["Veh_Usage"],
                "Annual_Miles_Range": profile["Annual_Miles_Range"],
                "Q_Valid_DT": profile["Q_Valid_DT"],
                "Coverage": profile["Coverage"],
                "Agent_Type": profile["Agent_Type"],
                "Region": profile["Region"],
                "Sal_Range": profile["Sal_Range"],
                "HH_Drivers": profile["HH_Drivers"],
                "Re_Quote": profile["Re_Quote"],
                "Vehicl_Cost_Range": profile["Vehicl_Cost_Range"],
                "Quoted_Premium": profile["Quoted_Premium"],
            }
            query_string = urllib.parse.urlencode(params)
            url = f"http://localhost:8501/?{query_string}"
            page.goto(url)
            run_btn = page.locator("button:has-text('Calculate The Risk 🔍')")
            run_btn.wait_for(state="visible", timeout=10000)
            run_btn.click()
            page.locator("text=Quote ID:").wait_for(state="visible", timeout=15000)
            raw_div = page.locator("#raw-testing-json")
            raw_div.wait_for(state="attached", timeout=15000)
            json_str = raw_div.inner_text()
            try:
                res = json.loads(json_str)
                decision = res["final_decision"]["decision"]
                tier = res["risk_evaluation"]["risk_tier"]
                prem = res["premium_advice"]["premium_issue"]
                esc = res["escalation_status"]["escalation_required"]
                is_accurate = False
                if "Low_Risk" in name:
                    if esc == False and tier in ["LOW", "MEDIUM"]:
                        is_accurate = True
                elif "High_Risk" in name:
                    if tier == "HIGH" and decision == "ESCALATE_TO_UNDERWRITER":
                        is_accurate = True
                elif "Medium_Risk" in name:
                    if tier in ["MEDIUM", "HIGH"]:
                        is_accurate = True
                elif "Premium_Sensitive" in name:
                    if prem == True:
                        is_accurate = True
                elif "Escalation_Guarantee" in name:
                    if esc == True:
                        is_accurate = True
            except Exception as e:
                is_accurate = False
                tier = "PARSE_ERROR"
                decision = str(e)
            if not is_accurate:
                failures.append(
                    f"{name}: Failed UI assertion. Tier={tier}, Decision={decision}"
                )
        browser.close()
    assert len(failures) == 0, f"UI Tests Failed: {failures}"
