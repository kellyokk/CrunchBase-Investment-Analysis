import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


st.set_page_config(page_title="Crunchbase Investor Dashboard", layout="wide")

st.title("Venture Capital Investor Dashboard")

#connect to sqlite
conn = sqlite3.connect("crunchbase.db")

query = """
WITH investor_company AS (
    SELECT DISTINCT
        investor_name,
        company_name,
        company_category_code,
        raised_amount_usd
    FROM investments
    WHERE investor_name IS NOT NULL
),

investor_counts AS (
    SELECT
        investor_name,
        COUNT(DISTINCT company_name) AS portfolio_companies,
        SUM(raised_amount_usd) AS total_deployed
    FROM investor_company
    GROUP BY investor_name
),

sector_rank AS (
    SELECT
        investor_name,
        company_category_code,
        COUNT(*) AS sector_count,
        ROW_NUMBER() OVER (
            PARTITION BY investor_name
            ORDER BY COUNT(*) DESC
        ) AS rn
    FROM investor_company
    GROUP BY investor_name, company_category_code
),

top_sector AS (
    SELECT
        investor_name,
        company_category_code AS top_sector
    FROM sector_rank
    WHERE rn = 1
)

SELECT
    ic.investor_name,
    ic.portfolio_companies,
    ts.top_sector,
    ic.total_deployed
FROM investor_counts ic
JOIN top_sector ts
    ON ic.investor_name = ts.investor_name
WHERE ic.portfolio_companies >= 10
"""

df = pd.read_sql(query, conn)

#clean
df["total_deployed"] = pd.to_numeric(df["total_deployed"], errors="coerce")

#sidebar filter
st.sidebar.header("Filters")

min_companies = st.sidebar.slider(
    "Minimum Portfolio Companies",
    10, int(df["portfolio_companies"].max()), 10
)

df = df[df["portfolio_companies"] >= min_companies]

#top metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Investors", len(df))
col2.metric("Total Capital Deployed", f"${df['total_deployed'].sum():,.0f}")
col3.metric("Avg Portfolio Size", f"{df['portfolio_companies'].mean():.1f}")

#big players - top investors
st.subheader("Top Investors")
st.dataframe(df.sort_values("total_deployed", ascending=False))

#visualize capital deployment by investors, see top investors- barchart
st.subheader("Capital Deployment by Investor")

top_df = df.sort_values("total_deployed", ascending=False).head(15)

fig1 = px.bar(
    top_df,
    x="investor_name",
    y="total_deployed",
    color="top_sector",
    title="Top Investors by Total Capital Deployed"
)

st.plotly_chart(fig1, use_container_width=True)

#sector distribution
st.subheader("Investor Focus by Sector")

sector_counts = df["top_sector"].value_counts().reset_index()
sector_counts.columns = ["sector", "count"]

fig2 = px.pie(
    sector_counts,
    names="sector",
    values="count",
    title="Most Common Investor Focus Areas"
)

st.plotly_chart(fig2, use_container_width=True)

#scatterplot of porfolio - capital relationship
st.subheader("Portfolio Size vs Capital Deployed")

fig3 = px.scatter(
    df,
    x="portfolio_companies",
    y="total_deployed",
    color="top_sector",
    hover_data=["investor_name"],
    title="Investor Strategy Map"
)

st.plotly_chart(fig3, use_container_width=True)