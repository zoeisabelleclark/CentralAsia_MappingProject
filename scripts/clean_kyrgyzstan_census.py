from pathlib import Path
import pandas as pd

ETHNICITY_FILE = Path("data/interim/kyrgyzstan/kyrgyzstan_ethnicity_long.csv")
TOTALS_FILE = Path("data/interim/kyrgyzstan/kyrgyzstan_region_totals.csv")
CROSSWALK_FILE = Path("data/raw/kyrgyzstan/reference/kyrgyzstan_region_crosswalk.csv")
OUTFILE = Path("data/interim/kyrgyzstan/census_clean.csv")

def main():
    df = pd.read_csv(ETHNICITY_FILE)
    totals = pd.read_csv(TOTALS_FILE)
    crosswalk = pd.read_csv(CROSSWALK_FILE)

    # Clean text
    for frame in [df, totals, crosswalk]:
        for col in frame.columns:
            if frame[col].dtype == "object":
                frame[col] = frame[col].astype(str).str.strip()

    # Merge in totals
    totals = totals[["region_name", "region_total_population"]].copy()
    df = df.merge(totals, on="region_name", how="left")

    # Merge in region key
    df = df.merge(
        crosswalk[["source_region_name", "region_key"]],
        left_on="region_name",
        right_on="source_region_name",
        how="left"
    )

    unmatched = sorted(df.loc[df["region_key"].isna(), "region_name"].dropna().unique())
    if unmatched:
        print("\nUnmatched region names:")
        for r in unmatched:
            print("-", r)
        raise ValueError("Some Kyrgyzstan region names are missing from the crosswalk.")

    # Calculate percent
    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    df["region_total_population"] = pd.to_numeric(df["region_total_population"], errors="coerce")
    df["percent"] = df["population"] / df["region_total_population"] * 100

    # Drop helper column
    df = df.drop(columns=["source_region_name"])

    df.to_csv(OUTFILE, index=False)
    print(f"Wrote {OUTFILE}")

if __name__ == "__main__":
    main()