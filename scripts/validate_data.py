from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

print("=" * 60)
print("ForgeIQ Dataset Validation")
print("=" * 60)

for folder in sorted(RAW_DATA.iterdir()):

    if folder.is_dir():

        print(f"\nModule : {folder.name}")

        for csv_file in sorted(folder.glob("*.csv")):

            df = pd.read_csv(csv_file)

            print(
                f"{csv_file.name:<35}"
                f" Rows : {len(df):<8}"
                f" Columns : {len(df.columns)}"
            )

print("\nValidation completed.")