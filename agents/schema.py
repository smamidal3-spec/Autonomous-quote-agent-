from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class AgentType(str, Enum):
    EA = "EA"
    IA = "IA"


class GenderOpt(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class MaritalStatus(str, Enum):
    WIDOW = "Widow"
    DIVORCED = "Dirvorced"
    MARRIED = "Married"
    SINGLE = "Single"


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "High School"
    COLLEGE = "College"
    BACHELORS = "Bachelors"
    MASTERS = "Masters"
    PHD = "Ph.D"


class SalaryRange(str, Enum):
    R1 = "<= ₹ 25 Lakh"
    R2 = "> ₹ 25 Lakh <= ₹ 40 Lakh"
    R3 = "> ₹ 40 Lakh <= ₹ 60 Lakh"
    R4 = "> ₹ 60 Lakh <= ₹ 90 Lakh"
    R5 = "> ₹ 90 Lakh "


class CoverageType(str, Enum):
    BASIC = "Basic"
    BALANCED = "Balanced"
    ENHANCED = "Enhanced"


class VehicleUsage(str, Enum):
    COMMUTE = "Commute"
    PLEASURE = "Pleasure"
    BUSINESS = "Business"


class AnnualMiles(str, Enum):
    M1 = "<= 7.5 K"
    M2 = "> 7.5 K & <= 15 K"
    M3 = "> 15 K & <= 25 K"
    M4 = "> 25 K & <= 35 K"
    M5 = "> 35 K & <= 45 K"
    M6 = "> 45 K & <= 55 K"
    M7 = "> 55 K"


class VehicleCost(str, Enum):
    C1 = "<= ₹ 10 Lakh"
    C2 = "> ₹ 10 Lakh <= ₹ 20 Lakh"
    C3 = "> ₹ 20 Lakh <= ₹ 30 Lakh"
    C4 = "> ₹ 30 Lakh <= ₹ 40 Lakh"
    C5 = "> ₹ 40 Lakh "


class ReQuoteOpt(str, Enum):
    NO = "No"
    YES = "Yes"


class PolicyType(str, Enum):
    CAR = "Car"
    VAN = "Van"
    TRUCK = "Truck"


class QuoteInput(BaseModel):
    Agent_Type: AgentType = AgentType.EA
    Q_Creation_DT: str = "2019/10/01"
    Q_Valid_DT: str = "2023/12/31"
    Policy_Bind_DT: str = "2019/10/02"
    Region: str = "A"
    Agent_Num: int = 10
    Policy_Type: PolicyType = PolicyType.TRUCK
    HH_Vehicles: int = 1
    HH_Drivers: int = 1
    Driver_Age: int = 30
    Driving_Exp: int = 5
    Prev_Accidents: int = 0
    Prev_Citations: int = 0
    Gender: GenderOpt = GenderOpt.MALE
    Marital_Status: MaritalStatus = MaritalStatus.MARRIED
    Education: EducationLevel = EducationLevel.BACHELORS
    Sal_Range: SalaryRange = SalaryRange.R2
    Coverage: CoverageType = CoverageType.BALANCED
    Veh_Usage: VehicleUsage = VehicleUsage.BUSINESS
    Annual_Miles_Range: AnnualMiles = AnnualMiles.M1
    Vehicl_Cost_Range: VehicleCost = VehicleCost.C2
    Re_Quote: ReQuoteOpt = ReQuoteOpt.NO
    Quoted_Premium: int = 1000


class RiskOutput(BaseModel):
    risk_score: float
    risk_tier: str
    risk_explanation: str


class FraudOutput(BaseModel):
    fraud_risk_score: float
    fraud_flag: bool
    fraud_reason_codes: List[str]
    rule_flags: Optional[List[str]] = []
    decision: Optional[str] = "CLEAR"


class ConversionOutput(BaseModel):
    conversion_probability: float
    conversion_band: str
    top_conversion_drivers: List[str]


class PersonalizationOutput(BaseModel):
    recommended_plan: str
    coverage_level: str
    recommended_addons: List[str]
    personalization_score: float


class PremiumOutput(BaseModel):
    premium_issue: bool
    recommended_premium_range: List[float]
    recommendation_reason: str


class RoutingExplanation(BaseModel):
    risk_factor: str
    conversion_driver: str
    premium_issue: str


class DecisionOutput(BaseModel):
    decision: str
    confidence_score: float
    decision_explanation: str
    detailed_explanation: Optional[RoutingExplanation] = None


class EscalationOutput(BaseModel):
    escalation_required: bool
    reason: str


class PipelineOutput(BaseModel):
    quote_id: str
    risk_evaluation: RiskOutput
    fraud_detection: Optional[FraudOutput] = None
    conversion_prediction: ConversionOutput
    personalization: Optional[PersonalizationOutput] = None
    premium_advice: PremiumOutput
    final_decision: DecisionOutput
    escalation_status: EscalationOutput
