"""
European Car Market — Strategic Intelligence Report
Prepared for executive review | Source: ACEA, JATO Dynamics, S&P Global Mobility
"""

import sys
from pathlib import Path
_src = Path(__file__).resolve().parent
if (_src / "loader.py").exists():
    sys.path.insert(0, str(_src))
elif (_src / "src" / "loader.py").exists():
    sys.path.insert(0, str(_src / "src"))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from loader import (
    load_sales_by_country, load_top_brands, load_top_models,
    load_manufacturer_groups, load_fuel_type_mix, load_segment_share,
    load_co2_by_country, load_production_by_country, build_yoy_comparison,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EU Car Market — Strategic Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Palette ───────────────────────────────────────────────────────────────────
BLUE   = "#185FA5"
TEAL   = "#1D9E75"
CORAL  = "#D85A30"
AMBER  = "#BA7517"
GRAY   = "#888780"
LGRAY  = "#f0f0f0"
COLORS = [BLUE, TEAL, CORAL, AMBER, "#534AB7", "#993556", "#3B6D11", "#854F0B", "#A32D2D", "#0F6E56"]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .report-title  { font-size: 26px; font-weight: 700; color: #0d1b2a; margin: 0; }
    .report-sub    { font-size: 14px; color: #888; margin-top: 4px; }
    .section-hd    { font-size: 18px; font-weight: 600; color: #0d1b2a;
                     border-left: 4px solid #185FA5; padding-left: 10px; margin: 4px 0 2px; }
    .insight-box   { background: #EAF3DE; border-left: 4px solid #1D9E75;
                     padding: 12px 16px; border-radius: 4px; margin-bottom: 8px; }
    .insight-lbl   { font-size: 11px; font-weight: 600; color: #3B6D11;
                     letter-spacing: .06em; text-transform: uppercase; }
    .insight-txt   { font-size: 13px; color: #27500A; margin-top: 4px; line-height: 1.5; }
    .warn-box      { background: #FAEEDA; border-left: 4px solid #BA7517;
                     padding: 12px 16px; border-radius: 4px; margin-bottom: 8px; }
    .warn-lbl      { font-size: 11px; font-weight: 600; color: #854F0B;
                     letter-spacing: .06em; text-transform: uppercase; }
    .warn-txt      { font-size: 13px; color: #633806; margin-top: 4px; line-height: 1.5; }
    .risk-box      { background: #FCEBEB; border-left: 4px solid #D85A30;
                     padding: 12px 16px; border-radius: 4px; margin-bottom: 8px; }
    .risk-lbl      { font-size: 11px; font-weight: 600; color: #A32D2D;
                     letter-spacing: .06em; text-transform: uppercase; }
    .risk-txt      { font-size: 13px; color: #791F1F; margin-top: 4px; line-height: 1.5; }
    .kpi-card      { background: #f9f9f9; border-radius: 8px;
                     padding: 14px 16px; border: 0.5px solid #e0e0e0; }
    .kpi-lbl       { font-size: 12px; color: #888; margin-bottom: 2px; }
    .kpi-val       { font-size: 26px; font-weight: 700; color: #0d1b2a; line-height: 1.1; }
    .kpi-delta-up  { font-size: 12px; color: #1D9E75; margin-top: 2px; }
    .kpi-delta-dn  { font-size: 12px; color: #D85A30; margin-top: 2px; }
    .kpi-ctx       { font-size: 11px; color: #aaa; margin-top: 2px; }
    .data-note     { font-size: 11px; color: #bbb; margin-top: 4px; }
    .spg-box       { background: #f0f4fa; border: 1px solid #b5d4f4;
                     border-radius: 8px; padding: 20px 24px; }
    .spg-title     { font-size: 16px; font-weight: 600; color: #185FA5; }
    .spg-body      { font-size: 13px; color: #444; margin-top: 8px; line-height: 1.7; }
    [data-testid="stSidebar"] { background: #0d1b2a !important; }
    [data-testid="stSidebar"] * { color: #e0e6ed !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_all():
    return {
        "c24":  load_sales_by_country(2024),
        "c25":  load_sales_by_country(2025),
        "b24":  load_top_brands(2024),
        "b25":  load_top_brands(2025),
        "mod":  load_top_models(),
        "fuel": load_fuel_type_mix(),
        "seg":  load_segment_share(),
        "co2":  load_co2_by_country(),
        "prod": load_production_by_country(),
        "yoy":  build_yoy_comparison(),
        "grp24":load_manufacturer_groups(2024),
        "grp25":load_manufacturer_groups(2025),
    }

D = load_all()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Navigation")
    section = st.radio("", [
        "Executive Summary",
        "1. Market Overview",
        "2. Growth Markets",
        "3. Brand & Model Landscape",
        "4. Technology Transition",
        "5. Competitive Positioning",
        "6. Buyer Intelligence",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Report scope**")
    st.markdown("- 31 European markets\n- Full-year 2024 & 2025\n- Q1 2026 snapshot")
    st.markdown("---")
    st.markdown("**Data sources**")
    st.markdown("ACEA · JATO Dynamics\nS&P Global Mobility\nICCT / EEA")
    st.markdown("---")
    st.caption("Prepared by Maria João Luz\nmariajoaoluz.com")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="report-title">European Car Market — Strategic Intelligence Report</div>'
    '<div class="report-sub">Full-year 2024 & 2025 · 31 markets · Prepared for executive review</div>',
    unsafe_allow_html=True,
)
st.divider()

# ── Helper: KPI card ──────────────────────────────────────────────────────────
def kpi(label, value, delta, delta_up, context=""):
    delta_class = "kpi-delta-up" if delta_up else "kpi-delta-dn"
    arrow = "▲" if delta_up else "▼"
    ctx_html = f'<div class="kpi-ctx">{context}</div>' if context else ""
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-lbl">{label}</div>'
        f'<div class="kpi-val">{value}</div>'
        f'<div class="{delta_class}">{arrow} {delta}</div>'
        f'{ctx_html}</div>'
    )

def insight(text):
    return (f'<div class="insight-box">'
            f'<div class="insight-lbl">Strategic Insight</div>'
            f'<div class="insight-txt">{text}</div></div>')

def warning(text):
    return (f'<div class="warn-box">'
            f'<div class="warn-lbl">Watch</div>'
            f'<div class="warn-txt">{text}</div></div>')

def risk(text):
    return (f'<div class="risk-box">'
            f'<div class="risk-lbl">Risk</div>'
            f'<div class="risk-txt">{text}</div></div>')

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
if section == "Executive Summary":
    st.markdown('<div class="section-hd">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    total_24 = D["c24"]["sales_2024"].sum()
    total_25 = D["c25"]["sales_2025"].sum()
    delta    = (total_25 - total_24) / total_24 * 100

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi("Total market 2025", f"{total_25/1e6:.2f}M",
                        f"{delta:.1f}% vs 2024", True,
                        "First time above 13M since 2019"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi("Fastest growing large market", "Spain",
                        "+12.9% in 2025", True,
                        "2nd consecutive double-digit year"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi("BEV share EU 2024", "13.6%",
                        "vs 14.6% in 2023", False,
                        "First-ever decline — regulatory inflection"), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi("Portugal 2025", "225K",
                        "+7.3% vs 2024", True,
                        "Above EU average growth (+2.4%)"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Key findings for the business")
        st.markdown(insight(
            "The European market has recovered to 13.3M units in 2025 — its strongest since 2019. "
            "However, growth is uneven: Spain and Poland are accelerating while France and Italy contract. "
            "Brands with strong southern European exposure are best positioned."
        ))
        st.markdown(insight(
            "Dacia Sandero became Europe's #1 model for the first time ever in 2024, "
            "dethroning VW Golf after decades. The value segment is winning. "
            "Consumers are prioritising affordability over premium — pressure on margin strategies."
        ))
        st.markdown(warning(
            "BEV share fell for the first time in history in 2024 (13.6% vs 14.6%), "
            "driven by Germany's 27% collapse after subsidy cancellation. "
            "The 2025 EU CO₂ targets (93.6 g/km) create compliance risk for OEMs "
            "still dependent on ICE volume."
        ))

    with c2:
        st.markdown("#### Competitive landscape shifts")
        st.markdown(insight(
            "VW Group consolidated leadership to 26.9% market share in 2025. "
            "Skoda entered the top-2 brands for the first time ever in Q1 2026, "
            "surpassing Toyota. Within our competitive set, this signals growing "
            "pressure in the C-segment."
        ))
        st.markdown(risk(
            "Tesla's sales collapsed -26.6% in 2025 — the sharpest fall of any major brand. "
            "Traditional OEMs are recovering EV ground. This creates both opportunity "
            "(loyalty recapture) and risk (pricing pressure in BEV segment)."
        ))
        st.markdown(risk(
            "Chinese brands (BYD, SAIC/MG) grew +270% and +5.1% respectively in 2025. "
            "Their market share remains small but trajectory is steep. "
            "Southern European markets — particularly Spain and Portugal — are "
            "highest-exposure entry points for Chinese volume brands."
        ))

    st.divider()
    st.markdown("#### Recommended focus areas")
    r1, r2, r3 = st.columns(3)
    with r1:
        st.info("**Iberian growth**\nSpain and Portugal both outpacing EU average. "
                "Review network capacity and model mix for these markets.")
    with r2:
        st.warning("**EV transition timeline**\nBEV stall vs regulatory targets creates "
                   "a compliance gap. Assess our OEM partners' compliance trajectories.")
    with r3:
        st.error("**Chinese brand monitoring**\nSet up systematic tracking of BYD and MG "
                 "penetration in our key markets. Early warning system needed.")

# ══════════════════════════════════════════════════════════════════════════════
# 1. MARKET OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif section == "1. Market Overview":
    st.markdown('<div class="section-hd">1. Market Overview</div>', unsafe_allow_html=True)

    total_24 = D["c24"]["sales_2024"].sum()
    total_25 = D["c25"]["sales_2025"].sum()
    delta = (total_25 - total_24) / total_24 * 100

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(kpi("EU+EFTA+UK 2025", f"{total_25/1e6:.2f}M", f"{delta:.1f}% YoY", True), unsafe_allow_html=True)
    with k2:
        pt25 = D["c25"][D["c25"]["country"]=="Portugal"]["sales_2025"].values[0]
        pt_d = D["c25"][D["c25"]["country"]=="Portugal"]["pct_change"].values[0]
        st.markdown(kpi("Portugal 2025", f"{pt25/1e3:.0f}K", f"{pt_d:+.1f}% YoY", pt_d>0, "7th consecutive growth year"), unsafe_allow_html=True)
    with k3:
        de25 = D["c25"][D["c25"]["country"]=="Germany"]["sales_2025"].values[0]
        de_d = D["c25"][D["c25"]["country"]=="Germany"]["pct_change"].values[0]
        st.markdown(kpi("Germany 2025", f"{de25/1e6:.2f}M", f"{de_d:+.1f}% YoY", de_d>0, "#1 market — 21% of EU"), unsafe_allow_html=True)
    with k4:
        sp25 = D["c25"][D["c25"]["country"]=="Spain"]["sales_2025"].values[0]
        sp_d = D["c25"][D["c25"]["country"]=="Spain"]["pct_change"].values[0]
        st.markdown(kpi("Spain 2025", f"{sp25/1e6:.2f}M", f"{sp_d:+.1f}% YoY", True, "Fastest growing top-5 market"), unsafe_allow_html=True)
    with k5:
        fr25 = D["c25"][D["c25"]["country"]=="France"]["sales_2025"].values[0]
        fr_d = D["c25"][D["c25"]["country"]=="France"]["pct_change"].values[0]
        st.markdown(kpi("France 2025", f"{fr25/1e6:.2f}M", f"{fr_d:+.1f}% YoY", False, "Structural contraction"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    iso_map = {
        "Austria":"AUT","Belgium":"BEL","Bulgaria":"BGR","Croatia":"HRV","Cyprus":"CYP",
        "Czechia":"CZE","Denmark":"DNK","Estonia":"EST","Finland":"FIN","France":"FRA",
        "Germany":"DEU","Greece":"GRC","Hungary":"HUN","Ireland":"IRL","Italy":"ITA",
        "Latvia":"LVA","Lithuania":"LTU","Luxembourg":"LUX","Malta":"MLT","Netherlands":"NLD",
        "Poland":"POL","Portugal":"PRT","Romania":"ROU","Slovakia":"SVK","Slovenia":"SVN",
        "Spain":"ESP","Sweden":"SWE","Iceland":"ISL","Norway":"NOR","Switzerland":"CHE",
        "United Kingdom":"GBR",
    }

    col_map, col_ins = st.columns([1.6, 1])

    with col_map:
        map_df = D["c25"].copy()
        map_df["iso"] = map_df["country"].map(iso_map)
        map_df = map_df.dropna(subset=["iso"])

        fig_map = px.choropleth(
            map_df, locations="iso", color="sales_2025",
            hover_name="country",
            hover_data={"sales_2025":":,.0f","pct_change":":.1f","iso":False},
            color_continuous_scale=[[0,"#E6F1FB"],[0.25,"#85B7EB"],[0.6,"#378ADD"],[1,"#042C53"]],
            scope="europe",
            labels={"sales_2025":"Sales 2025","pct_change":"YoY %"},
            title="New passenger car registrations — 2025",
        )
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=40, b=0), height=420,
            coloraxis_colorbar=dict(title="Units", tickformat=".2s", len=0.7),
            geo=dict(showframe=False, showcoastlines=False, bgcolor="rgba(0,0,0,0)",
                     projection_scale=1.35, center=dict(lat=54, lon=14)),
            paper_bgcolor="rgba(0,0,0,0)",
            title_font_size=14,
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_ins:
        st.markdown("#### What the map tells us")
        st.markdown(insight(
            "Germany, UK, France and Italy account for 61% of all European sales. "
            "But the growth story is in the periphery — Spain, Poland, and Iberia broadly "
            "are taking market share from the stagnating core."
        ))
        st.markdown(warning(
            "Estonia showed a -48.6% collapse in 2025 — driven by subsidy removal. "
            "This is a leading indicator of what happens when EV incentives are withdrawn abruptly."
        ))
        top5 = D["c25"].nlargest(5,"sales_2025")[["country","sales_2025","pct_change"]]
        top5.columns = ["Country","Sales 2025","YoY %"]
        top5["Sales 2025"] = top5["Sales 2025"].apply(lambda x: f"{x:,.0f}")
        top5["YoY %"] = top5["YoY %"].apply(lambda x: f"{x:+.1f}%")
        st.markdown("**Top 5 markets**")
        st.dataframe(top5, hide_index=True, use_container_width=True)
        st.markdown('<div class="data-note">Source: ACEA 2025</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2. GROWTH MARKETS
# ══════════════════════════════════════════════════════════════════════════════
elif section == "2. Growth Markets":
    st.markdown('<div class="section-hd">2. Growth Markets — 2025 vs 2024</div>', unsafe_allow_html=True)

    yoy_chart = D["yoy"].dropna(subset=["pct_change"]).copy()
    yoy_chart["highlight"] = yoy_chart["country"].isin(["Portugal","Spain"])
    yoy_chart = yoy_chart.sort_values("pct_change")

    def bar_color(row):
        if row["country"] == "Portugal": return CORAL
        if row["country"] == "Spain":    return AMBER
        return TEAL if row["pct_change"] >= 0 else "#E0E0E0"

    yoy_chart["color"] = yoy_chart.apply(bar_color, axis=1)

    fig_yoy = go.Figure(go.Bar(
        x=yoy_chart["pct_change"],
        y=yoy_chart["country"],
        orientation="h",
        marker_color=yoy_chart["color"],
        text=[f"{v:+.1f}%" for v in yoy_chart["pct_change"]],
        textposition="outside",
        textfont=dict(size=9),
        customdata=yoy_chart[["sales_2025","sales_2024"]].values,
        hovertemplate="<b>%{y}</b><br>Change: %{x:+.1f}%<br>2025: %{customdata[0]:,.0f}<br>2024: %{customdata[1]:,.0f}<extra></extra>",
    ))
    fig_yoy.add_vline(x=2.4, line_dash="dash", line_color=BLUE, line_width=1.5,
                      annotation_text="EU avg +2.4%", annotation_position="top",
                      annotation_font=dict(size=10, color=BLUE))
    fig_yoy.add_vline(x=0, line_color=GRAY, line_width=0.8)
    fig_yoy.update_layout(
        height=600, margin=dict(l=0, r=70, t=30, b=10),
        title="YoY growth by country — Portugal and Spain highlighted",
        title_font_size=13,
        xaxis=dict(title="% change vs 2024", gridcolor=LGRAY, zeroline=False),
        yaxis=dict(tickfont=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
    )

    col_chart, col_ins = st.columns([1.5, 1])
    with col_chart:
        st.plotly_chart(fig_yoy, use_container_width=True)

    with col_ins:
        st.markdown("#### Strategic reading")
        st.markdown(insight(
            "**Portugal (+7.3%) and Spain (+12.9%)** both outperformed the EU average (+2.4%) by a wide margin. "
            "The Iberian Peninsula is the strongest growth corridor in Western Europe. "
            "Our commercial strategy should reflect this asymmetry."
        ))
        st.markdown(insight(
            "**Norway (+39.4%) and Lithuania (+39.3%)** are structural BEV-driven growth markets. "
            "Norway's near-100% EV penetration creates a template for what mature electrification looks like."
        ))
        st.markdown(warning(
            "**France (-5.0%) and Italy (-2.1%)** — the 2nd and 4th largest European markets — "
            "contracted. Both economies face structural headwinds. "
            "Over-exposure to these markets without offsetting Iberian growth creates portfolio risk."
        ))
        st.markdown(risk(
            "**Estonia (-48.6%)** is a stark reminder: subsidy-driven EV booms collapse fast. "
            "Markets with high incentive dependency need scenario planning."
        ))

# ══════════════════════════════════════════════════════════════════════════════
# 3. BRAND & MODEL LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════════
elif section == "3. Brand & Model Landscape":
    st.markdown('<div class="section-hd">3. Brand & Model Landscape</div>', unsafe_allow_html=True)

    col_b, col_m = st.columns([1, 1])

    with col_b:
        st.markdown("##### Top 10 brands — sales & YoY growth (2025)")
        merged = D["b25"].merge(D["b24"][["brand","sales_2024"]], on="brand", how="left")
        merged = merged.sort_values("sales_2025")

        fig_b = go.Figure()
        fig_b.add_trace(go.Bar(
            y=merged["brand"], x=merged["sales_2024"],
            name="2024", orientation="h",
            marker_color="#C9DCEF", width=0.4,
        ))
        fig_b.add_trace(go.Bar(
            y=merged["brand"], x=merged["sales_2025"],
            name="2025", orientation="h",
            marker_color=BLUE, width=0.4,
        ))
        for _, row in merged.iterrows():
            d = row["pct_change"]
            color = TEAL if d >= 0 else CORAL
            fig_b.add_annotation(
                y=row["brand"], x=row["sales_2025"] * 1.02,
                text=f"{d:+.1f}%",
                showarrow=False, font=dict(size=9, color=color), xanchor="left",
            )
        fig_b.update_layout(
            barmode="overlay", height=380,
            margin=dict(l=0, r=70, t=10, b=30),
            legend=dict(orientation="h", y=-0.1),
            xaxis=dict(tickformat=".2s", gridcolor=LGRAY),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        )
        st.plotly_chart(fig_b, use_container_width=True)
        st.markdown(insight(
            "VW leads with 1.45M units (+5.9%). Skoda's +9.6% is the standout — "
            "value positioning in a cost-conscious market is working. "
            "Audi's flat performance (+0.3%) signals premium fatigue."
        ))

    with col_m:
        st.markdown("##### Top 10 models — Europe 2024")
        models_chart = D["mod"].copy()

        fig_m = go.Figure(go.Bar(
            x=models_chart["model"],
            y=[10 - i for i in range(len(models_chart))],
            marker_color=COLORS[:10],
            text=[f"{r['brand']}" for _, r in models_chart.iterrows()],
            textposition="inside",
            textfont=dict(color="white", size=10),
            customdata=models_chart[["fuel_type","notes"]].values,
            hovertemplate="<b>%{x}</b><br>Brand: %{text}<br>Fuel: %{customdata[0]}<extra></extra>",
        ))
        fig_m.update_layout(
            height=280, margin=dict(l=0, r=0, t=10, b=60),
            xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
            yaxis=dict(showticklabels=False, showgrid=False),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, font=dict(size=11),
        )
        st.plotly_chart(fig_m, use_container_width=True)

        tbl = D["mod"][["rank","model","brand","fuel_type"]].copy()
        tbl.columns = ["#","Model","Brand","Fuel"]
        st.dataframe(tbl, hide_index=True, use_container_width=True, height=160)
        st.markdown(insight(
            "Dacia Sandero at #1 is historically significant — "
            "the first time a budget brand topped the European model ranking. "
            "8 of the top 10 are petrol/hybrid. Pure BEV (Tesla Model Y) slipped to #4."
        ))

    st.divider()
    st.markdown("##### Group market share — 2024 vs 2025")
    c1, c2 = st.columns(2)
    for col, year, data in [(c1,"2024",D["grp24"]), (c2,"2025",D["grp25"])]:
        with col:
            top8 = data.nlargest(8,"market_share")
            fig_g = px.pie(
                top8, values="market_share", names="group",
                color_discrete_sequence=COLORS, hole=0.5,
                title=f"Group share — {year}",
            )
            fig_g.update_traces(textinfo="label+percent", textfont_size=10)
            fig_g.update_layout(
                height=280, margin=dict(l=0, r=0, t=40, b=0),
                showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                title_font_size=13,
            )
            st.plotly_chart(fig_g, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4. TECHNOLOGY TRANSITION
# ══════════════════════════════════════════════════════════════════════════════
elif section == "4. Technology Transition":
    st.markdown('<div class="section-hd">4. Technology Transition — Electrification & Emissions</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi("BEV share 2024","13.6%","vs 14.6% in 2023",False,"First-ever decline"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi("SUV dominance","53%","of all EU sales",True,"Up from 19% in 2015"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi("EU CO₂ avg 2024","107.8 g/km","vs target 93.6 g/km",False,"14 g/km gap to close"), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi("BEV Q1 2026","20.6%","record EU share",True,"vs 15.2% in Q1 2025"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_f, col_s = st.columns([1.3, 1])

    with col_f:
        st.markdown("##### Powertrain shift — EU market share 2021→2024")
        fuel_long = D["fuel"].melt(
            id_vars="year",
            value_vars=["petrol_pct","diesel_pct","bev_pct","phev_pct","hybrid_pct"],
            var_name="fuel", value_name="pct",
        )
        label_map = {"petrol_pct":"Petrol","diesel_pct":"Diesel","bev_pct":"Battery EV",
                     "phev_pct":"Plug-in Hybrid","hybrid_pct":"Hybrid"}
        fuel_long["fuel"] = fuel_long["fuel"].map(label_map)
        fuel_colors = {"Petrol":AMBER,"Diesel":GRAY,"Battery EV":BLUE,"Plug-in Hybrid":TEAL,"Hybrid":"#534AB7"}

        fig_f = px.bar(
            fuel_long, x="year", y="pct", color="fuel",
            color_discrete_map=fuel_colors,
            labels={"pct":"Market share (%)","year":"","fuel":""},
            text="pct",
        )
        fig_f.update_traces(texttemplate="%{text:.1f}%", textposition="inside",
                            textfont_size=9)
        fig_f.update_layout(
            barmode="stack", height=340,
            margin=dict(l=0, r=0, t=10, b=40),
            legend=dict(orientation="h", y=-0.15),
            yaxis=dict(ticksuffix="%", gridcolor=LGRAY, range=[0,105]),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        )
        st.plotly_chart(fig_f, use_container_width=True)
        st.markdown('<div class="data-note">Source: ACEA Pocket Guide 2025/2026</div>', unsafe_allow_html=True)

    with col_s:
        st.markdown("##### Body segment — EU 2024")
        fig_s = px.pie(
            D["seg"], values="share_pct", names="segment",
            color_discrete_sequence=COLORS, hole=0.55,
        )
        fig_s.update_traces(textinfo="label+percent", textfont_size=11)
        fig_s.update_layout(
            height=200, margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_s, use_container_width=True)

        st.markdown("##### Strategic reading")
        st.markdown(risk(
            "BEV's first-ever decline in 2024 creates a regulatory crisis: "
            "EU's 2025 target is 93.6 g/km but the fleet average was 107.8 g/km. "
            "OEMs face fines unless they push BEV volumes aggressively in H2 2025."
        ))
        st.markdown(insight(
            "Q1 2026 BEV share rebounded to 20.6% — a record. "
            "The market correction was temporary. Electrification is back on track. "
            "Charging infrastructure expansion (882K points in EU, +fast) is the enabler."
        ))

    st.divider()
    st.markdown("##### Average CO₂ by country — 2024")
    co2_chart = D["co2"][D["co2"]["country"] != "EU average"].sort_values("co2_gkm_2024")
    fig_co2 = go.Figure(go.Bar(
        x=co2_chart["co2_gkm_2024"], y=co2_chart["country"],
        orientation="h",
        marker_color=[TEAL if v < 93.6 else (AMBER if v < 107.8 else CORAL) for v in co2_chart["co2_gkm_2024"]],
        text=[f"{v:.0f}" for v in co2_chart["co2_gkm_2024"]],
        textposition="outside", textfont=dict(size=10),
    ))
    fig_co2.add_vline(x=93.6, line_dash="dash", line_color=BLUE,
                      annotation_text="2025 target 93.6", annotation_font=dict(size=9, color=BLUE))
    fig_co2.add_vline(x=107.8, line_dash="dot", line_color=GRAY,
                      annotation_text="EU avg 107.8", annotation_font=dict(size=9, color=GRAY))
    fig_co2.update_layout(
        height=300, margin=dict(l=0, r=70, t=30, b=10),
        xaxis=dict(title="g CO₂/km", gridcolor=LGRAY),
        yaxis=dict(tickfont=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=11),
        annotations=[dict(x=93.6, y=1.05, xref="x", yref="paper",
                          text="▼ Target zone", showarrow=False,
                          font=dict(size=9, color=BLUE))],
    )
    st.plotly_chart(fig_co2, use_container_width=True)
    st.markdown('<div class="data-note">Green = below target · Orange = above avg · Red = above avg — Source: ACEA/ICCT (12 confirmed countries)</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 5. COMPETITIVE POSITIONING
# ══════════════════════════════════════════════════════════════════════════════
elif section == "5. Competitive Positioning":
    st.markdown('<div class="section-hd">5. Competitive Positioning — Production & Supply</div>', unsafe_allow_html=True)

    prod_chart = D["prod"][D["prod"]["cars_produced"] > 0].merge(
        D["c24"][["country","sales_2024"]], on="country", how="left"
    ).dropna(subset=["sales_2024"]).sort_values("cars_produced", ascending=False).head(12)
    prod_chart["balance"] = prod_chart["cars_produced"] - prod_chart["sales_2024"]
    prod_chart["net"] = prod_chart["balance"].apply(lambda x: "Net exporter" if x > 0 else "Net importer")

    col_chart, col_ins = st.columns([1.5, 1])

    with col_chart:
        st.markdown("##### Production vs domestic sales — 2024 (top 12 producing nations)")
        fig_p = go.Figure()
        fig_p.add_trace(go.Bar(
            name="Cars produced", x=prod_chart["country"],
            y=prod_chart["cars_produced"], marker_color=BLUE,
        ))
        fig_p.add_trace(go.Bar(
            name="New registrations", x=prod_chart["country"],
            y=prod_chart["sales_2024"], marker_color="#B5D4F4",
        ))
        fig_p.update_layout(
            barmode="group", height=360,
            margin=dict(l=0, r=0, t=10, b=60),
            legend=dict(orientation="h", y=-0.15),
            yaxis=dict(tickformat=".2s", gridcolor=LGRAY),
            xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        )
        st.plotly_chart(fig_p, use_container_width=True)
        st.markdown('<div class="data-note">Source: S&P Global Mobility / ACEA 2024</div>', unsafe_allow_html=True)

    with col_ins:
        st.markdown("#### Supply chain reading")
        st.markdown(insight(
            "Germany produces 3.9M cars but only registers 2.8M domestically — "
            "a net exporter of 1.1M units. "
            "Spain produces 1.9M but registers only 1.0M. "
            "Portugal produces 229K (AutoEuropa) but registers 210K — nearly balanced."
        ))
        st.markdown(warning(
            "Czechia, Slovakia, and Hungary are major producers with small domestic markets. "
            "They are structurally dependent on export demand. "
            "Any EU tariff escalation or Chinese market access restrictions "
            "hits these markets hardest."
        ))

        st.markdown("**Net trade position**")
        balance_tbl = prod_chart[["country","cars_produced","sales_2024","balance","net"]].copy()
        balance_tbl.columns = ["Country","Produced","Registered","Balance","Position"]
        balance_tbl["Produced"]   = balance_tbl["Produced"].apply(lambda x: f"{x:,.0f}")
        balance_tbl["Registered"] = balance_tbl["Registered"].apply(lambda x: f"{x:,.0f}")
        balance_tbl["Balance"]    = balance_tbl["Balance"].apply(lambda x: f"{x:+,.0f}")
        st.dataframe(balance_tbl[["Country","Balance","Position"]], hide_index=True,
                     use_container_width=True, height=280)

# ══════════════════════════════════════════════════════════════════════════════
# 6. BUYER INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif section == "6. Buyer Intelligence":
    st.markdown('<div class="section-hd">6. Buyer Intelligence</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="spg-box">
    <div class="spg-title">📊 Buyer Demographics — S&P Global Mobility · Polk Automotive Solutions</div>
    <div class="spg-body">
    Full buyer demographic data (gender, age group, household income, purchase motivation, loyalty/conquest)
    by country, brand and model is available exclusively through <strong>S&P Global Mobility's Polk registration database</strong>.<br><br>
    <strong>European coverage:</strong> Italy · Spain · United Kingdom · France<br>
    <strong>Product:</strong> Polk Audiences / Polk Data Services<br>
    <strong>Access:</strong> Enterprise licence —
    <a href="https://www.spglobal.com/mobility/en/index.html" target="_blank">spglobal.com/mobility</a><br><br>
    The charts below use <strong>illustrative estimates</strong> based on published industry research.
    They are directionally correct but should not be used for commercial decisions without a Polk licence.
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### Illustrative buyer profile — Europe (estimates, not Polk data)")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown("**Gender split by segment**")
        gender_data = pd.DataFrame({
            "Segment": ["SUV","Small","Medium","Luxury","MPV"],
            "Male": [56, 41, 53, 71, 44],
            "Female": [44, 59, 47, 29, 56],
        })
        fig_g = go.Figure()
        fig_g.add_trace(go.Bar(name="Male",   x=gender_data["Segment"], y=gender_data["Male"],   marker_color=BLUE))
        fig_g.add_trace(go.Bar(name="Female", x=gender_data["Segment"], y=gender_data["Female"], marker_color=CORAL))
        fig_g.update_layout(
            barmode="stack", height=240,
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
            yaxis=dict(ticksuffix="%", gridcolor=LGRAY, range=[0,105]),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        )
        st.plotly_chart(fig_g, use_container_width=True)

    with d2:
        st.markdown("**Age distribution of new car buyers**")
        fig_a = go.Figure(go.Pie(
            labels=["18-35","36-50","51-65","65+"],
            values=[14, 34, 33, 19],
            hole=0.55,
            marker_colors=[BLUE, TEAL, AMBER, GRAY],
            textinfo="label+percent",
            textfont_size=11,
        ))
        fig_a.add_annotation(text="Illustrative", x=0.5, y=0.5, showarrow=False,
                             font=dict(size=9, color=GRAY), align="center")
        fig_a.update_layout(
            height=240, margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_a, use_container_width=True)

    with d3:
        st.markdown("**Purchase motivation (new car buyers)**")
        motiv = pd.DataFrame({
            "Motivation": ["Reliability","Running costs","Brand","Safety","Design","Green/EV"],
            "Score": [78, 65, 52, 48, 41, 33],
        }).sort_values("Score")
        fig_m = go.Figure(go.Bar(
            x=motiv["Score"], y=motiv["Motivation"],
            orientation="h", marker_color=BLUE,
            text=motiv["Score"].apply(lambda x: f"{x}%"),
            textposition="outside", textfont=dict(size=10),
        ))
        fig_m.update_layout(
            height=240, margin=dict(l=0, r=40, t=10, b=10),
            xaxis=dict(range=[0,100], gridcolor=LGRAY),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        )
        st.plotly_chart(fig_m, use_container_width=True)

    st.caption("⚠️ All figures above are illustrative estimates based on published industry research. "
               "For commercial use, activate S&P Global Mobility Polk licence.")

    st.divider()
    st.markdown("#### How to unlock real demographic data")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.info("**Short term (free)**\nRequest a demo at spglobal.com/mobility — sales reps often share sample cuts for qualified prospects.")
    with a2:
        st.warning("**Medium term**\nExplore whether your OEM partner (VW, Toyota, etc.) has an existing S&P data licence that covers your market.")
    with a3:
        st.error("**Long term**\nBudget for Polk Data Services as a strategic intelligence investment — ROI justification: one avoided bad launch pays for it.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("European Car Market Intelligence Report · Prepared by Maria João Luz · mariajoaoluz.com · "
           "Data: ACEA, JATO Dynamics, S&P Global Mobility, ICCT, EEA · 2024–2025")
