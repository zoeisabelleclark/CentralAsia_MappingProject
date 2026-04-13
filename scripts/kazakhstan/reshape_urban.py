from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/kazakhstan/census/kazakhstan_urban.csv")
OUTDIR = Path("data/interim/kazakhstan")
OUTDIR.mkdir(parents=True, exist_ok=True)

def clean_number(val):
    if pd.isna(val):
        return None
    val = str(val).strip().replace(",", "").replace(" ", "")
    return pd.to_numeric(val, errors="coerce")

def main():
    df = pd.read_csv(INFILE)

    # Keep only the first two useful columns
    df = df[["Urban population", "Unnamed: 1"]].copy()
    df = df.rename(columns={
        "Urban population": "region_name",
        "Unnamed: 1": "urban_population"
    })

    # Drop empty rows
    df = df.dropna(how="all")

    # Clean text + numbers
    df["region_name"] = df["region_name"].astype(str).str.strip()
    df["urban_population"] = df["urban_population"].apply(clean_number)

    # Remove the descriptive row
    df = df[df["region_name"] != "nan"]
    df = df[df["region_name"] != ""]

    # Separate national total if you want it later
    national = df[df["region_name"] == "Republic of Kazakhstan"].copy()
    national.to_csv(OUTDIR / "kazakhstan_urban_national.csv", index=False)

    # Keep only region rows
    regional = df[df["region_name"] != "Republic of Kazakhstan"].copy()

    regional["country"] = "Kazakhstan"
    regional.to_csv(OUTDIR / "urban_long.csv", index=False)

    print(f"Wrote {OUTDIR / 'urban_long.csv'}")
    print(f"Wrote {OUTDIR / 'kazakhstan_urban_national.csv'}")

if __name__ == "__main__":
    main()