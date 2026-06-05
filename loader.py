import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from data_embedded import (
    get_sales_by_country_2024, get_sales_by_country_2025,
    get_top_brands_2024, get_top_brands_2025, get_top_models,
    get_fuel_type_mix, get_segment_share, get_co2_by_country,
    get_cars_per_1000, get_production_by_country,
    get_manufacturer_groups, get_yoy_comparison,
)

AVAILABLE_YEARS = [2024, 2025]

def load_sales_by_country(year=2025):
    return get_sales_by_country_2025() if year == 2025 else get_sales_by_country_2024()

def load_top_brands(year=2025):
    return get_top_brands_2025() if year == 2025 else get_top_brands_2024()

def load_top_models(year=2024):
    return get_top_models()

def load_manufacturer_groups(year=2025):
    return get_manufacturer_groups(year)

def load_fuel_type_mix():
    return get_fuel_type_mix()

def load_segment_share():
    return get_segment_share()

def load_co2_by_country():
    return get_co2_by_country()

def load_cars_per_1000():
    return get_cars_per_1000()

def load_production_by_country():
    return get_production_by_country()

def load_employment():
    return pd.DataFrame()

def build_yoy_comparison():
    return get_yoy_comparison()
