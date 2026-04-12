from pathlib import Path
import math
import pandas as pd
import geopandas as gpd

INTERIM = Path("data/interim/kyrgyzstan")
OUT = Path("data/processed/kyrgyzstan")
OUT.mkdir(parents=True, exist_ok=True)

def shannon_diversity(group: pd.DataFrame) -> float:
    total = group["population"].sum()
    if total == 0:
        return 0.0

    proportions = group["population"] / total
    proportions = proportions[proportions > 0]
    return -sum(p * math.log(p) for p in proportions)

def main():
    stats = pd.read_csv(INTERIM / "census_clean.csv")
    regions = gpd.read_file(INTERIM / "kg_regions.json")

    stats["region_key"] = stats["region_key"].astype(str).str.strip()
    stats["ethnicity"] = stats["ethnicity"].astype(str).str.strip()
    stats["population"] = pd.to_numeric(stats["population"], errors="coerce")
    stats["region_total_population"] = pd.to_numeric(stats["region_total_population"], errors="coerce")
    stats["percent"] = pd.to_numeric(stats["percent"], errors="coerce")

    regions["region_key"] = regions["region_key"].astype(str).str.strip()
    if "region_name" in regions.columns:
        regions["region_name"] = regions["region_name"].astype(str).str.strip()

    idx = stats.groupby("region_key")["population"].idxmax()
    dominant = stats.loc[idx, ["region_key", "ethnicity", "population", "percent"]].copy()
    dominant = dominant.rename(columns={
        "ethnicity": "dominant_ethnicity",
        "population": "dominant_population",
        "percent": "dominant_percent"
    })

    totals = stats[["region_key", "region_total_population"]].drop_duplicates()

    diversity = (
        stats.groupby("region_key")
        .apply(shannon_diversity, include_groups=False)
        .reset_index(name="diversity_index")
    )

    summary = dominant.merge(totals, on="region_key", how="left")
    summary = summary.merge(diversity, on="region_key", how="left")

    merged = regions.merge(summary, on="region_key", how="left")

    merged.to_file(OUT / "regions.geojson", driver="GeoJSON")
    stats.to_json(OUT / "ethnicity_stats.json", orient="records", force_ascii=False)

    print("Wrote data/processed/kyrgyzstan/regions.geojson")
    print("Wrote data/processed/kyrgyzstan/ethnicity_stats.json")

if __name__ == "__main__":
    main()