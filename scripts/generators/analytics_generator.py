import random
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

MANUFACTURING_DIR = BASE_DIR / "data" / "raw" / "manufacturing"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "analytics"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Production Records
# ---------------------------------------------------------

production = pd.read_csv(
    MANUFACTURING_DIR / "production_records.csv"
)

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

kpis = []

for index, row in production.iterrows():

    kpis.append(
        {
            "kpi_id": f"KPI{index+1:06}",
            "record_id": row["record_id"],
            "production_efficiency": row["efficiency_percent"],
            "machine_utilization": random.randint(70, 98),
            "quality_score": round(random.uniform(90, 100), 2)
        }
    )

kpi_df = pd.DataFrame(kpis)

kpi_df.to_csv(
    OUTPUT_DIR / "kpis.csv",
    index=False
)

print("kpis.csv created")

# ---------------------------------------------------------
# Forecasts
# ---------------------------------------------------------

forecasts = []

for i in range(1, 366):

    forecasts.append(
        {
            "forecast_id": f"FC{i:04}",
            "forecast_day": i,
            "predicted_production": random.randint(3500, 5000),
            "predicted_inventory_demand": random.randint(1200, 2500)
        }
    )

forecast_df = pd.DataFrame(forecasts)

forecast_df.to_csv(
    OUTPUT_DIR / "forecasts.csv",
    index=False
)

print("forecasts.csv created")

# ---------------------------------------------------------
# Alerts
# ---------------------------------------------------------

alerts = []

for i in range(1, 501):

    alerts.append(
        {
            "alert_id": f"ALT{i:05}",
            "alert_type": random.choice(
                [
                    "Low Inventory",
                    "High Energy Consumption",
                    "Production Delay",
                    "Quality Issue"
                ]
            ),
            "priority": random.choice(
                [
                    "Low",
                    "Medium",
                    "High"
                ]
            ),
            "status": random.choice(
                [
                    "Open",
                    "Resolved"
                ]
            )
        }
    )

alerts_df = pd.DataFrame(alerts)

alerts_df.to_csv(
    OUTPUT_DIR / "alerts.csv",
    index=False
)

print("alerts.csv created")

print("\nAnalytics data generated successfully.")