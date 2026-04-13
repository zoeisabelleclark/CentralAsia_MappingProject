from pathlib import Path
import geopandas as gpd

INFILE = Path("data/interim/uzbekistan/uz_regions.json")
OUTFILE = Path("data/interim/uzbekistan/uzbekistan_region_reference.csv")

def main():
    gdf = gpd.read_file(INFILE)
    cols = [c for c in ["region_key", "region_name", "country"] if c in gdf.columns]
    ref = gdf[cols].drop_duplicates().sort_values("region_name")
    ref.to_csv(OUTFILE, index=False)
    print(ref.to_string(index=False))
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()