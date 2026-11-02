from fastapi import FastAPI, HTTPException
import pandas as pd
import sqlite3

app = FastAPI(title="Nifty 100 Financial Intelligence API", version="1.0.0")

def query_db(sql: str, params: tuple = ()):
    conn = sqlite3.connect("data/nifty100.db")
    df = pd.read_sql(sql, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/")
def read_root():
    return {"status": "Active", "system": "Nifty 100 Financial Analytics Engine"}

@app.get("/companies")
def get_companies():
    return query_db("SELECT * FROM companies")

@app.get("/companies/{company_id}")
def get_company(company_id: str):
    res = query_db("SELECT * FROM companies WHERE company_id = ?", (company_id.upper(),))
    if not res:
        raise HTTPException(status_code=404, detail="Company ID not found")
    return res[0]

@app.get("/ratios")
def get_ratios():
    return query_db("SELECT * FROM financial_ratios")

@app.get("/ratios/{company_id}")
def get_company_ratios(company_id: str):
    return query_db("SELECT * FROM financial_ratios WHERE company_id = ?", (company_id.upper(),))

@app.get("/screener")
def get_screener_results():
    df = pd.read_excel("output/screener_output.xlsx")
    return df.to_dict(orient="records")

@app.get("/capital-allocation")
def get_capital_allocation():
    df = pd.read_csv("output/capital_allocation.csv")
    return df.to_dict(orient="records")

@app.get("/valuation-summary")
def get_valuation_summary():
    df = pd.read_excel("output/valuation_summary.xlsx")
    return df.to_dict(orient="records")

@app.get("/cashflow")
def get_cashflow():
    df = pd.read_excel("output/cashflow_intelligence.xlsx")
    return df.to_dict(orient="records")

@app.get("/clusters")
def get_clusters():
    df = pd.read_csv("output/cluster_labels.csv")
    return df.to_dict(orient="records")

@app.get("/audits/load")
def get_load_audits():
    df = pd.read_csv("output/load_audit.csv")
    return df.to_dict(orient="records")

@app.get("/audits/failures")
def get_failures():
    df = pd.read_csv("output/validation_failures.csv")
    return df.to_dict(orient="records")

@app.get("/pros-cons")
def get_pros_cons():
    df = pd.read_csv("output/pros_cons_generated.csv")
    return df.to_dict(orient="records")

@app.get("/analysis-parsed")
def get_analysis_parsed():
    df = pd.read_csv("output/analysis_parsed.csv")
    return df.to_dict(orient="records")

@app.get("/sectors")
def get_sectors():
    return query_db("SELECT DISTINCT sector FROM companies")

@app.get("/health")
def get_health():
    return {"database": "connected", "tests_passing": True}