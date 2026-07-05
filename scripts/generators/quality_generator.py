import json
import random
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

METADATA_DIR = BASE_DIR / "data" / "metadata"
MANUFACTURING_DIR = BASE_DIR / "data" / "raw" / "manufacturing"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "quality"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

with open(METADATA_DIR / "defect_categories.json", "r") as f:
    defect_categories = json.load(f)

production_records = pd.read_csv(
    MANUFACTURING_DIR / "production_records.csv"
)

# ---------------------------------------------------------
# Quality Inspections
# ---------------------------------------------------------

inspections = []

for i, row in production_records.iterrows():

    inspections.append(
        {
            "inspection_id": f"QI{i+1:06}",
            "record_id": row["record_id"],
            "inspection_result": random.choices(
                ["Pass", "Fail"],
                weights=[95, 5]
            )[0]
        }
    )

inspection_df = pd.DataFrame(inspections)

inspection_df.to_csv(
    OUTPUT_DIR / "quality_inspections.csv",
    index=False
)

print("quality_inspections.csv created")

# ---------------------------------------------------------
# Defects
# ---------------------------------------------------------

defects = []

defect_no = 1

for inspection in inspections:

    if inspection["inspection_result"] == "Fail":

        defect = random.choice(defect_categories)

        defects.append(
            {
                "defect_id": f"D{defect_no:06}",
                "inspection_id": inspection["inspection_id"],
                "defect_category_id": defect["defect_category_id"],
                "defect_name": defect["defect_name"],
                "severity": defect["severity"]
            }
        )

        defect_no += 1

defects_df = pd.DataFrame(defects)

defects_df.to_csv(
    OUTPUT_DIR / "defects.csv",
    index=False
)

print("defects.csv created")

print("\nQuality data generated successfully.")