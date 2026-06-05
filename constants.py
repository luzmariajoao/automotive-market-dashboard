"""Reference constants for the European automotive market dashboard."""

# Top 10 best-selling brands in Europe 2024 (ACEA)
TOP_10_BRANDS = [
    "Volkswagen", "Toyota", "BMW", "Skoda", "Renault",
    "Mercedes", "Audi", "Peugeot", "Dacia", "Hyundai",
]

# The five largest national markets in Europe 2024
TOP_5_MARKETS = ["Germany", "United Kingdom", "France", "Italy", "Spain"]

# Region grouping used by ACEA
REGIONS = {
    "EU": "European Union",
    "EFTA": "Iceland, Norway, Switzerland",
    "UK": "United Kingdom",
}

# Fuel type categories (for grouping / colouring in the dashboard)
FUEL_TYPES = ["Petrol", "Diesel", "Hybrid", "Electric", "LPG"]

# Colour palette for consistent dashboard styling (brand-agnostic)
PALETTE = {
    "primary": "#185FA5",
    "secondary": "#1D9E75",
    "accent": "#D85A30",
    "neutral": "#888780",
}

# Data source attribution
SOURCES = {
    "sales_by_country": "ACEA via best-selling-cars.com (2024 full year)",
    "top_brands": "ACEA via best-selling-cars.com (2024 full year)",
    "top_models": "JATO Dynamics via best-selling-cars.com (2024 full year)",
    "manufacturer_groups": "ACEA via best-selling-cars.com (2024 full year)",
}
