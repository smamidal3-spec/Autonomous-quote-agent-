"use client";
import { motion } from "framer-motion";
import { PipelineOutput } from "../lib/types";
import { Clock, CheckCircle2, AlertTriangle, XCircle } from "lucide-react";
interface TimelineProps {
  result: PipelineOutput;
}
const STEPS = [
  { label: "Quote Submitted", icon: Clock, color: "bg-blue-500" },
  {
    label: "Risk Profile Generated",
    icon: CheckCircle2,
    color: "bg-violet-500",
  },
  { label: "Conversion Predicted", icon: CheckCircle2, color: "bg-cyan-500" },
  { label: "Premium Evaluated", icon: CheckCircle2, color: "bg-amber-500" },
  { label: "Final Decision Routed", icon: CheckCircle2, color: "bg-white/20" },
];
export default function QuoteTimeline({ result }: TimelineProps) {
  const isEscalation = result.escalation_status.escalation_required;
  return (
    <div className="glass-panel rounded-2xl p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
          <Clock className="w-5 h-5 text-white" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-white">Processing Timeline</h2>
          <p className="text-xs text-white/40">
            Quote ID: {result.quote_id.slice(0, 8)}...
          </p>
        </div>
      </div>
      <div className="relative">
        {/* Vertical Line */}
        <div className="absolute left-[15px] top-0 bottom-0 w-[2px] bg-gradient-to-b from-cyan-500/50 to-purple-500/50" />
        <div className="space-y-4">
          {STEPS.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.2, duration: 0.4 }}
              className="flex items-start gap-4 relative"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: i * 0.2 + 0.1, type: "spring" }}
                className={`w-8 h-8 rounded-full ${step.color} flex items-center justify-center z-10 shadow-lg`}
              >
                <step.icon className="w-4 h-4 text-white" />
              </motion.div>
              <div className="flex-1 bg-white/5 rounded-xl px-4 py-3 border border-white/5">
                <p className="text-sm font-semibold text-white">{step.label}</p>
                <p className="text-[10px] text-white/30 mt-0.5">
                  Step {i + 1} of 5 — Complete
                </p>
              </div>
            </motion.div>
          ))}
          {/* Escalation Step */}
          {isEscalation && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.2 }}
              className="flex items-start gap-4 relative"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 1.3, type: "spring" }}
                className="w-8 h-8 rounded-full bg-red-500 flex items-center justify-center z-10 shadow-lg animate-pulse"
              >
                <XCircle className="w-4 h-4 text-white" />
              </motion.div>
              <div className="flex-1 bg-red-500/10 rounded-xl px-4 py-3 border border-red-500/20">
                <p className="text-sm font-semibold text-red-400">
                  🚨 Escalated to Underwriter
                </p>
                <p className="text-[10px] text-white/40 mt-0.5">
                  {result.escalation_status.reason}
                </p>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
