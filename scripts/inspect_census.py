from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/census/kazakhstan_ethnicity.csv")

df = pd.read_csv(INFILE)

print("\nColumns:")
print(list(df.columns))

print("\nFirst rows:")
print(df.head())

print("\nUnique region names:")
for r in sorted(df["region_name"].dropna().astype(str).str.strip().unique()):
    print("-", r)

print("\nUnique ethnicities:")
for l in sorted(df["ethnicity"].dropna().astype(str).str.strip().unique()):
    print("-", l)