"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight } from "lucide-react";
import Dashboard from "../components/dashboard";
export default function Home() {
  const [entered, setEntered] = useState(false);
  return (
    <AnimatePresence mode="wait">
      {!entered ? (
        <motion.div
          key="welcome"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.4 }}
          className="min-h-screen flex flex-col items-center justify-center px-6"
        >
          {/* Subtle glow */}
          <div className="absolute top-1/3 w-[500px] h-[500px] bg-white/[0.02] rounded-full blur-[120px] pointer-events-none" />
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="text-center relative z-10 max-w-2xl"
          >
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/[0.06] bg-white/[0.02] mb-8">
              <div className="w-1.5 h-1.5 rounded-full bg-white/20" />
              <span className="text-[11px] text-white/40 font-medium tracking-wide">
                6 AI Agents Online
              </span>
            </div>
            <h1 className="text-4xl md:text-5xl font-semibold tracking-tight leading-[1.1] mb-6">
              <span className="text-white">Quote</span>
              <span className="text-white/30">AI</span>
            </h1>
            <p className="text-base text-white/30 leading-relaxed max-w-md mx-auto mb-12">
              Autonomous multi-agent pipeline for insurance risk profiling,
              conversion prediction, and decision routing.
            </p>
            <motion.button
              onClick={() => setEntered(true)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="inline-flex items-center gap-2.5 px-6 py-3 bg-white text-black text-sm font-medium rounded-lg hover:bg-white/90 transition-colors"
            >
              Open Console
              <ArrowRight className="w-4 h-4" />
            </motion.button>
          </motion.div>
          {/* Bottom text */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="absolute bottom-8 text-[11px] text-white/15 tracking-wide"
          >
            Risk Profiler · Conversion Predictor · Premium Advisor · Decision
            Router
          </motion.p>
        </motion.div>
      ) : (
        <motion.div
          key="dashboard"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <Dashboard />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
