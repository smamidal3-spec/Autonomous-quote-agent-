"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronRight, MapPin, AlertTriangle } from "lucide-react";
export const INDIA_RISK_DATA: {
  risk: string;
  color: string;
  dot: string;
  states: {
    code: string;
    name: string;
    regionCode: string;
    cities: string[];
  }[];
}[] = [
  {
    risk: "CRITICAL",
    color: "text-red-400 font-bold",
    dot: "bg-red-500",
    states: [
      {
        code: "UP",
        name: "Uttar Pradesh",
        regionCode: "A",
        cities: [
          "Lucknow",
          "Noida",
          "Agra",
          "Kanpur",
          "Varanasi",
          "Prayagraj",
          "Mathura",
          "Meerut",
          "Ghaziabad",
          "Aligarh",
          "Bareilly",
          "Moradabad",
          "Gorakhpur",
          "Firozabad",
          "Jhansi",
        ],
      },
      {
        code: "TN",
        name: "Tamil Nadu",
        regionCode: "A",
        cities: [
          "Chennai",
          "Coimbatore",
          "Madurai",
          "Salem",
          "Tiruchirappalli",
          "Tiruppur",
          "Vellore",
          "Erode",
          "Thoothukudi",
          "Thanjavur",
          "Dindigul",
          "Hosur",
        ],
      },
      {
        code: "DL",
        name: "Delhi NCR",
        regionCode: "A",
        cities: [
          "Outer Delhi",
          "East Delhi",
          "North Delhi",
          "South Delhi",
          "West Delhi",
          "Dwarka",
          "Rohini",
          "New Delhi",
          "Saket",
          "Lajpat Nagar",
        ],
      },
    ],
  },
  {
    risk: "VERY HIGH",
    color: "text-orange-400 font-semibold",
    dot: "bg-orange-500",
    states: [
      {
        code: "MH",
        name: "Maharashtra",
        regionCode: "B",
        cities: [
          "Pune",
          "Mumbai",
          "Thane",
          "Nagpur",
          "Nashik",
          "Aurangabad",
          "Solapur",
          "Kolhapur",
          "Navi Mumbai",
          "Pimpri-Chinchwad",
          "Akola",
          "Amravati",
          "Sangli",
          "Malegaon",
        ],
      },
      {
        code: "MP",
        name: "Madhya Pradesh",
        regionCode: "B",
        cities: [
          "Indore",
          "Bhopal",
          "Jabalpur",
          "Gwalior",
          "Ujjain",
          "Sagar",
          "Dewas",
          "Satna",
          "Ratlam",
          "Rewa",
          "Singrauli",
          "Burhanpur",
        ],
      },
      {
        code: "KA",
        name: "Karnataka",
        regionCode: "B",
        cities: [
          "Bengaluru",
          "Mysuru",
          "Hubli-Dharwad",
          "Mangaluru",
          "Belgaum",
          "Gulbarga",
          "Tumakuru",
          "Davangere",
          "Bellary",
          "Shimoga",
          "Raichur",
          "Bijapur",
        ],
      },
    ],
  },
  {
    risk: "HIGH",
    color: "text-amber-400",
    dot: "bg-amber-500",
    states: [
      {
        code: "RJ",
        name: "Rajasthan",
        regionCode: "C",
        cities: [
          "Jaipur",
          "Jodhpur",
          "Kota",
          "Udaipur",
          "Ajmer",
          "Bikaner",
          "Alwar",
          "Bhilwara",
          "Sikar",
          "Pali",
          "Sri Ganganagar",
          "Bharatpur",
        ],
      },
      {
        code: "TG",
        name: "Telangana",
        regionCode: "C",
        cities: [
          "Hyderabad",
          "Warangal",
          "Nizamabad",
          "Karimnagar",
          "Khammam",
          "Mahbubnagar",
          "Ramagundam",
          "Secunderabad",
          "Nalgonda",
          "Adilabad",
        ],
      },
      {
        code: "GJ",
        name: "Gujarat",
        regionCode: "C",
        cities: [
          "Ahmedabad",
          "Surat",
          "Vadodara",
          "Rajkot",
          "Bhavnagar",
          "Jamnagar",
          "Gandhinagar",
          "Junagadh",
          "Anand",
          "Navsari",
          "Morbi",
          "Mehsana",
        ],
      },
      {
        code: "BR",
        name: "Bihar",
        regionCode: "D",
        cities: [
          "Patna",
          "Gaya",
          "Bhagalpur",
          "Muzaffarpur",
          "Darbhanga",
          "Purnia",
          "Munger",
          "Arrah",
          "Begusarai",
          "Katihar",
          "Chapra",
          "Sasaram",
        ],
      },
      {
        code: "AP",
        name: "Andhra Pradesh",
        regionCode: "D",
        cities: [
          "Visakhapatnam",
          "Vijayawada",
          "Guntur",
          "Nellore",
          "Kurnool",
          "Tirupati",
          "Kakinada",
          "Rajahmundry",
          "Kadapa",
          "Anantapur",
          "Eluru",
          "Ongole",
        ],
      },
    ],
  },
  {
    risk: "MEDIUM-HIGH",
    color: "text-yellow-400",
    dot: "bg-yellow-400",
    states: [
      {
        code: "KL",
        name: "Kerala",
        regionCode: "D",
        cities: [
          "Thiruvananthapuram",
          "Kochi",
          "Kozhikode",
          "Thrissur",
          "Kollam",
          "Kannur",
          "Alappuzha",
          "Palakkad",
          "Malappuram",
          "Kottayam",
        ],
      },
      {
        code: "WB",
        name: "West Bengal",
        regionCode: "E",
        cities: [
          "Kolkata",
          "Howrah",
          "Siliguri",
          "Durgapur",
          "Asansol",
          "Darjeeling",
          "Bardhaman",
          "Malda",
          "Kharagpur",
          "Haldia",
          "Baharampur",
        ],
      },
    ],
  },
  {
    risk: "MEDIUM",
    color: "text-blue-400",
    dot: "bg-blue-400",
    states: [
      {
        code: "JH",
        name: "Jharkhand",
        regionCode: "E",
        cities: [
          "Ranchi",
          "Jamshedpur",
          "Dhanbad",
          "Bokaro",
          "Hazaribagh",
          "Deoghar",
          "Giridih",
          "Ramgarh",
        ],
      },
      {
        code: "OD",
        name: "Odisha",
        regionCode: "E",
        cities: [
          "Bhubaneswar",
          "Cuttack",
          "Rourkela",
          "Berhampur",
          "Sambalpur",
          "Puri",
          "Balasore",
          "Bhadrak",
        ],
      },
      {
        code: "PB",
        name: "Punjab",
        regionCode: "F",
        cities: [
          "Ludhiana",
          "Amritsar",
          "Jalandhar",
          "Patiala",
          "Bathinda",
          "Mohali",
          "Hoshiarpur",
          "Pathankot",
          "Moga",
          "Firozpur",
        ],
      },
      {
        code: "HR",
        name: "Haryana",
        regionCode: "F",
        cities: [
          "Faridabad",
          "Gurugram",
          "Panipat",
          "Ambala",
          "Hisar",
          "Rohtak",
          "Karnal",
          "Sonipat",
          "Yamunanagar",
          "Panchkula",
        ],
      },
      {
        code: "AS",
        name: "Assam",
        regionCode: "F",
        cities: [
          "Guwahati",
          "Dibrugarh",
          "Silchar",
          "Jorhat",
          "Tezpur",
          "Nagaon",
          "Tinsukia",
          "Bongaigaon",
        ],
      },
      {
        code: "CH",
        name: "Chhattisgarh",
        regionCode: "F",
        cities: [
          "Raipur",
          "Bhilai",
          "Bilaspur",
          "Durg",
          "Korba",
          "Rajnandgaon",
          "Jagdalpur",
          "Ambikapur",
        ],
      },
      {
        code: "UK",
        name: "Uttarakhand",
        regionCode: "G",
        cities: [
          "Dehradun",
          "Haridwar",
          "Haldwani",
          "Roorkee",
          "Rishikesh",
          "Kashipur",
          "Rudrapur",
          "Nainital",
          "Mussoorie",
        ],
      },
    ],
  },
  {
    risk: "MEDIUM-LOW",
    color: "text-white/80",
    dot: "bg-white/20",
    states: [
      {
        code: "JK",
        name: "Jammu & Kashmir",
        regionCode: "G",
        cities: [
          "Srinagar",
          "Jammu",
          "Anantnag",
          "Baramulla",
          "Sopore",
          "Kathua",
        ],
      },
      {
        code: "HP",
        name: "Himachal Pradesh",
        regionCode: "G",
        cities: [
          "Shimla",
          "Dharamshala",
          "Manali",
          "Kullu",
          "Mandi",
          "Solan",
          "Kangra",
          "Hamirpur",
        ],
      },
      {
        code: "GA",
        name: "Goa",
        regionCode: "H",
        cities: ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"],
      },
    ],
  },
  {
    risk: "LOW",
    color: "text-white/60",
    dot: "bg-white/20",
    states: [
      {
        code: "SK",
        name: "Sikkim",
        regionCode: "H",
        cities: ["Gangtok", "Namchi", "Mangan"],
      },
      {
        code: "MN",
        name: "Manipur",
        regionCode: "H",
        cities: ["Imphal", "Thoubal", "Bishnupur"],
      },
      {
        code: "NL",
        name: "Nagaland",
        regionCode: "H",
        cities: ["Kohima", "Dimapur", "Mokokchung"],
      },
      {
        code: "ML",
        name: "Meghalaya",
        regionCode: "H",
        cities: ["Shillong", "Tura", "Jowai"],
      },
      {
        code: "AR",
        name: "Arunachal Pradesh",
        regionCode: "H",
        cities: ["Itanagar", "Naharlagun", "Pasighat"],
      },
      {
        code: "MZ",
        name: "Mizoram",
        regionCode: "H",
        cities: ["Aizawl", "Lunglei"],
      },
      {
        code: "TR",
        name: "Tripura",
        regionCode: "H",
        cities: ["Agartala", "Udaipur", "Dharmanagar"],
      },
      {
        code: "PY",
        name: "Puducherry",
        regionCode: "H",
        cities: ["Puducherry", "Karaikal"],
      },
    ],
  },
];
interface StateTreeSelectProps {
  selectedState: string;
  selectedCity: string;
  onSelect: (stateCode: string, city: string) => void;
}
export default function StateTreeSelect({
  selectedState,
  selectedCity,
  onSelect,
}: StateTreeSelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [expandedState, setExpandedState] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const currentState = INDIA_RISK_DATA.flatMap((g) => g.states).find(
    (s) => s.code === selectedState,
  );
  const currentGroup = INDIA_RISK_DATA.find((g) =>
    g.states.some((s) => s.code === selectedState),
  );
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
        setExpandedState(null);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);
  return (
    <div ref={containerRef} className="relative">
      {/* Trigger */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between bg-white/[0.02] border border-white/[0.06] rounded-xl px-3 py-2 text-sm text-white/90 focus:outline-none focus:border-white/20 focus:bg-white/[0.04] transition-all"
      >
        <span className="truncate">
          {selectedCity && selectedState ? (
            <span>
              {selectedState}{" "}
              <span className="text-white/30 ml-2">— {selectedCity}</span>
            </span>
          ) : (
            <span className="text-white/20">Select Region & City</span>
          )}
        </span>
        <ChevronRight
          className={`w-4 h-4 text-white/40 transition-transform duration-200 ${isOpen ? "rotate-90" : ""}`}
        />
      </button>
      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute z-[100] w-full mt-2 bg-[#151518]/95 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl overflow-hidden"
          >
            <div className="max-h-[60vh] overflow-y-auto overscroll-contain custom-scrollbar mt-2 mb-2 pb-4">
              {INDIA_RISK_DATA.map((group) => (
                <div key={group.risk}>
                  {/* Risk Group Header */}
                  <div className="sticky top-0 bg-[#09090b]/90 backdrop-blur-sm border-b border-t first:border-t-0 border-white/[0.04] px-3 py-2 text-[10px] font-medium tracking-widest text-white/40 z-10 flex items-center gap-2 uppercase">
                    <div className={`w-1.5 h-1.5 rounded-full ${group.dot}`} />
                    {group.risk} ZONE
                  </div>
                  {/* States in this group */}
                  {group.states.map((state) => (
                    <div key={state.code} className="relative">
                      {/* State Row */}
                      <button
                        type="button"
                        onClick={() => {
                          setExpandedState(
                            expandedState === state.code ? null : state.code,
                          );
                        }}
                        className={`w-full px-3 py-2.5 text-left text-sm flex items-center justify-between transition-colors ${
                          expandedState === state.code
                            ? "bg-white/[0.04]"
                            : "hover:bg-white/[0.02]"
                        }`}
                      >
                        <span className="flex items-center gap-2">
                          <MapPin
                            className={`w-3.5 h-3.5 ${group.color.split(" ")[0]}`}
                          />
                          <span className="text-white/80">{state.name}</span>
                        </span>
                        <ChevronRight
                          className={`w-4 h-4 text-white/30 transition-transform duration-200 ${
                            expandedState === state.code ? "rotate-90" : ""
                          }`}
                        />
                      </button>
                      {/* Cities Tree (collapses under the state) */}
                      <AnimatePresence>
                        {expandedState === state.code && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: "auto", opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.2 }}
                            className="overflow-hidden"
                          >
                            <div className="pl-5 pr-2 pb-1 relative">
                              {/* Vertical tree line */}
                              <div className="absolute left-[18px] top-0 bottom-1 w-[1px] bg-white/10" />
                              {state.cities.map((city, ci) => (
                                <button
                                  key={city}
                                  type="button"
                                  onClick={() => {
                                    onSelect(state.code, city);
                                    setIsOpen(false);
                                    setExpandedState(null);
                                  }}
                                  className={`w-full text-left pl-4 py-2 text-[13px] flex items-center gap-2 transition-colors hover:bg-white/[0.04] relative ${
                                    selectedState === state.code &&
                                    selectedCity === city
                                      ? "text-white/80 bg-white/[0.03]"
                                      : "text-white/60"
                                  }`}
                                >
                                  {/* Horizontal branch line */}
                                  <div className="absolute left-[1px] top-1/2 w-3 h-[1px] bg-white/10" />
                                  <span className="text-[10px] text-white/20 tabular-nums w-4">
                                    {ci + 1}.
                                  </span>
                                  {city}
                                  {selectedState === state.code &&
                                    selectedCity === city && (
                                      <span className="ml-auto text-white/80">
                                        ✓
                                      </span>
                                    )}
                                </button>
                              ))}
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      `}</style>
    </div>
  );
}
