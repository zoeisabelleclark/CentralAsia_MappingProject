from pathlib import Path
import pandas as pd

INFILE = Path("data/interim/turkmenistan/urban_rural_long.csv")
CROSSWALK_FILE = Path("data/raw/turkmenistan/reference/region_crosswalk.csv")
OUTFILE = Path("data/interim/turkmenistan/urban_rural_clean.csv")

def main():
    df = pd.read_csv(INFILE)
    crosswalk = pd.read_csv(CROSSWALK_FILE)

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    crosswalk.columns = [c.strip().lower().replace(" ", "_") for c in crosswalk.columns]

    df["region_name"] = df["region_name"].astype(str).str.strip()
    crosswalk["source_region_name"] = crosswalk["source_region_name"].astype(str).str.strip()
    crosswalk["region_key"] = crosswalk["region_key"].astype(str).str.strip()

    for col in ["urban_population", "rural_population", "total_population", "urban_percent", "rural_percent"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.merge(
        crosswalk[["source_region_name", "region_key"]],
        left_on="region_name",
        right_on="source_region_name",
        how="left"
    )

    unmatched = sorted(df.loc[df["region_key"].isna(), "region_name"].dropna().unique())
    if unmatched:
        print("\nUnmatched region names:")
        for name in unmatched:
            print("-", name)
        raise ValueError("Some Turkmenistan region names are missing from the crosswalk.")

    df = df.drop(columns=["source_region_name"])
    df.to_csv(OUTFILE, index=False)

    print(f"Wrote {OUTFILE}")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()