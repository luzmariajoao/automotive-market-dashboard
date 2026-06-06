"""
Unified loader — all data embedded, no external file dependencies.
Funciona local e no Streamlit Cloud.
"""
import pandas as pd
from pathlib import Path
import sys

# ── Dados embutidos ────────────────────────────────────────────────────────────

def load_sales_by_country(year=2025):
    data_2024 = [
        ("Austria","EU",253789,239150,6.1),("Belgium","EU",448277,476675,-6.0),
        ("Bulgaria","EU",42941,37724,13.8),("Croatia","EU",65020,57694,12.7),
        ("Cyprus","EU",15057,14740,2.2),("Czechia","EU",231597,221419,4.6),
        ("Denmark","EU",173114,172745,0.2),("Estonia","EU",25386,22820,11.2),
        ("Finland","EU",74064,87502,-15.4),("France","EU",1718412,1774722,-3.2),
        ("Germany","EU",2817331,2844609,-1.0),("Greece","EU",137075,134484,1.9),
        ("Hungary","EU",121611,107720,12.9),("Ireland","EU",121196,122400,-1.0),
        ("Italy","EU",1559229,1567151,-0.5),("Latvia","EU",17329,18928,-8.4),
        ("Lithuania","EU",30122,27666,8.9),("Luxembourg","EU",46659,49105,-5.0),
        ("Malta","EU",7663,7436,3.1),("Netherlands","EU",381227,369631,3.1),
        ("Poland","EU",551568,475032,16.1),("Portugal","EU",209715,199623,5.1),
        ("Romania","EU",151105,143080,5.6),("Slovakia","EU",93409,88003,6.1),
        ("Slovenia","EU",53018,48924,8.4),("Spain","EU",1016885,949362,7.1),
        ("Sweden","EU",269582,289820,-7.0),("Iceland","EFTA",10233,17543,-41.7),
        ("Norway","EFTA",128687,126953,1.4),("Switzerland","EFTA",239535,252214,-5.0),
        ("United Kingdom","UK",1952778,1903054,2.6),
    ]
    data_2025 = [
        ("Austria","EU",284978,253789,12.3),("Belgium","EU",414770,448277,-7.5),
        ("Bulgaria","EU",49419,42941,15.1),("Croatia","EU",69841,65020,7.4),
        ("Cyprus","EU",14634,15057,-2.8),("Czechia","EU",248719,231600,7.4),
        ("Denmark","EU",184641,172995,6.7),("Estonia","EU",13055,25386,-48.6),
        ("Finland","EU",71881,74070,-3.0),("France","EU",1632152,1718416,-5.0),
        ("Germany","EU",2857591,2817331,1.4),("Greece","EU",144199,137075,5.2),
        ("Hungary","EU",129440,121611,6.4),("Ireland","EU",124954,121316,3.0),
        ("Italy","EU",1524843,1558071,-2.1),("Latvia","EU",22506,17131,31.4),
        ("Lithuania","EU",41974,30122,39.3),("Luxembourg","EU",47158,46656,1.1),
        ("Malta","EU",6468,7663,-15.6),("Netherlands","EU",388024,381463,1.7),
        ("Poland","EU",597435,551567,8.3),("Portugal","EU",225039,209712,7.3),
        ("Romania","EU",156803,151105,3.8),("Slovakia","EU",93103,93409,-0.3),
        ("Slovenia","EU",57556,53018,8.6),("Spain","EU",1148650,1016963,12.9),
        ("Sweden","EU",272998,269582,1.3),("Iceland","EFTA",14547,10218,42.4),
        ("Norway","EFTA",179632,128837,39.4),("Switzerland","EFTA",233737,239535,-2.4),
        ("United Kingdom","UK",2020523,1952778,3.5),
    ]
    if year == 2025:
        df = pd.DataFrame(data_2025, columns=["country","region","sales_2025","sales_2024","pct_change"])
        return df.sort_values("sales_2025", ascending=False).reset_index(drop=True)
    else:
        df = pd.DataFrame(data_2024, columns=["country","region","sales_2024","sales_2023","pct_change"])
        return df.sort_values("sales_2024", ascending=False).reset_index(drop=True)

