# Nifty 100 Financial Analytics - Data Dictionary

## Table: `companies`
Primary raw ingested dataset containing entity information and basic financial metrics. All monetary figures are in **INR Crore**.

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `company_id` | TEXT (PK) | Standardized, uppercase unique entity ticker/ID. |
| `company_name` | TEXT | Official registered corporate name. |
| `sector` | TEXT | Industry sector classification. |
| `revenue_base` | REAL | T-3 Base year revenue (INR Crore). |
| `revenue_end` | REAL | Current period revenue (INR Crore). |
| `net_profit` | REAL | Profit After Tax / PAT (INR Crore). |
| `total_equity` | REAL | Shareholders' total equity (INR Crore). |
| `total_debt` | REAL | Total outstanding long-term and short-term debt (INR Crore). |
| `ebit` | REAL | Earnings Before Interest and Taxes (INR Crore). |
| `interest_expense` | REAL | Annual finance/interest charges (INR Crore). |
| `stock_price` | REAL | Current Market Price / CMP (INR). |
| `eps` | REAL | Earnings Per Share (INR). |
| `capital_allocated_inr_cr` | REAL | Total Capital Employed (`total_equity` + `total_debt`). |

## Table: `financial_ratios`
Computed analytical metrics table populated during Sprint 2.

| Field Name | Data Type | Description | Special Edge-Case Values |
| :--- | :--- | :--- | :--- |
| `company_id` | TEXT (FK) | Normalized company ID. | — |
| `pe_ratio` | REAL | Price-to-Earnings Ratio (`stock_price` / `eps`). | `0.0` if EPS <= 0. |
| `roe` | REAL | Return on Equity % (`net_profit` / `total_equity` * 100). | `0.0` if Equity <= 0. |
| `debt_to_equity` | REAL | Leverage Ratio (`total_debt` / `total_equity`). | Excluded during screener for Financials. |
| `revenue_cagr_3yr` | TEXT/REAL | 3-Year Compound Annual Growth Rate. | `'TURNAROUND'` if `revenue_base` <= 0. |
| `interest_coverage`| TEXT/REAL | Debt Service Ability (`ebit` / `interest_expense`). | `'Debt Free'` if `interest_expense` == 0. |