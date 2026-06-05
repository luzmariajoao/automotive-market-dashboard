"""
Todos os dados embutidos directamente — sem dependência de ficheiros CSV externos.
Funciona local e no Streamlit Cloud sem precisar de data/.
"""
import pandas as pd

def get_sales_by_country_2024():
    data = [
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
    df = pd.DataFrame(data, columns=["country","region","sales_2024","sales_2023","pct_change"])
    return df.sort_values("sales_2024", ascending=False).reset_index(drop=True)

def get_sales_by_country_2025():
    data = [
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
    df = pd.DataFrame(data, columns=["country","region","sales_2025","sales_2024","pct_change"])
    return df.sort_values("sales_2025", ascending=False).reset_index(drop=True)

def get_top_brands_2024():
    data = [
        (1,"Volkswagen","Volkswagen Group",1371465,1357842,1.0,10.6),
        (2,"Toyota","Toyota Group",928767,828931,12.0,7.2),
        (3,"BMW","BMW Group",774925,729073,6.3,6.0),
        (4,"Skoda","Volkswagen Group",766510,679984,12.7,5.9),
        (5,"Renault","Renault Group",699214,681058,2.7,5.4),
        (6,"Mercedes","Mercedes-Benz",684027,671973,1.8,5.3),
        (7,"Audi","Volkswagen Group",663239,733305,-9.6,5.1),
        (8,"Peugeot","Stellantis",641264,637178,0.6,4.9),
        (9,"Dacia","Renault Group",578935,557154,3.9,4.5),
        (10,"Hyundai","Hyundai Group",534360,534307,0.0,4.1),
    ]
    return pd.DataFrame(data, columns=["rank","brand","group","sales_2024","sales_2023","pct_change","market_share"])

def get_top_brands_2025():
    data = [
        (1,"Volkswagen","Volkswagen Group",1452704,1371854,5.9,10.9),
        (2,"Toyota","Toyota Group",1005000,928767,8.1,7.6),
        (3,"Skoda","Volkswagen Group",840179,766469,9.6,6.3),
        (4,"BMW","BMW Group",800585,775119,3.3,6.0),
        (5,"Renault","Renault Group",750605,699151,7.4,5.7),
        (6,"Mercedes","Mercedes-Benz",710000,684027,3.8,5.4),
        (7,"Audi","Volkswagen Group",664680,662664,0.3,5.0),
        (8,"Peugeot","Stellantis",637834,641376,-0.6,4.8),
        (9,"Dacia","Renault Group",597088,578953,3.1,4.5),
        (10,"Hyundai","Hyundai Group",535205,534198,0.2,4.0),
    ]
    return pd.DataFrame(data, columns=["rank","brand","group","sales_2025","sales_2024","pct_change","market_share"])

def get_top_models():
    data = [
        (1,"Sandero","Dacia","Renault Group","Petrol/LPG","Top model in Spain and Portugal"),
        (2,"Clio","Renault","Renault Group","Petrol/Hybrid","Improved from 4th in 2023"),
        (3,"Golf","Volkswagen","Volkswagen Group","Petrol/Diesel","215700 units up 17%"),
        (4,"Model Y","Tesla","Tesla","Electric","Top in NL SE CH DK NO"),
        (5,"T-Roc","Volkswagen","Volkswagen Group","Petrol/Diesel","Slipped one position"),
        (6,"208","Peugeot","Stellantis","Petrol/Electric","Top model in 2022"),
        (7,"Yaris Cross","Toyota","Toyota Group","Hybrid","Improved one rank"),
        (8,"Octavia","Skoda","Volkswagen Group","Petrol/Diesel","Improved two ranks"),
        (9,"Duster","Dacia","Renault Group","Petrol/LPG/Hybrid","Entered top 10 from 15th"),
        (10,"Yaris","Toyota","Toyota Group","Hybrid","Entered top 10 from 14th"),
    ]
    return pd.DataFrame(data, columns=["rank","model","brand","group","fuel_type","notes"])

def get_fuel_type_mix():
    data = [
        (2021,39.9,19.8,9.1,8.9,19.6,2.8,40.6),
        (2022,36.4,22.7,12.1,9.4,16.4,3.0,47.3),
        (2023,35.3,25.8,14.6,7.7,13.6,3.0,51.1),
        (2024,33.3,30.9,13.6,7.1,11.9,3.1,54.8),
    ]
    return pd.DataFrame(data, columns=["year","petrol_pct","diesel_pct","bev_pct","phev_pct","hybrid_pct","alternative_pct","total_alternative_pct"])

def get_segment_share():
    data = [
        ("SUV","SUV",53,2024),("Small","A+B",19,2024),("Lower medium","C",15,2024),
        ("Upper medium","D",7,2024),("MPV","MPV",4,2024),("Luxury","E+F",2,2024),
    ]
    return pd.DataFrame(data, columns=["segment","code","share_pct","year"])

def get_co2_by_country():
    data = [
        ("Finland","EU",60.9,33.0),("Sweden","EU",61.0,33.0),("Denmark","EU",73.3,51.0),
        ("Netherlands","EU",80.0,33.0),("Norway","EFTA",35.0,89.0),("Belgium","EU",95.0,15.0),
        ("Portugal","EU",100.0,14.0),("France","EU",102.0,16.9),("Austria","EU",105.0,12.0),
        ("Spain","EU",107.0,6.0),("EU average","EU",107.8,None),
        ("Germany","EU",117.0,13.5),("Italy","EU",120.0,4.5),
    ]
    df = pd.DataFrame(data, columns=["country","region","co2_gkm_2024","bev_share_pct_2024"])
    return df.sort_values("co2_gkm_2024")

def get_cars_per_1000():
    data = [
        ("Netherlands",69),("Luxembourg",38),("Slovenia",34),("Belgium",29),
        ("Germany",28),("Denmark",26),("Austria",26),("Italy",25),("Sweden",25),
        ("France",23),("Ireland",25),("Czechia",23),("Spain",21),("Portugal",21),
        ("Estonia",21),("Slovakia",21),("Croatia",20),("Cyprus",18),("Poland",17),
        ("Malta",17),("Finland",16),("Greece",15),("Hungary",14),("Lithuania",13),
        ("Latvia",13),("Romania",13),("Bulgaria",10),("EU average",24),
    ]
    df = pd.DataFrame(data, columns=["country","cars_per_1000"])
    return df.sort_values("cars_per_1000", ascending=False)

def get_production_by_country():
    data = [
        ("Germany",3942396,198021,142087,4497),("Spain",1872988,467469,32554,1400),
        ("France",849437,498576,68270,2703),("Czechia",1446855,0,1429,4290),
        ("Slovakia",993750,0,0,0),("Romania",473110,0,0,0),
        ("Hungary",435541,0,839,0),("Poland",224017,336347,43885,7019),
        ("Italy",309336,224454,55066,1445),("Belgium",197624,38413,0,201),
        ("Portugal",229095,92042,2205,173),("Sweden",270807,33809,0,2010),
        ("Netherlands",0,7515,60319,649),("Slovenia",60903,0,0,25),
        ("Austria",72335,0,0,0),("Finland",22760,0,0,46),
    ]
    df = pd.DataFrame(data, columns=["country","cars_produced","vans_produced","trucks_produced","buses_produced"])
    return df[df["cars_produced"]>0].sort_values("cars_produced", ascending=False)

def get_manufacturer_groups(year=2025):
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
        cols = ["group","sales_2025","sales_2024","pct_change","market_share"]
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
        cols = ["group","sales_2024","sales_2023","pct_change","market_share"]
    return pd.DataFrame(data, columns=cols)

def get_yoy_comparison():
    df24 = get_sales_by_country_2024()[["country","region","sales_2024"]]
    df25 = get_sales_by_country_2025()[["country","sales_2025","pct_change"]]
    return df24.merge(df25, on="country", how="outer").sort_values("sales_2025", ascending=False)
