"use client";
import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, ArrowRight } from "lucide-react";
import { QuoteInput } from "../lib/types";
import { getDefaultQuoteInput } from "../lib/api-client";
import CustomSelect from "./custom-select";
import StateTreeSelect, { INDIA_RISK_DATA } from "./state-tree-select";
interface QuoteFormProps {
  onSubmit: (input: QuoteInput, customerName: string) => void;
  isLoading: boolean;
}
function NumberInput({
  numericValue,
  onChange,
  placeholder,
  step,
}: {
  numericValue: number;
  onChange: (n: number) => void;
  placeholder: string;
  step: string;
}) {
  const [display, setDisplay] = useState<string>(String(numericValue));
  const [prevNumericValue, setPrevNumericValue] = useState(numericValue);
  if (numericValue !== prevNumericValue) {
    setPrevNumericValue(numericValue);
    setDisplay(String(numericValue));
  }
  return (
    <input
      type="number"
      step={step}
      placeholder={placeholder}
      value={display}
      onChange={(e) => {
        const v = e.target.value;
        setDisplay(v);
        if (v === "") {
          onChange(0);
          return;
        }
        const value = Number(v);
        if (value < 0) return; // Prevent negative values unless explicitly allowed
        if (!isNaN(value)) {
          onChange(value);
        }
      }}
      className="w-full bg-white/[0.02] border border-white/[0.06] rounded-xl px-3 py-2 text-sm text-white/90 placeholder:text-white/20 focus:outline-none focus:border-white/20 focus:bg-white/[0.04] transition-all"
    />
  );
}
const SELECT_OPTIONS: Record<string, string[]> = {
  Coverage: ["Basic", "Balanced", "Enhanced"],
  Veh_Usage: ["Commute", "Pleasure", "Business"],
  Annual_Miles_Range: [
    "<= 7.5 K",
    "> 7.5 K & <= 15 K",
    "> 15 K & <= 25 K",
    "> 25 K & <= 35 K",
    "> 35 K & <= 45 K",
    "> 45 K & <= 55 K",
    "> 55 K",
  ],
  Sal_Range: [
    "<= ₹ 25 Lakh",
    "> ₹ 25 Lakh <= ₹ 40 Lakh",
    "> ₹ 40 Lakh <= ₹ 60 Lakh",
    "> ₹ 60 Lakh <= ₹ 90 Lakh",
    "> ₹ 90 Lakh ",
  ],
  Vehicl_Cost_Range: [
    "<= ₹ 10 Lakh",
    "> ₹ 10 Lakh <= ₹ 20 Lakh",
    "> ₹ 20 Lakh <= ₹ 30 Lakh",
    "> ₹ 30 Lakh <= ₹ 40 Lakh",
    "> ₹ 40 Lakh ",
  ],
  Region: ["A", "B", "C", "D", "E", "F", "G", "H"],
  Region_State: [
    "UP",
    "TN",
    "MH",
    "MP",
    "KA",
    "RJ",
    "DL",
    "KL",
    "GJ",
    "TG",
    "BR",
    "AP",
    "WB",
    "JH",
    "OD",
    "PB",
    "HR",
    "UK",
    "JK",
    "HP",
    "GA",
    "SK",
    "AS",
    "CH",
  ],
  Region_City: [],
  Gender: ["Male", "Female"],
  Marital_Status: ["Married", "Single", "Dirvorced", "Widow"],
  Education: ["High School", "College", "Bachelors", "Masters", "Ph.D"],
  Policy_Type: ["Car", "Truck", "Van"],
  Agent_Type: ["EA", "IA"],
  Re_Quote: ["No", "Yes"],
};
const STATE_RISK_DATA: Record<
  string,
  { name: string; risk: string; cities: string[]; regionCode: string }
