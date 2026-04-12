from pathlib import Path
import pandas as pd
import re
import unicodedata

INFILE = Path("data/raw/census/kazakhstan_ethnicity.csv")
OUTFILE = Path("data/interim/kazakhstan_census_long.csv")

def clean_text(text):
    if pd.isna(text):
        return text
    text = str(text).strip()

    # Normalize weird unicode (Cyrillic/Latin mix)
    text = unicodedata.normalize("NFKD", text)

    # Remove weird spacing
    text = re.sub(r"\s+", " ", text)

    return text

def clean_number(val):
    if pd.isna(val):
        return None
    val = str(val)
    val = val.replace(",", "").replace(" ", "")
    return pd.to_numeric(val, errors="coerce")

def main():
    df = pd.read_csv(INFILE)

    # Drop useless column
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Rename for consistency
    df = df.rename(columns={
        "Ethnicities": "ethnicity",
        "Code": "code"
    })

    # Clean ethnicity names
    df["ethnicity"] = df["ethnicity"].apply(clean_text)

    # ❌ Remove totals
    df = df[~df["ethnicity"].str.contains("total", case=False, na=False)]

    # Identify region columns
    region_cols = [c for c in df.columns if c not in ["code", "ethnicity"]]
    region_cols = [c for c in region_cols if c != "Republic of Kazakhstan"]

    # Clean column names (important!)
    clean_cols = {}
    for col in region_cols:
        new_col = clean_text(col)
        clean_cols[col] = new_col

    df = df.rename(columns=clean_cols)
    region_cols = list(clean_cols.values())

    print("\nCleaned region columns:")
    print(region_cols)

    # Melt
    long_df = df.melt(
        id_vars=["code", "ethnicity"],
        value_vars=region_cols,
        var_name="region_name",
        value_name="population"
    )

    # Clean region names again
    long_df["region_name"] = long_df["region_name"].apply(clean_text)

    # Clean numbers
    long_df["population"] = long_df["population"].apply(clean_number)

    # Drop empty
    long_df = long_df.dropna(subset=["population"])

    print("\nPreview:")
    print(long_df.head())

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    long_df.to_csv(OUTFILE, index=False)

    print(f"\nWrote {OUTFILE}")

if __name__ == "__main__":
    main()