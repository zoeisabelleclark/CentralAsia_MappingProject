from pathlib import Path
import pandas as pd

INFILE = Path("data/interim/uzbekistan/urban_rural_combined.csv")
CROSSWALK_FILE = Path("data/raw/uzbekistan/reference/uzbekistan_region_crosswalk.csv")
OUTFILE = Path("data/interim/uzbekistan/urban_rural_clean.csv")

def main():
    df = pd.read_csv(INFILE)
    crosswalk = pd.read_csv(CROSSWALK_FILE)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    crosswalk.columns = [c.strip().lower().replace(" ", "_") for c in crosswalk.columns]

    # Clean text fields
    df["region_name"] = df["region_name"].astype(str).str.strip()
    crosswalk["source_region_name"] = crosswalk["source_region_name"].astype(str).str.strip()
    crosswalk["region_key"] = crosswalk["region_key"].astype(str).str.strip()

    # Clean numeric fields
    numeric_cols = ["urban_population", "rural_population", "total_population", "urban_percent"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Optional: add rural percent if not already present
    if "rural_percent" not in df.columns and {"rural_population", "total_population"}.issubset(df.columns):
        df["rural_percent"] = df["rural_population"] / df["total_population"] * 100

    population_cols = ["urban_population", "rural_population", "total_population"]
    for col in population_cols:
        if col in df.columns:
            df[col] = df[col] * 1000

    # Merge crosswalk
    df = df.merge(
        crosswalk[["source_region_name", "region_key"]],
        left_on="region_name",
        right_on="source_region_name",
        how="left"
    )

    # Validate unmatched rows
    unmatched = sorted(df.loc[df["region_key"].isna(), "region_name"].dropna().unique())
    if unmatched:
        print("\nUnmatched region names:")
        for name in unmatched:
            print("-", name)
        raise ValueError("Some Uzbekistan region names are missing from the crosswalk.")

    # Drop helper column
    df = df.drop(columns=["source_region_name"])

    # Keep a clean column order
    preferred_order = [
        "country",
        "region_key",
        "region_name",
        "urban_population",
        "rural_population",
        "total_population",
        "urban_percent",
        "rural_percent",
    ]
    cols = [c for c in preferred_order if c in df.columns] + [c for c in df.columns if c not in preferred_order]
    df = df[cols]

    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTFILE, index=False)

    print(f"Wrote {OUTFILE}")
    print("\nPreview:")
    print(df.head().to_string(index=False))

if __name__ == "__main__":
    main()