from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/uzbekistan/census/uz_pop_urban.csv")
OUTFILE = Path("data/interim/uzbekistan/urban_long.csv")

OUTFILE.parent.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(INFILE)

    # Keep only relevant columns
    df = df[["Code", "Klassifikator_en", "2023"]].copy()

    df = df.rename(columns={
        "Klassifikator_en": "region_name",
        "2023": "urban_population"
    })

    # Clean text
    df["region_name"] = df["region_name"].astype(str).str.strip()

    # Convert numbers
    df["urban_population"] = pd.to_numeric(df["urban_population"], errors="coerce")

    # ❗ Filter to level-1 regions
    # Rule: codes with 4 digits are regions (you may need to tweak this)
    df = df[df["Code"].astype(str).str.len() == 4]

    # Remove national total
    df = df[df["region_name"] != "Republic of Uzbekistan"]

    df.to_csv(OUTFILE, index=False)
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()