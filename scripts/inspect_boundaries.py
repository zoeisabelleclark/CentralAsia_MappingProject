from pathlib import Path
import geopandas as gpd

BOUNDARY_FILE = Path("data/raw/turkmenistan/boundaries/tm.json")

gdf = gpd.read_file(BOUNDARY_FILE)

print("\nColumns:")
print(list(gdf.columns))

print("\nFirst 5 rows:")
print(gdf.head())

print("\nCRS:")
print(gdf.crs)

name_candidates = [c for c in gdf.columns if "name" in c.lower() or "adm" in c.lower()]
print("\nPossible name columns:")
print(name_candidates)

for col in name_candidates:
    print(f"\nUnique values in {col}:")
    vals = gdf[col].dropna().astype(str).unique().tolist()
    for v in vals[:50]:
        print("-", v)