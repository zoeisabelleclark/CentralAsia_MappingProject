from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/turkmenistan/census/urban_rural.csv")
OUTFILE = Path("data/interim/turkmenistan/urban_rural_long.csv")

def clean_number(val):
    if pd.isna(val):
        return None
    val = str(val).strip().replace(",", "").replace(" ", "")
    if val == "":
        return None
    return pd.to_numeric(val, errors="coerce")

def main():
    df = pd.read_csv(INFILE)

    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={
        "region": "region_name",
        "urban": "urban_population",
        "rural": "rural_population",
    })

    df = df[["region_name", "urban_population", "rural_population"]].copy()

    df["region_name"] = df["region_name"].astype(str).str.strip()
    df["urban_population"] = df["urban_population"].apply(clean_number)
    df["rural_population"] = df["rural_population"].apply(clean_number)

    # Save national total separately
    national = df[df["region_name"] == "Turkmenistan"].copy()
    national.to_csv("data/interim/turkmenistan/turkmenistan_national_urban_rural.csv", index=False)

    # Keep only regional rows
    df = df[df["region_name"] != "Turkmenistan"].copy()

    df["total_population"] = df["urban_population"] + df["rural_population"]
    df["urban_percent"] = df["urban_population"] / df["total_population"] * 100
    df["rural_percent"] = df["rural_population"] / df["total_population"] * 100
    df["country"] = "Turkmenistan"

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTFILE, index=False)

    print(df.to_string(index=False))
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()