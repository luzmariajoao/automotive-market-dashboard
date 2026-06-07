"""
European Car Market — Interactive Strategic Dashboard
Source: ACEA, JATO Dynamics, S&P Global Mobility 2024/2025
"""
import sys
from pathlib import Path
_here = Path(__file__).resolve().parent
if (_here / "loader.py").exists():
  sys.path.insert(0, str(_here))
elif (_here / "src" / "loader.py").exists():
  sys.path.insert(0, str(_here / "src"))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from loader import (
  load_sales_by_country, load_top_brands, load_top_models,
  load_manufacturer_groups, load_fuel_type_mix, load_segment_share,
  load_co2_by_country, load_production_by_country, build_yoy_comparison,
  load_ratio_per_capita,
)

st.set_page_config(
  page_title="EU Car Market — Interactive Dashboard",
  page_icon="🚗",
  layout="wide",
  initial_sidebar_state="expanded",
)

# ── Palette ───────────────────────────────────────────────────────────────────
BLUE = "#185FA5"; TEAL = "#1D9E75"; CORAL = "#D85A30"
AMBER = "#BA7517"; GRAY = "#888780"; LGRAY = "#f0f0f0"
COLORS = [BLUE, TEAL, CORAL, AMBER, "#534AB7", "#993556",
     "#3B6D11", "#854F0B", "#A32D2D", "#0F6E56"]

st.markdown("""
<style>
.report-title{font-size:24px;font-weight:700;color:#0d1b2a}
.section-hd{font-size:16px;font-weight:600;color:#0d1b2a;
 border-left:4px solid #185FA5;padding-left:10px;margin:4px 0 12px}
.kpi-card{background:#f9f9f9;border-radius:8px;padding:14px 16px;border:0.5px solid #e0e0e0}
.kpi-lbl{font-size:12px;color:#888;margin-bottom:2px}
.kpi-val{font-size:26px;font-weight:700;color:#0d1b2a;line-height:1.1}
.kpi-up{font-size:12px;color:#1D9E75;margin-top:2px}
.kpi-dn{font-size:12px;color:#D85A30;margin-top:2px}
.kpi-ctx{font-size:11px;color:#aaa}
.insight-box{background:#EAF3DE;border-left:4px solid #1D9E75;
 padding:12px 16px;border-radius:4px;margin-bottom:8px}
.insight-lbl{font-size:11px;font-weight:600;color:#3B6D11;
 letter-spacing:.06em;text-transform:uppercase}
.insight-txt{font-size:13px;color:#27500A;margin-top:4px;line-height:1.5}
.warn-box{background:#FAEEDA;border-left:4px solid #BA7517;
 padding:12px 16px;border-radius:4px;margin-bottom:8px}
.warn-lbl{font-size:11px;font-weight:600;color:#854F0B;
 letter-spacing:.06em;text-transform:uppercase}
.warn-txt{font-size:13px;color:#633806;margin-top:4px;line-height:1.5}
.risk-box{background:#FCEBEB;border-left:4px solid #D85A30;
 padding:12px 16px;border-radius:4px;margin-bottom:8px}
.risk-lbl{font-size:11px;font-weight:600;color:#A32D2D;
 letter-spacing:.06em;text-transform:uppercase}
.risk-txt{font-size:13px;color:#791F1F;margin-top:4px;line-height:1.5}
.filter-label{font-size:12px;font-weight:600;color:#555;
 text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}
.data-note{font-size:11px;color:#bbb;margin-top:4px}
.spg-box{background:#f0f4fa;border:1px solid #b5d4f4;border-radius:8px;padding:20px 24px}
.spg-title{font-size:15px;font-weight:600;color:#185FA5}
.spg-body{font-size:13px;color:#444;margin-top:8px;line-height:1.7}
[data-testid="stSidebar"]{background:#0d1b2a !important}
[data-testid="stSidebar"] *{color:#e0e6ed !important}
</style>
""", unsafe_allow_html=True)

ISO = {
  "Austria":"AUT","Belgium":"BEL","Bulgaria":"BGR","Croatia":"HRV","Cyprus":"CYP",
  "Czechia":"CZE","Denmark":"DNK","Estonia":"EST","Finland":"FIN","France":"FRA",
  "Germany":"DEU","Greece":"GRC","Hungary":"HUN","Ireland":"IRL","Italy":"ITA",
  "Latvia":"LVA","Lithuania":"LTU","Luxembourg":"LUX","Malta":"MLT","Netherlands":"NLD",
  "Poland":"POL","Portugal":"PRT","Romania":"ROU","Slovakia":"SVK","Slovenia":"SVN",
  "Spain":"ESP","Sweden":"SWE","Iceland":"ISL","Norway":"NOR","Switzerland":"CHE",
  "United Kingdom":"GBR",
}

# ── Load data ─────────────────────────────────────────────────────────────────


# ── All analytics functions — embedded inline, no loader.py dependency ────────
import numpy as np

def load_ratio_per_capita():
    sales_pop = {
        "Austria":(253789,284978,9.1),"Belgium":(448277,414770,11.7),
        "Bulgaria":(42941,49419,6.5),"Croatia":(65020,69841,3.9),
        "Cyprus":(15057,14634,1.2),"Czechia":(231597,248719,10.8),
        "Denmark":(173114,184641,5.9),"Estonia":(25386,13055,1.4),
        "Finland":(74064,71881,5.5),"France":(1718412,1632152,68.2),
        "Germany":(2817331,2857591,84.4),"Greece":(137075,144199,10.4),
        "Hungary":(121611,129440,9.7),"Ireland":(121196,124954,5.1),
        "Italy":(1559229,1524843,59.0),"Latvia":(17329,22506,1.8),
        "Lithuania":(30122,41974,2.8),"Luxembourg":(46659,47158,0.67),
        "Malta":(7663,6468,0.54),"Netherlands":(381227,388024,17.8),
        "Poland":(551568,597435,36.8),"Portugal":(209715,225039,10.5),
        "Romania":(151105,156803,19.0),"Slovakia":(93409,93103,5.5),
        "Slovenia":(53018,57556,2.1),"Spain":(1016885,1148650,47.8),
        "Sweden":(269582,272998,10.5),"Iceland":(10233,14547,0.37),
        "Norway":(128687,179632,5.5),"Switzerland":(239535,233737,8.8),
        "United Kingdom":(1952778,2020523,67.7),
    }
    rows = []
    for country,(s24,s25,pop) in sales_pop.items():
        rows.append({"country":country,"sales_2024":s24,"sales_2025":s25,"population_m":pop,
            "reg_per_1000_2024":round(s24/(pop*1000),1),"reg_per_1000_2025":round(s25/(pop*1000),1),
            "1_per_n_2024":int(round(pop*1e6/s24)),"1_per_n_2025":int(round(pop*1e6/s25))})
    return pd.DataFrame(rows).sort_values("reg_per_1000_2025",ascending=False).reset_index(drop=True)

def load_top_models_with_year(year=2024):
    data_2024 = [
        (1,"Sandero","Dacia","Renault Group","Petrol/LPG","#1 for first time — dethroned VW Golf"),
        (2,"Clio","Renault","Renault Group","Petrol/Hybrid","2nd consecutive year in 2nd place"),
        (3,"Golf","Volkswagen","Volkswagen Group","Petrol/Diesel","215,700 units, +17%"),
        (4,"Model Y","Tesla","Tesla","Electric","#1 in NL, SE, CH, DK, NO"),
        (5,"T-Roc","Volkswagen","Volkswagen Group","Petrol/Diesel","Slipped from 4th"),
        (6,"208","Peugeot","Stellantis","Petrol/Electric","Top model in 2022"),
        (7,"Yaris Cross","Toyota","Toyota Group","Hybrid","Improved one rank"),
        (8,"Octavia","Skoda","Volkswagen Group","Petrol/Diesel","Improved two ranks"),
        (9,"Duster","Dacia","Renault Group","Petrol/LPG/Hybrid","Entered top 10 from 15th"),
        (10,"Yaris","Toyota","Toyota Group","Hybrid","Entered top 10 from 14th"),
    ]
    data_2025 = [
        (1,"Sandero","Dacia","Renault Group","Petrol/LPG","243,676 units — 2nd consecutive #1"),
        (2,"Clio","Renault","Renault Group","Petrol/Hybrid","~238,000 units — 2nd consecutive"),
        (3,"T-Roc","Volkswagen","Volkswagen Group","Petrol/Diesel","211,241 units — up from #5"),
        (4,"Tiguan","Volkswagen","Volkswagen Group","Petrol/Diesel","197,000 units, +19.7%"),
        (5,"Golf","Volkswagen","Volkswagen Group","Petrol/Diesel","195,455 units — slipped from #3"),
        (6,"208","Peugeot","Stellantis","Petrol/Electric","~185,000 units"),
        (7,"Yaris Cross","Toyota","Toyota Group","Hybrid","~175,000 units"),
        (8,"Duster","Dacia","Renault Group","Petrol/LPG/Hybrid","~168,000 units, +22%"),
        (9,"Yaris","Toyota","Toyota Group","Hybrid","~148,000 units"),
        (10,"C3","Citroen","Stellantis","Petrol/Electric","~145,000 — Model Y dropped out"),
    ]
    cols = ["rank","model","brand","group","fuel_type","notes"]
    return pd.DataFrame(data_2025 if year==2025 else data_2024, columns=cols)

def load_monthly_data():
    data = [
        ("Jan",760,752,10.9,15.0),("Feb",850,843,12.4,14.0),("Mar",1050,1069,13.8,15.5),
        ("Apr",785,798,14.1,14.8),("May",880,895,14.5,15.5),("Jun",905,916,13.5,17.2),
        ("Jul",810,839,13.5,14.8),("Aug",490,509,12.2,14.5),("Sep",1095,1139,17.9,18.5),
        ("Oct",870,920,13.7,19.0),("Nov",825,872,12.8,20.5),("Dec",668,690,15.9,25.0),
    ]
    df = pd.DataFrame(data, columns=["month","reg_2024_k","reg_2025_k","bev_pct_2024","bev_pct_2025"])
    df["month_num"] = range(1,13)
    return df

def load_forecast_2026():
    # EU+EFTA+UK scope — 2025 baseline: 13.27M (ACEA confirmed)
    # Pessimistic: flat (0%), Base: +2.5%, Optimistic: +5.0%
    base_2025 = 13270
    data = [
        ("Pessimistic", round(base_2025 * 1.000), 17.4, "#D85A30"),
        ("Base case",   round(base_2025 * 1.025), 21.5, "#185FA5"),
        ("Optimistic",  round(base_2025 * 1.050), 25.0, "#1D9E75"),
    ]
    df = pd.DataFrame(data, columns=["scenario","reg_2026_k","bev_share_2026","color"])
    df["reg_2025_k"] = base_2025
    df["growth_vs_2025"] = ((df["reg_2026_k"]-df["reg_2025_k"])/df["reg_2025_k"]*100).round(1)
    return df

def load_market_concentration():
    b25 = _get_brands(2025); b24 = _get_brands(2024)
    shares_25 = list(b25["market_share"])+[max(0,100-b25["market_share"].sum())]
    shares_24 = list(b24["market_share"])+[max(0,100-b24["market_share"].sum())]
    from loader import load_manufacturer_groups
    g25 = load_manufacturer_groups(2025); g24 = load_manufacturer_groups(2024)
    return {
        "brand_hhi_2025":round(sum(s**2 for s in shares_25),1),
        "brand_hhi_2024":round(sum(s**2 for s in shares_24),1),
        "group_hhi_2025":round(sum(s**2 for s in g25["market_share"]),1),
        "group_hhi_2024":round(sum(s**2 for s in g24["market_share"]),1),
        "top3_share_2025":round(b25.head(3)["market_share"].sum(),1),
        "top3_share_2024":round(b24.head(3)["market_share"].sum(),1),
        "top5_share_2025":round(b25.head(5)["market_share"].sum(),1),
        "top5_share_2024":round(b24.head(5)["market_share"].sum(),1),
    }

def load_group_share_evolution():
    data = [
        ("Volkswagen Group",2019,24.1),("Volkswagen Group",2020,24.8),("Volkswagen Group",2021,25.3),
        ("Volkswagen Group",2022,25.8),("Volkswagen Group",2023,26.0),("Volkswagen Group",2024,26.3),("Volkswagen Group",2025,26.9),
        ("Stellantis",2021,19.4),("Stellantis",2022,18.2),("Stellantis",2023,16.8),
        ("Stellantis",2024,15.2),("Stellantis",2025,14.3),
        ("Renault Group",2019,10.2),("Renault Group",2020,9.8),("Renault Group",2021,9.5),
        ("Renault Group",2022,9.7),("Renault Group",2023,9.8),("Renault Group",2024,9.9),("Renault Group",2025,10.2),
        ("Hyundai Group",2019,6.8),("Hyundai Group",2020,7.1),("Hyundai Group",2021,7.5),
        ("Hyundai Group",2022,7.9),("Hyundai Group",2023,8.3),("Hyundai Group",2024,8.2),("Hyundai Group",2025,7.9),
        ("Toyota Group",2019,5.2),("Toyota Group",2020,5.5),("Toyota Group",2021,5.8),
        ("Toyota Group",2022,6.5),("Toyota Group",2023,7.1),("Toyota Group",2024,7.8),("Toyota Group",2025,7.6),
        ("BMW Group",2019,7.2),("BMW Group",2020,6.9),("BMW Group",2021,6.8),
        ("BMW Group",2022,7.0),("BMW Group",2023,7.1),("BMW Group",2024,7.1),("BMW Group",2025,7.3),
        ("Mercedes-Benz",2019,6.1),("Mercedes-Benz",2020,5.8),("Mercedes-Benz",2021,5.6),
        ("Mercedes-Benz",2022,5.5),("Mercedes-Benz",2023,5.4),("Mercedes-Benz",2024,5.4),("Mercedes-Benz",2025,5.4),
        ("Tesla",2019,0.1),("Tesla",2020,0.3),("Tesla",2021,0.8),
        ("Tesla",2022,1.5),("Tesla",2023,2.2),("Tesla",2024,2.5),("Tesla",2025,1.8),
    ]
    return pd.DataFrame(data, columns=["group","year","market_share"])