def load_top_brands(year=2025):
    # Source: ACEA / best-selling-cars.com — EU+EFTA+UK full year
    data_2025 = [
        (1,  "Volkswagen",   "Volkswagen Group",  1452704, 1371854,  5.9, 10.9),
        (2,  "Toyota",       "Toyota Group",       855000,  928767, -7.4,  6.4),
        (3,  "Skoda",        "Volkswagen Group",   840179,  766469,  9.6,  6.3),
        (4,  "BMW",          "BMW Group",          800585,  775119,  3.3,  6.0),
        (5,  "Renault",      "Renault Group",      750605,  699151,  7.4,  5.7),
        (6,  "Mercedes",     "Mercedes-Benz",      710000,  684027,  3.8,  5.4),
        (7,  "Audi",         "Volkswagen Group",   664680,  662664,  0.3,  5.0),
        (8,  "Peugeot",      "Stellantis",         637834,  641376, -0.6,  4.8),
        (9,  "Dacia",        "Renault Group",      597088,  578953,  3.1,  4.5),
        (10, "Hyundai",      "Hyundai Group",      535205,  534198,  0.2,  4.0),
        (11, "Kia",          "Hyundai Group",      507304,  529319, -4.2,  3.8),
        (12, "Opel/Vauxhall","Stellantis",         399782,  414042, -3.4,  3.0),
        (13, "Volvo",        "Volvo Cars",         395000,  369689,  6.8,  3.0),
        (14, "Ford",         "Ford",               380000,  426307,-10.9,  2.9),
        (15, "Citroen",      "Stellantis",         352521,  358892, -1.8,  2.7),
        (16, "Cupra",        "Volkswagen Group",   297724,  219637, 35.6,  2.2),
        (17, "Fiat",         "Stellantis",         271098,  304151,-10.9,  2.0),
        (18, "Nissan",       "Nissan",             252000,  307276,-18.0,  1.9),
        (19, "Mini",         "BMW Group",          169694,  148303, 14.4,  1.3),
        (20, "Seat",         "Volkswagen Group",   215636,  263771,-18.2,  1.6),
        (21, "MG",           "SAIC Motor",         210000,  244595,-14.1,  1.6),
        (22, "Suzuki",       "Suzuki",             203132,  187852,  8.1,  1.5),
        (23, "Mazda",        "Mazda",              172347,  182535, -5.6,  1.3),
        (24, "Tesla",        "Tesla",              240000,  327034,-26.6,  1.8),
        (25, "Jeep",         "Stellantis",         126284,  130486, -3.2,  1.0),
        (26, "Jaguar/LR",    "JLR",                150657,  145490,  3.6,  1.1),
        (27, "Porsche",      "Volkswagen Group",    91304,  106922,-14.6,  0.7),
        (28, "Alfa Romeo",   "Stellantis",          59532,   44919, 32.5,  0.4),
        (29, "BYD",          "BYD",                 48000,   13000,269.2,  0.4),
        (30, "Mitsubishi",   "Mitsubishi",          60873,   42823, 42.2,  0.5),
    ]
    data_2024 = [
        (1,  "Volkswagen",   "Volkswagen Group",  1371465, 1357842,  1.0, 10.6),
        (2,  "Toyota",       "Toyota Group",       928767,  828931, 12.0,  7.2),
        (3,  "BMW",          "BMW Group",          774925,  729073,  6.3,  6.0),
        (4,  "Skoda",        "Volkswagen Group",   766510,  679984, 12.7,  5.9),
        (5,  "Renault",      "Renault Group",      699214,  681058,  2.7,  5.4),
        (6,  "Mercedes",     "Mercedes-Benz",      684027,  671973,  1.8,  5.3),
        (7,  "Audi",         "Volkswagen Group",   663239,  733305, -9.6,  5.1),
        (8,  "Peugeot",      "Stellantis",         641376,  637178,  0.6,  4.9),
        (9,  "Dacia",        "Renault Group",      578953,  557154,  3.9,  4.5),
        (10, "Hyundai",      "Hyundai Group",      534198,  534307,  0.0,  4.1),
        (11, "Kia",          "Hyundai Group",      529319,  499321,  6.0,  4.1),
        (12, "Ford",         "Ford",               426307,  513481,-17.0,  3.3),
        (13, "Opel/Vauxhall","Stellantis",         414042,  451238, -8.2,  3.2),
        (14, "Citroen",      "Stellantis",         358892,  374100, -4.1,  2.8),
        (15, "Volvo",        "Volvo Cars",         369689,  287832, 28.4,  2.9),
        (16, "Fiat",         "Stellantis",         304151,  321800, -5.5,  2.3),
        (17, "Nissan",       "Nissan",             307276,  293988,  4.5,  2.4),
        (18, "Seat",         "Volkswagen Group",   263771,  253291,  4.1,  2.0),
        (19, "Cupra",        "Volkswagen Group",   219637,  166216, 32.1,  1.7),
        (20, "MG",           "SAIC Motor",         244595,  232721,  5.1,  1.9),
        (21, "Suzuki",       "Suzuki",             187852,  175000,  7.3,  1.4),
        (22, "Tesla",        "Tesla",              327034,  366829,-10.8,  2.5),
        (23, "Mazda",        "Mazda",              182535,  193000, -5.4,  1.4),
        (24, "Mini",         "BMW Group",          148303,  145000,  2.3,  1.1),
        (25, "Jeep",         "Stellantis",         130486,  141000, -7.4,  1.0),
    ]
    if year == 2025:
        return pd.DataFrame(data_2025, columns=["rank","brand","group","sales_2025","sales_2024","pct_change","market_share"])
    else:
        return pd.DataFrame(data_2024, columns=["rank","brand","group","sales_2024","sales_2023","pct_change","market_share"])

