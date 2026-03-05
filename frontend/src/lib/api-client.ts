import { QuoteInput, PipelineOutput } from "./types";
const API_BASE = "";
export async function evaluateQuote(
  input: QuoteInput,
): Promise<PipelineOutput> {
  const response = await fetch(`${API_BASE}/api/v1/evaluate_quote`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}
export function getDefaultQuoteInput(): QuoteInput {
  return {
    Agent_Type: "EA",
    Q_Creation_DT: "2019/10/01",
    Q_Valid_DT: "2023/12/31",
    Policy_Bind_DT: "2019/10/02",
    Region: "A",
    Agent_Num: 10,
    Policy_Type: "Truck",
    HH_Vehicles: 1,
    HH_Drivers: 1,
    Driver_Age: 30,
    Driving_Exp: 5,
    Prev_Accidents: 0,
    Prev_Citations: 0,
    Gender: "Male",
    Marital_Status: "Married",
    Education: "Bachelors",
    Sal_Range: "> ₹ 25 Lakh <= ₹ 40 Lakh",
    Coverage: "Balanced",
    Veh_Usage: "Business",
    Annual_Miles_Range: "<= 7.5 K",
    Vehicl_Cost_Range: "> ₹ 10 Lakh <= ₹ 20 Lakh",
    Re_Quote: "No",
    Quoted_Premium: 1000,
  };
}
