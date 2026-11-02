import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Nifty 100 Financial Intelligence", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect("data/nifty100.db")
    df_companies = pd.read_sql("SELECT * FROM companies", conn)
    df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
    conn.close()
    return df_companies, df_ratios

st.title("Nifty 100 Financial Analysis Dashboard")
st.warning("Note: Stock prices and market cap visualizers utilize SIMULATED datasets.")

df_comp, df_rat = load_data()

st.sidebar.title("Navigation")
screen = st.sidebar.radio("Select Screen", [
    "1. Overview & Screening",
    "2. Company Deep-Dive",
    "3. Financial Ratio Explorer",
    "4. Capital Allocation",
    "5. Valuation Analytics [SIMULATED]",
    "6. Sector Breakdown",
    "7. ML Clusters",
    "8. Executive Summary"
])

if screen.startswith("1"):
    st.header("Executive Screening Engine")
    st.dataframe(df_rat)
elif screen.startswith("2"):
    st.header("Company Deep-Dive")
    selected = st.selectbox("Select Company ID", df_comp["company_id"].unique())
    st.json(df_comp[df_comp["company_id"] == selected].to_dict(orient="records"))
elif screen.startswith("3"):
    st.header("Financial Ratio Matrix")
    st.scatter_chart(df_rat, x="pe_ratio", y="roe", color="sector")
elif screen.startswith("5"):
    st.header("Valuation Analytics (SIMULATED DATASET)")
    st.bar_chart(df_comp.set_index("company_id")["stock_price"])
else:
    st.header(screen)
    st.dataframe(df_comp.head(10))