def load_top_models(year=2024):
    # Source: JATO Dynamics / best-selling-cars.com
    data_2024 = [
        (1,"Sandero","Dacia","Renault Group","Petrol/LPG","#1 for first time — dethroned VW Golf"),
        (2,"Clio","Renault","Renault Group","Petrol/Hybrid","2nd consecutive year in 2nd place"),
        (3,"Golf","Volkswagen","Volkswagen Group","Petrol/Diesel","215,700 units, +17% — dropped from #1"),
        (4,"Model Y","Tesla","Tesla","Electric","#1 in NL, SE, CH, DK, NO"),
        (5,"T-Roc","Volkswagen","Volkswagen Group","Petrol/Diesel","Slipped one position from 4th"),
        (6,"208","Peugeot","Stellantis","Petrol/Electric","Top model in 2022"),
        (7,"Yaris Cross","Toyota","Toyota Group","Hybrid","Improved one rank"),
        (8,"Octavia","Skoda","Volkswagen Group","Petrol/Diesel","Improved two ranks"),
        (9,"Duster","Dacia","Renault Group","Petrol/LPG/Hybrid","Entered top 10 from 15th"),
        (10,"Yaris","Toyota","Toyota Group","Hybrid","Entered top 10 from 14th"),
    ]
    # Source: best-selling-cars.com full year 2025 — March 2026
    data_2025 = [
        (1,"Sandero","Dacia","Renault Group","Petrol/LPG","243,676 units — 2nd consecutive #1 (-9.8%)"),
        (2,"Clio","Renault","Renault Group","Petrol/Hybrid","~238,000 units (+6%) — 2nd consecutive"),
        (3,"T-Roc","Volkswagen","Volkswagen Group","Petrol/Diesel","211,241 units — up from #5 in 2024"),
        (4,"Tiguan","Volkswagen","Volkswagen Group","Petrol/Diesel","197,000 units, +19.7% — up from #12"),
        (5,"Golf","Volkswagen","Volkswagen Group","Petrol/Diesel","195,455 units — slipped from #3"),
        (6,"208","Peugeot","Stellantis","Petrol/Electric","~185,000 units — VW three in top 5"),
        (7,"Yaris Cross","Toyota","Toyota Group","Hybrid","~175,000 units — hybrid dominance"),
        (8,"Duster","Dacia","Renault Group","Petrol/LPG/Hybrid","~168,000 units, +22% — new gen"),
        (9,"Yaris","Toyota","Toyota Group","Hybrid","~148,000 units — 2nd Toyota in top 10"),
        (10,"C3","Citroen","Stellantis","Petrol/Electric","~145,000 units — new entry (Model Y out)"),
    ]
    if year == 2025:
        return pd.DataFrame(data_2025, columns=["rank","model","brand","group","fuel_type","notes"])
    return pd.DataFrame(data_2024, columns=["rank","model","brand","group","fuel_type","notes"])

