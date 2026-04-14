from pathlib import Path
import pandas as pd

URBAN = Path("data/interim/kazakhstan/urban_long.csv")
RURAL = Path("data/interim/kazakhstan/rural_long.csv")
OUT = Path("data/interim/kazakhstan/urban_rural_combined.csv")

def main():
    urban = pd.read_csv(URBAN)
    rural = pd.read_csv(RURAL)

    # Clean text
    urban["region_name"] = urban["region_name"].astype(str).str.strip()
    rural["region_name"] = rural["region_name"].astype(str).str.strip()

    # Merge ALL urban rows, attach rural where available
    df = urban.merge(
        rural[["region_name", "rural_population"]],
        on="region_name",
        how="left"
    )

    # Missing rural for city-only regions should be zero
    df["rural_population"] = pd.to_numeric(df["rural_population"], errors="coerce").fillna(0)
    df["urban_population"] = pd.to_numeric(df["urban_population"], errors="coerce")

    df["total_population"] = df["urban_population"] + df["rural_population"]
    df["urban_percent"] = df["urban_population"] / df["total_population"] * 100
    df["rural_percent"] = df["rural_population"] / df["total_population"] * 100

    df["country"] = "Kazakhstan"

    df.to_csv(OUT, index=False)
    print(f"Wrote {OUT}")

    print("\nCity rows check:")
    mask = df["region_name"].str.contains("Astana|Almaty|Shymkent", case=False, na=False)
    print(df.loc[mask].to_string(index=False))

if __name__ == "__main__":
    main()