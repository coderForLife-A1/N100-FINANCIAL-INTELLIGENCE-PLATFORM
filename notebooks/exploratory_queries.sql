-- D-04 Deliverable: 10 Exploratory & Analytical SQL Queries

-- Query 1: Top 10 Companies by Return on Equity (ROE)
SELECT company_id, company_name, sector, roe 
FROM financial_ratios 
ORDER BY roe DESC 
LIMIT 10;

-- Query 2: Sector-wise Average P/E Ratio excluding Financials
SELECT sector, ROUND(AVG(pe_ratio), 2) AS avg_pe 
FROM financial_ratios 
WHERE sector NOT IN ('Financial Services', 'Financials', 'Banking') 
GROUP BY sector 
ORDER BY avg_pe ASC;

-- Query 3: Identify Companies with TURNAROUND 3-Year Revenue CAGR
SELECT company_id, company_name, sector, revenue_cagr_3yr 
FROM financial_ratios 
WHERE revenue_cagr_3yr = 'TURNAROUND';

-- Query 4: Zero-Interest Expense (Debt Free) Companies
SELECT company_id, company_name, sector, interest_coverage 
FROM financial_ratios 
WHERE interest_coverage = 'Debt Free';

-- Query 5: High-Leverage Companies (Debt to Equity > 2.0)
SELECT company_id, company_name, sector, debt_to_equity 
FROM financial_ratios 
WHERE debt_to_equity > 2.0 AND sector NOT IN ('Financial Services', 'Banking') 
ORDER BY debt_to_equity DESC;

-- Query 6: Companies Meeting Core Screener Filter Criteria
SELECT company_id, company_name, pe_ratio, roe, debt_to_equity 
FROM financial_ratios 
WHERE pe_ratio <= 35.0 AND roe >= 15.0 AND (debt_to_equity <= 1.0 OR sector = 'Financials');

-- Query 7: Total Capital Allocated per Sector (in INR Crore)
SELECT sector, SUM(total_equity + total_debt) AS total_capital_inr_cr 
FROM companies 
GROUP BY sector 
ORDER BY total_capital_inr_cr DESC;

-- Query 8: Bottom 5 Undervalued Companies by Low P/E with ROE > 10%
SELECT company_id, company_name, pe_ratio, roe 
FROM financial_ratios 
WHERE pe_ratio > 0 AND roe > 10.0 
ORDER BY pe_ratio ASC 
LIMIT 5;

-- Query 9: Average Interest Coverage Ratio by Sector
SELECT sector, ROUND(AVG(CAST(interest_coverage AS FLOAT)), 2) AS avg_interest_coverage 
FROM financial_ratios 
WHERE interest_coverage != 'Debt Free' 
GROUP BY sector;

-- Query 10: Aggregated Nifty 100 Financial Overview
SELECT 
    COUNT(company_id) AS total_companies,
    ROUND(AVG(pe_ratio), 2) AS market_avg_pe,
    ROUND(AVG(roe), 2) AS market_avg_roe
FROM financial_ratios;