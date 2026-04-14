from pathlib import Path
import geopandas as gpd
import pandas as pd

BASE = Path("data/processed")

COUNTRIES = [
    "kazakhstan",
    "kyrgyzstan",
    "uzbekistan",
    "tajikistan",
    "turkmenistan",
]

def main():
    for country in COUNTRIES:
        path = BASE / country / "regions.geojson"
        gdf = gpd.read_file(path)

        # Make sure population is numeric
        if "total_population" not in gdf.columns:
            raise ValueError(f"{country}: missing total_population column")

        gdf["total_population"] = pd.to_numeric(gdf["total_population"], errors="coerce")

        # Reproject for area calculation
        projected = gdf.to_crs(epsg=6933)

        # Area in square kilometers
        gdf["area_sq_km"] = projected.geometry.area / 1_000_000

        # Density = people per sq km
        gdf["population_density"] = gdf["total_population"] / gdf["area_sq_km"]

        # Clean weird values
        gdf.loc[gdf["area_sq_km"] <= 0, "population_density"] = pd.NA

        gdf.to_file(path, driver="GeoJSON")

        print(f"\nUpdated {path}")
        cols = [c for c in ["country", "region_name", "total_population", "area_sq_km", "population_density"] if c in gdf.columns]
        print(gdf[cols].head().to_string(index=False))

if __name__ == "__main__":
    main()