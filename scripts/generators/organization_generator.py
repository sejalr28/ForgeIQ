"""
ForgeIQ Organization Generator
"""

import json
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

METADATA_DIR = BASE_DIR / "data" / "metadata"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "organization"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Load Metadata
# ---------------------------------------------------------

with open(METADATA_DIR / "factory_layout.json", "r") as f:
    factory_layout = json.load(f)

with open(METADATA_DIR / "departments.json", "r") as f:
    departments = json.load(f)


# ---------------------------------------------------------
# Generate Factories
# ---------------------------------------------------------

factories = []

for factory in factory_layout["factories"]:

    factories.append(
        {
            "factory_id": factory["factory_id"],
            "factory_name": factory["factory_name"],
            "city": factory["city"],
            "country": "India",
            "plant_type": "Manufacturing",
            "status": "Active"
        }
    )

factories_df = pd.DataFrame(factories)

factories_df.to_csv(
    OUTPUT_DIR / "factories.csv",
    index=False
)

print("factories.csv created")


# ---------------------------------------------------------
# Generate Departments
# ---------------------------------------------------------

departments_df = pd.DataFrame(departments)

departments_df.to_csv(
    OUTPUT_DIR / "departments.csv",
    index=False
)

print("departments.csv created")


# ---------------------------------------------------------
# Generate Production Lines
# ---------------------------------------------------------

production_lines = []

for factory in factory_layout["factories"]:

    for line in factory["production_lines"]:

        production_lines.append(
            {
                "line_id": line["line_id"],
                "factory_id": factory["factory_id"],
                "line_name": line["line_name"],
                "product_family": line["product"],
                "daily_capacity": line["daily_capacity"],
                "operators": line["operators"],
                "supervisors": line["supervisors"],
                "shift_pattern": "A/B/C",
                "status": "Active"
            }
        )

production_lines_df = pd.DataFrame(production_lines)

production_lines_df.to_csv(
    OUTPUT_DIR / "production_lines.csv",
    index=False
)

print("production_lines.csv created")


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("\n--------------------------------------")
print("Organization data generated successfully")
print("--------------------------------------")
print(f"Factories         : {len(factories_df)}")
print(f"Departments       : {len(departments_df)}")
print(f"Production Lines  : {len(production_lines_df)}")