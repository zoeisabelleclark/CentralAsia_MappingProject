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
    # Load ethnicity + urban data
    ethnicity = pd.read_csv(INTERIM / "census_clean.csv")
    urban = pd.read_csv(INTERIM / "urban_rural_clean.csv")
    regions = gpd.read_file(INTERIM / "kg_regions.json")

    # Clean ethnicity fields
    ethnicity["region_key"] = ethnicity["region_key"].astype(str).str.strip()
    ethnicity["ethnicity"] = ethnicity["ethnicity"].astype(str).str.strip()
    ethnicity["population"] = pd.to_numeric(ethnicity["population"], errors="coerce")
    ethnicity["region_total_population"] = pd.to_numeric(ethnicity["region_total_population"], errors="coerce")
    ethnicity["percent"] = pd.to_numeric(ethnicity["percent"], errors="coerce")

    # Dominant ethnicity
    idx = ethnicity.groupby("region_key")["population"].idxmax()
    dominant = ethnicity.loc[idx, ["region_key", "ethnicity", "population", "percent"]].copy()
    dominant = dominant.rename(columns={
        "ethnicity": "dominant_ethnicity",
        "population": "dominant_population",
        "percent": "dominant_percent",
    })

    totals = ethnicity[["region_key", "region_total_population"]].drop_duplicates()

    # Diversity
    diversity = (
        ethnicity.groupby("region_key")
        .apply(shannon_diversity, include_groups=False)
        .reset_index(name="diversity_index")
    )

    ethnicity_summary = dominant.merge(totals, on="region_key", how="left")
    ethnicity_summary = ethnicity_summary.merge(diversity, on="region_key", how="left")

    # Clean urban fields
    urban["region_key"] = urban["region_key"].astype(str).str.strip()
    for col in ["urban_population", "rural_population", "total_population", "urban_percent", "rural_percent"]:
        if col in urban.columns:
            urban[col] = pd.to_numeric(urban[col], errors="coerce")

    urban_summary = urban[
        ["region_key", "urban_population", "rural_population", "total_population", "urban_percent", "rural_percent"]
    ].copy()

    # Clean boundary fields
    regions["region_key"] = regions["region_key"].astype(str).str.strip()
    if "region_name" in regions.columns:
        regions["region_name"] = regions["region_name"].astype(str).str.strip()

    # Merge everything onto boundaries
    merged = regions.merge(ethnicity_summary, on="region_key", how="left")
    merged = merged.merge(urban_summary, on="region_key", how="left")

    # Write outputs
    merged.to_file(OUT / "regions.geojson", driver="GeoJSON")
    ethnicity.to_json(OUT / "ethnicity_stats.json", orient="records", force_ascii=False)
    urban.to_json(OUT / "urban_stats.json", orient="records", force_ascii=False)

    print("Wrote data/processed/kyrgyzstan/regions.geojson")
    print("Wrote data/processed/kyrgyzstan/ethnicity_stats.json")
    print("Wrote data/processed/kyrgyzstan/urban_stats.json")

if __name__ == "__main__":
    main()