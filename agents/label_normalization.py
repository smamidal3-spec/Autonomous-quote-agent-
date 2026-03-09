"""Normalization helpers for salary, vehicle cost, coverage, and mileage labels.

The training data includes multiple string variants (including legacy mojibake
values). These helpers keep inference stable while making matching logic reusable.
"""

from __future__ import annotations


def _normalize(value: str | None) -> str:
    if value is None:
        return ""
    normalized = str(value).strip().lower()
    normalized = normalized.replace("₹", "inr")
    normalized = normalized.replace("â‚¹", "inr")
    normalized = normalized.replace("rs.", "inr")
    normalized = normalized.replace("rs ", "inr ")
    return " ".join(normalized.split())


LOW_SALARY_LABELS = {
    "<= â‚¹ 25 lakh",
    "<= inr 25 lakh",
    "<= rs 25 lakh",
    "<= 25 lakh",
}

HIGH_VEHICLE_COST_LABELS = {
    "> 30 k",
    "20 k - 30 k",
    "> â‚¹30 lakh",
    "â‚¹20l - â‚¹30l",
    "> â‚¹ 30 lakh <= â‚¹ 40 lakh",
    "> â‚¹ 40 lakh",
    "> â‚¹ 40 lakh ",
    "> inr 30 lakh <= inr 40 lakh",
    "> inr 40 lakh",
}

SALARY_NUMERIC_MAP = {
    "<= â‚¹ 25 lakh": 2.5,
    "<= inr 25 lakh": 2.5,
    "> â‚¹ 25 lakh <= â‚¹ 40 lakh": 3.75,
    "> inr 25 lakh <= inr 40 lakh": 3.75,
    "> â‚¹ 40 lakh <= â‚¹ 60 lakh": 6.25,
    "> inr 40 lakh <= inr 60 lakh": 6.25,
    "> â‚¹ 60 lakh <= â‚¹ 90 lakh": 8.75,
    "> inr 60 lakh <= inr 90 lakh": 8.75,
    "> â‚¹ 90 lakh": 12.5,
    "> â‚¹ 90 lakh ": 12.5,
    "> inr 90 lakh": 12.5,
}

VEHICLE_COST_NUMERIC_MAP = {
    "<= â‚¹ 10 lakh": 10,
    "<= inr 10 lakh": 10,
    "> â‚¹ 10 lakh <= â‚¹ 20 lakh": 15,
    "> inr 10 lakh <= inr 20 lakh": 15,
    "> â‚¹ 20 lakh <= â‚¹ 30 lakh": 25,
    "> inr 20 lakh <= inr 30 lakh": 25,
    "> â‚¹ 30 lakh <= â‚¹ 40 lakh": 35,
    "> inr 30 lakh <= inr 40 lakh": 35,
    "> â‚¹ 40 lakh": 40,
    "> â‚¹ 40 lakh ": 40,
    "> inr 40 lakh": 40,
}

COVERAGE_NUMERIC_MAP = {"basic": 1, "balanced": 2, "enhanced": 3}

MILES_NUMERIC_MAP = {
    "<= 7.5 k": 5,
    "> 7.5 k & <= 15 k": 11,
    "> 15 k & <= 25 k": 20,
    "> 25 k & <= 35 k": 30,
    "> 35 k & <= 45 k": 40,
    "> 45 k & <= 55 k": 50,
    "> 55 k": 60,
}


def is_low_salary(value: str | None) -> bool:
    return _normalize(value) in LOW_SALARY_LABELS


def is_high_vehicle_cost(value: str | None) -> bool:
    return _normalize(value) in HIGH_VEHICLE_COST_LABELS


def salary_to_numeric(value: str | None, default: float = 6.25) -> float:
    return SALARY_NUMERIC_MAP.get(_normalize(value), default)


def vehicle_cost_to_numeric(value: str | None, default: float = 15.0) -> float:
    return VEHICLE_COST_NUMERIC_MAP.get(_normalize(value), default)


def coverage_to_numeric(value: str | None, default: float = 2.0) -> float:
    return COVERAGE_NUMERIC_MAP.get(_normalize(value), default)


def miles_to_numeric(value: str | None, default: float = 11.0) -> float:
    return MILES_NUMERIC_MAP.get(_normalize(value), default)
