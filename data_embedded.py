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
        (9,"Duster","Dacia","Renault Group","Petrol
