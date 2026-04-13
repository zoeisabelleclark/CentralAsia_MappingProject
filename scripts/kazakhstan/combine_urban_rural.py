from pathlib import Path
import pandas as pd

URBAN = Path("data/interim/kazakhstan/urban_long.csv")
RURAL = Path("data/interim/kazakhstan/rural_long.csv")
OUT = Path("data/interim/kazakhstan/urban_rural_combined.csv")

def main():
    urban = pd.read_csv(URBAN)
    rural = pd.read_csv(RURAL)

    df = urban.merge(rural, on=["region_name", "country"], how="inner")

    df["total_population"] = df["urban_population"] + df["rural_population"]
    df["urban_percent"] = df["urban_population"] / df["total_population"] * 100
    df["rural_percent"] = df["rural_population"] / df["total_population"] * 100

    df.to_csv(OUT, index=False)
    print(f"Wrote {OUT}")
    print(df.head().to_string(index=False))

if __name__ == "__main__":
    main()