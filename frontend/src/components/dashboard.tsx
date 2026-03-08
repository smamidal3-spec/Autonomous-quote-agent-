"use client";
import { useState, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import QuoteForm from "./quote-form";
import PipelineVisualizer from "./pipeline-visualizer";
import DecisionDashboard from "./decision-dashboard";
import { evaluateQuote, getDefaultQuoteInput } from "../lib/api-client";
import { QuoteInput, PipelineOutput } from "../lib/types";
import { RotateCcw } from "lucide-react";
export default function Dashboard() {
  const [result, setResult] = useState<PipelineOutput | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [history, setHistory] = useState<PipelineOutput[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [formKey, setFormKey] = useState(0);
  const handleSubmit = useCallback(
    async (input: QuoteInput, customerName: string) => {
      setIsProcessing(true);
      setResult(null);
      setError(null);
      setCurrentStep(0);
      const stepInterval = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= 6) {
            clearInterval(stepInterval);
            return 6;
          }
          return prev + 1;
        });
      }, 600);
      try {
        const response = await evaluateQuote(input);
        clearInterval(stepInterval);
        setCurrentStep(7);
        const enrichedResult = { ...response, customer_name: customerName };
        setResult(enrichedResult);
        setHistory((prev) => [enrichedResult, ...prev]);
      } catch (err) {
        clearInterval(stepInterval);
        setCurrentStep(0);
        setError(
          err instanceof Error ? err.message : "Failed to process quote",
        );
      } finally {
        setIsProcessing(false);
      }
    },
    [],
  );
  const handleReset = () => {
    setResult(null);
    setError(null);
    setCurrentStep(0);
    setIsProcessing(false);
    setFormKey((prev) => prev + 1);
  };
  const statusText = useMemo(() => {
    if (!isProcessing) return "System Idle";
    switch (currentStep) {
      case 1:
        return "Analyzing Risk Profile...";
      case 2:
        return "Running Fraud Detection...";
      case 3:
        return "Predicting Conversion...";
      case 4:
        return "Personalising Coverage...";
      case 5:
        return "Calculating Premium...";
      case 6:
        return "Routing Decision...";
      default:
        return "Processing...";
    }
  }, [isProcessing, currentStep]);
  return (
    <div className="min-h-screen bg-[#09090b] selection:bg-white/10">
      {/* Header */}
      <header className="border-b border-white/[0.04] px-6 py-4 sticky top-0 bg-[#09090b]/80 backdrop-blur-md z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-[14px] font-semibold tracking-tight text-white/90">
              Quote<span className="text-white/20">AI</span>
            </h1>
            <div className="h-3 w-[1px] bg-white/[0.08]" />
            <div className="flex items-center gap-2">
              <motion.div
                animate={isProcessing ? { opacity: [0.3, 1, 0.3] } : {}}
                transition={{ duration: 1.5, repeat: Infinity }}
                className={`w-1.5 h-1.5 rounded-full ${isProcessing ? "bg-white/20" : "bg-white/10"}`}
              />
              <span className="text-[11px] text-white/30 font-medium tracking-wide tabular-nums uppercase">
                {statusText}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-4">
              <button
                onClick={handleReset}
                className="flex items-center gap-1.5 text-[11px] text-white/20 hover:text-white/50 transition-colors"
                title="New Quote"
              >
                <RotateCcw className="w-3 h-3" />
                <span>Reset</span>
              </button>
            </div>
            <div className="h-3 w-[1px] bg-white/[0.08]" />
            <span className="text-[11px] text-white/15 tracking-tight uppercase">
              {history.length} processed
            </span>
          </div>
        </div>
      </header>
      {/* Content */}
      <main className="max-w-7xl mx-auto px-6 py-10">
        <div className="grid grid-cols-12 gap-10">
          {/* Left Column: Form & History */}
          <div className="col-span-12 lg:col-span-4 space-y-10">
            <section>
              <QuoteForm
                key={formKey}
                onSubmit={handleSubmit}
                isLoading={isProcessing}
              />
            </section>
            {history.length > 0 && (
              <section className="pt-6 border-t border-white/[0.04]">
                <h3 className="text-[11px] font-medium text-white/15 uppercase tracking-widest mb-4">
                  Recent Activity
                </h3>
                <div className="space-y-2 max-h-[350px] overflow-y-auto pr-2 custom-scrollbar">
                  {history.map((h, i) => (
                    <div
                      key={h.quote_id}
                      className="p-3 rounded-xl bg-white/[0.01] border border-white/[0.03] flex items-center justify-between group hover:bg-white/[0.02] transition-colors cursor-pointer"
                      onClick={() => setResult(h)}
                    >
                      <div className="flex flex-col gap-0.5">
                        <span className="text-[12px] text-white/70 font-medium">
                          {h.customer_name || "Unknown Applicant"}
                        </span>
                        <span className="text-[10px] text-white/15 tabular-nums">
                          #{h.quote_id.slice(0, 8)}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`text-[10px] px-1.5 py-0.5 rounded border ${
                            h.risk_evaluation.risk_tier === "HIGH"
                              ? "border-red-500/20 text-red-500/40"
                              : h.risk_evaluation.risk_tier === "MEDIUM"
                                ? "border-amber-500/20 text-amber-500/40"
                                : "border-white/10 text-white/40"
                          }`}
                        >
                          {h.risk_evaluation.risk_tier}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </div>
          {/* Middle Column: Pipeline Visualizer */}
          <div className="col-span-12 lg:col-span-4">
            <PipelineVisualizer
              result={result}
              isProcessing={isProcessing}
              currentStep={currentStep}
            />
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="mt-6 p-4 rounded-xl border border-red-500/10 bg-red-500/[0.02] text-[12px] text-red-400/60 leading-relaxed"
                >
                  {error}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
          {/* Right Column: Deep Analysis & Stats */}
          <div className="col-span-12 lg:col-span-4">
            <DecisionDashboard result={result} history={history} />
          </div>
        </div>
      </main>
      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.03);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.08);
        }
      `}</style>
    </div>
  );
}
