"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
interface CustomSelectProps {
  value: string;
  options: string[];
  displayFn?: (val: string) => string;
  onChange: (val: string) => void;
}
export default function CustomSelect({
  value,
  options,
  displayFn,
  onChange,
}: CustomSelectProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node))
        setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);
  const display = displayFn ? displayFn(value) : value;
  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between bg-white/[0.02] border border-white/[0.06] rounded-xl px-3 py-2 text-sm text-white/90 focus:outline-none focus:border-white/20 focus:bg-white/[0.04] transition-all"
      >
        <span className="truncate">{display}</span>
        <ChevronDown
          className={`w-4 h-4 text-white/40 transition-transform duration-200 ${open ? "rotate-180" : ""}`}
        />
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute z-50 mt-2 w-full bg-[#151518]/95 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl overflow-hidden max-h-48 overflow-y-auto"
          >
            {options.map((opt) => {
              const label = displayFn ? displayFn(opt) : opt;
              const isSelected = opt === value;
              return (
                <button
                  key={opt}
                  type="button"
                  onClick={() => {
                    onChange(opt);
                    setOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-[13px] transition-colors ${
                    isSelected
                      ? "bg-white/[0.03] text-white/80"
                      : "text-white/70 hover:bg-white/[0.04] hover:text-white"
                  }`}
                >
                  {label}
                </button>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
