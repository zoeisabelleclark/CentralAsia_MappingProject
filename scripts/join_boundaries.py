from pathlib import Path
import pandas as pd
import geopandas as gpd

INTERIM = Path("data/interim")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    # Load cleaned census data
    stats = pd.read_csv(INTERIM / "census_clean.csv")

    # Load prepared boundaries, not raw boundaries
    regions = gpd.read_file(INTERIM / "kazakhstan_regions.json")

    # Basic cleanup
    stats["region_key"] = stats["region_key"].astype(str).str.strip()
    stats["ethnicity"] = stats["ethnicity"].astype(str).str.strip()
    stats["population"] = pd.to_numeric(stats["population"], errors="coerce")

    regions["region_key"] = regions["region_key"].astype(str).str.strip()
    regions["region_name"] = regions["region_name"].astype(str).str.strip()

    # Drop rows with missing population
    stats = stats.dropna(subset=["population"])

    # Calculate total population by region
    totals = (
        stats.groupby("region_key", as_index=False)["population"]
        .sum()
        .rename(columns={"population": "region_total_population"})
    )

    # Find dominant ethnicity by region
    idx = stats.groupby("region_key")["population"].idxmax()
    dominant = stats.loc[idx, ["region_key", "ethnicity", "population"]].copy()

    dominant = dominant.rename(columns={
        "ethnicity": "dominant_ethnicity",
        "population": "dominant_population"
    })

    # Add totals and percent
    dominant = dominant.merge(totals, on="region_key", how="left")
    dominant["dominant_percent"] = (
        dominant["dominant_population"] / dominant["region_total_population"] * 100
    )

    # Merge onto boundaries
    merged = regions.merge(dominant, on="region_key", how="left")

    # Write outputs
    merged.to_file(OUT / "regions.geojson", driver="GeoJSON")
    stats.to_json(OUT / "ethnicity_stats.json", orient="records", force_ascii=False)

    print("Wrote data/processed/regions.geojson")
    print("Wrote data/processed/ethnicity_stats.json")

    # Optional debug: show unmatched regions
    missing = merged[merged["dominant_ethnicity"].isna()][["region_key", "region_name"]]
    if not missing.empty:
        print("\nRegions with no matched ethnicity data:")
        print(missing.to_string(index=False))

if __name__ == "__main__":
    main()