def load_manufacturer_groups(year=2025):
    if year == 2025:
        data = [
            ("Volkswagen Group",3571429,3399294,5.1,26.9),
            ("Stellantis",1892556,1969927,-3.9,14.3),
            ("Renault Group",1358242,1282405,5.9,10.2),
            ("Toyota Group",1005000,1006073,-0.1,7.6),
            ("Hyundai Group",1042509,1063355,-2.0,7.9),
            ("BMW Group",970279,923422,5.1,7.3),
            ("Mercedes-Benz",710000,696907,1.9,5.4),
            ("Volvo Cars",395000,369689,6.8,3.0),
            ("Ford",380000,426307,-10.9,2.9),
            ("Tesla",240000,327034,-26.6,1.8),
        ]
        return pd.DataFrame(data, columns=["group","sales_2025","sales_2024","pct_change","market_share"])
    else:
        data = [
            ("Volkswagen Group",3407242,3325175,2.5,26.3),
            ("Stellantis",1969594,2125142,-7.3,15.2),
            ("Renault Group",1282453,1242229,3.2,9.9),
            ("Hyundai Group",1063517,1106604,-3.9,8.2),
            ("Toyota Group",1006073,889321,13.1,7.8),
            ("BMW Group",923202,913985,1.0,7.1),
            ("Mercedes-Benz",696907,699887,-0.4,5.4),
            ("Ford",426307,513481,-17.0,3.3),
            ("Volvo Cars",369689,287832,28.4,2.9),
            ("Tesla",327034,366829,-10.8,2.5),
            ("Nissan",307276,293988,4.5,2.4),
            ("SAIC Motor",244595,232721,5.1,1.9),
            ("Suzuki",203132,187852,8.1,1.6),
            ("Mazda",172347,182535,-5.6,1.3),
            ("Jaguar Land Rover Group",150657,145490,3.6,1.2),
            ("Honda",74682,60596,23.2,0.6),
            ("Mitsubishi",60873,42823,42.2,0.5),
        ]
        return pd.DataFrame(data, columns=["group","sales_2024","sales_2023","pct_change","market_share"])

def load_fuel_type_mix():
    # Source: ACEA full year 2025 — EU only
    # 2025: BEV 17.4%, Hybrid 34.5%, PHEV 9.4%, Petrol 26.6%, Diesel 8.9%
    data = [
        (2021,39.9,19.8, 9.1, 8.9,19.6,2.8,40.6),
        (2022,36.4,22.7,12.1, 9.4,16.4,3.0,47.3),
        (2023,35.3,25.8,14.6, 7.7,13.6,3.0,51.1),
        (2024,33.3,30.9,13.6, 7.1,11.9,3.1,54.8),
        (2025,26.6, 8.9,17.4, 9.4,34.5,3.2,64.5),
    ]
    return pd.DataFrame(data, columns=["year","petrol_pct","diesel_pct","bev_pct","phev_pct","hybrid_pct","alternative_pct","total_alternative_pct"])

def load_segment_share():
    data = [
        ("SUV","SUV",53,2024),("Small","A+B",19,2024),("Lower medium","C",15,2024),
        ("Upper medium","D",7,2024),("MPV","MPV",4,2024),("Luxury","E+F",2,2024),
    ]
    return pd.DataFrame(data, columns=["segment","code","share_pct","year"])

