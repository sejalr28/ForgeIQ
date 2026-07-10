"""
ForgeIQ Energy Generator
Part 1
"""

import random
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from config import RANDOM_SEED

random.seed(RANDOM_SEED)

MANUFACTURING_DIR = BASE_DIR / "data" / "raw" / "manufacturing"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "energy"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

machines = pd.read_csv(
    MANUFACTURING_DIR / "machines.csv"
)

machine_status = pd.read_csv(
    MANUFACTURING_DIR / "machine_status.csv"
)


# ---------------------------------------------------------
# Energy Meters
# ---------------------------------------------------------

energy_meters = []

for _, machine in machines.iterrows():

    energy_meters.append(
        {
            "meter_id": f"EM{machine['machine_id']}",
            "machine_id": machine["machine_id"],
            "power_rating_kw": machine["power_kw"]
        }
    )

energy_meters_df = pd.DataFrame(energy_meters)

energy_meters_df.to_csv(
    OUTPUT_DIR / "energy_meters.csv",
    index=False
)

print("energy_meters.csv created")

# ---------------------------------------------------------
# Energy Usage
# ---------------------------------------------------------

energy_usage = []

ELECTRICITY_RATE = 8.50   # ₹ per kWh

for _, status in machine_status.iterrows():

    machine = machines[
        machines["machine_id"] == status["machine_id"]
    ].iloc[0]

    runtime_hours = status["runtime_minutes"] / 60

    energy_consumed = round(
        runtime_hours *
        machine["power_kw"] *
        random.uniform(0.90, 1.05),
        2
    )

    energy_cost = round(
        energy_consumed * ELECTRICITY_RATE,
        2
    )

    energy_usage.append(
        {
            "machine_id": status["machine_id"],
            "day": status["day"],
            "runtime_minutes": status["runtime_minutes"],
            "power_rating_kw": machine["power_kw"],
            "energy_consumed_kwh": energy_consumed,
            "energy_cost_inr": energy_cost
        }
    )

energy_usage_df = pd.DataFrame(
    energy_usage
)

energy_usage_df.to_csv(
    OUTPUT_DIR / "energy_usage.csv",
    index=False
)

print("energy_usage.csv created")


print()

print("======================================")
print("ForgeIQ Energy Module")
print("======================================")

print(f"Energy Meters      : {len(energy_meters_df)}")
print(f"Energy Usage Rows  : {len(energy_usage_df)}")