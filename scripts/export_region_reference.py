from pathlib import Path
import geopandas as gpd

INFILE = Path("data/interim/kazakhstan_regions.json")
OUTFILE = Path("data/interim/kazakhstan_region_reference.csv")

gdf = gpd.read_file(INFILE)
df = gdf[["region_key", "region_name", "country"]].copy()
df = df.sort_values("region_name")

df.to_csv(OUTFILE, index=False)
print(df)
print(f"Wrote {OUTFILE}")