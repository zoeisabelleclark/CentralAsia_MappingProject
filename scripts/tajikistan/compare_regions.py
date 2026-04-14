from pathlib import Path
import pandas as pd
import geopandas as gpd

CENSUS_FILE = Path("data/interim/tajikistan/urban_rural_long.csv")
BOUNDARY_FILE = Path("data/interim/tajikistan/tajikistan_regions.geojson")

def main():
    census = pd.read_csv(CENSUS_FILE)
    boundaries = gpd.read_file(BOUNDARY_FILE)

    census_regions = sorted(census["region_name"].dropna().unique())
    boundary_regions = sorted(boundaries["region_name"].dropna().unique())

    print("\n=== CENSUS REGIONS ===")
    for r in census_regions:
        print("-", r)

    print("\n=== BOUNDARY REGIONS ===")
    for r in boundary_regions:
        print("-", r)

    print("\n=== IN CENSUS BUT NOT IN BOUNDARIES ===")
    for r in sorted(set(census_regions) - set(boundary_regions)):
        print("-", r)

    print("\n=== IN BOUNDARIES BUT NOT IN CENSUS ===")
    for r in sorted(set(boundary_regions) - set(census_regions)):
        print("-", r)

if __name__ == "__main__":
    main()