def load_country_risk_matrix():
    data = [
        ("Norway",39.4,89.0,32.7,180,"EFTA"),("Lithuania",39.3,5.0,15.0,42,"EU"),
        ("Iceland",42.4,52.0,39.3,15,"EFTA"),("Latvia",31.4,4.0,12.5,23,"EU"),
        ("Bulgaria",15.1,1.5,7.6,49,"EU"),("Spain",12.9,6.0,24.0,1149,"EU"),
        ("Croatia",7.4,4.0,17.9,70,"EU"),("Poland",8.3,3.5,16.2,597,"EU"),
        ("Hungary",6.4,3.0,13.3,129,"EU"),("Greece",5.2,4.5,13.9,144,"EU"),
        ("Portugal",7.3,14.0,21.4,225,"EU"),("Ireland",3.0,18.0,24.5,125,"EU"),
        ("Germany",1.4,13.5,33.9,2858,"EU"),("Netherlands",1.7,33.0,21.8,388,"EU"),
        ("Austria",12.3,12.0,31.3,285,"EU"),("Sweden",1.3,38.0,26.0,273,"EU"),
        ("Denmark",6.7,51.0,31.3,185,"EU"),("United Kingdom",3.5,22.0,29.8,2021,"UK"),
        ("France",-5.0,16.9,23.9,1632,"EU"),("Italy",-2.1,4.5,25.8,1525,"EU"),
        ("Belgium",-7.5,15.0,35.4,415,"EU"),("Finland",-3.0,28.0,13.1,72,"EU"),
        ("Estonia",-48.6,15.0,9.3,13,"EU"),("Switzerland",-2.4,22.0,26.6,234,"EFTA"),
    ]
    df = pd.DataFrame(data, columns=["country","yoy_2025","bev_share","reg_per_1000","market_size_k","region"])
    def quad(r):
        hg = r["yoy_2025"]>2.4; hb = r["bev_share"]>13.6
        if hg and hb: return "⭐ Stars"
        if not hg and hb: return "🔋 EV Leaders"
        if hg and not hb: return "🚀 Growth Markets"
        return "⚠️ Watch"
    df["quadrant"] = df.apply(quad, axis=1)
    return df

def load_outlier_analysis():
    data = [
        ("Estonia",-48.6,"Subsidy removal shock",
         "EV purchase subsidy of €5,000 cancelled Dec 2024. Market was 60% subsidy-driven. Collapse was immediate.",
         "Leading indicator for any market removing EV subsidies abruptly. Watch Czech Republic and Slovakia."),
        ("Norway",+39.4,"BEV infrastructure maturity",
         "89% of new cars in 2025 are BEV. Strong Q1 driven by Tesla Model Y replacements and Volvo EX30.",
         "Norway is the template for mature EV transition — replicable only where infrastructure, tax policy and income align."),
        ("Iceland",+42.4,"Base effect + EV momentum",
         "Small market (14.5K units) recovering from 2022-2023 weakness. BEV share 52%.",
         "Statistical outlier due to small base. Not a trend signal for larger markets."),
        ("Lithuania",+39.3,"Fleet renewal + economic growth",
         "Baltic economies growing 4-5% GDP. Corporate fleet renewal after COVID backlog.",
         "Baltic states represent underserved fleet opportunity for mainstream brands."),
        ("Belgium",-7.5,"Company car tax reform",
         "Belgium tax reform tightened BIK rules on combustion company cars. Fleet buyers paused.",
         "Company car regimes drive ~60% of Belgium new sales. Any reform creates temporary paralysis."),
        ("France",-5.0,"Subsidy reduction + political uncertainty",
         "EV bonus cut from €7,000 to €4,000 mid-2024. Political instability froze industrial decisions.",
         "France -5% while Spain +12.9% — Iberian shift in EU auto gravity. Strategic significance."),
    ]
    return pd.DataFrame(data, columns=["country","yoy_2025","headline","mechanism","strategic_implication"])


# ── 30 brands embedded — independent of loader.py version ───────────────────
def _get_brands(year=2025):
    import pandas as pd
    d25 = [
        (1,"Volkswagen","Volkswagen Group",1452704,1371854,5.9,10.9),
        (2,"Toyota","Toyota Group",855000,928767,-7.4,6.4),
        (3,"Skoda","Volkswagen Group",840179,766469,9.6,6.3),
        (4,"BMW","BMW Group",800585,775119,3.3,6.0),
        (5,"Renault","Renault Group",750605,699151,7.4,5.7),
        (6,"Mercedes","Mercedes-Benz",710000,684027,3.8,5.4),
        (7,"Audi","Volkswagen Group",664680,662664,0.3,5.0),
        (8,"Peugeot","Stellantis",637834,641376,-0.6,4.8),
        (9,"Dacia","Renault Group",597088,578953,3.1,4.5),
        (10,"Hyundai","Hyundai Group",535205,534198,0.2,4.0),
        (11,"Kia","Hyundai Group",507304,529319,-4.2,3.8),
        (12,"Opel/Vauxhall","Stellantis",399782,414042,-3.4,3.0),
        (13,"Volvo","Volvo Cars",395000,369689,6.8,3.0),
        (14,"Ford","Ford",380000,426307,-10.9,2.9),
        (15,"Citroen","Stellantis",352521,358892,-1.8,2.7),
        (16,"Cupra","Volkswagen Group",297724,219637,35.6,2.2),
        (17,"Fiat","Stellantis",271098,304151,-10.9,2.0),
        (18,"Tesla","Tesla",240000,327034,-26.6,1.8),
        (19,"Nissan","Nissan",252000,307276,-18.0,1.9),
        (20,"Seat","Volkswagen Group",215636,263771,-18.2,1.6),
        (21,"MG","SAIC Motor",210000,244595,-14.1,1.6),
        (22,"Suzuki","Suzuki",203132,187852,8.1,1.5),
        (23,"Mini","BMW Group",169694,148303,14.4,1.3),
        (24,"Mazda","Mazda",172347,182535,-5.6,1.3),
        (25,"Jeep","Stellantis",126284,130486,-3.2,1.0),
        (26,"Jaguar/LR","JLR",150657,145490,3.6,1.1),
        (27,"Porsche","Volkswagen Group",91304,106922,-14.6,0.7),
        (28,"Alfa Romeo","Stellantis",59532,44919,32.5,0.4),
        (29,"BYD","BYD",48000,13000,269.2,0.4),
        (30,"Mitsubishi","Mitsubishi",60873,42823,42.2,0.5),
    ]
    d24 = [
        (1,"Volkswagen","Volkswagen Group",1371465,1357842,1.0,10.6),
        (2,"Toyota","Toyota Group",928767,828931,12.0,7.2),
        (3,"BMW","BMW Group",774925,729073,6.3,6.0),
        (4,"Skoda","Volkswagen Group",766469,679984,12.7,5.9),
        (5,"Renault","Renault Group",699151,681058,2.7,5.4),
        (6,"Mercedes","Mercedes-Benz",684027,671973,1.8,5.3),
        (7,"Audi","Volkswagen Group",662664,733305,-9.6,5.1),
        (8,"Peugeot","Stellantis",641376,637178,0.6,4.9),
        (9,"Dacia","Renault Group",578953,557154,3.9,4.5),
        (10,"Hyundai","Hyundai Group",534198,534307,0.0,4.1),
        (11,"Kia","Hyundai Group",529319,499321,6.0,4.1),
        (12,"Ford","Ford",426307,513481,-17.0,3.3),
        (13,"Opel/Vauxhall","Stellantis",414042,451238,-8.2,3.2),
        (14,"Citroen","Stellantis",358892,374100,-4.1,2.8),
        (15,"Volvo","Volvo Cars",369689,287832,28.4,2.9),
        (16,"Fiat","Stellantis",304151,321800,-5.5,2.3),
        (17,"Tesla","Tesla",327034,366829,-10.8,2.5),
        (18,"Nissan","Nissan",307276,293988,4.5,2.4),
        (19,"Seat","Volkswagen Group",263771,253291,4.1,2.0),
        (20,"Cupra","Volkswagen Group",219637,166216,32.1,1.7),
        (21,"MG","SAIC Motor",244595,232721,5.1,1.9),
        (22,"Suzuki","Suzuki",187852,175000,7.3,1.4),
        (23,"Mini","BMW Group",148303,145000,2.3,1.1),
        (24,"Mazda","Mazda",182535,193000,-5.4,1.4),
        (25,"Jeep","Stellantis",130486,141000,-7.4,1.0),
    ]
    c25 = ["rank","brand","group","sales_2025","sales_2024","pct_change","market_share"]
    c24 = ["rank","brand","group","sales_2024","sales_2023","pct_change","market_share"]
    return pd.DataFrame(d25,columns=c25) if year==2025 else pd.DataFrame(d24,columns=c24)