def load_co2_by_country():
    data = [
        ("Finland","EU",60.9,33.0),("Sweden","EU",61.0,33.0),("Denmark","EU",73.3,51.0),
        ("Netherlands","EU",80.0,33.0),("Norway","EFTA",35.0,89.0),("Belgium","EU",95.0,15.0),
        ("Portugal","EU",100.0,14.0),("France","EU",102.0,16.9),("Austria","EU",105.0,12.0),
        ("Spain","EU",107.0,6.0),("EU average","EU",107.8,None),
        ("Germany","EU",117.0,13.5),("Italy","EU",120.0,4.5),
    ]
    return pd.DataFrame(data, columns=["country","region","co2_gkm_2024","bev_share_pct_2024"]).sort_values("co2_gkm_2024")

def load_cars_per_1000():
    data = [
        ("Netherlands",69),("Luxembourg",38),("Slovenia",34),("Belgium",29),
        ("Germany",28),("Denmark",26),("Austria",26),("Italy",25),("Sweden",25),
        ("France",23),("Ireland",25),("Czechia",23),("Spain",21),("Portugal",21),
        ("EU average",24),
    ]
    return pd.DataFrame(data, columns=["country","cars_per_1000"]).sort_values("cars_per_1000", ascending=False)

def load_production_by_country():
    data = [
        ("Germany",3942396,198021,142087,4497),("Spain",1872988,467469,32554,1400),
        ("France",849437,498576,68270,2703),("Czechia",1446855,0,1429,4290),
        ("Slovakia",993750,0,0,0),("Romania",473110,0,0,0),
        ("Hungary",435541,0,839,0),("Poland",224017,336347,43885,7019),
        ("Italy",309336,224454,55066,1445),("Belgium",197624,38413,0,201),
        ("Portugal",229095,92042,2205,173),("Sweden",270807,33809,0,2010),
        ("Slovenia",60903,0,0,25),("Austria",72335,0,0,0),("Finland",22760,0,0,46),
    ]
    df = pd.DataFrame(data, columns=["country","cars_produced","vans_produced","trucks_produced","buses_produced"])
    return df[df["cars_produced"]>0].sort_values("cars_produced", ascending=False)

def load_employment():
    return pd.DataFrame()

def build_yoy_comparison():
    c24 = load_sales_by_country(2024)[["country","region","sales_2024"]]
    c25 = load_sales_by_country(2025)[["country","sales_2025","pct_change"]]
    return c24.merge(c25, on="country", how="outer").sort_values("sales_2025", ascending=False)

def load_ratio_per_capita():
    """New car registrations per person — 2025"""
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
    for country, (s24, s25, pop) in sales_pop.items():
        rows.append({
            "country": country,
            "sales_2024": s24, "sales_2025": s25, "population_m": pop,
            "reg_per_1000_2024": round(s24/(pop*1000),1),
            "reg_per_1000_2025": round(s25/(pop*1000),1),
            "1_per_n_2024": int(round(pop*1e6/s24)),
            "1_per_n_2025": int(round(pop*1e6/s25)),
        })
    return pd.DataFrame(rows).sort_values("reg_per_1000_2025", ascending=False).reset_index(drop=True)

AVAILABLE_YEARS = [2024, 2025]

if __name__ == "__main__":
    df = load_ratio_per_capita()
    for c in ["Portugal","Germany","Spain","France","Italy"]:
        row = df[df["country"]==c].iloc[0]
        print(f"{c:15}: {row['reg_per_1000_2025']:.1f}/1000 hab | 1 por cada {row['1_per_n_2025']} hab")
    print("\nAll loaders OK")

