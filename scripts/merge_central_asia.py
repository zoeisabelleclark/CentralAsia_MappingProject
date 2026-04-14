from pathlib import Path
import pandas as pd
import geopandas as gpd

BASE = Path("data/processed")
OUT = BASE / "central_asia"
OUT.mkdir(parents=True, exist_ok=True)

COUNTRIES = [
    "kazakhstan",
    "kyrgyzstan",
    "uzbekistan",
    "tajikistan",
    "turkmenistan",
]

def main():
    geo_frames = []
    stats_frames = []

    for country in COUNTRIES:
        geo_path = BASE / country / "regions.geojson"
        stats_path = BASE / country / "urban_stats.json"

        gdf = gpd.read_file(geo_path)
        stats = pd.read_json(stats_path)


        keep_geo_cols = [
            c for c in [
                "country",
                "region_key",
                "region_name",
                "urban_population",
                "rural_population",
                "total_population",
                "urban_percent",
                "rural_percent",
                "area_sq_km",
                "population_density",
                "geometry",
            ]
            if c in gdf.columns
        ]

        keep_stats_cols = [
            c for c in [
                "country",
                "region_key",
                "region_name",
                "urban_population",
                "rural_population",
                "total_population",
                "urban_percent",
                "rural_percent",
            ]
            if c in stats.columns
        ]

        gdf = gdf[keep_geo_cols].copy()
        stats = stats[keep_stats_cols].copy()
        print(f"{country}: geo rows={len(gdf)}, stats rows={len(stats)}")

        # Fill country if missing
        if "country" not in gdf.columns:
            gdf["country"] = country.title()
        if "country" not in stats.columns:
            stats["country"] = country.title()

        # Clean text
        for col in ["country", "region_key", "region_name"]:
            if col in gdf.columns:
                gdf[col] = gdf[col].astype(str).str.strip()
            if col in stats.columns:
                stats[col] = stats[col].astype(str).str.strip()

        geo_frames.append(gdf)
        stats_frames.append(stats)

    merged_geo = gpd.GeoDataFrame(
        pd.concat(geo_frames, ignore_index=True),
        geometry="geometry",
        crs=geo_frames[0].crs if geo_frames else None,
    )

    merged_stats = pd.concat(stats_frames, ignore_index=True)

    merged_geo.to_file(OUT / "regions.geojson", driver="GeoJSON")
    merged_stats.to_json(OUT / "urban_stats.json", orient="records", force_ascii=False)

    print(f"Wrote {OUT / 'regions.geojson'}")
    print(f"Wrote {OUT / 'urban_stats.json'}")
    print("\nCountries included:")
    print(merged_geo["country"].value_counts().to_string())

if __name__ == "__main__":
    main()