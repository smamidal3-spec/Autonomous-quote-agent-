"use client";
import { motion, AnimatePresence } from "framer-motion";
import { PipelineOutput } from "../lib/types";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
interface Props {
  result: PipelineOutput | null;
  history: PipelineOutput[];
}
const COLORS: Record<string, string> = {
  LOW: "#ffffff10",
  MEDIUM: "#ffffff20",
  HIGH: "#ffffff40",
};
const RISK_COLORS: Record<string, string> = {
  LOW: "#4ade8050",
  MEDIUM: "#fbbf2450",
  HIGH: "#f8717150",
};
export default function DecisionDashboard({ result, history }: Props) {
  const total = history.length;
  const escalations = history.filter(
    (h) => h.escalation_status.escalation_required,
  ).length;
  const autoApproved = history.filter(
    (h) => h.final_decision.decision === "AUTO_APPROVE",
  ).length;
  const avgConv =
    total > 0
      ? history.reduce(
          (s, h) => s + h.conversion_prediction.conversion_probability,
          0,
        ) / total
      : 0;
  const riskDist = [
    {
      name: "Low",
      value: history.filter((h) => h.risk_evaluation.risk_tier === "LOW")
        .length,
      color: RISK_COLORS.LOW,
    },
    {
      name: "Med",
      value: history.filter((h) => h.risk_evaluation.risk_tier === "MEDIUM")
        .length,
      color: RISK_COLORS.MEDIUM,
    },
    {
      name: "High",
      value: history.filter((h) => h.risk_evaluation.risk_tier === "HIGH")
        .length,
      color: RISK_COLORS.HIGH,
    },
  ].filter((d) => d.value > 0);
  return (
    <div className="space-y-8">
      <h2 className="text-[11px] font-medium text-white/15 uppercase tracking-[0.2em]">
        Deep Analysis
      </h2>
      {/* Grid Stats */}
      <div className="grid grid-cols-2 gap-4">
        {[
          { label: "Throughput", value: total },
          { label: "Avg Conversion", value: `${avgConv.toFixed(0)}%` },
          {
            label: "Approval Rate",
            value:
              total > 0
                ? `${((autoApproved / total) * 100).toFixed(0)}%`
                : "0%",
          },
          {
            label: "Escalation Rate",
            value:
              total > 0 ? `${((escalations / total) * 100).toFixed(0)}%` : "0%",
          },
        ].map((s, i) => (
          <div
            key={i}
            className="card p-5 group hover:border-white/10 transition-colors"
          >
            <span className="text-[22px] font-extralight text-white/80 tabular-nums">
              {s.value}
            </span>
            <p className="text-[9px] text-white/15 uppercase tracking-widest mt-1 font-bold group-hover:text-white/30 transition-colors">
              {s.label}
            </p>
          </div>
        ))}
      </div>
      {/* Risk Concentration Chart */}
      {total > 0 && (
        <div className="card p-6 overflow-hidden relative">
          <div className="flex justify-between items-center mb-6">
            <span className="text-[10px] text-white/20 uppercase tracking-[0.2em] font-bold">
              Distribution
            </span>
            <span className="text-[9px] text-white/10 uppercase tracking-widest tabular-nums">
              N={total}
            </span>
          </div>
          <div className="h-[120px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskDist}
                  cx="50%"
                  cy="50%"
                  innerRadius={35}
                  outerRadius={50}
                  paddingAngle={8}
                  dataKey="value"
                  strokeWidth={0}
                  animationBegin={0}
                  animationDuration={1000}
                >
                  {riskDist.map((d, i) => (
                    <Cell key={i} fill={d.color} />
                  ))}
                </Pie>
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-[#151518] border border-white/10 px-2 py-1.5 rounded-lg text-[10px] text-white/60">
                          {payload[0].name}: {payload[0].value} units
                        </div>
                      );
                    }
                    return null;
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-6 mt-2">
            {riskDist.map((d) => (
              <div key={d.name} className="flex items-center gap-2">
                <div
                  className="w-1 h-1 rounded-full"
                  style={{ backgroundColor: d.color }}
                />
                <span className="text-[9px] text-white/20 font-bold uppercase tracking-tight">
                  {d.name}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
      {/* Insight Panel */}
      <AnimatePresence mode="wait">
        {result ? (
          <motion.div
            key={result.quote_id}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            className="space-y-6"
          >
            <div>
              <div className="flex items-center gap-2 mb-2">
                <div className="h-[1px] w-3 bg-white/20" />
                <span className="text-[10px] text-white/30 uppercase tracking-[0.2em] font-bold">
                  Reasoning Engine
                </span>
              </div>
              <p className="text-[12px] text-white/40 leading-relaxed font-light pl-5 border-l border-white/[0.04]">
                {result.risk_evaluation.risk_explanation}
              </p>
            </div>
            {result.final_decision.detailed_explanation && (
              <div className="pt-4 border-t border-white/[0.04]">
                <span className="text-[10px] text-white/15 uppercase tracking-[0.2em] font-bold mb-3 block">
                  Router Arbitration
                </span>
                <div className="space-y-3">
                  {Object.entries(
                    result.final_decision.detailed_explanation,
                  ).map(([key, val]) => (
                    <div
                      key={key}
                      className="flex justify-between items-center text-[11px] group"
                    >
                      <span className="text-white/15 group-hover:text-white/25 transition-colors">
                        {key.replace(/_/g, " ")}
                      </span>
                      <span className="text-white/40 font-mono tracking-tight">
                        {val}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        ) : (
          <div className="card p-8 border-dashed flex flex-col items-center justify-center text-center opacity-40">
            <p className="text-[11px] text-white/30 font-light max-w-[180px] leading-relaxed">
              Waiting for pipeline throughput... Analysis will stream here
              automatically.
            </p>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
