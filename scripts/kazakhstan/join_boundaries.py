from pathlib import Path
import math
import pandas as pd
import geopandas as gpd

INTERIM = Path("data/interim")
OUT = Path("data/processed")
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
    regions = gpd.read_file(INTERIM / "kazakhstan_regions.json")

    stats["region_key"] = stats["region_key"].astype(str).str.strip()
    stats["ethnicity"] = stats["ethnicity"].astype(str).str.strip()
    stats["population"] = pd.to_numeric(stats["population"], errors="coerce")

    stats = stats.dropna(subset=["population"])

    regions["region_key"] = regions["region_key"].astype(str).str.strip()
    if "region_name" in regions.columns:
        regions["region_name"] = regions["region_name"].astype(str).str.strip()

    totals = (
        stats.groupby("region_key", as_index=False)["population"]
        .sum()
        .rename(columns={"population": "region_total_population"})
    )

    stats = stats.merge(totals, on="region_key", how="left")
    stats["percent"] = stats["population"] / stats["region_total_population"] * 100

    idx = stats.groupby("region_key")["population"].idxmax()
    dominant = stats.loc[idx, ["region_key", "ethnicity", "population", "percent"]].copy()
    dominant = dominant.rename(columns={
        "ethnicity": "dominant_ethnicity",
        "population": "dominant_population",
        "percent": "dominant_percent"
    })

    diversity = (
        stats.groupby("region_key", as_index=False)
        .apply(shannon_diversity, include_groups=False)
        .reset_index()
    )
    diversity.columns = ["index", "region_key", "diversity_index"]
    diversity = diversity[["region_key", "diversity_index"]]

    summary = dominant.merge(totals, on="region_key", how="left")
    summary = summary.merge(diversity, on="region_key", how="left")

    merged = regions.merge(summary, on="region_key", how="left")

    merged.to_file(OUT / "regions.geojson", driver="GeoJSON")
    stats.to_json(OUT / "ethnicity_stats.json", orient="records", force_ascii=False)

    print("Wrote data/processed/regions.geojson")
    print("Wrote data/processed/ethnicity_stats.json")

if __name__ == "__main__":
    main()