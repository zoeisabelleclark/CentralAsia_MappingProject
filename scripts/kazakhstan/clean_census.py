from pathlib import Path
import pandas as pd

RAW = Path("data/raw/census")
REF = Path("data/raw/reference")
OUT = Path("data/interim")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    # Load reshaped census data
    df = pd.read_csv(OUT / "kazakhstan_census_long.csv")

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Basic cleaning
    df["region_name"] = df["region_name"].astype(str).str.strip()
    df["ethnicity"] = df["ethnicity"].astype(str).str.strip()

    # Check expected columns
    required = ["region_name", "ethnicity", "population"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Load crosswalk
    crosswalk = pd.read_csv(REF / "kazakhstan_region_crosswalk.csv")
    crosswalk.columns = [c.strip().lower().replace(" ", "_") for c in crosswalk.columns]

    crosswalk["source_region_name"] = crosswalk["source_region_name"].astype(str).str.strip()
    crosswalk["region_key"] = crosswalk["region_key"].astype(str).str.strip()

    # Merge crosswalk onto census data
    df = df.merge(
        crosswalk[["source_region_name", "region_key"]],
        left_on="region_name",
        right_on="source_region_name",
        how="left"
    )

    # Report anything that did not match
    unmatched = sorted(df.loc[df["region_key"].isna(), "region_name"].dropna().unique())
    if unmatched:
        print("\nUnmatched region names:")
        for name in unmatched:
            print("-", name)
        raise ValueError("Some region names are missing from the crosswalk.")

    # Drop helper column from the crosswalk
    df = df.drop(columns=["source_region_name"])

    # Optional: add country
    df["country"] = "Kazakhstan"

    # Save cleaned output
    df.to_csv(OUT / "census_clean.csv", index=False)
    print("Wrote data/interim/census_clean.csv")

if __name__ == "__main__":
    main()