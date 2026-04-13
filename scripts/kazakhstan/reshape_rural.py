from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/kazakhstan/census/kazakhstan_rural.csv")
OUTDIR = Path("data/interim/kazakhstan")
OUTDIR.mkdir(parents=True, exist_ok=True)

def clean_number(val):
    if pd.isna(val):
        return None
    val = str(val).strip().replace(",", "").replace(" ", "")
    return pd.to_numeric(val, errors="coerce")

def main():
    df = pd.read_csv(INFILE)

    df = df[["Rural population", "Unnamed: 1"]].copy()
    df = df.rename(columns={
        "Rural population": "region_name",
        "Unnamed: 1": "rural_population"
    })

    df = df.dropna(how="all")

    df["region_name"] = df["region_name"].astype(str).str.strip()
    df["rural_population"] = df["rural_population"].apply(clean_number)

    df = df[df["region_name"] != "nan"]
    df = df[df["region_name"] != ""]

    national = df[df["region_name"] == "Republic of Kazakhstan"].copy()
    national.to_csv(OUTDIR / "kazakhstan_rural_national.csv", index=False)

    regional = df[df["region_name"] != "Republic of Kazakhstan"].copy()

    regional["country"] = "Kazakhstan"
    regional.to_csv(OUTDIR / "rural_long.csv", index=False)

    print(f"Wrote {OUTDIR / 'rural_long.csv'}")
    print(f"Wrote {OUTDIR / 'kazakhstan_rural_national.csv'}")

if __name__ == "__main__":
    main()