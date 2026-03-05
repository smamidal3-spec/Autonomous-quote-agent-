"use client";
import { motion } from "framer-motion";
import { PipelineOutput } from "../lib/types";
import { Brain, BarChart3, AlertCircle } from "lucide-react";
interface ExplainabilityPanelProps {
  result: PipelineOutput;
}
export default function ExplainabilityPanel({
  result,
}: ExplainabilityPanelProps) {
  return (
    <div className="glass-panel rounded-2xl p-6 space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
          <Brain className="w-5 h-5 text-white" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-white">AI Explainability</h2>
          <p className="text-xs text-white/40">Why the AI made this decision</p>
        </div>
      </div>
      {/* Risk Drivers */}
      <div>
        <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-3 flex items-center gap-2">
          <BarChart3 className="w-3.5 h-3.5" /> Risk Analysis
        </h3>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white/5 rounded-xl p-4 border border-white/5"
        >
          <p className="text-sm text-white/70 leading-relaxed">
            {result.risk_evaluation.risk_explanation}
          </p>
        </motion.div>
      </div>
      {/* Top Conversion Drivers */}
      <div>
        <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-3 flex items-center gap-2">
          <BarChart3 className="w-3.5 h-3.5" /> Top Conversion Drivers
        </h3>
        <div className="space-y-2">
          {result.conversion_prediction.top_conversion_drivers.map(
            (driver, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.15 }}
                className="flex items-center gap-3 bg-white/5 rounded-xl px-4 py-3 border border-white/5"
              >
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-black ${
                    i === 0
                      ? "bg-cyan-500/20 text-cyan-400"
                      : i === 1
                        ? "bg-blue-500/20 text-blue-400"
                        : "bg-purple-500/20 text-purple-400"
                  }`}
                >
                  #{i + 1}
                </div>
                <span className="text-sm text-white/80 font-medium">
                  {driver.replace(/_/g, " ")}
                </span>
              </motion.div>
            ),
          )}
        </div>
      </div>
      {/* Premium Reasoning */}
      <div>
        <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-3 flex items-center gap-2">
          <AlertCircle className="w-3.5 h-3.5" /> Premium Reasoning
        </h3>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className={`rounded-xl p-4 border ${
            result.premium_advice.premium_issue
              ? "bg-amber-500/5 border-amber-500/20"
              : "bg-white/[0.02] border-white/10"
          }`}
        >
          <p className="text-sm text-white/70 leading-relaxed">
            {result.premium_advice.recommendation_reason}
          </p>
        </motion.div>
      </div>
      {/* Decision Routing Logic */}
      {result.final_decision.detailed_explanation && (
        <div>
          <h3 className="text-xs font-semibold text-white/50 uppercase tracking-wider mb-3">
            Routing Logic
          </h3>
          <div className="grid grid-cols-1 gap-2">
            {Object.entries(result.final_decision.detailed_explanation).map(
              ([key, value], i) => (
                <motion.div
                  key={key}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 * i }}
                  className="bg-white/5 rounded-lg px-4 py-2.5 border border-white/5 flex items-center justify-between"
                >
                  <span className="text-xs text-white/40 uppercase">
                    {key.replace(/_/g, " ")}
                  </span>
                  <span className="text-xs text-white/80 font-medium">
                    {value}
                  </span>
                </motion.div>
              ),
            )}
          </div>
        </div>
      )}
    </div>
  );
}