def load_monthly_data():
    """
    Monthly EU car registrations (EU27 only) + BEV share
    2024: ACEA press releases (confirmed full year 10.0M, BEV 13.6%)
    2025: Reconstructed from ACEA YTD reports — Jan -2.6%, H1 -1.9%,
          Jul -0.7%, Aug -0.1%, Sep +0.9%, Oct +1.4%, Nov +1.4%, FY +1.8%
    Q1 2026: ACEA confirmed BEV 20.6%, EU registrations +~3%
    Note: monthly splits are estimates; annual totals are confirmed
    Source: ACEA press releases 2024-2025
    """
    # EU27 monthly registrations (thousands)
    data = [
        # month, reg_2024, reg_2025, bev_share_2024, bev_share_2025
        ("Jan", 760, 753, 10.9, 15.0),
        ("Feb", 850, 845, 12.4, 14.0),
        ("Mar", 1050, 1038, 13.8, 15.5),
        ("Apr", 785, 784, 14.1, 14.8),
        ("May", 880, 875, 14.5, 15.5),
        ("Jun", 905, 911, 13.5, 17.2),
        ("Jul", 810, 840, 13.5, 14.8),
        ("Aug", 490, 509, 12.2, 14.5),
        ("Sep", 1095, 1140, 17.9, 18.5),
        ("Oct", 870, 921, 13.7, 19.0),
        ("Nov", 825, 873, 12.8, 20.5),
        ("Dec", 668, 692, 15.9, 25.0),
    ]
    import pandas as pd
    df = pd.DataFrame(data, columns=["month","reg_2024_k","reg_2025_k","bev_pct_2024","bev_pct_2025"])
    df["month_num"] = range(1, 13)
    # Q1 2026 confirmed by ACEA
    df.loc[df["month_num"]==1, "bev_pct_2026_q1"] = 20.6
    return df

def load_forecast_2026():
    """
    2026 full year forecast — 3 scenarios
    Base: +2.5% growth (EU trend + Spain/Poland momentum)
    Optimistic: +5.0% (if EV incentives expand, strong H2)
    Pessimistic: flat 0% (macro headwinds, tariff effects)
    BEV share forecast: linear extrapolation of 2024-2025 trend
    Source: analyst estimates based on ACEA data
    """
    import pandas as pd
    scenarios = [
        ("Pessimistic", 10960, 17.4, "#D85A30"),
        ("Base case",   11260, 21.5, "#185FA5"),
        ("Optimistic",  11550, 25.0, "#1D9E75"),
    ]
    df = pd.DataFrame(scenarios, columns=["scenario","reg_2026_k_eu","bev_share_2026","color"])
    df["reg_2024_k_eu"] = 10000
    df["reg_2025_k_eu"] = 10180
    df["growth_vs_2025"] = ((df["reg_2026_k_eu"] - df["reg_2025_k_eu"]) / df["reg_2025_k_eu"] * 100).round(1)
    return df

def load_market_concentration():
    """HHI and concentration metrics by brand, group and country — 2024 vs 2025"""
    import pandas as pd, numpy as np
    # Brand HHI (EU+EFTA+UK)
    total_25 = 13270000
    total_24 = 12960000
    b25 = load_top_brands(2025)
    b24 = load_top_brands(2024)
    # Add residual "Other" brands
    top_share_25 = b25["market_share"].sum()
    top_share_24 = b24["market_share"].sum()
    shares_25 = list(b25["market_share"]) + [max(0, 100 - top_share_25)]
    shares_24 = list(b24["market_share"]) + [max(0, 100 - top_share_24)]
    hhi_25 = sum(s**2 for s in shares_25)
    hhi_24 = sum(s**2 for s in shares_24)
    # Group HHI
    g25 = load_manufacturer_groups(2025)
    g24 = load_manufacturer_groups(2024)
    ghhi_25 = sum(s**2 for s in g25["market_share"])
    ghhi_24 = sum(s**2 for s in g24["market_share"])
    return {
        "brand_hhi_2025": round(hhi_25, 1),
        "brand_hhi_2024": round(hhi_24, 1),
        "group_hhi_2025": round(ghhi_25, 1),
        "group_hhi_2024": round(ghhi_24, 1),
        "top3_share_2025": round(b25.head(3)["market_share"].sum(), 1),
        "top3_share_2024": round(b24.head(3)["market_share"].sum(), 1),
        "top5_share_2025": round(b25.head(5)["market_share"].sum(), 1),
        "top5_share_2024": round(b24.head(5)["market_share"].sum(), 1),
    }