> = {
  UP: {
    name: "Uttar Pradesh",
    risk: "CRITICAL",
    cities: ["Lucknow", "Noida", "Agra", "Kanpur", "Varanasi", "Prayagraj"],
    regionCode: "A",
  },
  TN: {
    name: "Tamil Nadu",
    risk: "CRITICAL",
    cities: ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    regionCode: "A",
  },
  MH: {
    name: "Maharashtra",
    risk: "VERY HIGH",
    cities: ["Pune", "Mumbai", "Thane", "Nagpur", "Nashik", "Aurangabad"],
    regionCode: "B",
  },
  MP: {
    name: "Madhya Pradesh",
    risk: "VERY HIGH",
    cities: ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain"],
    regionCode: "B",
  },
  KA: {
    name: "Karnataka",
    risk: "VERY HIGH",
    cities: ["Bengaluru", "Mysuru", "Hubli-Dharwad", "Mangaluru", "Belgaum"],
    regionCode: "B",
  },
  RJ: {
    name: "Rajasthan",
    risk: "HIGH",
    cities: ["Jaipur", "Jodhpur", "Kota", "Udaipur", "Ajmer", "Bikaner"],
    regionCode: "C",
  },
  TG: {
    name: "Telangana",
    risk: "HIGH",
    cities: ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
    regionCode: "C",
  },
  GJ: {
    name: "Gujarat",
    risk: "HIGH",
    cities: ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
    regionCode: "C",
  },
  BR: {
    name: "Bihar",
    risk: "HIGH",
    cities: ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga"],
    regionCode: "D",
  },
  AP: {
    name: "Andhra Pradesh",
    risk: "HIGH",
    cities: ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati"],
    regionCode: "D",
  },
  DL: {
    name: "Delhi NCR",
    risk: "CRITICAL (URBAN)",
    cities: ["Outer Delhi", "East Delhi", "South Delhi", "Dwarka"],
    regionCode: "A",
  },
  KL: {
    name: "Kerala",
    risk: "MEDIUM-HIGH",
    cities: ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"],
    regionCode: "D",
  },
  WB: {
    name: "West Bengal",
    risk: "MEDIUM-HIGH",
    cities: ["Kolkata", "Howrah", "Siliguri", "Durgapur"],
    regionCode: "E",
  },
  JH: {
    name: "Jharkhand",
    risk: "MEDIUM",
    cities: ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro"],
    regionCode: "E",
  },
  OD: {
    name: "Odisha",
    risk: "MEDIUM",
    cities: ["Bhubaneswar", "Cuttack", "Rourkela"],
    regionCode: "E",
  },
  PB: {
    name: "Punjab",
    risk: "MEDIUM",
    cities: ["Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
    regionCode: "F",
  },
  HR: {
    name: "Haryana",
    risk: "MEDIUM",
    cities: ["Faridabad", "Gurugram", "Panipat", "Ambala"],
    regionCode: "F",
  },
  AS: {
    name: "Assam",
    risk: "MEDIUM",
    cities: ["Guwahati", "Dibrugarh", "Silchar"],
    regionCode: "F",
  },
  CH: {
    name: "Chhattisgarh",
    risk: "MEDIUM",
    cities: ["Raipur", "Bhilai", "Bilaspur"],
    regionCode: "F",
  },
  UK: {
    name: "Uttarakhand",
    risk: "MEDIUM",
    cities: ["Dehradun", "Haridwar", "Haldwani", "Rishikesh"],
    regionCode: "G",
  },
  JK: {
    name: "Jammu & Kashmir",
    risk: "MEDIUM-LOW",
    cities: ["Srinagar", "Jammu"],
    regionCode: "G",
  },
  HP: {
    name: "Himachal Pradesh",
    risk: "MEDIUM-LOW",
    cities: ["Shimla", "Dharamshala", "Manali"],
    regionCode: "G",
  },
  GA: {
    name: "Goa",
    risk: "MEDIUM-LOW",
    cities: ["Panaji", "Margao"],
    regionCode: "H",
  },
  SK: { name: "Sikkim", risk: "LOW", cities: ["Gangtok"], regionCode: "H" },
};
const RISK_BADGE: Record<string, string> = {
  CRITICAL: "🔴",
  "CRITICAL (URBAN)": "🔴",
  "VERY HIGH": "🟠",
  HIGH: "🟡",
  "MEDIUM-HIGH": "🟡",
  MEDIUM: "🔵",
  "MEDIUM-LOW": "🟢",
  LOW: "🟢",
};
const DISPLAY_LABELS: Record<string, Record<string, string>> = {
  Region_State: Object.fromEntries(
    Object.entries(STATE_RISK_DATA).map(([code, d]) => [
      code,
      `${RISK_BADGE[d.risk] || ""} ${d.name} — ${d.risk}`,
    ]),
  ),
  Agent_Type: { EA: "Exclusive Agent", IA: "Independent Agent" },
  Sal_Range: {
    "<= ₹ 25 Lakh": "≤ ₹25 Lakh",
    "> ₹ 25 Lakh <= ₹ 40 Lakh": "₹25L — ₹40 Lakh",
    "> ₹ 40 Lakh <= ₹ 60 Lakh": "₹40L — ₹60 Lakh",
    "> ₹ 60 Lakh <= ₹ 90 Lakh": "₹60L — ₹90 Lakh",
    "> ₹ 90 Lakh ": "> ₹90 Lakh",
  },
  Vehicl_Cost_Range: {
    "<= ₹ 10 Lakh": "≤ ₹10 Lakh",
    "> ₹ 10 Lakh <= ₹ 20 Lakh": "₹10L — ₹20 Lakh",
    "> ₹ 20 Lakh <= ₹ 30 Lakh": "₹20L — ₹30 Lakh",
    "> ₹ 30 Lakh <= ₹ 40 Lakh": "₹30L — ₹40 Lakh",
    "> ₹ 40 Lakh ": "> ₹40 Lakh",
  },
  Annual_Miles_Range: {
    "<= 7.5 K": "≤ 7,500 miles",
    "> 7.5 K & <= 15 K": "7,500 - 15,000 miles",
    "> 15 K & <= 25 K": "15,000 - 25,000 miles",
    "> 25 K & <= 35 K": "25,000 - 35,000 miles",
    "> 35 K & <= 45 K": "35,000 - 45,000 miles",
    "> 45 K & <= 55 K": "45,000 - 55,000 miles",
    "> 55 K": "> 55,000 miles",
  },
  Marital_Status: {
    Dirvorced: "Divorced",
  },
};
type FieldDef = {
  key: string;
  label: string;
  type: "int" | "float" | "select" | "text";
};
const sections: { title: string; fields: FieldDef[] }[] = [
  {
    title: "Driver",
    fields: [
      { key: "Customer_Name", label: "Customer Name", type: "text" },
      { key: "Driver_Age", label: "Age", type: "int" },
      { key: "Driving_Exp", label: "Experience (years)", type: "int" },
      { key: "Gender", label: "Gender", type: "select" },
      { key: "Marital_Status", label: "Marital Status", type: "select" },
      { key: "Education", label: "Education", type: "select" },
    ],
  },
  {
    title: "History",
    fields: [
      { key: "Prev_Accidents", label: "Previous Accidents", type: "int" },
      { key: "Prev_Citations", label: "Previous Citations", type: "int" },
      { key: "Annual_Miles_Range", label: "Annual Kilometres", type: "select" },
      { key: "Region_State", label: "State (Risk Zone)", type: "select" },
    ],
  },
  {
    title: "Vehicle",
    fields: [
      { key: "Policy_Type", label: "Vehicle Type", type: "select" },
      { key: "Veh_Usage", label: "Vehicle Usage", type: "select" },
      { key: "Vehicl_Cost_Range", label: "Vehicle Cost", type: "select" },
      { key: "Coverage", label: "Coverage", type: "select" },
    ],
  },
  {
    title: "Premium",
    fields: [
      { key: "Sal_Range", label: "Salary Range", type: "select" },
      { key: "Quoted_Premium", label: "Quoted Premium (₹)", type: "int" },
      { key: "Agent_Type", label: "Agent Type", type: "select" },
      { key: "Re_Quote", label: "Re-Quote", type: "select" },
    ],
  },
];
export default function QuoteForm({ onSubmit, isLoading }: QuoteFormProps) {
  const [formData, setFormData] = useState<QuoteInput>(getDefaultQuoteInput());
  const [customerName, setCustomerName] = useState("");
  const [selectedState, setSelectedState] = useState("UP");
  const [selectedCity, setSelectedCity] = useState("");
  const [tab, setTab] = useState(0);
  const handleStateSelect = (stateCode: string, city: string) => {
    setSelectedState(stateCode);
    setSelectedCity(city);
    const stateData = INDIA_RISK_DATA.flatMap((g) => g.states).find(
      (s) => s.code === stateCode,
    );
    if (stateData) {
      setFormData((prev) => ({ ...prev, Region: stateData.regionCode }));
    }
  };
  const updateField = (key: string, value: string | number) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };
  const getDisplayFn = (key: string) => {
    const labels = DISPLAY_LABELS[key];
    if (!labels) return undefined;
    return (val: string) => labels[val] || val;
  };
  const getFieldValue = (key: string): string | number => {
    return formData[key as keyof QuoteInput] as string | number;
  };
  return (
    <div className="card p-6 md:p-8 relative overflow-visible">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-32 bg-white/[0.03] blur-[100px] pointer-events-none" />
      <div className="mb-8 relative z-10">
        <h2 className="text-lg font-light text-white mb-2 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-white/80" />
          New Quote
        </h2>
        <p className="text-sm text-white/40">
          Enter applicant details to run the autonomous evaluation pipeline.
        </p>
      </div>
      {/* Tabs */}
      <div className="flex gap-4 border-b border-white/[0.04] mb-8 relative z-10">
        {sections.map((s, i) => (
          <button
            key={i}
            onClick={() => setTab(i)}
            className={`pb-3 text-xs font-semibold transition-colors relative ${
              tab === i ? "text-white" : "text-white/40 hover:text-white/60"
            }`}
          >
            {s.title}
            {tab === i && (
              <motion.div
                layoutId="tab-underline"
                className="absolute -bottom-[1px] left-0 right-0 h-[2px] bg-white/20"
              />
            )}
          </button>
        ))}
      </div>
      {/* Fields */}
      <AnimatePresence mode="wait">
        <motion.div
          key={tab}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.15 }}
          className="space-y-3"
        >
          {sections[tab].fields.map((field) => {
            if (field.key === "Customer_Name") {
              return (
                <div key={field.key}>
                  <label className="text-xs font-medium text-white/60 ml-1 mb-2 block">
                    {field.label}
                  </label>
                  <input
                    type="text"
                    placeholder="Enter full name"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    className="w-full bg-white/[0.02] border border-white/[0.06] rounded-xl px-3 py-2 text-sm text-white/90 placeholder:text-white/20 focus:outline-none focus:border-white/20 focus:bg-white/[0.04] transition-all"
                  />
                </div>
              );
            }
            if (field.key === "Region_State") {
              return (
                <div key={field.key}>
                  <label className="text-xs font-medium text-white/60 ml-1 mb-2 block">
                    {field.label}
                  </label>
                  <StateTreeSelect
                    selectedState={selectedState}
                    selectedCity={selectedCity}
                    onSelect={handleStateSelect}
                  />
                </div>
              );
            }
            const rawVal = getFieldValue(field.key);
            return (
              <div key={field.key} className="mb-4">
                <label className="text-xs font-medium text-white/60 ml-1 mb-2 block">
                  {field.label}
                </label>
                {field.type === "select" ? (
                  <CustomSelect
                    value={String(rawVal)}
                    options={SELECT_OPTIONS[field.key] || []}
                    displayFn={getDisplayFn(field.key)}
                    onChange={(val) => updateField(field.key, val)}
                  />
                ) : (
                  <NumberInput
                    numericValue={rawVal as number}
                    placeholder={field.label}
                    step={field.type === "float" ? "0.5" : "1"}
                    onChange={(n) => updateField(field.key, n)}
                  />
                )}
              </div>
            );
          })}
        </motion.div>
      </AnimatePresence>
      <motion.button
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
        onClick={() => onSubmit(formData, customerName || "Unknown Applicant")}
        disabled={isLoading}
        className="w-full mt-8 py-4 bg-white text-black font-semibold rounded-xl disabled:opacity-50 flex items-center justify-center gap-2 hover:bg-white/90 transition-colors"
      >
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-black/20 border-t-black rounded-full animate-spin" />
            Evaluating Risk Profile...
          </>
        ) : (
          <>
            Generate Quote
            <ArrowRight className="w-4 h-4" />
          </>
        )}
      </motion.button>
    </div>
  );
}
