from pathlib import Path
import geopandas as gpd
import re
import unicodedata

INFILE = Path("data/raw/turkmenistan/boundaries/tm.json")
OUTFILE = Path("data/interim/turkmenistan/turkmenistan_regions.geojson")

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

    # Change these after inspection if needed
    id_col = "id"
    name_col = "name"

    gdf = gdf[[id_col, name_col, "geometry"]].copy()
    gdf = gdf.rename(columns={
        id_col: "source_id",
        name_col: "region_name"
    })

    gdf["source_id"] = gdf["source_id"].astype(str).str.strip()
    gdf["region_name"] = gdf["region_name"].astype(str).str.strip()

    # Optional manual name fixes for display
    NAME_FIXES = {
        
    }
    gdf["region_name"] = gdf["region_name"].replace(NAME_FIXES)

    gdf["country"] = "Tajikistan"
    gdf["region_key"] = "TJK_" + gdf["region_name"].apply(slugify)

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(OUTFILE, driver="GeoJSON")

    print(gdf[["source_id", "region_name", "region_key"]].to_string(index=False))
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()