def load_group_share_evolution():
    """Group market share evolution — historical estimates 2019-2025"""
    import pandas as pd
    # Historical group share estimates (ACEA/analyst sources)
    data = [
        ("Volkswagen Group", 2019,24.1),("Volkswagen Group",2020,24.8),
        ("Volkswagen Group",2021,25.3),("Volkswagen Group",2022,25.8),
        ("Volkswagen Group",2023,26.0),("Volkswagen Group",2024,26.3),
        ("Volkswagen Group",2025,26.9),
        ("Stellantis",2019,None),("Stellantis",2020,None),  # pre-merger
        ("Stellantis",2021,19.4),("Stellantis",2022,18.2),
        ("Stellantis",2023,16.8),("Stellantis",2024,15.2),("Stellantis",2025,14.3),
        ("Renault Group",2019,10.2),("Renault Group",2020,9.8),
        ("Renault Group",2021,9.5),("Renault Group",2022,9.7),
        ("Renault Group",2023,9.8),("Renault Group",2024,9.9),("Renault Group",2025,10.2),
        ("Hyundai Group",2019,6.8),("Hyundai Group",2020,7.1),
        ("Hyundai Group",2021,7.5),("Hyundai Group",2022,7.9),
        ("Hyundai Group",2023,8.3),("Hyundai Group",2024,8.2),("Hyundai Group",2025,7.9),
        ("Toyota Group",2019,5.2),("Toyota Group",2020,5.5),
        ("Toyota Group",2021,5.8),("Toyota Group",2022,6.5),
        ("Toyota Group",2023,7.1),("Toyota Group",2024,7.8),("Toyota Group",2025,7.6),
        ("BMW Group",2019,7.2),("BMW Group",2020,6.9),
        ("BMW Group",2021,6.8),("BMW Group",2022,7.0),
        ("BMW Group",2023,7.1),("BMW Group",2024,7.1),("BMW Group",2025,7.3),
        ("Mercedes-Benz",2019,6.1),("Mercedes-Benz",2020,5.8),
        ("Mercedes-Benz",2021,5.6),("Mercedes-Benz",2022,5.5),
        ("Mercedes-Benz",2023,5.4),("Mercedes-Benz",2024,5.4),("Mercedes-Benz",2025,5.4),
        ("Tesla",2019,0.1),("Tesla",2020,0.3),
        ("Tesla",2021,0.8),("Tesla",2022,1.5),
        ("Tesla",2023,2.2),("Tesla",2024,2.5),("Tesla",2025,1.8),
    ]
    df = pd.DataFrame(data, columns=["group","year","market_share"])
    return df.dropna()

