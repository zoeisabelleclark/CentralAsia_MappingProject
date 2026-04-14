from pathlib import Path
import pandas as pd
import geopandas as gpd

INTERIM = Path("data/interim/tajikistan")
OUT = Path("data/processed/tajikistan")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    stats = pd.read_csv(INTERIM / "urban_rural_clean.csv")
    regions = gpd.read_file(INTERIM / "tajikistan_regions.geojson")

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

    print("Wrote data/processed/tajikistan/regions.geojson")
    print("Wrote data/processed/tajikistan/urban_stats.json")

    missing = merged[merged["urban_percent"].isna()]
    if not missing.empty:
        cols = [c for c in ["region_key", "region_name"] if c in missing.columns]
        print("\nRegions with no matched urban/rural data:")
        print(missing[cols].to_string(index=False))

if __name__ == "__main__":
    main()