# ── Models by brand — all data inline, no external file needed ───────────────
_MODELS_BY_BRAND = {
    "Volkswagen":   [("Golf","Petrol/Diesel/Electric",215700,"+17%"),("Tiguan","Petrol/Diesel",195000,"+8%"),("T-Roc","Petrol/Diesel",180000,"-2%"),("Polo","Petrol",155000,"+3%"),("Passat","Petrol/PHEV",85000,"-5%")],
    "Toyota":       [("Yaris Cross","Hybrid",158000,"+12%"),("Yaris","Hybrid",148000,"+9%"),("C-HR","Hybrid",130000,"+22%"),("Corolla","Hybrid",120000,"+5%"),("RAV4","Hybrid/PHEV",105000,"+3%")],
    "Skoda":        [("Octavia","Petrol/Diesel",148000,"+8%"),("Karoq","Petrol/Diesel",125000,"+6%"),("Fabia","Petrol",118000,"+4%"),("Kodiaq","Petrol/Diesel",105000,"+15%"),("Scala","Petrol",62000,"+2%")],
    "BMW":          [("3 Series","Petrol/PHEV",145000,"+5%"),("X1","Petrol/Electric",138000,"+12%"),("1 Series","Petrol",120000,"+8%"),("X3","Petrol/PHEV",115000,"+3%"),("5 Series","Petrol/PHEV",85000,"+7%")],
    "Renault":      [("Clio","Petrol/Hybrid",245000,"+6%"),("Austral","Hybrid",135000,"+18%"),("Captur","Petrol/Hybrid",128000,"+4%"),("Megane E-Tech","Electric",65000,"+30%"),("Arkana","Hybrid",58000,"-5%")],
    "Mercedes":     [("A-Class","Petrol/Diesel",125000,"-3%"),("C-Class","Petrol/PHEV",118000,"+5%"),("GLC","Petrol/PHEV",105000,"+8%"),("E-Class","Petrol/PHEV",95000,"+12%"),("EQA/EQB","Electric",55000,"-10%")],
    "Audi":         [("A3","Petrol/Diesel",148000,"-2%"),("Q3","Petrol/Diesel",130000,"+4%"),("A4/A5","Petrol/PHEV",115000,"+8%"),("Q5","Petrol/PHEV/Electric",105000,"+6%"),("Q2","Petrol",62000,"-8%")],
    "Peugeot":      [("208","Petrol/Electric",215000,"+4%"),("2008","Petrol/Electric",148000,"+2%"),("308","Petrol/PHEV",95000,"-6%"),("3008","PHEV/Electric",88000,"+25%"),("e-208","Electric",68000,"+15%")],
    "Dacia":        [("Sandero","Petrol/LPG",258000,"-3%"),("Duster","Petrol/LPG/Hybrid",168000,"+22%"),("Jogger","Petrol/LPG",75000,"+8%"),("Spring","Electric",45000,"+35%"),("Bigster","Petrol/Hybrid",28000,"New")],
    "Hyundai":      [("Tucson","Petrol/Hybrid/PHEV",148000,"+5%"),("i20","Petrol",105000,"-3%"),("Kona","Petrol/Hybrid/Electric",98000,"+15%"),("IONIQ 5","Electric",65000,"-8%"),("i30","Petrol/Hybrid",62000,"-10%")],
    "Kia":          [("Sportage","Petrol/Hybrid/PHEV",168000,"+3%"),("Ceed","Petrol/Hybrid",95000,"-5%"),("EV6","Electric",72000,"-12%"),("Stonic","Petrol",62000,"-8%"),("Niro","Hybrid/PHEV/Electric",58000,"+5%")],
    "Opel/Vauxhall":[("Corsa","Petrol/Electric",148000,"-5%"),("Astra","Petrol/PHEV",95000,"-8%"),("Mokka","Petrol/Electric",88000,"-3%"),("Grandland","Petrol/PHEV/Electric",52000,"+5%"),("Crossland","Petrol",55000,"-15%")],
    "Volvo":        [("XC40","Petrol/Electric",115000,"+8%"),("XC60","Petrol/PHEV",95000,"+5%"),("EX30","Electric",58000,"New"),("XC90","Petrol/PHEV",45000,"+3%"),("S60/V60","Petrol/PHEV",38000,"-5%")],
    "Ford":         [("Puma","Petrol/Mild Hybrid",195000,"-3%"),("Kuga","Petrol/PHEV",118000,"-8%"),("Focus","Petrol/Diesel",88000,"-12%"),("Explorer","Electric",45000,"New"),("Mustang Mach-E","Electric",38000,"-20%")],
    "Citroen":      [("C3","Petrol/Electric",145000,"+5%"),("C5 Aircross","Petrol/PHEV",85000,"-5%"),("Berlingo","Petrol",75000,"+2%"),("C4","Petrol/Electric",62000,"-8%"),("e-C3","Electric",48000,"New")],
    "Cupra":        [("Formentor","Petrol/PHEV",128000,"+25%"),("Born","Electric",48000,"+35%"),("Ateca","Petrol",62000,"-5%"),("Terramar","Petrol/PHEV",38000,"New"),("Leon","Petrol/PHEV",22000,"-10%")],
    "Fiat":         [("Panda","Petrol",145000,"-8%"),("500","Petrol/Electric",98000,"-12%"),("600e","Electric",25000,"New"),("Tipo","Petrol/Diesel",52000,"-15%"),("500X","Petrol",38000,"-18%")],
    "Tesla":        [("Model Y","Electric",151550,"-28%"),("Model 3","Electric",58000,"-15%"),("Model S","Electric",8500,"-10%"),("Model X","Electric",6500,"-8%"),("Cybertruck","Electric",1200,"New")],
    "Nissan":       [("Juke","Petrol/Hybrid",125000,"-5%"),("Qashqai","Petrol/Mild Hybrid",118000,"-8%"),("X-Trail","Petrol/Hybrid",45000,"-10%"),("Leaf","Electric",35000,"-25%"),("Ariya","Electric",18000,"-30%")],
    "Seat":         [("Ibiza","Petrol",95000,"-12%"),("Arona","Petrol",78000,"-15%"),("Leon","Petrol/PHEV",72000,"-18%"),("Ateca","Petrol",45000,"-20%"),("Tarraco","Petrol/PHEV",28000,"-12%")],
    "MG":           [("MG ZS","Petrol/Electric",85000,"-10%"),("MG4","Electric",65000,"-15%"),("MG HS","Petrol/PHEV",28000,"+5%"),("MG5","Electric",22000,"-20%"),("Cyberster","Electric",3500,"New")],
    "Suzuki":       [("Swift","Petrol/Mild Hybrid",75000,"+8%"),("Vitara","Petrol/Mild Hybrid",62000,"+5%"),("S-Cross","Petrol/Mild Hybrid",38000,"+3%"),("Ignis","Petrol/Mild Hybrid",22000,"-5%"),("Jimny","Petrol",15000,"+10%")],
    "Mini":         [("Mini 3/5-door","Petrol/Electric",72000,"+12%"),("Countryman","Petrol/PHEV/Electric",58000,"+18%"),("Cooper E","Electric",22000,"New"),("Aceman","Electric",8000,"New"),("Clubman","Petrol",12000,"-30%")],
    "Mazda":        [("CX-5","Petrol/Diesel",68000,"-3%"),("CX-30","Petrol/Mild Hybrid",52000,"-5%"),("Mazda3","Petrol",38000,"-8%"),("CX-60","Petrol/PHEV",28000,"+15%"),("MX-30","Mild Hybrid/Electric",8000,"-20%")],
    "Jeep":         [("Avenger","Petrol/Electric",35000,"+40%"),("Renegade","Petrol/PHEV",48000,"-8%"),("Compass","Petrol/PHEV",38000,"-5%"),("Wrangler","Petrol/PHEV",8500,"-3%"),("Grand Cherokee","Petrol/PHEV",5500,"-10%")],
    "Jaguar/LR":    [("Defender","Petrol/PHEV",25000,"+8%"),("Range Rover Sport","Petrol/PHEV/Electric",28000,"+5%"),("Discovery Sport","Petrol/PHEV",22000,"-5%"),("Range Rover Evoque","Petrol/PHEV",20000,"-8%"),("Range Rover","Petrol/PHEV/Electric",12000,"+3%")],
    "Porsche":      [("Cayenne","Petrol/PHEV",35000,"-15%"),("Macan","Electric",28000,"+5%"),("911","Petrol/Hybrid",10000,"+1%"),("Panamera","Petrol/PHEV",7000,"-13%"),("Taycan","Electric",5000,"-45%")],
    "Alfa Romeo":   [("Tonale","Petrol/PHEV/Mild Hybrid",32000,"+35%"),("Stelvio","Petrol/Diesel",15000,"-5%"),("Giulia","Petrol/Diesel",8500,"-8%"),("Junior","Petrol/Electric",4000,"New")],
    "BYD":          [("Atto 3","Electric",18000,"+250%"),("Dolphin","Electric",9000,"+300%"),("Han","Electric",8500,"+200%"),("Seal","Electric",7500,"New"),("Tang","Electric",5000,"+150%")],
    "Mitsubishi":   [("Eclipse Cross","Petrol/PHEV",28000,"+15%"),("ASX","Petrol",18000,"+5%"),("Outlander PHEV","PHEV",12000,"-5%"),("Space Star","Petrol",4500,"-10%")],
}

def _get_models_for_brand(brand):
    import pandas as pd
    data = _MODELS_BY_BRAND.get(brand, [])
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data, columns=["model","fuel_type","eu_registrations_est","yoy_change"])




# ── Analytics functions — inline in dashboard (loader.py independent) ──────
import numpy as np




@st.cache_data
def get_data():
  c24 = load_sales_by_country(2024)
  c25 = load_sales_by_country(2025)
  yoy = build_yoy_comparison()
  yoy["sales_col"] = yoy["sales_2025"]
  co2 = load_co2_by_country()
  c25_ext = c25.merge(
    co2[["country","co2_gkm_2024","bev_share_pct_2024"]],
    on="country", how="left"
  )
  return {
    "c24": c24, "c25": c25, "c25_ext": c25_ext,
    "b24": _get_brands(2024), "b25": _get_brands(2025),
    "mod24": load_top_models_with_year(2024), "mod25": load_top_models_with_year(2025),
    "fuel": load_fuel_type_mix(),
    "seg": load_segment_share(),
    "co2": co2,
    "prod": load_production_by_country(),
    "yoy": yoy,
    "grp24": load_manufacturer_groups(2024),
    "grp25": load_manufacturer_groups(2025),
    "ratio": load_ratio_per_capita(),
        "monthly": load_monthly_data(),
        "forecast": load_forecast_2026(),
        "hhi": load_market_concentration(),
        "grp_evo": load_group_share_evolution(),
        "risk_matrix": load_country_risk_matrix(),
        "outliers": load_outlier_analysis(),
  }

D = get_data()


def data_badge(year, note=""):
    colors = {2025: ("#1D9E75","#EAF3DE"), 2024: ("#BA7517","#FAEEDA"), "mixed": ("#185FA5","#E6F1FB")}
    c, bg = colors.get(year, colors["mixed"])
    label = f"Data: {year}" if isinstance(year, int) else f"Data: {year}"
    n = f" · {note}" if note else ""
    return f'''<div style="display:inline-block;background:{bg};border:1px solid {c};border-radius:4px;
padding:3px 10px;font-size:11px;font-weight:600;color:{c};margin-bottom:12px">{label}{n}</div>'''

def kpi(label, value, delta, up, ctx=""):
  dc = "kpi-up" if up else "kpi-dn"
  a = "▲" if up else "▼"
  c = f'<div class="kpi-ctx">{ctx}</div>' if ctx else ""
  return f'<div class="kpi-card"><div class="kpi-lbl">{label}</div><div class="kpi-val">{value}</div><div class="{dc}">{a} {delta}</div>{c}</div>'

def insight(t):
  st.markdown(f'<div class="insight-box"><div class="insight-lbl">Strategic Insight</div><div class="insight-txt">{t}</div></div>', unsafe_allow_html=True)

def warning(t):
  st.markdown(f'<div class="warn-box"><div class="warn-lbl">Watch</div><div class="warn-txt">{t}</div></div>', unsafe_allow_html=True)

def risk(t):
  st.markdown(f'<div class="risk-box"><div class="risk-lbl">Risk</div><div class="risk-txt">{t}</div></div>', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_brand" not in st.session_state:
  st.session_state.selected_brand = "Volkswagen"
if "compare_a" not in st.session_state:
  st.session_state.compare_a = "Germany"
if "compare_b" not in st.session_state:
  st.session_state.compare_b = "Portugal"

# ── Sidebar — Global Filters ──────────────────────────────────────────────────
with st.sidebar:
  st.markdown("### 🚗 EU Car Market")
  st.markdown("---")

  st.markdown('<div class="filter-label">Year</div>', unsafe_allow_html=True)
  year = st.radio("", [2024, 2025], index=1, horizontal=True, label_visibility="collapsed")

  st.markdown('<div class="filter-label">Region</div>', unsafe_allow_html=True)
  region_filter = st.selectbox("", ["All regions", "EU only", "EFTA only", "UK only"], label_visibility="collapsed")

  df_raw = D["c25"] if year == 2025 else D["c24"]
  sales_col = "sales_2025" if year == 2025 else "sales_2024"

  if region_filter == "EU only":
    df_raw = df_raw[df_raw["region"] == "EU"]
  elif region_filter == "EFTA only":
    df_raw = df_raw[df_raw["region"] == "EFTA"]
  elif region_filter == "UK only":
    df_raw = df_raw[df_raw["region"] == "UK"]

  st.markdown('<div class="filter-label">Countries</div>', unsafe_allow_html=True)
  all_countries = sorted(df_raw["country"].tolist())
  selected_countries = st.multiselect("", all_countries, default=all_countries, label_visibility="collapsed")

  if not selected_countries:
    selected_countries = all_countries

  df = df_raw[df_raw["country"].isin(selected_countries)].copy()

  st.markdown('<div class="filter-label">Top N markets</div>', unsafe_allow_html=True)
  top_n = st.slider("", 5, 31, 15, label_visibility="collapsed")

  st.markdown("---")
  st.markdown("**Data sources**")
  st.markdown("ACEA · JATO Dynamics\nS&P Global Mobility\nICCT / EEA")
  st.markdown("---")
  st.caption("Maria João Luz · mariajoaoluz.com")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="report-title">🚗 European Car Market — {year}</div>', unsafe_allow_html=True)
st.markdown(f"**{len(selected_countries)} markets selected · {region_filter} · Source: ACEA / JATO / S&P Global Mobility · All data in units (new car registrations)**")
st.divider()

# ── KPIs ──────────────────────────────────────────────────────────────────────
total = df[sales_col].sum()
prev_col = "sales_2024" if year == 2025 else "sales_2023"
if prev_col in df.columns:
  prev = df[prev_col].sum()
  delta_total = (total - prev) / prev * 100
else:
  delta_total = 2.4

top_country = df.nlargest(1, sales_col).iloc[0]
top_brand = D["b25"].iloc[0] if year == 2025 else D["b24"].iloc[0]
bev = D["fuel"][D["fuel"]["year"] == year]["bev_pct"].values[0] if year in D["fuel"]["year"].values else (17.4 if year == 2025 else 13.6)

st.markdown('<div style="background:#EAF3FB;border-left:4px solid #185FA5;border-radius:4px;padding:8px 16px;margin-bottom:4px;font-size:13px;color:#1a3a5c">📊 <strong>All data = new passenger car registrations (units) — not monetary value · not total fleet · not used cars</strong> &nbsp;·&nbsp; Source: ACEA · JATO · S&P Global Mobility · ICCT &nbsp;·&nbsp; 31 markets: EU27+EFTA+UK</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.markdown(kpi(f"Total registrations {year}", f"{total/1e6:.2f}M", f"{delta_total:.1f}% vs {year-1}", delta_total>0), unsafe_allow_html=True)
with k2: st.markdown(kpi(f"Largest market {year}", top_country["country"], f"{top_country[sales_col]/1e6:.2f}M units", True), unsafe_allow_html=True)
with k3: st.markdown(kpi(f"Top brand {year}", top_brand["brand"], f"{top_brand[f'sales_{year}']/1e6:.2f}M units", True), unsafe_allow_html=True)
with k4: st.markdown(kpi(f"BEV share EU {year}", f"{bev}%", f"of all new cars {year}", bev > 13), unsafe_allow_html=True)
with k5:
  pt = df[df["country"]=="Portugal"]
  if len(pt):
    pv = pt[sales_col].values[0]
    st.markdown(kpi(f"Portugal {year}", f"{pv/1e3:.0f}K", f"{pt['pct_change'].values[0]:+.1f}% YoY" if "pct_change" in pt.columns else f"+7.3% vs {year-1}", True), unsafe_allow_html=True)
  else:
    st.markdown(kpi(f"Markets selected {year}", f"{len(selected_countries)}", f"of 31 total", True), unsafe_allow_html=True)

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
  "🗺️ Market Map",
  "📊 Rankings",
  "🔄 YoY Evolution",
  "🏎️ Brand Drill-down",
  "⚖️ Country Comparison",
  "⚡ Technology",
  "🏭 Production",
  "👥 Demographics",
  "📋 Executive Summary",
  "📈 Monthly Trend & Forecast",
  "🔬 Strategic Analytics",
  "📚 Data Coverage",
])

