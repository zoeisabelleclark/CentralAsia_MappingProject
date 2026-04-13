from pathlib import Path
import geopandas as gpd
import re
import unicodedata

INFILE = Path("data/raw/uzbekistan/boundaries/uz.json")
OUTFILE = Path("data/interim/uzbekistan/uz_regions.json")

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

    # Change these to match your actual raw columns
    id_col = "id"
    name_col = "name"

    gdf = gdf[[id_col, name_col, "geometry"]].copy()
    gdf = gdf.rename(columns={id_col: "source_id", name_col: "region_name"})

    gdf["source_id"] = gdf["source_id"].astype(str).str.strip()
    gdf["region_name"] = gdf["region_name"].astype(str).str.strip()

    # Fix ambiguous Tashkent names using the source ID
    gdf.loc[gdf["source_id"] == "UZTO", "region_name"] = "Tashkent region"
    gdf.loc[gdf["source_id"] == "UZTK", "region_name"] = "Tashkent city"

    # # Add any other manual fixes here if needed
    # NAME_FIXES = {
    #     "Karakalpakstan": "Republic of Karakalpakstan",
    # }
    # gdf["region_name"] = gdf["region_name"].replace(NAME_FIXES)

    gdf["country"] = "Uzbekistan"
    gdf["region_key"] = "UZB_" + gdf["region_name"].apply(slugify)

    # Optional explicit overrides if you want total control
    gdf.loc[gdf["source_id"] == "UZTO", "region_key"] = "UZB_TASHKENT"
    gdf.loc[gdf["source_id"] == "UZTK", "region_key"] = "UZB_TASHKENT_CITY"

    print(gdf[["source_id", "region_name", "region_key"]].sort_values("region_name").to_string(index=False))

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(OUTFILE, driver="GeoJSON")
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()