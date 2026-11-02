import os
import glob
import sqlite3
import yaml
import pandas as pd
import numpy as np

DB_PATH = "data/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"

def get_db_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def normalize_company_id(df: pd.DataFrame, col_name: str = "company_id") -> pd.DataFrame:
    """Trims spaces and converts company_id to uppercase."""
    if col_name in df.columns:
        df[col_name] = df[col_name].astype(str).str.strip().str.upper()
    return df

def clean_numeric(val):
    """Parses numeric values, stripping commas or currency characters."""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).replace(",", "").replace("₹", "").strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def calculate_cagr(start_val: float, end_val: float, periods: int) -> str | float:
    """Calculates CAGR; returns 'TURNAROUND' if the base year value is <= 0."""
    if pd.isna(start_val) or pd.isna(end_val) or start_val <= 0:
        return "TURNAROUND"
    return round((((end_val / start_val) ** (1 / periods)) - 1) * 100, 2)

def compute_interest_coverage(ebit: float, interest_expense: float) -> str | float:
    """Displays 'Debt Free' if interest expense is zero."""
    if pd.isna(interest_expense) or interest_expense == 0:
        return "Debt Free"
    return round(ebit / interest_expense, 2)

def run_pipeline():
    os.makedirs("output", exist_ok=True)
    conn = get_db_connection()
    
    excel_files = glob.glob("data/raw/*.xlsx") + glob.glob("data/raw/*.xls")
    if not excel_files:
        raise FileNotFoundError("No Excel files found in data/raw/. Please verify raw datasets are placed correctly.")
        
    audit_logs = []
    failures = []
    raw_dfs = []
    
    # Map common raw column aliases to standard internal keys
    col_map = {
        "Company ID": "company_id",
        "Symbol": "company_id",
        "Ticker": "company_id",
        "Company Name": "company_name",
        "Company": "company_name",
        "Sector": "sector",
        "Industry": "sector",
        "Revenue Base": "revenue_base",
        "Revenue 2023": "revenue_base",
        "Revenue End": "revenue_end",
        "Revenue 2026": "revenue_end",
        "Net Profit": "net_profit",
        "PAT": "net_profit",
        "Total Equity": "total_equity",
        "Shareholders Equity": "total_equity",
        "Total Debt": "total_debt",
        "Borrowings": "total_debt",
        "EBIT": "ebit",
        "Operating Profit": "ebit",
        "Interest Expense": "interest_expense",
        "Finance Costs": "interest_expense",
        "Stock Price": "stock_price",
        "CMP": "stock_price",
        "EPS": "eps"
    }

    for f in excel_files:
        try:
            # Enforce rule: pd.read_excel(path, header=1)
            df = pd.read_excel(f, header=1)
            df.rename(columns=lambda c: col_map.get(str(c).strip(), str(c).strip()), inplace=True)
            df = normalize_company_id(df)
            
            raw_dfs.append(df)
            audit_logs.append({"file_name": os.path.basename(f), "status": "SUCCESS", "rows": len(df)})
        except Exception as e:
            failures.append({"file_name": os.path.basename(f), "error": str(e)})
            audit_logs.append({"file_name": os.path.basename(f), "status": "FAILED", "rows": 0})
            
    pd.DataFrame(audit_logs).to_csv("output/load_audit.csv", index=False)
    pd.DataFrame(failures).to_csv("output/validation_failures.csv", index=False)
    
    df_base = pd.concat(raw_dfs, ignore_index=True)
    df_base = normalize_company_id(df_base)
    
    # Clean numeric fields
    numeric_cols = ["revenue_base", "revenue_end", "net_profit", "total_equity", "total_debt", "ebit", "interest_expense", "stock_price", "eps"]
    for col in numeric_cols:
        if col in df_base.columns:
            df_base[col] = df_base[col].apply(clean_numeric)
        else:
            df_base[col] = 0.0

    df_base.to_sql("companies", conn, if_exists="replace", index=False)
    
    # Process ratios
    ratios = []
    for _, row in df_base.iterrows():
        cagr = calculate_cagr(row["revenue_base"], row["revenue_end"], 3)
        interest_cov = compute_interest_coverage(row["ebit"], row["interest_expense"])
        
        roe = (row["net_profit"] / row["total_equity"] * 100) if row["total_equity"] > 0 else 0.0
        de_ratio = (row["total_debt"] / row["total_equity"]) if row["total_equity"] > 0 else 0.0
        pe_ratio = (row["stock_price"] / row["eps"]) if row["eps"] > 0 else 0.0
        
        ratios.append({
            "company_id": row["company_id"],
            "company_name": row.get("company_name", row["company_id"]),
            "sector": row.get("sector", "Unassigned"),
            "pe_ratio": round(pe_ratio, 2),
            "roe": round(roe, 2),
            "debt_to_equity": round(de_ratio, 2),
            "revenue_cagr_3yr": cagr,
            "interest_coverage": interest_cov
        })
        
    df_ratios = pd.DataFrame(ratios)
    df_ratios.to_sql("financial_ratios", conn, if_exists="replace", index=False)
    
    # Capital Allocation Output
    df_base["capital_allocated_inr_cr"] = df_base["total_equity"] + df_base["total_debt"]
    df_base[["company_id", "sector", "capital_allocated_inr_cr"]].to_csv(
        "output/capital_allocation.csv", index=False
    )
    
    # Stock Screener
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
        
    skip_sectors = config["filters"]["skip_de_sectors"]
    max_pe = config["filters"]["max_pe"]
    min_roe = config["filters"]["min_roe"]
    max_de = config["filters"]["max_debt_to_equity"]
    
    screener_results = []
    for _, row in df_ratios.iterrows():
        passes_pe = row["pe_ratio"] <= max_pe
        passes_roe = row["roe"] >= min_roe
        passes_de = True if row["sector"] in skip_sectors else (row["debt_to_equity"] <= max_de)
        
        if passes_pe and passes_roe and passes_de:
            screener_results.append(row.to_dict())
            
    pd.DataFrame(screener_results).to_excel("output/screener_output.xlsx", index=False)
    df_ratios.to_excel("output/peer_comparison.xlsx", index=False)
    df_base[["company_id", "stock_price", "eps"]].to_excel("output/valuation_summary.xlsx", index=False)
    df_base[["company_id", "ebit", "net_profit"]].to_excel("output/cashflow_intelligence.xlsx", index=False)
    
    conn.close()

if __name__ == "__main__":
    run_pipeline()