import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


# ── Shared color palette ──────────────────────────────────────────────────────
ACCENT = "#E63946"       # red for poverty
BLUE   = "#457B9D"       # blue for GDP
GREEN  = "#2A9D8F"       # green for unemployment
BG     = "#0F172A"       # dark navy background
CARD   = "#1E293B"       # card background
TEXT   = "#F1F5F9"       # light text

CHART_LAYOUT = dict(
    paper_bgcolor=BG,
    plot_bgcolor=CARD,
    font=dict(color=TEXT, family="Inter, sans-serif"),
    margin=dict(l=40, r=40, t=60, b=40),
)


# ── 1. Horizontal Bar — Poverty Rate by Region ────────────────────────────────
def chart_poverty_bar(df: pd.DataFrame) -> go.Figure:
    df_sorted = df.sort_values("poverty_rate", ascending=True)
    fig = px.bar(
        df_sorted,
        x="poverty_rate",
        y="region_name",
        orientation="h",
        title="Poverty Rate by Region (2021)",
        labels={"poverty_rate": "Poverty Rate (%)", "region_name": ""},
        color="poverty_rate",
        color_continuous_scale=["#457B9D", "#E63946"],
    )
    fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Poverty Rate: %{x}%<extra></extra>")
    return fig


# ── 2. Horizontal Bar — GRDP by Region ───────────────────────────────────────
def chart_gdp_bar(df: pd.DataFrame) -> go.Figure:
    df_sorted = df.sort_values("grdp", ascending=True)
    fig = px.bar(
        df_sorted,
        x="grdp",
        y="region_name",
        orientation="h",
        title="Gross Regional Domestic Product by Region (2021, Billion PHP)",
        labels={"grdp": "GRDP (Billion PHP)", "region_name": ""},
        color="grdp",
        color_continuous_scale=["#1E293B", "#457B9D"],
    )
    fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig.update_traces(hovertemplate="<b>%{y}</b><br>GRDP: ₱%{x}B<extra></extra>")
    return fig


# ── 3. Horizontal Bar — Unemployment Rate by Region ──────────────────────────
def chart_unemployment_bar(df: pd.DataFrame) -> go.Figure:
    df_sorted = df.sort_values("unemployment_rate", ascending=True)
    fig = px.bar(
        df_sorted,
        x="unemployment_rate",
        y="region_name",
        orientation="h",
        title="Unemployment Rate by Region (2021)",
        labels={"unemployment_rate": "Unemployment Rate (%)", "region_name": ""},
        color="unemployment_rate",
        color_continuous_scale=["#1E293B", "#2A9D8F"],
    )
    fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Unemployment: %{x}%<extra></extra>")
    return fig


# ── 4. Scatter — Poverty vs GRDP ─────────────────────────────────────────────
def chart_scatter_poverty_gdp(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="grdp",
        y="poverty_rate",
        text="region_code",
        title="Correlation: Poverty Rate vs GRDP",
        labels={"grdp": "GRDP (Billion PHP)", "poverty_rate": "Poverty Rate (%)"},
        trendline="ols",
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(
        textposition="top center",
        marker=dict(size=10),
        hovertemplate="<b>%{text}</b><br>GRDP: ₱%{x}B<br>Poverty: %{y}%<extra></extra>"
    )
    fig.update_layout(**CHART_LAYOUT)
    return fig


# ── 5. Scatter — Poverty vs Unemployment ────────────────────────────────────
def chart_scatter_poverty_unemployment(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="unemployment_rate",
        y="poverty_rate",
        text="region_code",
        title="Correlation: Poverty Rate vs Unemployment Rate",
        labels={"unemployment_rate": "Unemployment Rate (%)", "poverty_rate": "Poverty Rate (%)"},
        trendline="ols",
        color_discrete_sequence=[GREEN],
    )
    fig.update_traces(
        textposition="top center",
        marker=dict(size=10),
        hovertemplate="<b>%{text}</b><br>Unemployment: %{x}%<br>Poverty: %{y}%<extra></extra>"
    )
    fig.update_layout(**CHART_LAYOUT)
    return fig


# ── 6. Scatter — GDP vs Unemployment ────────────────────────────────────────
def chart_scatter_gdp_unemployment(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="grdp",
        y="unemployment_rate",
        text="region_code",
        title="Correlation: GRDP vs Unemployment Rate",
        labels={"grdp": "GRDP (Billion PHP)", "unemployment_rate": "Unemployment Rate (%)"},
        trendline="ols",
        color_discrete_sequence=[BLUE],
    )
    fig.update_traces(
        textposition="top center",
        marker=dict(size=10),
        hovertemplate="<b>%{text}</b><br>GRDP: ₱%{x}B<br>Unemployment: %{y}%<extra></extra>"
    )
    fig.update_layout(**CHART_LAYOUT)
    return fig


# ── 7. Correlation Heatmap ───────────────────────────────────────────────────
def chart_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    cols = ["poverty_rate", "grdp", "unemployment_rate"]
    labels = ["Poverty Rate", "GRDP", "Unemployment Rate"]
    corr = df[cols].corr().round(2)

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale="RdBu",
        zmid=0,
        text=corr.values,
        texttemplate="%{text}",
        hovertemplate="%{y} vs %{x}: %{z}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title="Correlation Heatmap (All Indicators)",
    )
    return fig