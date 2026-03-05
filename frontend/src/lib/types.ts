export interface QuoteInput {
  Agent_Type: string;
  Q_Creation_DT: string;
  Q_Valid_DT: string;
  Policy_Bind_DT: string;
  Region: string;
  Agent_Num: number;
  Policy_Type: string;
  HH_Vehicles: number;
  HH_Drivers: number;
  Driver_Age: number;
  Driving_Exp: number;
  Prev_Accidents: number;
  Prev_Citations: number;
  Gender: string;
  Marital_Status: string;
  Education: string;
  Sal_Range: string;
  Coverage: string;
  Veh_Usage: string;
  Annual_Miles_Range: string;
  Vehicl_Cost_Range: string;
  Re_Quote: string;
  Quoted_Premium: number;
}
export interface RiskOutput {
  risk_score: number;
  risk_tier: "LOW" | "MEDIUM" | "HIGH";
  risk_explanation: string;
}
export interface FraudOutput {
  fraud_risk_score: number;
  fraud_flag: boolean;
  fraud_reason_codes: string[];
  rule_flags?: string[];
  decision?: string;
}
export interface ConversionOutput {
  conversion_probability: number;
  conversion_band: "LOW" | "MEDIUM" | "HIGH";
  top_conversion_drivers: string[];
}
export interface PersonalizationOutput {
  recommended_plan: string;
  coverage_level: string;
  recommended_addons: string[];
  personalization_score: number;
}
export interface PremiumOutput {
  premium_issue: boolean;
  recommended_premium_range: number[];
  recommendation_reason: string;
}
export interface RoutingExplanation {
  risk_factor: string;
  conversion_driver: string;
  premium_issue: string;
}
export interface DecisionOutput {
  decision: "AUTO_APPROVE" | "FOLLOW_UP_AGENT" | "ESCALATE_TO_UNDERWRITER";
  confidence_score: number;
  decision_explanation: string;
  detailed_explanation?: RoutingExplanation;
}
export interface EscalationOutput {
  escalation_required: boolean;
  reason: string;
}
export interface PipelineOutput {
  quote_id: string;
  risk_evaluation: RiskOutput;
  fraud_detection?: FraudOutput;
  conversion_prediction: ConversionOutput;
  personalization?: PersonalizationOutput;
  premium_advice: PremiumOutput;
  final_decision: DecisionOutput;
  escalation_status: EscalationOutput;
  customer_name?: string; // Frontend only
}
