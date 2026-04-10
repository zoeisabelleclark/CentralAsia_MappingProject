from pathlib import Path
import geopandas as gpd
import pandas as pd
import re
import unicodedata

INFILE = Path("data/raw/kyrgyzstan/boundaries/kg.json")
OUTFILE = Path("data/interim/kyrgyzstan/kg_regions.json")

def slugify(text: str) -> str:
    text = str(text).strip()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text

def main():
    gdf = gpd.read_file(INFILE)

    source_name_col = "name"

    gdf = gdf[[source_name_col, "geometry"]].copy()
    gdf["region_name"] = gdf[source_name_col].astype(str).str.strip()

    # make display names nicer
    gdf["region_name"] = gdf["region_name"].str.replace(r"([a-z])([A-Z])", r"\1 \2", regex=True)
    gdf["region_key"] = "KGZ_" + gdf["region_name"].apply(slugify)
    gdf["country"] = "Kyrgyzstan"

    print(gdf[["region_name", "region_key"]])

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(OUTFILE, driver="GeoJSON")
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()