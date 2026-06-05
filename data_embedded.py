
def get_population():
    """Population by country (millions, 2024 estimate) — Eurostat/UN"""
    data = [
        ("Austria",9.1),("Belgium",11.7),("Bulgaria",6.5),("Croatia",3.9),
        ("Cyprus",1.2),("Czechia",10.8),("Denmark",5.9),("Estonia",1.4),
        ("Finland",5.5),("France",68.2),("Germany",84.4),("Greece",10.4),
        ("Hungary",9.7),("Ireland",5.1),("Italy",59.0),("Latvia",1.8),
        ("Lithuania",2.8),("Luxembourg",0.67),("Malta",0.54),("Netherlands",17.8),
        ("Poland",36.8),("Portugal",10.5),("Romania",19.0),("Slovakia",5.5),
        ("Slovenia",2.1),("Spain",47.8),("Sweden",10.5),("Iceland",0.37),
        ("Norway",5.5),("Switzerland",8.8),("United Kingdom",67.7),
    ]
    df = pd.DataFrame(data, columns=["country","population_m"])
    return df

def get_registrations_per_capita():
    """New car registrations per 1000 inhabitants — 2024 and 2025"""
    sales_data = {
        "Austria":(253789,284978),"Belgium":(448277,414770),"Bulgaria":(42941,49419),
        "Croatia":(65020,69841),"Cyprus":(15057,14634),"Czechia":(231597,248719),
        "Denmark":(173114,184641),"Estonia":(25386,13055),"Finland":(74064,71881),
        "France":(1718412,1632152),"Germany":(2817331,2857591),"Greece":(137075,144199),
        "Hungary":(121611,129440),"Ireland":(121196,124954),"Italy":(1559229,1524843),
        "Latvia":(17329,22506),"Lithuania":(30122,41974),"Luxembourg":(46659,47158),
        "Malta":(7663,6468),"Netherlands":(381227,388024),"Poland":(551568,597435),
        "Portugal":(209715,225039),"Romania":(151105,156803),"Slovakia":(93409,93103),
        "Slovenia":(53018,57556),"Spain":(1016885,1148650),"Sweden":(269582,272998),
        "Iceland":(10233,14547),"Norway":(128687,179632),"Switzerland":(239535,233737),
        "United Kingdom":(1952778,2020523),
    }
    pop_data = {
        "Austria":9.1,"Belgium":11.7,"Bulgaria":6.5,"Croatia":3.9,"Cyprus":1.2,
        "Czechia":10.8,"Denmark":5.9,"Estonia":1.4,"Finland":5.5,"France":68.2,
        "Germany":84.4,"Greece":10.4,"Hungary":9.7,"Ireland":5.1,"Italy":59.0,
        "Latvia":1.8,"Lithuania":2.8,"Luxembourg":0.67,"Malta":0.54,"Netherlands":17.8,
        "Poland":36.8,"Portugal":10.5,"Romania":19.0,"Slovakia":5.5,"Slovenia":2.1,
        "Spain":47.8,"Sweden":10.5,"Iceland":0.37,"Norway":5.5,"Switzerland":8.8,
        "United Kingdom":67.7,
    }
    import pandas as pd
    rows = []
    for country, (s24, s25) in sales_data.items():
        pop = pop_data.get(country, 10.0)
        rows.append({
            "country": country,
            "sales_2024": s24,
            "sales_2025": s25,
            "population_m": pop,
            "reg_per_1000_2024": round(s24 / (pop * 1000), 1),
            "reg_per_1000_2025": round(s25 / (pop * 1000), 1),
            "1_per_n_2024": int(round(pop * 1e6 / s24)),
            "1_per_n_2025": int(round(pop * 1e6 / s25)),
        })
    df = pd.DataFrame(rows).sort_values("reg_per_1000_2025", ascending=False).reset_index(drop=True)
    return df
