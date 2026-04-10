from pathlib import Path
import pandas as pd
import geopandas as gpd

INTERIM = Path("data/interim/uzbekistan")
OUT = Path("data/processed/uzbekistan")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    stats = pd.read_csv(INTERIM / "urban_rural_clean.csv")
    regions = gpd.read_file(INTERIM / "uz_regions.json")

    # Clean join keys
    stats["region_key"] = stats["region_key"].astype(str).str.strip()
    regions["region_key"] = regions["region_key"].astype(str).str.strip()

    if "region_name" in regions.columns:
        regions["region_name"] = regions["region_name"].astype(str).str.strip()

    # Ensure numeric fields are numeric
    numeric_cols = ["urban_population", "rural_population", "total_population", "urban_percent", "rural_percent"]
    for col in numeric_cols:
        if col in stats.columns:
            stats[col] = pd.to_numeric(stats[col], errors="coerce")

    # Merge stats onto geometry
    merged = regions.merge(stats, on="region_key", how="left", suffixes=("", "_stat"))

    # If both region_name columns exist, prefer boundary display name
    if "region_name_stat" in merged.columns:
        merged = merged.drop(columns=["region_name_stat"])

    # Write outputs
    merged.to_file(OUT / "regions.geojson", driver="GeoJSON")
    stats.to_json(OUT / "urban_stats.json", orient="records", force_ascii=False)

    print("Wrote data/processed/uzbekistan/regions.geojson")
    print("Wrote data/processed/uzbekistan/urban_stats.json")

    missing = merged[merged["urban_percent"].isna()]
    if not missing.empty:
        cols = [c for c in ["region_key", "region_name"] if c in missing.columns]
        print("\nRegions with no matched urban/rural data:")
        print(missing[cols].to_string(index=False))

if __name__ == "__main__":
    main()