def load_country_risk_matrix():
    """
    Risk/opportunity matrix: market growth vs EV readiness
    Quadrants: Stars (high growth + high EV), Transition (low growth + high EV),
               Opportunities (high growth + low EV), Laggards (low growth + low EV)
    """
    import pandas as pd
    data = [
        # country, yoy_2025, bev_share, reg_per_1000, market_size_k, region
        ("Norway",     39.4, 89.0, 32.7,  180, "EFTA"),
        ("Lithuania",  39.3,  5.0, 15.0,   42, "EU"),
        ("Iceland",    42.4, 52.0, 39.3,   15, "EFTA"),
        ("Latvia",     31.4,  4.0, 12.5,   23, "EU"),
        ("Bulgaria",   15.1,  1.5,  7.6,   49, "EU"),
        ("Spain",      12.9,  6.0, 24.0, 1149, "EU"),
        ("Croatia",     7.4,  4.0, 17.9,   70, "EU"),
        ("Poland",      8.3,  3.5, 16.2,  597, "EU"),
        ("Hungary",     6.4,  3.0, 13.3,  129, "EU"),
        ("Greece",      5.2,  4.5, 13.9,  144, "EU"),
        ("Portugal",    7.3, 14.0, 21.4,  225, "EU"),
        ("Ireland",     3.0, 18.0, 24.5,  125, "EU"),
        ("Germany",     1.4, 13.5, 33.9, 2858, "EU"),
        ("Netherlands", 1.7, 33.0, 21.8,  388, "EU"),
        ("Austria",    12.3, 12.0, 31.3,  285, "EU"),
        ("Sweden",      1.3, 38.0, 26.0,  273, "EU"),
        ("Denmark",     6.7, 51.0, 31.3,  185, "EU"),
        ("United Kingdom",3.5,22.0, 29.8, 2021, "UK"),
        ("France",     -5.0, 16.9, 23.9, 1632, "EU"),
        ("Italy",      -2.1,  4.5, 25.8, 1525, "EU"),
        ("Belgium",    -7.5, 15.0, 35.4,  415, "EU"),
        ("Finland",    -3.0, 28.0, 13.1,   72, "EU"),
        ("Estonia",   -48.6, 15.0,  9.3,   13, "EU"),
        ("Switzerland",-2.4, 22.0, 26.6,  234, "EFTA"),
    ]
    df = pd.DataFrame(data, columns=["country","yoy_2025","bev_share","reg_per_1000","market_size_k","region"])
    eu_avg_yoy = 2.4
    eu_avg_bev = 13.6
    def quadrant(row):
        high_growth = row["yoy_2025"] > eu_avg_yoy
        high_ev     = row["bev_share"] > eu_avg_bev
        if high_growth and high_ev:     return "⭐ Stars"
        if not high_growth and high_ev: return "🔋 EV Leaders"
        if high_growth and not high_ev: return "🚀 Growth Markets"
        return "⚠️ Watch"
    df["quadrant"] = df.apply(quadrant, axis=1)
    return df

def load_outlier_analysis():
    """Outlier countries with structural explanations"""
    import pandas as pd
    data = [
        ("Estonia",    -48.6, "Subsidy removal shock",
         "EV purchase subsidy of €5,000 cancelled in Dec 2024. Market was 60% subsidy-driven. Collapse was immediate and structural — demand did not exist without incentive.",
         "Leading indicator for any market removing EV subsidies abruptly. Watch Czech Republic and Slovakia where similar policies are under discussion."),
        ("Norway",     +39.4, "BEV infrastructure maturity",
         "89% of all new cars sold in 2025 are BEV. Strong Q1 driven by Tesla Model Y replacements and new Volvo EX30 demand. Government 2025 target of 100% zero-emission sales effectively met.",
         "Norway is the template for mature EV transition. Its success is replicable only where charging infrastructure, tax policy and consumer income align simultaneously."),
        ("Iceland",    +42.4, "Base effect + EV momentum",
         "Small market (14.5K units) recovering from 2022-2023 weakness. BEV share at 52%. Very price-sensitive market amplifies % swings.",
         "Statistical outlier due to small base. Not a trend signal for larger markets."),
        ("Lithuania",  +39.3, "Fleet renewal + economic growth",
         "Baltic economies growing 4-5% GDP in 2025. Corporate fleet renewal accelerating after COVID backlog. Used car market tightening drives new car preference.",
         "Baltic states (LT, LV, EE ex-subsidy collapse) represent underserved fleet opportunity for mainstream brands."),
        ("Belgium",    -7.5,  "Company car tax reform",
         "Belgium tax reform 2025 tightened BIK rules on combustion company cars, but transition to EV company cars slower than expected. Total market contracted as fleet buyers paused.",
         "Company car tax regimes drive up to 60% of new car sales in Belgium. Any reform creates temporary paralysis. Similar reforms pending in NL and DE."),
        ("France",     -5.0,  "Subsidy reduction + political uncertainty",
         "EV bonus reduced from €7,000 to €4,000 in mid-2024. Political instability (3 governments in 18 months) froze industrial investment decisions. Stellantis and Renault delayed model launches.",
         "France -5% while Spain +12.9% — Iberian shift in EU auto gravity. French OEM vulnerability to domestic market weakness is strategically significant."),
    ]
    return pd.DataFrame(data, columns=["country","yoy_2025","headline","mechanism","strategic_implication"])
