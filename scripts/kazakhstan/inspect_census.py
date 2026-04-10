from pathlib import Path
import pandas as pd

INFILE = Path("data/raw/kyrgyzstan/census/ethnicity_by_region_eng.csv")

def main():
    df = pd.read_csv(INFILE)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 10 rows:")
    print(df.head(10).to_string())

if __name__ == "__main__":
    main()



