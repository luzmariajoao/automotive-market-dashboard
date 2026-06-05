"""
European Car Market Dashboard
Estilo executivo — fonte: ACEA, JATO, S&P Global Mobility (2024/2025)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from loader import (
    load_sales_by_country, load_top_brands, load_top_models,
    load_manufacturer_groups, load_fuel_type_mix, load_segment_share,
    load_co2_by_country, load_production_by_country, build_yoy_comparison,
)

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="European Car Market",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Palette ───────────────────────────────────────────────────────────────────
BLUE   = "#185FA5"
TEAL   = "#1D9E75"
CORAL  = "#D85A30"
AMBER  = "#BA7517"
GRAY   = "#888780"
COLORS = [BLUE, TEAL, CORAL, AMBER, "#534AB7", "#993556", "#3B6D11", "#854F0B", "#A32D2D", "#0F6E56"]

st.markdown("""
<style>
    .kpi-label  { font-size: 13px; color: #888780; margin-bottom: 2px; }
    .kpi-value  { font-size: 28px; font-weight: 600; color: #1a1a1a; line-height: 1.1; }
    .kpi-delta  { font-size: 12px; margin-top: 2px; }
    .kpi-up     { color: #1D9E75; }
    .kpi-down   { color: #D85A30; }
    .section-title { font-size: 16px; font-weight: 600; color: #1a1a1a; margin: 8px 0 4px; }
    .data-note  { font-size: 11px; color: #aaa; margin-top: 4px; }
    .spg-banner { background: #f5f5f5; border-left: 3px solid #185FA5;
                  padding: 16px 20px; border-radius: 4px; }
    .spg-title  { font-size: 15px; font-weight: 600; color: #185FA5; }
    .spg-body   { font-size: 13px; color: #555; margin-top: 6px; line-height: 1.6; }
    div[data-testid="stMetric"] { background: #f9f9f9; border-radius: 8px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🚗 European Car Market Dashboard")
st.markdown("**2024 – 2025 · 31 markets · Source: ACEA / JATO Dynamics / S&P Global Mobility**")
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
countries_24 = load_sales_by_country(2024)
countries_25 = load_sales_by_country(2025)
brands_24    = load_top_brands(2024)
brands_25    = load_top_brands(2025)
models       = load_top_models()
fuel         = load_fuel_type_mix()
segments     = load_segment_share()
co2          = load_co2_by_country()
production   = load_production_by_country()
yoy          = build_yoy_comparison()

# ── KPI Row ───────────────────────────────────────────────────────────────────
total_24 = countries_24["sales_2024"].sum()
total_25 = countries_25["sales_2025"].sum()
delta_pct = ((total_25 - total_24) / total_24) * 100

top_brand    = brands_25.iloc[0]["brand"]
bev_24       = fuel[fuel["year"] == 2024]["bev_pct"].values[0]
suv_share    = segments[segments["segment"] == "SUV"]["share_pct"].values[0]
top_model    = models.iloc[0]["model"]
top_brand_m  = models.iloc[0]["brand"]

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f'<div class="kpi-label">Total sales 2025</div>'
                f'<div class="kpi-value">{total_25/1e6:.1f}M</div>'
                f'<div class="kpi-delta kpi-up">▲ {delta_pct:.1f}% vs 2024</div>',
                unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-label">Top brand 2025</div>'
                f'<div class="kpi-value">{top_brand}</div>'
                f'<div class="kpi-delta" style="color:#888">#{1} Europe</div>',
                unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-label">Top model 2024</div>'
                f'<div class="kpi-value">{top_model}</div>'
                f'<div class="kpi-delta" style="color:#888">{top_brand_m}</div>',
                unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-label">BEV share 2024</div>'
                f'<div class="kpi-value">{bev_24}%</div>'
                f'<div class="kpi-delta kpi-down">▼ vs 15.5% in 2023</div>',
                unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="kpi-label">SUV dominance 2024</div>'
                f'<div class="kpi-value">{suv_share}%</div>'
                f'<div class="kpi-delta" style="color:#888">of all EU sales</div>',
                unsafe_allow_html=True)

st.divider()

# ── Row 1: Map + Top Brands ───────────────────────────────────────────────────
col_map, col_brands = st.columns([1.4, 1])

with col_map:
    st.markdown('<div class="section-title">New car registrations by country — 2025</div>',
                unsafe_allow_html=True)

    iso_map = {
        "Austria":"AUT","Belgium":"BEL","Bulgaria":"BGR","Croatia":"HRV",
        "Cyprus":"CYP","Czechia":"CZE","Denmark":"DNK","Estonia":"EST",
        "Finland":"FIN","France":"FRA","Germany":"DEU","Greece":"GRC",
        "Hungary":"HUN","Ireland":"IRL","Italy":"ITA","Latvia":"LVA",
        "Lithuania":"LTU","Luxembourg":"LUX","Malta":"MLT","Netherlands":"NLD",
        "Poland":"POL","Portugal":"PRT","Romania":"ROU","Slovakia":"SVK",
        "Slovenia":"SVN","Spain":"ESP","Sweden":"SWE","Iceland":"ISL",
        "Norway":"NOR","Switzerland":"CHE","United Kingdom":"GBR",
    }
    map_df = countries_25.copy()
    map_df["iso"] = map_df["country"].map(iso_map)
    map_df = map_df.dropna(subset=["iso"])

    fig_map = px.choropleth(
        map_df,
        locations="iso",
        color="sales_2025",
        hover_name="country",
        hover_data={"sales_2025": ":,.0f", "pct_change": ":.1f", "iso": False},
        color_continuous_scale=[[0, "#E6F1FB"], [0.3, "#85B7EB"],
                                 [0.6, "#378ADD"], [1, "#042C53"]],
        scope="europe",
        labels={"sales_2025": "Sales 2025", "pct_change": "YoY %"},
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=360,
        coloraxis_colorbar=dict(
            title="Sales",
            tickformat=".2s",
            len=0.7,
        ),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor="rgba(0,0,0,0)",
            projection_scale=1.3,
            center=dict(lat=54, lon=14),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('<div class="data-note">Source: ACEA 2025 full-year</div>',
                unsafe_allow_html=True)

with col_brands:
    st.markdown('<div class="section-title">Top 10 brands — 2025 vs 2024</div>',
                unsafe_allow_html=True)

    merged = brands_25.merge(
        brands_24[["brand", "sales_2024"]], on="brand", how="left"
    )
    merged = merged.sort_values("sales_2025")

    fig_brands = go.Figure()
    fig_brands.add_trace(go.Bar(
        y=merged["brand"], x=merged["sales_2024"],
        name="2024", orientation="h",
        marker_color="#B5D4F4", width=0.35,
    ))
    fig_brands.add_trace(go.Bar(
        y=merged["brand"], x=merged["sales_2025"],
        name="2025", orientation="h",
        marker_color=BLUE, width=0.35,
    ))
    fig_brands.update_layout(
        barmode="overlay",
        height=360,
        margin=dict(l=0, r=10, t=10, b=30),
        legend=dict(orientation="h", y=-0.08, x=0),
        xaxis=dict(tickformat=".2s", gridcolor="#f0f0f0"),
        yaxis=dict(tickfont=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    st.plotly_chart(fig_brands, use_container_width=True)
    st.markdown('<div class="data-note">Source: ACEA 2024 & 2025</div>',
                unsafe_allow_html=True)

st.divider()

# ── Row 2: YoY evolution + Fuel mix ──────────────────────────────────────────
col_yoy, col_fuel = st.columns([1.3, 1])

with col_yoy:
    st.markdown('<div class="section-title">YoY change by country — 2025 vs 2024</div>',
                unsafe_allow_html=True)

    yoy_chart = yoy[yoy["country"] != "EU total"].dropna(subset=["pct_change"])
    yoy_chart = yoy_chart.sort_values("pct_change")

    fig_yoy = go.Figure(go.Bar(
        x=yoy_chart["pct_change"],
        y=yoy_chart["country"],
        orientation="h",
        marker_color=[TEAL if v >= 0 else CORAL for v in yoy_chart["pct_change"]],
        text=[f"{v:+.1f}%" for v in yoy_chart["pct_change"]],
        textposition="outside",
        textfont=dict(size=9),
    ))
    fig_yoy.add_vline(x=0, line_color=GRAY, line_width=1)
    fig_yoy.update_layout(
        height=420,
        margin=dict(l=0, r=60, t=10, b=10),
        xaxis=dict(title="% change", gridcolor="#f0f0f0", zeroline=False),
        yaxis=dict(tickfont=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    st.plotly_chart(fig_yoy, use_container_width=True)

with col_fuel:
    st.markdown('<div class="section-title">Fuel type mix evolution — EU</div>',
                unsafe_allow_html=True)

    fuel_long = fuel.melt(
        id_vars="year",
        value_vars=["petrol_pct", "diesel_pct", "bev_pct", "phev_pct", "hybrid_pct"],
        var_name="fuel", value_name="pct",
    )
    label_map = {
        "petrol_pct": "Petrol", "diesel_pct": "Diesel",
        "bev_pct": "BEV", "phev_pct": "PHEV", "hybrid_pct": "Hybrid",
    }
    fuel_long["fuel"] = fuel_long["fuel"].map(label_map)
    fuel_colors = {"Petrol": AMBER, "Diesel": GRAY, "BEV": BLUE,
                   "PHEV": TEAL, "Hybrid": "#534AB7"}

    fig_fuel = px.bar(
        fuel_long, x="year", y="pct", color="fuel",
        color_discrete_map=fuel_colors,
        labels={"pct": "Market share (%)", "year": "", "fuel": ""},
        text_auto=False,
    )
    fig_fuel.update_layout(
        height=240,
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(orientation="h", y=-0.15, x=0, font=dict(size=11)),
        yaxis=dict(ticksuffix="%", gridcolor="#f0f0f0"),
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    st.plotly_chart(fig_fuel, use_container_width=True)

    st.markdown('<div class="section-title" style="margin-top:8px">Body segment share — 2024</div>',
                unsafe_allow_html=True)

    fig_seg = px.pie(
        segments, values="share_pct", names="segment",
        color_discrete_sequence=COLORS,
        hole=0.55,
    )
    fig_seg.update_traces(textinfo="label+percent", textfont_size=11)
    fig_seg.update_layout(
        height=180,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown('<div class="data-note">Source: ACEA Pocket Guide 2025/2026</div>',
                unsafe_allow_html=True)

st.divider()

# ── Row 3: CO2 + Production vs Sales ─────────────────────────────────────────
col_co2, col_prod = st.columns(2)

with col_co2:
    st.markdown('<div class="section-title">Average CO₂ g/km by country — 2024</div>',
                unsafe_allow_html=True)

    co2_chart = co2[co2["country"] != "EU average"].sort_values("co2_gkm_2024")
    fig_co2 = go.Figure(go.Bar(
        x=co2_chart["co2_gkm_2024"],
        y=co2_chart["country"],
        orientation="h",
        marker_color=[TEAL if v < 107.8 else CORAL for v in co2_chart["co2_gkm_2024"]],
        text=[f"{v:.0f}" for v in co2_chart["co2_gkm_2024"]],
        textposition="outside",
        textfont=dict(size=10),
    ))
    fig_co2.add_vline(x=107.8, line_dash="dash", line_color=GRAY,
                      annotation_text="EU avg 107.8", annotation_position="top right",
                      annotation_font_size=10)
    fig_co2.update_layout(
        height=320,
        margin=dict(l=0, r=60, t=10, b=10),
        xaxis=dict(title="g CO₂/km", gridcolor="#f0f0f0"),
        yaxis=dict(tickfont=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    st.plotly_chart(fig_co2, use_container_width=True)
    st.markdown('<div class="data-note">Source: ACEA / ICCT 2024 (partial — 12 confirmed countries)</div>',
                unsafe_allow_html=True)

with col_prod:
    st.markdown('<div class="section-title">Production vs sales by country — 2024</div>',
                unsafe_allow_html=True)

    prod_chart = production[production["cars_produced"] > 0].copy()
    prod_chart = prod_chart.merge(
        countries_24[["country", "sales_2024"]], on="country", how="left"
    ).dropna(subset=["sales_2024"])
    prod_chart = prod_chart.sort_values("cars_produced", ascending=False).head(12)

    fig_prod = go.Figure()
    fig_prod.add_trace(go.Bar(
        name="Produced", x=prod_chart["country"],
        y=prod_chart["cars_produced"], marker_color=BLUE,
    ))
    fig_prod.add_trace(go.Bar(
        name="Sold (new reg.)", x=prod_chart["country"],
        y=prod_chart["sales_2024"], marker_color="#B5D4F4",
    ))
    fig_prod.update_layout(
        barmode="group",
        height=320,
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(orientation="h", y=-0.12, x=0),
        yaxis=dict(tickformat=".2s", gridcolor="#f0f0f0"),
        xaxis=dict(tickangle=-30, tickfont=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown('<div class="data-note">Source: S&P Global Mobility / ACEA 2024</div>',
                unsafe_allow_html=True)

st.divider()

# ── Row 4: Top 10 Models ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">Top 10 best-selling models — Europe 2024</div>',
            unsafe_allow_html=True)

col_models_chart, col_models_table = st.columns([1, 1])

with col_models_chart:
    models_chart = models.sort_values("rank", ascending=False)
    fig_models = go.Figure(go.Bar(
        x=[f"#{r} {m}" for r, m in zip(models_chart["rank"], models_chart["model"])],
        y=models_chart["rank"].apply(lambda r: 11 - r),
        marker_color=COLORS[:10][::-1],
        text=models_chart["brand"],
        textposition="inside",
        textfont=dict(color="white", size=10),
    ))
    fig_models.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=80),
        xaxis=dict(tickangle=-30, tickfont=dict(size=9)),
        yaxis=dict(showticklabels=False, showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(size=11),
    )
    st.plotly_chart(fig_models, use_container_width=True)

with col_models_table:
    display_df = models[["rank", "model", "brand", "fuel_type"]].copy()
    display_df.columns = ["#", "Model", "Brand", "Fuel"]
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True,
        height=280,
    )
    st.markdown('<div class="data-note">Source: JATO Dynamics 2024</div>',
                unsafe_allow_html=True)

st.divider()

# ── Demographics placeholder ──────────────────────────────────────────────────
st.markdown('<div class="section-title">Buyer demographics</div>', unsafe_allow_html=True)

st.markdown("""
<div class="spg-banner">
    <div class="spg-title">📊 This module requires S&P Global Mobility — Polk Automotive Solutions</div>
    <div class="spg-body">
        Buyer demographic data (gender, age group, household income, buying motivation) by country,
        brand and model is available exclusively through <strong>S&P Global Mobility's Polk registration data</strong>.<br><br>
        Coverage: Italy · Spain · United Kingdom · France (+ US, Canada, Australia)<br>
        Product: <em>Polk Audiences / Polk Data Services</em><br>
        Access: Enterprise licence via <a href="https://www.spglobal.com/mobility/en/index.html" target="_blank">spglobal.com/mobility</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)
with d1:
    st.markdown("**Gender split** *(illustrative)*")
    fig_d1 = go.Figure(go.Pie(
        labels=["Male", "Female"],
        values=[60, 40],
        hole=0.6,
        marker_colors=[BLUE, CORAL],
        textinfo="label+percent",
        textfont_size=11,
    ))
    fig_d1.add_annotation(text="Sample data<br>S&P required",
                          x=0.5, y=0.5, showarrow=False,
                          font=dict(size=9, color=GRAY), align="center")
    fig_d1.update_layout(
        height=200, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_d1, use_container_width=True)

with d2:
    st.markdown("**Age groups** *(illustrative)*")
    fig_d2 = px.bar(
        x=["18-35", "36-50", "51-65", "65+"],
        y=[15, 35, 32, 18],
        color_discrete_sequence=[BLUE],
        labels={"x": "", "y": "%"},
    )
    fig_d2.update_layout(
        height=200, margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(ticksuffix="%", gridcolor="#f0f0f0"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    st.plotly_chart(fig_d2, use_container_width=True)

with d3:
    st.markdown("**Top segment by gender** *(illustrative)*")
    demo_data = pd.DataFrame({
        "Segment": ["SUV", "Small", "Medium", "Luxury", "MPV"],
        "Male %": [55, 40, 52, 70, 45],
        "Female %": [45, 60, 48, 30, 55],
    })
    fig_d3 = go.Figure()
    fig_d3.add_trace(go.Bar(name="Male", x=demo_data["Segment"],
                            y=demo_data["Male %"], marker_color=BLUE))
    fig_d3.add_trace(go.Bar(name="Female", x=demo_data["Segment"],
                            y=demo_data["Female %"], marker_color=CORAL))
    fig_d3.update_layout(
        barmode="group", height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
        yaxis=dict(ticksuffix="%", gridcolor="#f0f0f0"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )
    st.plotly_chart(fig_d3, use_container_width=True)

st.caption("⚠️ Demographic charts above are illustrative only. Real data requires S&P Global Mobility licence.")

st.divider()
st.caption("Dashboard by Maria João Luz · mariajoaoluz.com · Data: ACEA, JATO Dynamics, S&P Global Mobility · 2024–2025")
