import random
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

MANUFACTURING_DIR = BASE_DIR / "data" / "raw" / "manufacturing"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "energy"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Machines
# ---------------------------------------------------------

machines = pd.read_csv(
    MANUFACTURING_DIR / "machines.csv"
)

# ---------------------------------------------------------
# Energy Meters
# ---------------------------------------------------------

meters = []

for index, row in machines.iterrows():

    meters.append(
        {
            "meter_id": f"EM{index+1:04}",
            "machine_id": row["machine_id"],
            "meter_type": "Electricity"
        }
    )

meters_df = pd.DataFrame(meters)

meters_df.to_csv(
    OUTPUT_DIR / "energy_meters.csv",
    index=False
)

print("energy_meters.csv created")

# ---------------------------------------------------------
# Energy Usage
# ---------------------------------------------------------

usage = []

for index, row in meters_df.iterrows():

    usage.append(
        {
            "usage_id": f"EU{index+1:05}",
            "meter_id": row["meter_id"],
            "energy_consumption_kwh": round(random.uniform(50, 500), 2),
            "operating_hours": random.randint(6, 24),
            "energy_cost_inr": round(random.uniform(500, 6000), 2)
        }
    )

usage_df = pd.DataFrame(usage)

usage_df.to_csv(
    OUTPUT_DIR / "energy_usage.csv",
    index=False
)

print("energy_usage.csv created")

print("\nEnergy data generated successfully.")