from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/kyrgyzstan/census/kyrgyzstan_urban_rural_eng.csv")
OUTDIR = Path("data/interim/kyrgyzstan")
OUTDIR.mkdir(parents=True, exist_ok=True)

def clean_number(val):
    if pd.isna(val):
        return None
    val = str(val).strip().replace(",", "").replace(" ", "")
    return pd.to_numeric(val, errors="coerce")

def main():
    df = pd.read_csv(INFILE)

    df = df.rename(columns={
        "Unnamed: 0": "region_name",
        "население": "total_population",
        "городское": "urban_population",
        "сельское": "rural_population"
    })

    df = df[["region_name", "total_population", "urban_population", "rural_population"]].copy()
    df = df.dropna(how="all")

    df["region_name"] = df["region_name"].astype(str).str.strip()

    for col in ["total_population", "urban_population", "rural_population"]:
        df[col] = df[col].apply(clean_number)

    # Drop blank row and national total
    df = df[df["region_name"] != "nan"]
    df = df[df["region_name"] != ""]
    national = df[df["region_name"] == "Kyrgyzstan"].copy()
    national.to_csv(OUTDIR / "kyrgyzstan_urban_rural_national.csv", index=False)

    regional = df[df["region_name"] != "Kyrgyzstan"].copy()

    regional["urban_percent"] = regional["urban_population"] / regional["total_population"] * 100
    regional["rural_percent"] = regional["rural_population"] / regional["total_population"] * 100
    regional["country"] = "Kyrgyzstan"

    regional.to_csv(OUTDIR / "urban_rural_long.csv", index=False)

    print(f"Wrote {OUTDIR / 'urban_rural_long.csv'}")
    print(f"Wrote {OUTDIR / 'kyrgyzstan_urban_rural_national.csv'}")

if __name__ == "__main__":
    main()