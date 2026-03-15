import streamlit as st
import pandas as pd
from src.data_loader import load_merged, load_poverty, load_gdp, load_unemployment
from src.charts import (
    chart_poverty_bar,
    chart_gdp_bar,
    chart_unemployment_bar,
    chart_scatter_poverty_gdp,
    chart_scatter_poverty_unemployment,
    chart_scatter_gdp_unemployment,
    chart_correlation_heatmap,
)
from src.correlation import get_pearson_stats, get_correlation_matrix

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PH Regional Data Dashboard",
    page_icon="🇵🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0F172A; color: #F1F5F9; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1E293B; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #334155;
    }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 13px !important; }
    [data-testid="stMetricValue"] { color: #F1F5F9 !important; font-size: 28px !important; }

    /* Headers */
    h1, h2, h3 { color: #F1F5F9 !important; }

    /* Divider */
    hr { border-color: #334155; }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] { color: #94A3B8; }
    .stTabs [aria-selected="true"] { color: #F1F5F9 !important; border-bottom-color: #E63946 !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] { border-radius: 10px; }

    /* Correlation badge */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_merged()

df = get_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇵🇭 PH Data Dashboard")
    st.markdown("Regional economic and social indicators across the Philippines.")
    st.divider()

    st.markdown("### 🔍 Filter Regions")
    all_regions = df["region_name"].tolist()
    selected_regions = st.multiselect(
        "Select regions to highlight:",
        options=all_regions,
        default=all_regions,
    )

    st.divider()
    st.markdown("### 📅 Data Year")
    st.info("All indicators: **2021**\nSource: PSA Philippines")

    st.divider()
    st.markdown("### 📊 About")
    st.markdown("""
    This dashboard explores the correlation between:
    - 🔴 Poverty Rate
    - 🔵 GRDP (Gross Regional Domestic Product)
    - 🟢 Unemployment Rate

    across all **17 Philippine regions**.
    """)

# ── Filter Data ───────────────────────────────────────────────────────────────
filtered_df = df[df["region_name"].isin(selected_regions)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🇵🇭 Philippines Regional Data Dashboard")
st.markdown("Exploring the relationship between **poverty**, **GDP**, and **unemployment** across regions.")
st.divider()

# ── KPI Metrics ───────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📍 Regions", f"{len(filtered_df)}")
with col2:
    st.metric("🔴 Avg Poverty Rate", f"{filtered_df['poverty_rate'].mean():.1f}%")
with col3:
    st.metric("🔵 Avg GRDP", f"₱{filtered_df['grdp'].mean():.0f}B")
with col4:
    st.metric("🟢 Avg Unemployment", f"{filtered_df['unemployment_rate'].mean():.1f}%")
with col5:
    highest_poverty = filtered_df.loc[filtered_df["poverty_rate"].idxmax(), "region_name"]
    st.metric("⚠️ Highest Poverty", highest_poverty.split()[0])

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📊 Regional Indicators",
    "🔗 Correlation Analysis",
    "📋 Data Table"
])

# ────────────────────────────────────────────────────────────────────────────
# TAB 1 — Regional Indicators
# ────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Regional Breakdown")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(chart_poverty_bar(filtered_df), use_container_width=True)
    with c2:
        st.plotly_chart(chart_gdp_bar(filtered_df), use_container_width=True)

    st.plotly_chart(chart_unemployment_bar(filtered_df), use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────
# TAB 2 — Correlation Analysis
# ────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Correlation Analysis")
    st.markdown("How strongly do poverty, GDP, and unemployment relate to each other across regions?")

    # Pearson stats table
    stats_data = get_pearson_stats(filtered_df)
    stats_df = pd.DataFrame(stats_data)
    stats_df.columns = ["Indicator Pair", "Pearson r", "P-Value", "Significant?", "Strength"]

    st.dataframe(
        stats_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # Heatmap
    st.plotly_chart(chart_correlation_heatmap(filtered_df), use_container_width=True)

    st.divider()

    # Scatter plots
    st.markdown("### Scatter Plots with Trend Lines")
    s1, s2 = st.columns(2)
    with s1:
        st.plotly_chart(chart_scatter_poverty_gdp(filtered_df), use_container_width=True)
    with s2:
        st.plotly_chart(chart_scatter_poverty_unemployment(filtered_df), use_container_width=True)

    st.plotly_chart(chart_scatter_gdp_unemployment(filtered_df), use_container_width=True)

    # Insights box
    st.divider()
    st.markdown("### 💡 Key Insights")
    st.info("""
    **What the data tells us:**

    🔴 **Poverty vs GRDP (r = -0.63):** Regions with higher economic output tend to have lower poverty rates — but the relationship isn't perfect, suggesting GDP growth alone doesn't eliminate poverty.

    🟢 **Poverty vs Unemployment (r = -0.76):** Surprisingly negative — regions with lower unemployment (like BARMM) still have high poverty, suggesting underemployment and informal work are bigger issues than unemployment itself.

    🔵 **GRDP vs Unemployment (r = +0.80):** Urban economic hubs like NCR have both high GDP *and* high unemployment — driven by a larger formal labor market and more people actively seeking work.
    """)

# ────────────────────────────────────────────────────────────────────────────
# TAB 3 — Data Table
# ────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### Raw Data")

    display_df = filtered_df.copy()
    display_df.columns = ["Region Code", "Region Name", "Poverty Rate (%)", "GRDP (₱B)", "Unemployment Rate (%)"]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Filtered Data (CSV)",
            data=csv,
            file_name="ph_regional_data.csv",
            mime="text/csv",
        )
    with col_dl2:
        st.markdown("📌 **Sources:** PSA Philippines, NSCB Regional Accounts")