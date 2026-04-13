from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/uzbekistan/census/uz_pop_rural.csv")
OUTFILE = Path("data/interim/uzbekistan/rural_long.csv")

df = pd.read_csv(INFILE)

df = df[["Code", "Klassifikator_en", "2023"]].copy()

df = df.rename(columns={
    "Klassifikator_en": "region_name",
    "2023": "rural_population"
})

df["region_name"] = df["region_name"].astype(str).str.strip()
df["rural_population"] = pd.to_numeric(df["rural_population"], errors="coerce")

df = df[df["Code"].astype(str).str.len() == 4]
df = df[df["region_name"] != "Republic of Uzbekistan"]

df.to_csv(OUTFILE, index=False)