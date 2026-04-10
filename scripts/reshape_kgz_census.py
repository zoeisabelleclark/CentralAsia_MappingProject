from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/kyrgyzstan/census/ethnicity_by_region_eng.csv")
OUTDIR = Path("data/interim/kyrgyzstan")
OUTDIR.mkdir(parents=True, exist_ok=True)

def clean_number(val):
    if pd.isna(val):
        return None
    val = str(val).strip()
    if val in {"", "-", "—"}:
        return 0
    val = val.replace(",", "").replace(" ", "")
    return pd.to_numeric(val, errors="coerce")

def main():
    df = pd.read_csv(INFILE)

    # Rename first column to ethnicity
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "ethnicity"})

    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]

    # Drop fully empty rows
    df = df.dropna(how="all")

    # Clean ethnicity labels
    df["ethnicity"] = df["ethnicity"].astype(str).str.strip()

    # Remove helper/header rows
    df = df[~df["ethnicity"].isin(["", "Including"])]

    # Region columns are everything except ethnicity
    region_cols = [
    c for c in df.columns
    if c not in ["ethnicity", "Kyrgyz Republic"]
]

    # Melt to long
    long_df = df.melt(
        id_vars=["ethnicity"],
        value_vars=region_cols,
        var_name="region_name",
        value_name="population"
    )

    # Clean text
    long_df["region_name"] = long_df["region_name"].astype(str).str.strip()
    long_df["ethnicity"] = long_df["ethnicity"].astype(str).str.strip()

    # Clean numbers
    long_df["population"] = long_df["population"].apply(clean_number)

    # Drop rows where population could not be parsed
    long_df = long_df.dropna(subset=["population"])

    # Add country
    long_df["country"] = "Kyrgyzstan"

    # Save full long table
    long_df.to_csv(OUTDIR / "kyrgyzstan_census_long.csv", index=False)

    # Save totals separately
    totals = long_df[long_df["ethnicity"] == "Whole population"].copy()
    totals = totals.rename(columns={"population": "region_total_population"})
    totals.to_csv(OUTDIR / "kyrgyzstan_region_totals.csv", index=False)

    # Save ethnicity-only table
    ethnicity_only = long_df[long_df["ethnicity"] != "Whole population"].copy()
    ethnicity_only.to_csv(OUTDIR / "kyrgyzstan_ethnicity_long.csv", index=False)

    print("Wrote:")
    print(OUTDIR / "kyrgyzstan_census_long.csv")
    print(OUTDIR / "kyrgyzstan_region_totals.csv")
    print(OUTDIR / "kyrgyzstan_ethnicity_long.csv")

if __name__ == "__main__":
    main()