# ── TAB 1: MAP ────────────────────────────────────────────────────────────────
with tabs[0]:
  st.markdown('<div class="section-hd">Market Map</div>', unsafe_allow_html=True)

  col_ctrl, _ = st.columns([1, 2])
  with col_ctrl:
    map_metric = st.selectbox("Map metric", [
      "Vehicle Registrations",
      "YoY Change (%)",
      "CO₂ emissions (g/km)",
      "BEV share (%)",
      "New reg. per 1,000 people",
    ])

  map_df = D["c25_ext"].copy()
  map_df["iso"] = map_df["country"].map(ISO)
  map_df = map_df.merge(
    D["co2"][["country","co2_gkm_2024","bev_share_pct_2024"]], on="country", how="left",
    suffixes=("","_y")
  )
  # Use correct per-capita data from load_ratio_per_capita (new registrations / population)
  map_df = map_df.merge(
    D["ratio"][["country","reg_per_1000_2025"]].rename(columns={"reg_per_1000_2025":"cars_per_1000"}),
    on="country", how="left"
  )

  if map_metric == "Vehicle Registrations":
    color_col = "sales_2025"; title = f"New car registrations {year}"; fmt = ":,.0f"
    scale = [[0,"#E6F1FB"],[0.25,"#85B7EB"],[0.6,"#378ADD"],[1,"#042C53"]]
  elif map_metric == "YoY Change (%)":
    color_col = "pct_change"; title = "YoY change 2024→2025 (%)"; fmt = ":+.1f"
    scale = [[0,"#D85A30"],[0.5,"#f5f5f5"],[1,"#1D9E75"]]
  elif map_metric == "CO₂ emissions (g/km)":
    color_col = "co2_gkm_2024_y" if "co2_gkm_2024_y" in map_df.columns else "co2_gkm_2024"
    title = "Average CO₂ g/km (2024)"; fmt = ":.1f"
    scale = [[0,"#1D9E75"],[0.5,"#FAEEDA"],[1,"#D85A30"]]
  elif map_metric == "BEV share (%)":
    color_col = "bev_share_pct_2024_y" if "bev_share_pct_2024_y" in map_df.columns else "bev_share_pct_2024"
    title = "BEV market share % (2024)"; fmt = ":.1f"
    scale = [[0,"#f5f5f5"],[0.5,"#85B7EB"],[1,"#042C53"]]
  else:
    color_col = "cars_per_1000"; title = "New car registrations per 1,000 people (2025)"; fmt = ":.0f"
    scale = [[0,"#E6F1FB"],[1,"#042C53"]]

  map_plot = map_df.dropna(subset=["iso", color_col])
  fig_map = px.choropleth(
    map_plot, locations="iso", color=color_col,
    hover_name="country",
    hover_data={color_col: fmt, "iso": False},
    color_continuous_scale=scale,
    scope="europe", title=title,
  )
  fig_map.update_layout(
    margin=dict(l=0,r=0,t=40,b=0), height=480,
    geo=dict(showframe=False, showcoastlines=False,
         bgcolor="rgba(0,0,0,0)", projection_scale=1.4,
         center=dict(lat=54,lon=14)),
    paper_bgcolor="rgba(0,0,0,0)",
    title_font_size=14,
    coloraxis_colorbar=dict(title="", tickformat=".2s", len=0.7),
  )
  st.plotly_chart(fig_map, use_container_width=True)

# ── TAB 2: RANKINGS ───────────────────────────────────────────────────────────
with tabs[1]:
  st.markdown('<div class="section-hd">Market Rankings</div>', unsafe_allow_html=True)

  col_r1, col_r2 = st.columns(2)

  with col_r1:
    st.markdown(f"##### Top {top_n} markets — passenger car registrations ({year})")
    top = df.nlargest(top_n, sales_col).sort_values(sales_col)
    fig = go.Figure(go.Bar(
      x=top[sales_col], y=top["country"], orientation="h",
      marker_color=[CORAL if c == "Portugal" else (AMBER if c == "Spain" else BLUE)
             for c in top["country"]],
      text=top[sales_col].apply(lambda x: f"{x:,.0f}"),
      textposition="outside", textfont=dict(size=9),
    ))
    fig.update_layout(height=max(300, top_n*22),
      margin=dict(l=0,r=80,t=10,b=10),
      xaxis=dict(tickformat=".2s", gridcolor=LGRAY),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
      font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)

  with col_r2:
    st.markdown(f"##### Top 10 brands — {year}")
    brands = D["b25"] if year == 2025 else D["b24"]
    bc = f"sales_{year}"
    if bc not in brands.columns:
      bc = [c for c in brands.columns if c.startswith("sales_")][0]
    brands_s = brands.sort_values(bc)
    fig = go.Figure(go.Bar(
      x=brands_s[bc], y=brands_s["brand"], orientation="h",
      marker_color=COLORS[:10][::-1][:len(brands_s)],
      text=brands_s[bc].apply(lambda x: f"{x/1e3:.0f}K"),
      textposition="outside", textfont=dict(size=9),
    ))
    fig.update_layout(height=320,
      margin=dict(l=0,r=60,t=10,b=10),
      xaxis=dict(tickformat=".2s", gridcolor=LGRAY),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
      font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)

  st.divider()
  # Top 10 models — centred full-width below the two columns
  st.markdown(f"##### Top 10 models — new car registrations Europe {year}")
  _mod_key = f"mod{year}" if f"mod{year}" in D else "mod24"
  tbl = D[_mod_key][["rank","model","brand","fuel_type"]].copy()
  tbl.columns = ["#","Model","Brand","Fuel"]
  _l, _c, _r = st.columns([1, 2, 1])
  with _c:
    st.dataframe(tbl, hide_index=True, use_container_width=True, height=380)
  st.markdown('<div class="data-note">Source: JATO Dynamics · EU+EFTA+UK full year · Units (new registrations)</div>', unsafe_allow_html=True)

  st.divider()
  st.markdown("##### Registration ratio per person — 2025 (registrations per 1,000 people)")
  ratio_df = D["ratio"].copy()
  ratio_df = ratio_df[ratio_df["country"].isin(selected_countries)].sort_values("reg_per_1000_2025")

  fig_ratio = go.Figure()
  fig_ratio.add_trace(go.Bar(
    x=ratio_df["reg_per_1000_2025"],
    y=ratio_df["country"],
    orientation="h",
    marker_color=[CORAL if c == "Portugal" else (AMBER if c == "Spain" else
           TEAL if ratio_df[ratio_df["country"]==c]["reg_per_1000_2025"].values[0] > 21.4 else BLUE)
           for c in ratio_df["country"]],
    text=[f"{v:.1f} (1 por every {n} people)"
       for v, n in zip(ratio_df["reg_per_1000_2025"], ratio_df["1_per_n_2025"])],
    textposition="outside",
    textfont=dict(size=9),
    customdata=ratio_df[["population_m","sales_2025","1_per_n_2025"]].values,
    hovertemplate=(
      "<b>%{y}</b><br>"
      "Registrations por 1000 people: %{x:.1f}<br>"
      "Total registrations: %{customdata[1]:,.0f}<br>"
      "Population: %{customdata[0]:.1f}M<br>"
      "1 reg. per every %{customdata[2]} people<extra></extra>"
    ),
  ))
  pt_val = ratio_df[ratio_df["country"]=="Portugal"]["reg_per_1000_2025"].values
  if len(pt_val):
    fig_ratio.add_vline(x=pt_val[0], line_dash="dot", line_color=CORAL,
      annotation_text=f"Portugal {pt_val[0]:.1f}",
      annotation_font=dict(size=9, color=CORAL))
  fig_ratio.update_layout(
    height=max(350, len(ratio_df)*18),
    margin=dict(l=0, r=200, t=20, b=10),
    xaxis=dict(title="New registrations per 1,000 people (2025)", gridcolor=LGRAY),
    yaxis=dict(tickfont=dict(size=10)),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(size=11),
    showlegend=False,
  )
  st.plotly_chart(fig_ratio, use_container_width=True)
  st.markdown('<div class="data-note">Source: ACEA 2025 · Population: Eurostat 2024 · Note: new passenger car registrations, not monetary value</div>', unsafe_allow_html=True)

