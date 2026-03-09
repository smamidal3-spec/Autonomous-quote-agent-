from agents.label_normalization import (
    coverage_to_numeric,
    is_high_vehicle_cost,
    is_low_salary,
    miles_to_numeric,
    salary_to_numeric,
    vehicle_cost_to_numeric,
)


def test_salary_normalization() -> None:
    assert is_low_salary("<= INR 25 Lakh")
    assert salary_to_numeric("<= ₹ 25 Lakh") == 2.5


def test_vehicle_cost_normalization() -> None:
    assert is_high_vehicle_cost("> ₹ 40 Lakh ")
    assert vehicle_cost_to_numeric("> ₹ 20 Lakh <= ₹ 30 Lakh") == 25


def test_coverage_and_miles_numeric_mapping() -> None:
    assert coverage_to_numeric("Balanced") == 2
    assert miles_to_numeric("> 35 K & <= 45 K") == 40
