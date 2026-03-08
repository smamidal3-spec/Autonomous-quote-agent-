"use client";
import { motion, AnimatePresence } from "framer-motion";
import { PipelineOutput } from "../lib/types";
import { Copy, CheckCircle2, ShieldAlert, Sparkles } from "lucide-react";
import { useState } from "react";
interface Props {
  result: PipelineOutput | null;
  isProcessing: boolean;
  currentStep: number;
}
const TIER_DOT: Record<string, string> = {
  LOW: "bg-white/20",
  MEDIUM: "bg-amber-500/60",
  HIGH: "bg-red-500/60",
};
const DECISION_LABEL: Record<string, string> = {
  AUTO_APPROVE: "Auto-Approved",
  FOLLOW_UP_AGENT: "Manual Follow-up",
  ESCALATE_TO_UNDERWRITER: "Underwriter Review",
};
const FEATURE_LABELS: Record<string, string> = {
  driver_age: "Driver Age",
  driving_exp: "Driving Experience",
  prev_accidents: "Accident History",
  prev_citations: "Citation Record",
  quoted_premium: "Premium Amount",
  q_creation_dt: "Quote Recency",
  q_valid_dt: "Quote Validity Window",
  policy_bind_dt: "Policy Binding Speed",
  annual_miles_range: "Annual Mileage",
  vehicl_cost_range: "Vehicle Value",
  sal_range: "Income Bracket",
  region: "Risk Zone",
  gender: "Demographics",
  marital_status: "Marital Status",
  education: "Education Level",
  coverage: "Coverage Tier",
  veh_usage: "Vehicle Usage",
  policy_type: "Vehicle Type",
  agent_type: "Agent Channel",
  agent_num: "Agent Experience",
  hh_vehicles: "Household Vehicles",
  hh_drivers: "Household Drivers",
  re_quote: "Re-Quote Status",
};
const FRAUD_REASON_LABELS: Record<string, string> = {
  high_accident_velocity: "High Accident Rate",
  age_vehicle_mismatch: "Age-Vehicle Mismatch",
  premium_risk_mismatch: "Underpriced Premium",
  high_violation_frequency: "Frequent Violations",
  coverage_usage_mismatch: "Coverage-Usage Gap",
  suspicious_requote_pattern: "Suspicious Re-Quote",
  statistical_anomaly: "Statistical Anomaly",
  none: "Clean",
  agent_error_passthrough: "Check Skipped",
};
const agents = [
  { name: "Risk Profiler", step: 1, desc: "ML Classification & Tiering" },
  { name: "Fraud Detector", step: 2, desc: "Anomaly Detection & Scoring" },
  { name: "Conversion Predictor", step: 3, desc: "SHAP Driver Analysis" },
  { name: "Personalisation", step: 4, desc: "Segment-Based Recommendations" },
  { name: "Premium Advisor", step: 5, desc: "Elasticity Calibration" },
  { name: "Decision Router", step: 6, desc: "Heuristic Arbitration" },
];
export default function PipelineVisualizer({
  result,
  isProcessing,
  currentStep,
}: Props) {
  const [copied, setCopied] = useState(false);
  const copyResult = () => {
    if (!result) return;
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  const getFeatureLabel = (key: string) => {
    const lowerKey = key.toLowerCase();
    return (
      FEATURE_LABELS[lowerKey] ||
      key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
    );
  };
  const renderAgentContent = (step: number) => {
    if (!result) return null;
    switch (step) {
      case 1:
        return (
          <div className="space-y-4 mt-6">
            <div className="flex justify-between items-baseline mb-2">
              <span className="text-2xl font-light text-white tabular-nums">
                {result.risk_evaluation.risk_score.toFixed(1)}
                <span className="text-[10px] text-white/30 ml-1 uppercase tracking-widest font-medium">
                  Score
                </span>
              </span>
              <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-white/[0.03] border border-white/[0.05]">
                <div
                  className={`w-1.5 h-1.5 rounded-full ${TIER_DOT[result.risk_evaluation.risk_tier]}`}
                />
                <span className="text-[9px] text-white/70 font-semibold uppercase tracking-widest">
                  {result.risk_evaluation.risk_tier} RISK
                </span>
              </div>
            </div>
            <div className="w-full h-1 bg-white/[0.04] rounded-full overflow-hidden relative">
              <motion.div
                initial={{ width: 0 }}
                animate={{
                  width: `${Math.min(result.risk_evaluation.risk_score, 100)}%`,
                }}
                transition={{ duration: 1.2, ease: "easeOut" }}
                className={`absolute h-full ${TIER_DOT[result.risk_evaluation.risk_tier]}`}
              />
            </div>
            <p className="text-[11px] text-white/40 mt-3 leading-relaxed">
              {result.risk_evaluation.risk_explanation}
            </p>
            <p className="text-[12px] text-gray-400 mt-3 leading-relaxed italic font-serif">
              This agent assesses the overall risk profile of the applicant
              based on various data points, assigning a risk score and tier.
            </p>
          </div>
        );
      case 2: // Fraud Detection
        if (!result.fraud_detection)
          return (
            <p className="text-[12px] text-gray-400 mt-3 italic font-serif">
              No data
            </p>
          );
        return (
          <div className="space-y-4 mt-6">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                {result.fraud_detection.fraud_flag ? (
                  <ShieldAlert className="w-4 h-4 text-red-400" />
                ) : (
                  <CheckCircle2 className="w-4 h-4 text-white/80" />
                )}
                <span
                  className={`text-[10px] font-bold uppercase tracking-widest ${result.fraud_detection.fraud_flag ? "text-red-400" : "text-white/80"}`}
                >
                  {result.fraud_detection.fraud_flag ? "FLAGGED" : "CLEAR"}
                </span>
              </div>
              <span className="text-xl font-light text-white tabular-nums">
                {(result.fraud_detection.fraud_risk_score * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full h-1 bg-white/[0.04] rounded-full overflow-hidden relative">
              <motion.div
                initial={{ width: 0 }}
                animate={{
                  width: `${result.fraud_detection.fraud_risk_score * 100}%`,
                }}
                transition={{ duration: 1, ease: "easeOut" }}
                className={`absolute h-full ${result.fraud_detection.fraud_flag ? "bg-red-500/60" : "bg-white/20"}`}
              />
            </div>
            <div className="flex flex-wrap gap-2">
              {result.fraud_detection.fraud_reason_codes.map((code, i) => (
                <span
                  key={i}
                  className={`text-[9px] uppercase tracking-widest px-2 py-1 rounded-md border ${
                    code === "none" || code === "agent_error_passthrough"
                      ? "bg-white/[0.02] border-white/[0.05] text-white/30"
                      : "bg-red-500/10 border-red-500/20 text-red-400/80"
                  }`}
                >
                  {FRAUD_REASON_LABELS[code] || code.replace(/_/g, " ")}
                </span>
              ))}
            </div>
            <p className="text-[12px] text-gray-600 mt-4 leading-relaxed font-serif">
              {result.fraud_detection.fraud_flag
                ? `Suspicious request flagged for review with a ${(result.fraud_detection.fraud_risk_score * 100).toFixed(0)}% anomaly score. Primary reasons: ${result.fraud_detection.fraud_reason_codes
                    .filter((c) => c !== "none")
                    .map((c) => FRAUD_REASON_LABELS[c] || c.replace(/_/g, " "))
                    .join(", ")}.`
                : `Quote request appears normal with no significant fraud indicators. Primary factor: ${result.fraud_detection.fraud_reason_codes.map((c) => FRAUD_REASON_LABELS[c] || c.replace(/_/g, " ")).join(", ")}.`}
            </p>
          </div>
        );
      case 3: // Conversion Predictor
        return (
          <div className="space-y-4 mt-6">
            <div className="flex justify-between items-baseline mb-2">
              <span className="text-2xl font-light text-white tabular-nums">
                {result.conversion_prediction.conversion_probability.toFixed(1)}
                %
              </span>
              <span className="text-[9px] text-white/40 uppercase tracking-widest font-bold">
                {result.conversion_prediction.conversion_band} INTENT
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {result.conversion_prediction.top_conversion_drivers.map(
                (d, i) => (
                  <span
                    key={i}
                    className="text-[10px] text-white/60 bg-white/[0.03] px-2.5 py-1 rounded-md border border-white/[0.05]"
                  >
                    {getFeatureLabel(d)}
                  </span>
                ),
              )}
            </div>
            <p className="text-[12px] text-gray-600 mt-4 leading-relaxed font-serif">
              Customer shows{" "}
              {result.conversion_prediction.conversion_band.toLowerCase()}{" "}
              intent to purchase based on{" "}
              {result.conversion_prediction.top_conversion_drivers.length} key
              attributes.
            </p>
          </div>
        );
      case 4: // Personalization
        if (!result.personalization) return null;
        return (
          <div className="space-y-4 mt-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <Sparkles className="w-3.5 h-3.5 text-blue-400" />
                <span className="text-[11px] text-white/80 font-medium tracking-wide">
                  {result.personalization.recommended_plan}
                </span>
              </div>
              <span className="text-[9px] text-white/30 uppercase tracking-widest font-bold">
                {result.personalization.coverage_level}
              </span>
            </div>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-[9px] text-white/30 uppercase tracking-widest font-bold">
                Match
              </span>
              <div className="flex-1 h-1 bg-white/[0.04] rounded-full overflow-hidden relative">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{
                    width: `${result.personalization.personalization_score * 100}%`,
                  }}
                  transition={{ duration: 1 }}
                  className="absolute h-full bg-blue-500/60"
                />
              </div>
              <span className="text-[10px] text-white/50 tabular-nums">
                {(result.personalization.personalization_score * 100).toFixed(
                  0,
                )}
                %
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {result.personalization.recommended_addons.map((addon, i) => (
                <span
                  key={i}
                  className="text-[9px] uppercase tracking-widest px-2 py-1 rounded-md bg-white/[0.02] border border-white/[0.04] text-white/60"
                >
                  {addon}
                </span>
              ))}
            </div>
          </div>
        );
      case 5: // Premium Advisor
        return (
          <div className="space-y-3 mt-4">
            <div
              className={`text-[10px] uppercase font-bold tracking-widest ${result.premium_advice.premium_issue ? "text-amber-400/80" : "text-white/40"}`}
            >
              {result.premium_advice.premium_issue
                ? "Calibration Required"
                : "Market Aligned"}
            </div>
            <p className="text-[12px] text-white/60 leading-relaxed pl-3 border-l-2 border-white/10">
              {result.premium_advice.recommendation_reason}
            </p>
          </div>
        );
      case 6: // Decision Router
        return (
          <div className="space-y-4 mt-4">
            <div className="flex justify-between items-baseline">
              <span className="text-lg font-medium text-white/90">
                {DECISION_LABEL[result.final_decision.decision]}
              </span>
              <span className="text-[9px] text-white/40 uppercase tracking-widest tabular-nums">
                {(result.final_decision.confidence_score * 100).toFixed(0)}%
                CONFIDENCE
              </span>
            </div>
            {result.escalation_status.escalation_required && (
              <div className="px-3 py-2 bg-red-500/10 border border-red-500/20 rounded-lg">
                <p className="text-[10px] text-red-400/80 uppercase tracking-widest">
                  {result.escalation_status.reason}
                </p>
              </div>
            )}
            <button
              onClick={copyResult}
              className="mt-2 flex items-center justify-center p-2 gap-2 text-[10px] uppercase tracking-widest text-white/40 hover:text-white/80 border border-white/10 hover:border-white/20 rounded-lg transition-colors self-start"
            >
              {copied ? (
                <CheckCircle2 className="w-3.5 h-3.5" />
              ) : (
                <Copy className="w-3.5 h-3.5" />
              )}
              <span>{copied ? "COPIED" : "COPY RAW PAYLOAD"}</span>
            </button>
            <p className="text-[11px] text-white/40 mt-3 leading-relaxed">
              {result.final_decision.decision_explanation}
            </p>
          </div>
        );
    }
  };
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-[11px] font-medium text-white/15 uppercase tracking-[0.2em]">
          Agent Pipeline
        </h2>
      </div>
      <div className="relative pl-8">
        {/* Vertical connector line */}
        <div className="absolute left-[13px] top-[14px] bottom-[14px] w-[1px] bg-white/[0.04]" />
        <div className="space-y-4">
          {agents.map((agent, i) => {
            const isActive = isProcessing && currentStep === agent.step;
            const isDone =
              currentStep > agent.step || (!isProcessing && result != null);
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0.1, x: -5 }}
                animate={{ opacity: isDone ? 1 : isActive ? 1 : 0.1, x: 0 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="relative"
              >
                {/* Connector dot */}
                <div className="absolute -left-[30px] top-[18px]">
                  <div
                    className={`w-3 h-3 rounded-full border-[2px] border-[#09090b] transition-all duration-300 ${
                      isDone
                        ? "bg-white/40"
                        : isActive
                          ? "bg-white/20 scale-125"
                          : "bg-white/10"
                    }`}
                  >
                    {isActive && (
                      <div className="absolute inset-0 rounded-full bg-white/20 animate-ping opacity-40" />
                    )}
                  </div>
                </div>
                <div
                  className={`card overflow-hidden transition-colors ${isActive ? "border-white/20 bg-white/[0.03]" : ""}`}
                >
                  <div className="p-5">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-[13px] font-medium text-white/80 tracking-wide">
                        {agent.name}
                      </h4>
                      <div className="flex items-center gap-1.5">
                        {isDone && (
                          <CheckCircle2 className="w-3 h-3 text-white/40" />
                        )}
                        <span className="text-[9px] text-white/20 uppercase tracking-widest font-bold">
                          {isActive ? "ACTIVE" : isDone ? "COMPLETE" : "STNDBY"}
                        </span>
                      </div>
                    </div>
                    <p className="text-[11px] text-white/30 max-w-xs leading-relaxed">
                      {agent.desc}
                    </p>
                    {isDone && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        transition={{ duration: 0.4 }}
                      >
                        {renderAgentContent(agent.step)}
                      </motion.div>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
