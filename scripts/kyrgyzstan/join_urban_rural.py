from pathlib import Path
import pandas as pd
import geopandas as gpd

INTERIM = Path("data/interim/kyrgyzstan")
OUT = Path("data/processed/kyrgyzstan")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    stats = pd.read_csv(INTERIM / "urban_rural_clean.csv")
    regions = gpd.read_file(INTERIM / "kg_regions.json")

    stats["region_key"] = stats["region_key"].astype(str).str.strip()
    regions["region_key"] = regions["region_key"].astype(str).str.strip()

    if "region_name" in regions.columns:
        regions["region_name"] = regions["region_name"].astype(str).str.strip()

    for col in ["urban_population", "rural_population", "total_population", "urban_percent", "rural_percent"]:
        if col in stats.columns:
            stats[col] = pd.to_numeric(stats[col], errors="coerce")

    merged = regions.merge(stats, on="region_key", how="left", suffixes=("", "_stat"))

    if "region_name_stat" in merged.columns:
        merged = merged.drop(columns=["region_name_stat"])

    merged.to_file(OUT / "regions.geojson", driver="GeoJSON")
    stats.to_json(OUT / "urban_stats.json", orient="records", force_ascii=False)

    print("Wrote data/processed/kyrgyzstan/regions.geojson")
    print("Wrote data/processed/kyrgyzstan/urban_stats.json")

if __name__ == "__main__":
    main()