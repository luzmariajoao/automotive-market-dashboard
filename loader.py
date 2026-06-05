"""Data loading and light processing for the European car market dashboard."""

from pathlib import Path
import pandas as pd

# Funciona local (loader.py em src/) e no Streamlit Cloud (loader.py na raiz)
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent if (_HERE.parent / "data").exists() else _HERE
RAW = _ROOT / "data" / "raw"
PROCESSED = _ROOT / "data" / "processed"

AVAILABLE_YEARS = [2024, 2025]


def load_sales_by_country(year: int = 2025) -> pd.DataFrame:
    """Country-level new car registrations for a given year."""
    df = pd.read_csv(RAW / f"sales_by_country_{year}.csv")
    df = df.sort_values(f"sales_{year}", ascending=False).reset_index(drop=True)
    return df


def load_top_brands(year: int = 2025) -> pd.DataFrame:
    """Top 10 best-selling brands for a given year."""
    return pd.read_csv(RAW / f"top_brands_{year}.csv")


def load_top_models(year: int = 2024) -> pd.DataFrame:
    """Top 10 best-selling models (2024 only — 2025 models data pending)."""
    return pd.read_csv(RAW / "top_models_2024.csv")


def load_manufacturer_groups(year: int = 2025) -> pd.DataFrame:
    """Manufacturer groups by market share for a given year."""
    return pd.read_csv(RAW / f"manufacturer_groups_{year}.csv")


def build_yoy_comparison() -> pd.DataFrame:
    """Merge 2024 and 2025 country data for year-on-year comparison."""
    df24 = pd.read_csv(RAW / "sales_by_country_2024.csv")[["country", "region", "sales_2024"]]
    df25 = pd.read_csv(RAW / "sales_by_country_2025.csv")[["country", "sales_2025", "pct_change"]]
    merged = df24.merge(df25, on="country", how="outer")
    merged = merged.sort_values("sales_2025", ascending=False).reset_index(drop=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    merged.to_csv(PROCESSED / "yoy_comparison.csv", index=False)
    return merged


if __name__ == "__main__":
    print("=== 2025 Top 10 países ===")
    c = load_sales_by_country(2025)
    print(c.head(10)[["country", "sales_2025", "pct_change"]].to_string(index=False))
    print("\n=== Comparação 2024 vs 2025 (top 5) ===")
    yoy = build_yoy_comparison()
    print(yoy.head(5)[["country", "sales_2024", "sales_2025", "pct_change"]].to_string(index=False))


def load_fuel_type_mix() -> pd.DataFrame:
    """EU fuel type market share by year 2021-2024 (ACEA)."""
    return pd.read_csv(RAW / "fuel_type_mix_eu_2021_2024.csv")


def load_segment_share() -> pd.DataFrame:
    """EU car segment share 2024 — SUV, Small, Medium, etc. (ACEA/S&P)."""
    return pd.read_csv(RAW / "segment_share_eu_2024.csv")


def load_co2_by_country() -> pd.DataFrame:
    """Average CO2 g/km and BEV share by country 2024 (ACEA/ICCT)."""
    df = pd.read_csv(RAW / "co2_by_country_2024.csv")
    return df.sort_values("co2_gkm_2024")


def load_cars_per_1000() -> pd.DataFrame:
    """New cars sold per 1000 inhabitants by country 2024 (ACEA)."""
    return pd.read_csv(RAW / "cars_per_1000_inhabitants_2024.csv").sort_values(
        "cars_per_1000", ascending=False
    )


def load_production_by_country() -> pd.DataFrame:
    """Car production by country 2024 (S&P Global Mobility)."""
    df = pd.read_csv(RAW / "production_by_country_2024.csv")
    return df[df.country != "EU total"].sort_values("cars_produced", ascending=False)


def load_employment() -> pd.DataFrame:
    """Automotive direct employment by country 2023 (Eurostat)."""
    df = pd.read_csv(RAW / "automotive_employment_2023.csv")
    return df[df.country != "EU total"].sort_values("direct_jobs", ascending=False)
