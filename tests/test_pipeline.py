import pytest
import pandas as pd
from src.data_pipeline import normalize_company_id, calculate_cagr, compute_interest_coverage

def test_company_id_normalization():
    df = pd.DataFrame({"company_id": [" comp_001 ", "comp_002", "COMP_003 "]})
    normalized = normalize_company_id(df)
    assert list(normalized["company_id"]) == ["COMP_001", "COMP_002", "COMP_003"]

def test_cagr_turnaround_on_negative_base():
    # Rule: If CAGR has a negative base year, return TURNAROUND
    result = calculate_cagr(start_val=-50.0, end_val=100.0, periods=3)
    assert result == "TURNAROUND"

def test_cagr_normal_calculation():
    result = calculate_cagr(start_val=100.0, end_val=133.1, periods=3)
    assert round(result, 1) == 10.0

def test_interest_coverage_zero_debt():
    # Rule: If Interest Expense = 0, display Debt Free
    result = compute_interest_coverage(ebit=500.0, interest_expense=0.0)
    assert result == "Debt Free"

def test_interest_coverage_normal():
    result = compute_interest_coverage(ebit=500.0, interest_expense=50.0)
    assert result == 10.0