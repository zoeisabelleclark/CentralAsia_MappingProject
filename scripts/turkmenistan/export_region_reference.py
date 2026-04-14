from pathlib import Path
import geopandas as gpd

INFILE = Path("data/interim/turkmenistan/turkmenistan_regions.geojson")
OUTFILE = Path("data/interim/turkmenistan/region_reference.csv")

def main():
    gdf = gpd.read_file(INFILE)
    df = gdf[["region_key", "region_name", "country"]].drop_duplicates().sort_values("region_name")
    df.to_csv(OUTFILE, index=False)
    print(df.to_string(index=False))
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()