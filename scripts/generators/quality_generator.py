"""
ForgeIQ Quality Generator
Part 1
"""

import json
import random
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from config import RANDOM_SEED

random.seed(RANDOM_SEED)

METADATA_DIR = BASE_DIR / "data" / "metadata"
MANUFACTURING_DIR = BASE_DIR / "data" / "raw" / "manufacturing"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "quality"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

production_records = pd.read_csv(
    MANUFACTURING_DIR / "production_records.csv"
)

with open(METADATA_DIR / "defect_categories.json") as f:
    defect_categories = json.load(f)


# ---------------------------------------------------------
# Quality Inspections
# ---------------------------------------------------------

quality_inspections = []

inspection_number = 1

for _, record in production_records.iterrows():

    passed = record["actual_quantity"] - record["rejected_quantity"]

    inspection_result = (
        "PASS"
        if passed >= record["planned_quantity"] * 0.97
        else "FAIL"
    )

    quality_inspections.append(
        {
            "inspection_id": f"QI{inspection_number:06}",
            "production_order_id": record["production_order_id"],
            "machine_id": record["machine_id"],
            "inspected_quantity": record["actual_quantity"],
            "accepted_quantity": passed,
            "rejected_quantity": record["rejected_quantity"],
            "inspection_result": inspection_result
        }
    )

    inspection_number += 1

quality_df = pd.DataFrame(
    quality_inspections
)

quality_df.to_csv(
    OUTPUT_DIR / "quality_inspections.csv",
    index=False
)

print("quality_inspections.csv created")

# ---------------------------------------------------------
# Defects
# ---------------------------------------------------------

defects = []

defect_number = 1

for _, record in production_records.iterrows():

    if record["rejected_quantity"] == 0:
        continue

    category = random.choice(defect_categories)

    defects.append(
    {
        "defect_id": f"DEF{defect_number:06}",
        "production_order_id": record["production_order_id"],
        "machine_id": record["machine_id"],
        "defect_category_id": category["defect_category_id"],
        "defect_name": category["defect_name"],
        "severity": category["severity"],
        "inspection_department": category["inspection_department"],
        "quantity": record["rejected_quantity"]
    }
)

defect_number += 1

defects_df = pd.DataFrame(defects)

defects_df.to_csv(
    OUTPUT_DIR / "defects.csv",
    index=False
)

print("defects.csv created")

print()

print("======================================")
print("ForgeIQ Quality Module")
print("======================================")

print(f"Quality Inspections : {len(quality_df)}")
print(f"Defects             : {len(defects_df)}")