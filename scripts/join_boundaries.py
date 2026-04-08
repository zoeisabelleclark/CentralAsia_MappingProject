from pathlib import Path
import pandas as pd
import geopandas as gpd

INTERIM = Path("data/interim")
RAW = Path("data/raw/boundaries")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    stats = pd.read_csv(INTERIM / "census_clean.csv")

    # Replace with actual boundary file
    regions = gpd.read_file(RAW / "regions.geojson")

    regions["region_name"] = regions["region_name"].str.strip()

    # Example aggregation: dominant language by region
    idx = stats.groupby("region_name")["speakers"].idxmax()
    dominant = stats.loc[idx, ["region_name", "language", "speakers", "percent"]]

    merged = regions.merge(dominant, on="region_name", how="left")
    merged.to_file(OUT / "regions.geojson", driver="GeoJSON")

    stats.to_json(OUT / "language_stats.json", orient="records", force_ascii=False)
    print("Wrote processed outputs")

if __name__ == "__main__":
    main()