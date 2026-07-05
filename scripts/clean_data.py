from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

for folder in RAW_DATA.iterdir():

    if folder.is_dir():

        for csv in folder.glob("*.csv"):

            csv.unlink()

print("Old CSV files removed.")