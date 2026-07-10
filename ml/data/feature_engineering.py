"""
ForgeIQ Feature Engineering Pipeline
"""

import os

import pandas as pd
from sqlalchemy import text,create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


machines = pd.read_sql(
    text("SELECT * FROM machines"),
    engine
)

machine_status = pd.read_sql(
    text("SELECT * FROM machine_status"),
    engine
)

production_records = pd.read_sql(
    text("SELECT * FROM production_records"),
    engine
)

energy_usage = pd.read_sql(
    text("SELECT * FROM energy_usage"),
    engine
)

print("Tables Loaded Successfully")


# Average energy consumed per machine
energy_features = (
    energy_usage
    .groupby("machine_id", as_index=False)
    .agg(
        avg_energy_kwh=("energy_consumed_kwh", "mean")
    )
)

# Average production metrics per machine
production_features = (
    production_records
    .groupby("machine_id", as_index=False)
    .agg(
        avg_efficiency=("efficiency_percent", "mean"),
        avg_rejects=("rejected_quantity", "mean"),
        avg_downtime=("downtime_minutes", "mean")
    )
)

# Merge all tables
dataset = (
    machine_status
    .merge(
        machines,
        on="machine_id",
        how="left"
    )
    .merge(
        production_features,
        on="machine_id",
        how="left"
    )
    .merge(
        energy_features,
        on="machine_id",
        how="left"
    )
)



dataset["failure"] = dataset["failure_event"]

dataset.to_csv(
    "ml/data/ml_dataset.csv",
    index=False
)

print(dataset.head())

print()

print("=================================")
print("ML Dataset Created Successfully")
print("=================================")

print(f"Rows    : {len(dataset)}")
print(f"Columns : {len(dataset.columns)}")