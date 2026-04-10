from pathlib import Path
import pandas as pd

URBAN = Path("data/interim/uzbekistan/urban_long.csv")
RURAL = Path("data/interim/uzbekistan/rural_long.csv")
OUT = Path("data/interim/uzbekistan/urban_rural_combined.csv")

def main():
    urban = pd.read_csv(URBAN)
    rural = pd.read_csv(RURAL)

    df = urban.merge(rural, on="region_name", how="inner")

    df["total_population"] = df["urban_population"] + df["rural_population"]
    df["urban_percent"] = df["urban_population"] / df["total_population"] * 100

    df["country"] = "Uzbekistan"

    df.to_csv(OUT, index=False)
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()