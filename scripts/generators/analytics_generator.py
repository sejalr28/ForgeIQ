"""
ForgeIQ Analytics Generator
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
QUALITY_DIR = BASE_DIR / "data" / "raw" / "quality"
ENERGY_DIR = BASE_DIR / "data" / "raw" / "energy"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "analytics"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

production = pd.read_csv(
    MANUFACTURING_DIR / "production_records.csv"
)

quality = pd.read_csv(
    QUALITY_DIR / "quality_inspections.csv"
)

energy = pd.read_csv(
    ENERGY_DIR / "energy_usage.csv"
)

# ---------------------------------------------------------
# Daily KPIs
# ---------------------------------------------------------

kpis = []

for day in sorted(energy["day"].unique()):

    day_energy = energy[
        energy["day"] == day
    ]

    production_day = production.iloc[
        (day - 1) * 6 : day * 6
    ]

    total_units = production_day[
        "actual_quantity"
    ].sum()

    rejected = production_day[
        "rejected_quantity"
    ].sum()

    runtime = production_day[
        "runtime_minutes"
    ].sum()

    downtime = production_day[
        "downtime_minutes"
    ].sum()

    total_energy = round(
        day_energy["energy_consumed_kwh"].sum(),
        2
    )

    kpis.append(
        {
            "day": day,
            "production_units": total_units,
            "rejected_units": rejected,
            "runtime_minutes": runtime,
            "downtime_minutes": downtime,
            "energy_kwh": total_energy
        }
    )

kpis_df = pd.DataFrame(kpis)

kpis_df.to_csv(
    OUTPUT_DIR / "kpis.csv",
    index=False
)

print("kpis.csv created")


# ---------------------------------------------------------
# Production Forecast
# ---------------------------------------------------------

forecasts = []

for _, row in kpis_df.iterrows():

    forecast = int(
        row["production_units"] *
        random.uniform(0.97, 1.05)
    )

    forecasts.append(
        {
            "day": row["day"],
            "actual_production": row["production_units"],
            "forecast_production": forecast,
            "forecast_error_percent": round(
                abs(forecast - row["production_units"])
                / row["production_units"] * 100,
                2
            )
        }
    )

forecasts_df = pd.DataFrame(forecasts)

forecasts_df.to_csv(
    OUTPUT_DIR / "forecasts.csv",
    index=False
)

print("forecasts.csv created")

# ---------------------------------------------------------
# Alerts
# ---------------------------------------------------------

alerts = []

alert_number = 1

for _, row in kpis_df.iterrows():

    if row["downtime_minutes"] > 60:

        alerts.append(
            {
                "alert_id": f"ALT{alert_number:05}",
                "day": row["day"],
                "alert_type": "High Downtime",
                "priority": "High"
            }
        )

        alert_number += 1

    if row["rejected_units"] > 20:

        alerts.append(
            {
                "alert_id": f"ALT{alert_number:05}",
                "day": row["day"],
                "alert_type": "High Reject Rate",
                "priority": "Medium"
            }
        )

        alert_number += 1

alerts_df = pd.DataFrame(alerts)

alerts_df.to_csv(
    OUTPUT_DIR / "alerts.csv",
    index=False
)

print("alerts.csv created")


print()

print("======================================")
print("ForgeIQ Analytics Module")
print("======================================")

print(f"KPIs            : {len(kpis_df)}")
print(f"Forecasts       : {len(forecasts_df)}")
print(f"Alerts          : {len(alerts_df)}")