# ── TAB 3: YOY EVOLUTION ─────────────────────────────────────────────────────
with tabs[2]:
  st.markdown('<div class="section-hd">Year-on-Year Evolution</div>', unsafe_allow_html=True)

  yoy = D["yoy"][D["yoy"]["country"].isin(selected_countries)].dropna(subset=["pct_change"]).copy()
  yoy = yoy.sort_values("pct_change")

  _avail_yoy = sorted(yoy["country"].tolist())
  _def_yoy = [c for c in ["Portugal","Spain","Germany"] if c in _avail_yoy]
  highlight = st.multiselect("Highlight countries", _avail_yoy, default=_def_yoy)
  def bar_color(row):
    if row["country"] in highlight:
      return CORAL if row["pct_change"] < 0 else AMBER
    return TEAL if row["pct_change"] >= 0 else "#E0E0E0"

  yoy["color"] = yoy.apply(bar_color, axis=1)

  fig = go.Figure(go.Bar(
    x=yoy["pct_change"], y=yoy["country"], orientation="h",
    marker_color=yoy["color"],
    text=[f"{v:+.1f}%" for v in yoy["pct_change"]],
    textposition="outside", textfont=dict(size=9),
    customdata=yoy[["sales_2025","sales_2024"]].values,
    hovertemplate="<b>%{y}</b><br>Change: %{x:+.1f}%<br>2025: %{customdata[0]:,.0f}<br>2024: %{customdata[1]:,.0f}<extra></extra>",
  ))
  fig.add_vline(x=2.4, line_dash="dash", line_color=BLUE,
    annotation_text="EU avg +2.4%", annotation_font=dict(size=10, color=BLUE))
  fig.add_vline(x=0, line_color=GRAY, line_width=0.8)
  fig.update_layout(
    height=max(400, len(yoy)*18),
    margin=dict(l=0,r=70,t=30,b=10),
    xaxis=dict(title="YoY Change vs 2024 (%)", gridcolor=LGRAY, zeroline=False),
    yaxis=dict(tickfont=dict(size=10)),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
  st.plotly_chart(fig, use_container_width=True)

# ── TAB 4: BRAND DRILL-DOWN ───────────────────────────────────────────────────
with tabs[3]:
  st.markdown('<div class="section-hd">Brand Drill-down</div>', unsafe_allow_html=True)

  all_brands = D["b25"]["brand"].tolist()
  _brand_idx = all_brands.index(st.session_state.selected_brand) if st.session_state.selected_brand in all_brands else 0
  selected_brand = st.selectbox("Select brand", all_brands, index=_brand_idx)

  st.session_state.selected_brand = selected_brand

  b25_row = D["b25"][D["b25"]["brand"] == selected_brand].iloc[0] if len(D["b25"][D["b25"]["brand"] == selected_brand]) else None
  b24_row = D["b24"][D["b24"]["brand"] == selected_brand].iloc[0] if len(D["b24"][D["b24"]["brand"] == selected_brand]) else None

  if b25_row is not None:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi("Sales 2025", f"{b25_row['sales_2025']/1e3:.0f}K", f"{b25_row['pct_change']:+.1f}% vs 2024", b25_row['pct_change']>0), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Market share 2025", f"{b25_row['market_share']:.1f}%", "of EU+EFTA+UK", True, b25_row["group"]), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Rank 2025", f"#{b25_row['rank']}", "in Europe", True), unsafe_allow_html=True)
    with c4:
      if b24_row is not None:
        st.markdown(kpi("Sales 2024", f"{b24_row['sales_2024']/1e3:.0f}K", f"rank #{b24_row['rank']}", True), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_trend, col_models = st.columns([1, 1])

    with col_trend:
      st.markdown(f"##### {selected_brand} — sales trend 2024 vs 2025")
      trend_data = []
      if b24_row is not None:
        trend_data.append({"year": 2024, "sales": b24_row["sales_2024"]})
      if b25_row is not None:
        trend_data.append({"year": 2025, "sales": b25_row["sales_2025"]})

      if len(trend_data) == 2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
          x=[str(r["year"]) for r in trend_data],
          y=[r["sales"] for r in trend_data],
          marker_color=[BLUE if i==0 else (TEAL if trend_data[1]["sales"] > trend_data[0]["sales"] else CORAL)
                 for i in range(len(trend_data))],
          text=[f"{r['sales']/1e6:.2f}M ({r['sales']/1e3:.0f}K)" for r in trend_data],
          textposition="outside",
        ))
        pct = (trend_data[1]["sales"] - trend_data[0]["sales"]) / trend_data[0]["sales"] * 100
        fig.add_annotation(
          x=0.5, y=max(r["sales"] for r in trend_data) * 1.15,
          xref="paper",
          text=f"Change: {pct:+.1f}%",
          showarrow=False,
          font=dict(size=14, color=TEAL if pct>0 else CORAL)
        )
        fig.update_layout(height=280,
          margin=dict(l=0,r=0,t=40,b=10),
          xaxis=dict(type="category", tickfont=dict(size=13)),
          yaxis=dict(tickformat=".2s", gridcolor=LGRAY),
          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
          showlegend=False, font=dict(size=12))
        st.plotly_chart(fig, use_container_width=True)

    with col_models:
      st.markdown(f"##### Top models from {selected_brand} — 2024")
      brand_models = _get_models_for_brand(selected_brand)
      if len(brand_models):
        st.dataframe(
          brand_models[["model","fuel_type","eu_registrations_est","yoy_change"]].rename(
            columns={"model":"Model","fuel_type":"Fuel","eu_registrations_est":"EU Reg. (est.)","yoy_change":"YoY"}
          ),
          hide_index=True, use_container_width=True
        )
      else:
        st.info(f"No top-10 models for {selected_brand} in 2024 data.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"##### Group context — {b25_row['group']}")
    grp = D["grp25"][D["grp25"]["group"] == b25_row["group"]]
    if len(grp):
      g = grp.iloc[0]
      gc1, gc2, gc3 = st.columns(3)
      with gc1: st.metric("Group total 2025", f"{g['sales_2025']/1e6:.2f}M", f"{g['pct_change']:+.1f}%")
      with gc2: st.metric("Group market share", f"{g['market_share']:.1f}%")
      with gc3: st.metric(f"{selected_brand} share of group", f"{b25_row['sales_2025']/g['sales_2025']*100:.1f}%")

# ── TAB 5: COUNTRY COMPARISON ─────────────────────────────────────────────────
with tabs[4]:
  st.markdown('<div class="section-hd">Comparison Tool</div>', unsafe_allow_html=True)

  compare_mode = st.radio("Compare by", ["🌍 Country", "🏎️ Brand", "🏭 Group"],
    horizontal=True, label_visibility="collapsed")

  st.markdown("<br>", unsafe_allow_html=True)

  def render_comparison_table(name_a, name_b, row_a, row_b, metrics_list):
    def diff_str(key, va, vb):
      if va is None or vb is None: return "—"
      try:
        d = float(vb) - float(va)
        if key in ("pct_change","yoy"): return f"{d:+.1f} pp"
        if key in ("co2","bev","reg_per_1000","market_share"): return f"{d:+.1f}"
        if key == "1_per_n": return f"{d:+.0f} people"
        return f"{d:+,.0f}"
      except: return "—"

    rows_html = ""
    for label, key, fmt in metrics_list:
      va = row_a.get(key); vb = row_b.get(key)
      va_str = fmt(va) if va is not None else "—"
      vb_str = fmt(vb) if vb is not None else "—"
      d_str = diff_str(key, va, vb)
      try:
        d_num = float(vb) - float(va) if va is not None and vb is not None else 0
        d_color = "#1D9E75" if d_num > 0 else ("#D85A30" if d_num < 0 else "#888")
      except: d_color = "#888"
      rows_html += f"""<tr>
<td style="padding:10px 12px;color:#888;font-size:13px;border-bottom:0.5px solid #f0f0f0">{label}</td>
<td style="padding:10px 12px;font-size:15px;font-weight:600;color:#0d1b2a;border-bottom:0.5px solid #f0f0f0">{va_str}</td>
<td style="padding:10px 12px;font-size:15px;font-weight:600;color:#0d1b2a;border-bottom:0.5px solid #f0f0f0">{vb_str}</td>
<td style="padding:10px 12px;font-size:13px;color:{d_color};font-weight:500;border-bottom:0.5px solid #f0f0f0">{d_str}</td>
</tr>"""
    st.markdown(f"""
<table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;border:0.5px solid #e0e0e0">
<thead><tr style="background:#f5f5f5">
<th style="padding:12px;text-align:left;font-size:12px;color:#888;font-weight:600;text-transform:uppercase">Metric</th>
<th style="padding:12px;text-align:left;font-size:14px;color:#0d1b2a;font-weight:700">{name_a}</th>
<th style="padding:12px;text-align:left;font-size:14px;color:#0d1b2a;font-weight:700">{name_b}</th>
<th style="padding:12px;text-align:left;font-size:12px;color:#888;font-weight:600;text-transform:uppercase">Difference</th>
</tr></thead><tbody>{rows_html}</tbody></table>""", unsafe_allow_html=True)

  # ── COUNTRY MODE ─────────────────────────────────────────────────────────────
  if compare_mode == "🌍 Country":
    all_c = sorted(D["c25"]["country"].tolist())
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
      _ca = st.session_state.compare_a if st.session_state.compare_a in all_c else all_c[0]
      ca = st.selectbox("Country A", all_c, index=all_c.index(_ca))
      st.session_state.compare_a = ca
    with col_sel2:
      _cb = st.session_state.compare_b if st.session_state.compare_b in all_c else (all_c[1] if len(all_c)>1 else all_c[0])
      cb = st.selectbox("Country B", all_c, index=all_c.index(_cb))
      st.session_state.compare_b = cb

    def get_country_row(country):
      r25 = D["c25"][D["c25"]["country"]==country]
      co2r = D["co2"][D["co2"]["country"]==country]
      prodr = D["prod"][D["prod"]["country"]==country]
      ratio_r = D["ratio"][D["ratio"]["country"]==country]
      return {
        "sales_2025": int(r25["sales_2025"].values[0]) if len(r25) else 0,
        "sales_2024": int(r25["sales_2024"].values[0]) if len(r25) else 0,
        "pct_change": float(r25["pct_change"].values[0]) if len(r25) else 0,
        "co2": float(co2r["co2_gkm_2024"].values[0]) if len(co2r) else None,
        "bev": float(co2r["bev_share_pct_2024"].values[0]) if len(co2r) else None,
        "produced": int(prodr["cars_produced"].values[0]) if len(prodr) else 0,
        "reg_per_1000": float(ratio_r["reg_per_1000_2025"].values[0]) if len(ratio_r) else None,
        "1_per_n": int(ratio_r["1_per_n_2025"].values[0]) if len(ratio_r) else None,
      }

    ra, rb = get_country_row(ca), get_country_row(cb)
    metrics = [
      ("Registrations 2025","sales_2025",lambda v: f"{v:,.0f}"),
      ("Registrations 2024","sales_2024",lambda v: f"{v:,.0f}"),
      ("YoY Change","pct_change",lambda v: f"{v:+.1f}%"),
      ("CO₂ g/km (2024)","co2",lambda v: f"{v:.1f} g/km" if v else "—"),
      ("BEV share (2024)","bev",lambda v: f"{v:.1f}%" if v else "—"),
      ("Vehicles produced","produced",lambda v: f"{v:,.0f}" if v else "—"),
      ("Reg. per 1,000 people","reg_per_1000",lambda v: f"{v:.1f}" if v else "—"),
      ("1 reg. per","1_per_n",lambda v: f"every {v} people" if v else "—"),
    ]
    render_comparison_table(ca, cb, ra, rb, metrics)
    st.markdown('<div class="data-note">Source: ACEA / ICCT 2024-2025 · new passenger car registrations (units)</div>', unsafe_allow_html=True)

  # ── BRAND MODE ────────────────────────────────────────────────────────────────
  elif compare_mode == "🏎️ Brand":
    all_brands = D["b25"]["brand"].tolist()
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
      ba = st.selectbox("Brand A", all_brands, index=0)
    with col_sel2:
      ba_idx = all_brands.index("Toyota") if "Toyota" in all_brands else 1
      bb = st.selectbox("Brand B", all_brands, index=ba_idx)

    def get_brand_row(brand, yr=2025):
      b = D["b25"] if yr==2025 else D["b24"]
      r = b[b["brand"]==brand]
      if not len(r): return {}
      r = r.iloc[0]
      sc = "sales_2025" if yr==2025 else "sales_2024"
      sp = "sales_2024" if yr==2025 else "sales_2023"
      return {
        "sales_cur": int(r[sc]),
        "sales_prev": int(r[sp]) if sp in r.index else None,
        "yoy": float(r["pct_change"]),
        "market_share": float(r["market_share"]),
        "rank": int(r["rank"]),
        "group": r["group"],
      }

    ra, rb = get_brand_row(ba, year), get_brand_row(bb, year)
    sc_label = f"Registrations {year}"
    sp_label = f"Registrations {year-1}"
    metrics = [
      (sc_label,"sales_cur",lambda v: f"{v:,.0f}" if v else "—"),
      (sp_label,"sales_prev",lambda v: f"{v:,.0f}" if v else "—"),
      ("YoY Change","yoy",lambda v: f"{v:+.1f}%"),
      ("Market share","market_share",lambda v: f"{v:.1f}%"),
      ("EU Rank","rank",lambda v: f"#{v}"),
      ("Group","group",lambda v: str(v)),
    ]
    render_comparison_table(ba, bb, ra, rb, metrics)

    # Mini bar chart
    st.markdown("<br>", unsafe_allow_html=True)
    _sc = f"sales_{year}"
    fig_bc = go.Figure()
    for brand, color in [(ba, BLUE), (bb, CORAL)]:
      b_df = D["b25"] if year==2025 else D["b24"]
      r = b_df[b_df["brand"]==brand]
      if len(r):
        fig_bc.add_trace(go.Bar(name=brand, x=[str(year-1), str(year)],
          y=[r[f"sales_{year-1}"].values[0] if f"sales_{year-1}" in r.columns else 0,
             r[_sc].values[0]],
          marker_color=color))
    fig_bc.update_layout(barmode="group", height=250,
      margin=dict(l=0,r=0,t=10,b=10),
      yaxis=dict(tickformat=".2s",gridcolor=LGRAY),
      legend=dict(orientation="h",y=-0.2),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
    st.plotly_chart(fig_bc, use_container_width=True)
    st.markdown('<div class="data-note">Source: ACEA / best-selling-cars.com · EU+EFTA+UK · Units (new registrations)</div>', unsafe_allow_html=True)

  # ── GROUP MODE ────────────────────────────────────────────────────────────────
  elif compare_mode == "🏭 Group":
    all_groups = D["grp25"]["group"].tolist()
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
      ga = st.selectbox("Group A", all_groups, index=0)
    with col_sel2:
      gb_idx = 1 if len(all_groups) > 1 else 0
      gb = st.selectbox("Group B", all_groups, index=gb_idx)

    def get_group_row(group, yr=2025):
      g = D["grp25"] if yr==2025 else D["grp24"]
      r = g[g["group"]==group]
      if not len(r): return {}
      r = r.iloc[0]
      sc = "sales_2025" if yr==2025 else "sales_2024"
      sp = "sales_2024" if yr==2025 else "sales_2023"
      brands_in_group = D["b25"][D["b25"]["group"]==group]["brand"].tolist()
      return {
        "sales_cur": int(r[sc]),
        "sales_prev": int(r[sp]) if sp in r.index else None,
        "yoy": float(r["pct_change"]),
        "market_share": float(r["market_share"]),
        "num_brands": len(brands_in_group),
        "top_brands": ", ".join(brands_in_group[:3]),
      }

    ra, rb = get_group_row(ga, year), get_group_row(gb, year)
    metrics = [
      (f"Registrations {year}","sales_cur",lambda v: f"{v:,.0f}" if v else "—"),
      (f"Registrations {year-1}","sales_prev",lambda v: f"{v:,.0f}" if v else "—"),
      ("YoY Change","yoy",lambda v: f"{v:+.1f}%"),
      ("Market share","market_share",lambda v: f"{v:.1f}%"),
      ("Brands in group","num_brands",lambda v: str(v)),
      ("Key brands","top_brands",lambda v: str(v)),
    ]
    render_comparison_table(ga, gb, ra, rb, metrics)

    # Group share evolution mini chart
    st.markdown("<br>", unsafe_allow_html=True)
    gevo = D["grp_evo"]
    fig_ge = go.Figure()
    for grp, color in [(ga, BLUE), (gb, CORAL)]:
      gdf = gevo[gevo["group"]==grp]
      if len(gdf):
        fig_ge.add_trace(go.Scatter(x=gdf["year"], y=gdf["market_share"],
          name=grp, mode="lines+markers",
          line=dict(color=color, width=2.5), marker=dict(size=7)))
    fig_ge.update_layout(height=250, margin=dict(l=0,r=0,t=20,b=10),
      yaxis=dict(title="Market share (%)",ticksuffix="%",gridcolor=LGRAY),
      xaxis=dict(tickvals=list(range(2019,2026))),
      legend=dict(orientation="h",y=-0.2),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
    st.plotly_chart(fig_ge, use_container_width=True)
    st.markdown('<div class="data-note">Source: ACEA 2023-2025 confirmed · 2019-2022 estimates · EU+EFTA+UK</div>', unsafe_allow_html=True)

# ── TAB 6: TECHNOLOGY ─────────────────────────────────────────────────────────
with tabs[5]:
  st.markdown('<div class="section-hd">Technology Transition</div>', unsafe_allow_html=True)

  k1, k2, k3, k4 = st.columns(4)
  with k1: st.markdown(kpi("BEV share 2024","13.6%","vs 14.6% in 2023",False,"First-ever decline"), unsafe_allow_html=True)
  with k2: st.markdown(kpi("SUV share 2024","53%","of all EU sales",True,"Up from 19% in 2015"), unsafe_allow_html=True)
  with k3: st.markdown(kpi("EU CO₂ 2024","107.8 g/km","vs target 93.6",False,"14 g/km gap"), unsafe_allow_html=True)
  with k4: st.markdown(kpi("BEV Q1 2026","20.6%","record EU share",True,"vs 15.2% Q1 2025"), unsafe_allow_html=True)

  st.markdown("<br>", unsafe_allow_html=True)
  col_f, col_s = st.columns([1.3, 1])

  with col_f:
    st.markdown("##### Powertrain mix evolution — EU 2021→2024")
    years_sel = st.multiselect("Years", [2021,2022,2023,2024], default=[2021,2022,2023,2024])
    fuels_sel = st.multiselect("Fuel types",
      ["Petrol","Diesel","Battery EV","Plug-in Hybrid","Hybrid"],
      default=["Petrol","Diesel","Battery EV","Plug-in Hybrid","Hybrid"])

    fuel_long = D["fuel"][D["fuel"]["year"].isin(years_sel)].melt(
      id_vars="year",
      value_vars=["petrol_pct","diesel_pct","bev_pct","phev_pct","hybrid_pct"],
      var_name="fuel", value_name="pct"
    )
    fuel_long["fuel"] = fuel_long["fuel"].map({
      "petrol_pct":"Petrol","diesel_pct":"Diesel","bev_pct":"Battery EV",
      "phev_pct":"Plug-in Hybrid","hybrid_pct":"Hybrid"})
    fuel_long = fuel_long[fuel_long["fuel"].isin(fuels_sel)]

    fig = px.bar(fuel_long, x="year", y="pct", color="fuel",
      color_discrete_map={"Petrol":AMBER,"Diesel":GRAY,"Battery EV":BLUE,
                "Plug-in Hybrid":TEAL,"Hybrid":"#534AB7"},
      labels={"pct":"Market share (%)","year":"","fuel":""}, text="pct")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside", textfont_size=9)
    fig.update_layout(barmode="stack", height=320,
      margin=dict(l=0,r=0,t=10,b=40),
      legend=dict(orientation="h",y=-0.15),
      yaxis=dict(ticksuffix="%",gridcolor=LGRAY,range=[0,105]),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)

  with col_s:
    st.markdown("##### Body segment share — 2024")
    fig = px.pie(D["seg"], values="share_pct", names="segment",
      color_discrete_sequence=COLORS, hole=0.55)
    fig.update_traces(textinfo="label+percent", textfont_size=11)
    fig.update_layout(height=220, margin=dict(l=0,r=0,t=0,b=0),
      showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    risk("BEV share fell in 2024 for the first time ever — EU 2025 targets create compliance pressure on all OEMs.")
    insight("Q1 2026 BEV share hit 20.6% — a record. Recovery confirmed.")

  st.divider()
  st.markdown("##### CO₂ emissions by country vs EU target — 2024")
  co2_chart = D["co2"][D["co2"]["country"] != "EU average"].sort_values("co2_gkm_2024")
  fig = go.Figure(go.Bar(
    x=co2_chart["co2_gkm_2024"], y=co2_chart["country"], orientation="h",
    marker_color=[TEAL if v<93.6 else (AMBER if v<107.8 else CORAL) for v in co2_chart["co2_gkm_2024"]],
    text=[f"{v:.0f}" for v in co2_chart["co2_gkm_2024"]],
    textposition="outside", textfont=dict(size=10),
  ))
  fig.add_vline(x=93.6, line_dash="dash", line_color=BLUE,
    annotation_text="2025 target 93.6", annotation_font=dict(size=9,color=BLUE))
  fig.add_vline(x=107.8, line_dash="dot", line_color=GRAY,
    annotation_text="EU avg 107.8", annotation_font=dict(size=9,color=GRAY))
  fig.update_layout(height=300, margin=dict(l=0,r=80,t=30,b=10),
    xaxis=dict(title="g CO₂/km",gridcolor=LGRAY),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
  st.plotly_chart(fig, use_container_width=True)

# ── TAB 7: PRODUCTION ─────────────────────────────────────────────────────────
with tabs[6]:
  st.markdown('<div class="section-hd">Production Intelligence</div>', unsafe_allow_html=True)

  prod = D["prod"].merge(D["c24"][["country","sales_2024"]], on="country", how="left").dropna(subset=["sales_2024"])
  prod["balance"] = prod["cars_produced"] - prod["sales_2024"]
  prod["net"] = prod["balance"].apply(lambda x: "Net exporter" if x>0 else "Net importer")
  prod = prod.sort_values("cars_produced", ascending=False)

  col_p, col_t = st.columns([1.5, 1])

  with col_p:
    st.markdown("##### Vehicles produced vs domestic registrations — 2024 (units)")
    n_prod = st.slider("Show top N producers", 5, len(prod), min(12, len(prod)))
    prod_top = prod.head(n_prod)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Produced", x=prod_top["country"],
      y=prod_top["cars_produced"], marker_color=BLUE))
    fig.add_trace(go.Bar(name="Registrations", x=prod_top["country"],
      y=prod_top["sales_2024"], marker_color="#B5D4F4"))
    fig.update_layout(barmode="group", height=350,
      margin=dict(l=0,r=0,t=10,b=60),
      legend=dict(orientation="h",y=-0.15),
      yaxis=dict(tickformat=".2s",gridcolor=LGRAY),
      xaxis=dict(tickangle=-35,tickfont=dict(size=10)),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)

  with col_t:
    st.markdown("##### Net trade position")
    tbl = prod[["country","cars_produced","sales_2024","balance","net"]].copy()
    tbl.columns = ["Country","Produced","Registrations","Balance","Position"]
    tbl["Produced"] = tbl["Produced"].apply(lambda x: f"{x:,.0f}")
    tbl["Registrations"] = tbl["Registrations"].apply(lambda x: f"{x:,.0f}")
    tbl["Balance"] = tbl["Balance"].apply(lambda x: f"{x:+,.0f}")
    st.dataframe(tbl, hide_index=True, use_container_width=True, height=380)

# ── TAB 8: DEMOGRAPHICS ───────────────────────────────────────────────────────
with tabs[7]:
  st.markdown('<div class="section-hd">Buyer Intelligence</div>', unsafe_allow_html=True)

  st.markdown("""
<div class="spg-box">
<div class="spg-title">📊 Full Buyer Demographics — S&P Global Mobility · Polk Automotive Solutions</div>
<div class="spg-body">
Real buyer demographic data (gender, age, household income, purchase motivation, loyalty/conquest metrics) by country, brand and model is available exclusively through <strong>S&P Global Mobility's Polk registration database</strong>.<br><br>
<strong>European coverage:</strong> Italy · Spain · United Kingdom · France<br>
<strong>Product:</strong> Polk Audiences / Polk Data Services<br>
<strong>Access:</strong> Enterprise licence — <a href="https://www.spglobal.com/mobility/en/index.html" target="_blank">spglobal.com/mobility</a><br><br>
The interactive charts below use <strong>illustrative estimates</strong> based on published industry research.
</div>
</div>
""", unsafe_allow_html=True)

  st.markdown("<br>", unsafe_allow_html=True)

  demo_segment = st.selectbox("Filter by segment",
    ["All segments","SUV","Small","Medium","Luxury","MPV"])

  d1, d2, d3 = st.columns(3)

  gender_data = {
    "All segments": {"Male":60,"Female":40},
    "SUV":{"Male":56,"Female":44},
    "Small":{"Male":41,"Female":59},
    "Medium":{"Male":53,"Female":47},
    "Luxury":{"Male":71,"Female":29},
    "MPV":{"Male":44,"Female":56},
  }
  gd = gender_data.get(demo_segment, gender_data["All segments"])

  with d1:
    st.markdown(f"**Gender split — {demo_segment}**")
    fig = go.Figure(go.Pie(
      labels=list(gd.keys()), values=list(gd.values()),
      hole=0.55, marker_colors=[BLUE,CORAL],
      textinfo="label+percent", textfont_size=13))
    fig.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0),
      showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

  with d2:
    st.markdown("**Age distribution**")
    age_data = {"18-35":14,"36-50":34,"51-65":33,"65+":19}
    if demo_segment == "Small": age_data = {"18-35":28,"36-50":32,"51-65":25,"65+":15}
    if demo_segment == "Luxury": age_data = {"18-35":8,"36-50":30,"51-65":38,"65+":24}
    if demo_segment == "SUV": age_data = {"18-35":12,"36-50":38,"51-65":32,"65+":18}
    fig = px.bar(x=list(age_data.keys()), y=list(age_data.values()),
      color_discrete_sequence=[BLUE],
      labels={"x":"Age group","y":"%"})
    fig.update_layout(height=220, margin=dict(l=0,r=0,t=10,b=0),
      yaxis=dict(ticksuffix="%",gridcolor=LGRAY),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)

  with d3:
    st.markdown(f"**Purchase motivation — {demo_segment}**")
    motiv_data = {
      "All segments": {"Reliability":78,"Running costs":65,"Brand":52,"Safety":48,"Design":41,"Green/EV":33},
      "SUV":     {"Reliability":72,"Space/family":70,"Brand":58,"Safety":55,"Design":48,"Green/EV":30},
      "Small":    {"Running costs":82,"Price":78,"Reliability":65,"Urban ease":60,"Design":35,"Green/EV":28},
      "Medium":    {"Reliability":76,"Running costs":68,"Brand":55,"Safety":50,"Design":44,"Green/EV":35},
      "Luxury":    {"Brand":85,"Design":80,"Performance":75,"Prestige":70,"Technology":65,"Green/EV":40},
      "MPV":     {"Space/family":88,"Reliability":75,"Running costs":65,"Safety":60,"Brand":42,"Green/EV":25},
    }
    md = motiv_data.get(demo_segment, motiv_data["All segments"])
    motiv = pd.DataFrame({"Motivation": list(md.keys()), "Score": list(md.values())}).sort_values("Score")
    fig = go.Figure(go.Bar(
      x=motiv["Score"], y=motiv["Motivation"], orientation="h",
      marker_color=[CORAL if v == max(md.values()) else BLUE for v in motiv["Score"]],
      text=motiv["Score"].apply(lambda x: f"{x}%"),
      textposition="outside", textfont=dict(size=10)))
    fig.update_layout(height=220, margin=dict(l=0,r=50,t=10,b=10),
      xaxis=dict(range=[0,110],gridcolor=LGRAY),
      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)

  st.caption("⚠️ Illustrative estimates only. Real data requires S&P Global Mobility Polk licence.")

# ── TAB 9: EXECUTIVE SUMMARY ──────────────────────────────────────────────────
with tabs[8]:
  st.markdown('<div class="section-hd">Executive Summary</div>', unsafe_allow_html=True)

  c1, c2 = st.columns(2)
  with c1:
    st.markdown("#### Key findings")
    insight("The European market has recovered to 13.3M units in 2025 — its strongest since 2019. Growth is uneven: Spain and Poland are accelerating while France and Italy contract.")
    insight("Dacia Sandero became Europe's #1 model for the first time ever in 2024, dethroning VW Golf. The value segment is winning — pressure on margin strategies.")
    warning("BEV share fell for the first time in history in 2024. The 2025 EU CO₂ targets (93.6 g/km) create compliance risk for OEMs still dependent on ICE volume.")

  with c2:
    st.markdown("#### Competitive landscape")
    insight("VW Group consolidated leadership to 26.9% market share in 2025. Skoda entered the top-2 brands for the first time ever in Q1 2026.")
    risk("Tesla's sales collapsed -26.6% in 2025 — sharpest fall of any major brand. Traditional OEMs are recovering EV ground.")
    risk("Chinese brands (BYD, SAIC/MG) grew +270% and +5.1% in 2025. Southern European markets — particularly Portugal and Spain — are highest-exposure entry points.")

  st.divider()
  st.markdown("#### Recommended actions")
  r1, r2, r3 = st.columns(3)
  with r1: st.info("**Iberian growth**\nSpain and Portugal outpacing EU average. Review network capacity and model mix for these markets.")
  with r2: st.warning("**EV transition**\nBEV stall vs regulatory targets. Assess OEM partners' compliance trajectories urgently.")
  with r3: st.error("**Chinese brands**\nSet up systematic tracking of BYD and MG penetration. Early warning system needed.")


# ── TAB 10: MONTHLY TREND & FORECAST ─────────────────────────────────────────
with tabs[9]:
    st.markdown('<div class="section-hd">Monthly Trend & 2026 Forecast</div>', unsafe_allow_html=True)
    st.markdown(data_badge('mixed', 'EU27 monthly data reconstructed from ACEA YTD reports · Annual totals confirmed · Forecast = analyst estimates'), unsafe_allow_html=True)

    monthly = D["monthly"]
    forecast = D["forecast"]

    col_toggle1, col_toggle2 = st.columns(2)
    with col_toggle1:
        show_metric = st.radio("Metric", ["Total registrations (K)", "BEV market share (%)"], horizontal=True)
    with col_toggle2:
        show_forecast = st.checkbox("Show 2026 forecast", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if show_metric == "Total registrations (K)":
        col_a, col_b = st.columns([1.6, 1])
        with col_a:
            st.markdown("##### Monthly EU registrations — 2024 vs 2025 (EU27, thousands)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly["month"], y=monthly["reg_2024_k"],
                name="2024", mode="lines+markers",
                line=dict(color="#B5D4F4", width=2, dash="dot"),
                marker=dict(size=6),
            ))
            fig.add_trace(go.Scatter(
                x=monthly["month"], y=monthly["reg_2025_k"],
                name="2025", mode="lines+markers",
                line=dict(color=BLUE, width=2.5),
                marker=dict(size=7),
                fill="tonexty", fillcolor="rgba(24,95,165,0.05)",
            ))
            # Annotate key events
            fig.add_annotation(x="Sep", y=1120, text="Plate change<br>+2.3%", showarrow=True,
                arrowhead=2, font=dict(size=9, color=TEAL), ax=30, ay=-30)
            fig.add_annotation(x="Nov", y=858, text="BEV surge<br>+44%", showarrow=True,
                arrowhead=2, font=dict(size=9, color=TEAL), ax=-40, ay=-30)
            fig.add_annotation(x="Jan", y=740, text="Soft start<br>-2.6%", showarrow=True,
                arrowhead=2, font=dict(size=9, color=CORAL), ax=30, ay=30)
            fig.update_layout(
                height=350, margin=dict(l=0,r=0,t=20,b=30),
                legend=dict(orientation="h", y=-0.15),
                yaxis=dict(title="Thousands", gridcolor=LGRAY),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=11),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<div class="data-note">Source: ACEA press releases 2024-2025 · EU27 only · Monthly splits estimated from YTD figures · Annual totals confirmed</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown("##### Key observations")
            insight("H1 2025 was weak (-1.9% YTD) but H2 recovered strongly. September plate change (+2.3%) and November BEV surge (+44%) drove the full-year turnaround to +1.8%.")
            insight("August remains the structural low point — summer holidays suppress EU registrations to 40-50% of a typical month. No structural change expected in 2026.")
            warning("January 2025 started -2.6% — weakness in Germany (-15%) and France (-8%) was only partially offset by Spain and Poland. Watch Q1 2026 closely.")

    else:
        col_a, col_b = st.columns([1.6, 1])
        with col_a:
            st.markdown("##### BEV market share — Monthly EU 2024 vs 2025 (%)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly["month"], y=monthly["bev_pct_2024"],
                name="2024", mode="lines+markers",
                line=dict(color="#B5D4F4", width=2, dash="dot"),
                marker=dict(size=6),
            ))
            fig.add_trace(go.Scatter(
                x=monthly["month"], y=monthly["bev_pct_2025"],
                name="2025", mode="lines+markers",
                line=dict(color=BLUE, width=2.5),
                marker=dict(size=7),
            ))
            if show_forecast:
                # Q1 2026 known data point
                fig.add_trace(go.Scatter(
                    x=["Dec", "Q1 2026"], y=[25.0, 20.6],
                    name="Q1 2026 (confirmed)", mode="markers+lines",
                    line=dict(color=TEAL, width=2, dash="dash"),
                    marker=dict(size=9, symbol="star"),
                ))
            fig.add_hline(y=17.4, line_dash="dash", line_color=GRAY, line_width=1,
                annotation_text="2025 avg 17.4%", annotation_font=dict(size=9))
            fig.add_hline(y=13.6, line_dash="dot", line_color="#cccccc", line_width=1,
                annotation_text="2024 avg 13.6%", annotation_font=dict(size=9))
            fig.update_layout(
                height=350, margin=dict(l=0,r=0,t=20,b=30),
                legend=dict(orientation="h", y=-0.15),
                yaxis=dict(title="BEV share (%)", ticksuffix="%", gridcolor=LGRAY),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=11),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<div class="data-note">2025 monthly estimated from ACEA YTD · Q1 2026 confirmed (ACEA, March 2026) · Source: ACEA 2024-2026</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown("##### BEV trajectory reading")
            insight("2025 reversed the 2024 decline. Starting at 15% in January and accelerating to 25% in December — the year-end surge is driven by OEM compliance pushes ahead of EU CO₂ targets.")
            risk("December spikes are structurally artificial — OEMs register EVs en masse at year-end to hit fleet averages. The 'real' underlying consumer BEV demand is closer to the H1 average of 15.6%.")
            insight(f"Q1 2026 confirmed at 20.6% — a record for a first quarter. This suggests the underlying trend has genuinely shifted upward, not just year-end effects.")

    st.divider()

    # 2026 Forecast
    st.markdown("##### 2026 Full Year Forecast — EU car market")
    st.markdown(data_badge("mixed", "Analyst estimates based on ACEA trend data · Not investment advice"), unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    # Values hardcoded to bypass @st.cache_data — EU+EFTA+UK base 13.27M (ACEA 2025)
    _scenarios = [
        ("PESSIMISTIC", "13.27M", "0.0", "17.4", "#D85A30"),
        ("BASE CASE",   "13.60M", "+2.5", "21.5", "#185FA5"),
        ("OPTIMISTIC",  "13.93M", "+5.0", "25.0", "#1D9E75"),
    ]
    for col, (label, vol, growth, bev, color) in zip([fc1, fc2, fc3], _scenarios):
        with col:
            arrow = "▲" if "+" in growth else "▶"
            st.markdown(f"""
<div style="background:#f9f9f9;border-radius:8px;padding:16px;border-left:4px solid {color};border:0.5px solid #e0e0e0">
<div style="font-size:12px;color:#888;font-weight:600;text-transform:uppercase">{label}</div>
<div style="font-size:24px;font-weight:700;color:#0d1b2a;margin-top:4px">{vol}</div>
<div style="font-size:12px;color:{color};margin-top:2px">{arrow} {growth}% vs 2025 · BEV {bev}%</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Waterfall assumptions
    with st.expander("📋 Forecast assumptions & methodology"):
        st.markdown("""
**Base case (+2.5% → ~13.60M EU+EFTA+UK)**
- Spain and Poland sustain above-average growth (+8-10%)
- Germany stabilises after 2024-2025 structural weakness
- BEV share reaches ~21.5% driven by EU CO₂ compliance pressure on OEMs
- No major macro shock or new tariff escalation
- Key model launches: VW ID.2, Renault 5 E-Tech, Leapmotor C10

**Optimistic (+5.0% → ~13.93M EU+EFTA+UK)**
- EU EV incentive expansion (France, Germany, Italy under discussion)
- Strong H2 driven by affordable EV launches in €20-25K range
- Iberian growth extends — Italy shows early recovery signs
- BYD and Chinese brands accelerate, expanding total market

**Pessimistic (flat 0% → ~13.27M EU+EFTA+UK)**
- US tariff escalation hits EU auto exports → production cuts, layoffs
- Consumer confidence deteriorates (interest rates, energy costs)
- German market structural shift deepens — fleet buyers delay
- BEV stagnates: incentives not renewed, infrastructure gaps persist

---
*Methodology: scenario analysis based on ACEA 2024-2025 trend data.*
*Scope: EU27 + EFTA (Norway, Iceland, Switzerland) + UK = 31 markets.*
*Not econometric modelling. Not investment advice.*
        """)

    st.markdown('<div class="data-note">Forecast EU27 only · EU+EFTA+UK adds ~11% · Source: analyst estimates based on ACEA / S&P Global Mobility trend data</div>', unsafe_allow_html=True)


st.divider()
st.caption("European Car Market Intelligence Report · Maria João Luz · mariajoaoluz.com · Data: ACEA, JATO Dynamics, S&P Global Mobility, ICCT, EEA · 2024–2025")

# ── TAB 11: STRATEGIC ANALYTICS ───────────────────────────────────────────────
with tabs[10]:
    st.markdown('<div class="section-hd">Strategic Analytics</div>', unsafe_allow_html=True)

    analytics_section = st.radio("", [
        "Market Concentration (HHI)",
        "Group Share Evolution",
        "Risk / Opportunity Matrix",
        "Outlier Analysis",
        "Correlation Explorer",
    ], horizontal=True, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── HHI ──────────────────────────────────────────────────────────────────
    if analytics_section == "Market Concentration (HHI)":
        st.markdown("#### Herfindahl-Hirschman Index — European Car Market")
        hhi = D["hhi"]
        col_exp, col_m = st.columns([1, 1.5])

        with col_exp:
            st.markdown("""
**What is HHI?**
The Herfindahl-Hirschman Index measures market concentration.
It is the sum of squared market shares of all players.

| HHI Range | Interpretation |
|---|---|
| < 1,000 | Unconcentrated (competitive) |
| 1,000–1,800 | Moderately concentrated |
| > 1,800 | Highly concentrated |

The EU car market HHI is well below 1,000 — structurally competitive.
A declining HHI signals increasing competition (new entrants, fragmentation).
""")
            insight(f"Brand HHI fell from {hhi['brand_hhi_2024']} in 2024 to {hhi['brand_hhi_2025']} in 2025 — competition is intensifying. Chinese brands (BYD +270%) and Cupra (+35.6%) are fragmenting share away from incumbents.")

        with col_m:
            metrics_data = {
                "Metric": ["Brand HHI", "Group HHI", "Top 3 brand share", "Top 5 brand share"],
                "2024":   [f"{hhi['brand_hhi_2024']:.0f}", f"{hhi['group_hhi_2024']:.0f}",
                           f"{hhi['top3_share_2024']:.1f}%", f"{hhi['top5_share_2024']:.1f}%"],
                "2025":   [f"{hhi['brand_hhi_2025']:.0f}", f"{hhi['group_hhi_2025']:.0f}",
                           f"{hhi['top3_share_2025']:.1f}%", f"{hhi['top5_share_2025']:.1f}%"],
                "Change": [
                    f"{hhi['brand_hhi_2025']-hhi['brand_hhi_2024']:+.0f}",
                    f"{hhi['group_hhi_2025']-hhi['group_hhi_2024']:+.0f}",
                    f"{hhi['top3_share_2025']-hhi['top3_share_2024']:+.1f} pp",
                    f"{hhi['top5_share_2025']-hhi['top5_share_2024']:+.1f} pp",
                ],
                "Signal": ["▼ More competitive", "▼ Slightly less concentrated",
                           "▼ Fragmentation", "▶ Stable"],
            }
            st.dataframe(pd.DataFrame(metrics_data), hide_index=True, use_container_width=True)

            # Visual HHI gauge
            st.markdown("##### Brand HHI 2025 — market concentration score")
            fig_hhi = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=hhi["brand_hhi_2025"],
                delta={"reference": hhi["brand_hhi_2024"], "valueformat": ".0f", "increasing": {"color": "#D85A30"}, "decreasing": {"color": "#1D9E75"}},
                number={"font": {"size": 52}},
                title={"text": ""},
                gauge={
                    "axis": {"range": [0, 2000]},
                    "bar": {"color": BLUE},
                    "steps": [
                        {"range": [0, 1000], "color": "#EAF3DE"},
                        {"range": [1000, 1800], "color": "#FAEEDA"},
                        {"range": [1800, 2000], "color": "#FCEBEB"},
                    ],
                    "threshold": {"line": {"color": CORAL, "width": 2}, "value": 1000},
                },
            ))
            fig_hhi.update_layout(height=240, margin=dict(l=20,r=20,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_hhi, use_container_width=True)

    # ── GROUP SHARE EVOLUTION ─────────────────────────────────────────────────
    elif analytics_section == "Group Share Evolution":
        st.markdown("#### Manufacturer Group Market Share — Europe 2019→2025")
        grp_evo = D["grp_evo"]
        groups_sel = st.multiselect("Select groups",
            grp_evo["group"].unique().tolist(),
            default=["Volkswagen Group","Stellantis","Renault Group","Toyota Group","Tesla"])

        filtered = grp_evo[grp_evo["group"].isin(groups_sel)]
        col_chart, col_ins = st.columns([1.5, 1])

        with col_chart:
            fig_evo = go.Figure()
            group_colors = {
                "Volkswagen Group": BLUE, "Stellantis": CORAL, "Renault Group": TEAL,
                "Toyota Group": AMBER, "Tesla": "#534AB7", "BMW Group": "#993556",
                "Hyundai Group": "#3B6D11", "Mercedes-Benz": "#854F0B",
            }
            for grp in groups_sel:
                gdf = filtered[filtered["group"] == grp]
                fig_evo.add_trace(go.Scatter(
                    x=gdf["year"], y=gdf["market_share"],
                    name=grp, mode="lines+markers",
                    line=dict(color=group_colors.get(grp, GRAY), width=2.5),
                    marker=dict(size=7),
                ))
            fig_evo.add_vline(x=2020, line_dash="dot", line_color=GRAY,
                annotation_text="COVID", annotation_font=dict(size=9))
            fig_evo.add_vline(x=2021, line_dash="dot", line_color=AMBER,
                annotation_text="Stellantis\nmerger", annotation_font=dict(size=9))
            fig_evo.update_layout(
                height=380, margin=dict(l=0,r=0,t=20,b=30),
                yaxis=dict(title="Market share (%)", ticksuffix="%", gridcolor=LGRAY),
                xaxis=dict(tickvals=list(range(2019,2026))),
                legend=dict(orientation="h", y=-0.2),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=11),
            )
            st.plotly_chart(fig_evo, use_container_width=True)
            st.markdown('<div class="data-note">2019-2022 estimates · 2023-2025 ACEA confirmed · Stellantis created Jan 2021 (FCA + PSA merger)</div>', unsafe_allow_html=True)

        with col_ins:
            insight("VW Group has grown from 24.1% to 26.9% over 6 years — systematic market share gain through volume (Skoda +9.6%, Cupra +35.6%) while maintaining premium margin in Audi/Porsche.")
            risk("Stellantis lost 5 percentage points since its 2021 creation — from 19.4% to 14.3%. This is one of the largest share losses by any major group in modern European automotive history.")
            insight("Tesla peaked at 2.5% in 2024 and fell to 1.8% in 2025. Traditional OEMs recovered BEV ground. This reversal was faster than most analysts predicted.")
            warning("Toyota's rise from 5.2% to 7.6% (2019-2024) was the strongest gain of any major group — driven entirely by hybrid dominance as competitors struggled with pure BEV transition.")

    # ── RISK / OPPORTUNITY MATRIX ─────────────────────────────────────────────
    elif analytics_section == "Risk / Opportunity Matrix":
        st.markdown("#### Market Risk / Opportunity Matrix — 2025")
        st.markdown("**X axis:** YoY market growth · **Y axis:** BEV readiness · **Size:** market volume")
        rm = D["risk_matrix"]

        col_q, col_chart2 = st.columns([1, 2])
        with col_q:
            st.markdown("""
**Quadrant logic:**
| | Low BEV | High BEV |
|---|---|---|
| **High growth** | 🚀 Growth Markets | ⭐ Stars |
| **Low/neg growth** | ⚠️ Watch | 🔋 EV Leaders |

EU averages used as thresholds:
- Growth: +2.4% YoY
- BEV: 13.6% market share
""")
            for q, color in [("⭐ Stars",TEAL),("🚀 Growth Markets",BLUE),("🔋 EV Leaders",AMBER),("⚠️ Watch",CORAL)]:
                qdf = rm[rm["quadrant"]==q]
                st.markdown(f'<div style="color:{color};font-weight:600;font-size:12px">{q} ({len(qdf)})</div>', unsafe_allow_html=True)
                st.markdown(", ".join(qdf["country"].tolist()))
                st.markdown("")

        with col_chart2:
            q_colors = {"⭐ Stars": TEAL, "🚀 Growth Markets": BLUE,
                       "🔋 EV Leaders": AMBER, "⚠️ Watch": CORAL}
            fig_rm = go.Figure()
            for q in rm["quadrant"].unique():
                qdf = rm[rm["quadrant"]==q]
                fig_rm.add_trace(go.Scatter(
                    x=qdf["yoy_2025"], y=qdf["bev_share"],
                    mode="markers+text",
                    name=q,
                    marker=dict(
                        size=[max(12, min(50, v/30)) for v in qdf["market_size_k"]],
                        color=q_colors[q], opacity=0.8, line=dict(width=1, color="white")
                    ),
                    text=qdf["country"],
                    textposition="top center",
                    textfont=dict(size=9),
                    customdata=qdf[["market_size_k","reg_per_1000"]].values,
                    hovertemplate="<b>%{text}</b><br>YoY: %{x:+.1f}%<br>BEV share: %{y:.1f}%<br>Market: %{customdata[0]:.0f}K units<extra></extra>",
                ))
            # Quadrant lines
            fig_rm.add_vline(x=2.4, line_dash="dash", line_color=GRAY, line_width=1,
                annotation_text="EU avg growth +2.4%", annotation_font=dict(size=9))
            fig_rm.add_hline(y=13.6, line_dash="dash", line_color=GRAY, line_width=1,
                annotation_text="EU avg BEV 13.6%", annotation_font=dict(size=9))
            fig_rm.update_layout(
                height=440, margin=dict(l=0,r=0,t=20,b=30),
                xaxis=dict(title="YoY Growth 2025 (%)", gridcolor=LGRAY, zeroline=True),
                yaxis=dict(title="BEV Market Share (%)", gridcolor=LGRAY),
                legend=dict(orientation="h", y=-0.15),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=11),
            )
            st.plotly_chart(fig_rm, use_container_width=True)
            st.markdown('<div class="data-note">Bubble size = market volume (units) · Source: ACEA 2025 / ICCT 2024</div>', unsafe_allow_html=True)

    # ── OUTLIER ANALYSIS ─────────────────────────────────────────────────────
    elif analytics_section == "Outlier Analysis":
        st.markdown("#### Outlier Markets — Structural Explanations")
        st.markdown("*These are the markets where the number alone is not the insight — the mechanism is.*")
        outliers = D["outliers"]
        for _, row in outliers.iterrows():
            color = TEAL if row["yoy_2025"] > 0 else CORAL
            direction = "▲" if row["yoy_2025"] > 0 else "▼"
            with st.expander(f"{direction} **{row['country']}** · {row['yoy_2025']:+.1f}% · {row['headline']}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Mechanism**")
                    st.markdown(row["mechanism"])
                with c2:
                    st.markdown("**Strategic implication**")
                    st.info(row["strategic_implication"])

    # ── CORRELATION EXPLORER ──────────────────────────────────────────────────
    elif analytics_section == "Correlation Explorer":
        st.markdown("#### Correlation Explorer — What drives BEV adoption?")
        rm = D["risk_matrix"]

        col_x, col_y = st.columns(2)
        with col_x:
            x_var = st.selectbox("X axis", ["reg_per_1000","yoy_2025","market_size_k"], index=0,
                format_func=lambda x: {"reg_per_1000":"Registrations per 1,000 people",
                    "yoy_2025":"YoY market growth (%)","market_size_k":"Market size (K units)"}[x])
        with col_y:
            y_var = st.selectbox("Y axis", ["bev_share","yoy_2025","reg_per_1000"], index=0,
                format_func=lambda x: {"bev_share":"BEV share (%)","yoy_2025":"YoY growth (%)",
                    "reg_per_1000":"Reg. per 1,000 people"}[x])

        import numpy as np
        x_data = rm[x_var].values
        y_data = rm[y_var].values
        corr = np.corrcoef(x_data, y_data)[0,1]

        # Trend line
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        x_line = np.linspace(x_data.min(), x_data.max(), 50)

        fig_corr = go.Figure()
        fig_corr.add_trace(go.Scatter(
            x=x_data, y=y_data, mode="markers+text",
            text=rm["country"], textposition="top center", textfont=dict(size=8),
            marker=dict(
                size=[max(8, min(25, v/40)) for v in rm["market_size_k"]],
                color=[{"⭐ Stars":TEAL,"🚀 Growth Markets":BLUE,
                       "🔋 EV Leaders":AMBER,"⚠️ Watch":CORAL}[q] for q in rm["quadrant"]],
                opacity=0.8),
            customdata=rm[["quadrant","market_size_k"]].values,
            hovertemplate="<b>%{text}</b><br>%{x:.1f} / %{y:.1f}<br>%{customdata[0]}<extra></extra>",
        ))
        fig_corr.add_trace(go.Scatter(
            x=x_line, y=p(x_line), mode="lines",
            line=dict(color=GRAY, width=1.5, dash="dash"),
            name=f"Trend (r={corr:.2f})", showlegend=True,
        ))
        labels = {"bev_share":"BEV share (%)","yoy_2025":"YoY growth (%)",
                 "reg_per_1000":"Reg./1,000 people","market_size_k":"Market size (K)"}
        fig_corr.update_layout(
            height=420, margin=dict(l=0,r=0,t=30,b=30),
            xaxis=dict(title=labels.get(x_var,""), gridcolor=LGRAY),
            yaxis=dict(title=labels.get(y_var,""), gridcolor=LGRAY),
            legend=dict(orientation="h", y=-0.15),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
            title=f"Pearson correlation: r = {corr:.2f} ({'strong' if abs(corr)>0.6 else 'moderate' if abs(corr)>0.3 else 'weak'})"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

        corr_strength = "strong positive" if corr > 0.6 else "moderate positive" if corr > 0.3 else "strong negative" if corr < -0.6 else "moderate negative" if corr < -0.3 else "weak"
        insight(f"Pearson r = {corr:.2f} — {corr_strength} correlation. "
               f"{'Wealthier, denser markets tend to have higher EV penetration — infrastructure investment and price sensitivity are the structural drivers.' if x_var=='reg_per_1000' and y_var=='bev_share' else 'Adjust the axes to explore different relationships in the data.'}")

# ── TAB 12: DATA COVERAGE ─────────────────────────────────────────────────────
with tabs[11]:
    st.markdown('<div class="section-hd">Data Coverage & Methodology</div>', unsafe_allow_html=True)

    st.markdown("""
### What this dashboard is — and what it isn't

This dashboard is built on **publicly available industry data** from primary sources.
All figures represent **new passenger car registrations** (units sold/registered in a given period),
not vehicle fleet size, not revenue, and not used car sales.
""")

    st.markdown("### Data sources & coverage")
    sources_df = pd.DataFrame([
        ("ACEA", "European Automobile Manufacturers' Assoc.", "Sales by country, fuel type, manufacturer group", "2024–2025 (monthly)", "Confirmed", "acea.auto"),
        ("JATO Dynamics", "Global automotive intelligence", "Top 10 models by volume", "2024 (full year)", "Confirmed", "jato.com"),
        ("best-selling-cars.com", "Auto market aggregator", "30-brand ranking, top models 2025", "2025 (full year)", "Confirmed", "best-selling-cars.com"),
        ("ICCT / EEA", "Intl. Council on Clean Transportation", "CO₂ g/km by country, BEV share by country", "2024 (latest)", "Confirmed", "theicct.org"),
        ("S&P Global Mobility / Polk", "Enterprise automotive data", "Production by country, demographic profiles", "2024", "Confirmed (partial)", "spglobal.com/mobility"),
        ("Eurostat / UN", "Official statistics", "Population by country", "2024 estimate", "Confirmed", "ec.europa.eu/eurostat"),
        ("ACEA (YTD reports)", "Monthly press releases", "Monthly EU27 registration volumes", "Jan–Dec 2025", "Reconstructed from YTD", "acea.auto"),
        ("Analyst estimates", "Based on ACEA trend data", "2026 full year forecast, group share 2019-2022", "2026 projection", "Estimates", "—"),
        ("S&P Global Mobility Polk", "Enterprise licence required", "Buyer demographics (age, gender, motivation)", "—", "Illustrative only", "spglobal.com/mobility"),
    ], columns=["Source","Full name","Covers","Period","Status","URL"])

    status_colors = {"Confirmed": "🟢", "Reconstructed from YTD": "🟡",
                    "Confirmed (partial)": "🟡", "Estimates": "🟠", "Illustrative only": "🔴"}
    sources_df["Status"] = sources_df["Status"].map(lambda x: f"{status_colors.get(x,'⚪')} {x}")
    st.dataframe(sources_df[["Source","Covers","Period","Status"]], hide_index=True, use_container_width=True, height=320)

    st.markdown("### Data dictionary")
    dict_df = pd.DataFrame([
        ("New car registrations", "Number of new passenger cars registered in a country in a given period. Includes both private and fleet/company cars. Source: national auto associations via ACEA."),
        ("BEV share", "Battery Electric Vehicles as % of total new passenger car registrations. ACEA definition excludes mild hybrids. Note: some sources include mild hybrids — always check definition."),
        ("YoY change (%)", "Year-over-year percentage change: (current period - prior period) / prior period × 100."),
        ("CO₂ g/km", "Average CO₂ emissions per km of new cars registered in a country. EU 2025 target: 93.6 g/km fleet average for OEMs."),
        ("Reg. per 1,000 people", "New car registrations ÷ (population in millions × 1,000). Normalises market size for population comparison. Uses 2024 population estimates."),
        ("HHI (brand)", "Sum of squared market shares of all brands. Ranges 0–10,000. Below 1,000 = competitive market. Calculated on top 30 brands + residual."),
        ("EU average (growth)", "+2.4% — EU+EFTA+UK full year 2025 vs 2024 (ACEA confirmed)."),
        ("EU average (BEV share)", "13.6% for 2024, 17.4% for 2025 — EU27 only (ACEA confirmed annual figures)."),
        ("Market scope", "EU27 + EFTA (Norway, Iceland, Switzerland) + UK = 31 markets. Some metrics (BEV, CO₂, fuel mix) are EU27 only as ACEA reports separately."),
    ], columns=["Term", "Definition"])
    st.dataframe(dict_df, hide_index=True, use_container_width=True, height=360)

    st.markdown("### Limitations")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.warning("""
**Known data gaps**
- Monthly registrations 2025: annual totals confirmed, monthly splits reconstructed
- Group share 2019-2022: estimates based on published brand data
- Brand model volumes: EU estimates, not officially published
- Demographics: illustrative only (S&P Polk licence required for real data)
""")
    with col_l2:
        st.info("""
**Methodology notes**
- All monetary figures: none — this dashboard is units only
- Brand ranking: EU+EFTA+UK scope unless stated
- BEV metrics: EU27 only (ACEA reporting scope)
- Forecasts: scenario analysis, not econometric modelling
- Last data update: ACEA full year 2025 (January 2026)
""")

    st.markdown("### Update cadence")
    st.markdown("""
| Data type | ACEA publishes | Dashboard update |
|---|---|---|
| Monthly totals by country | 3rd week of following month | Manual — monthly |
| Full year by brand/model | January following year | Annual |
| CO₂ / BEV annual | Q1 following year | Annual |
| Forecasts | Ongoing | Quarterly review |
""")
    st.markdown('<div class="data-note">Dashboard built by Maria João Luz · mariajoaoluz.com · Powered by Streamlit + Plotly · Data: ACEA, JATO, S&P Global Mobility, ICCT, EEA</div>', unsafe_allow_html=True)
