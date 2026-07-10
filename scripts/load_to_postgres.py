"""
ForgeIQ PostgreSQL Data Loader
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DB_USER = "postgres"
DB_PASSWORD = "postgres123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "forgeiq_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)



BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "raw"

# ---------------------------------------------------------
# Helper Function
# ---------------------------------------------------------

def load_csv(folder, filename, table_name):

    file_path = DATA_DIR / folder / filename

    print(f"Loading {filename} -> {table_name}")

    df = pd.read_csv(file_path)

    df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

    print(f"Loaded {len(df)} rows")

# =========================================================
# Organization
# =========================================================

load_csv("organization", "factories.csv", "factories")
load_csv("organization", "departments.csv", "departments")
load_csv("organization", "production_lines.csv", "production_lines")

# =========================================================
# Workforce
# =========================================================

load_csv("workforce", "roles.csv", "roles")
load_csv("workforce", "employees.csv", "employees")
load_csv("workforce", "shifts.csv", "shifts")
load_csv("workforce", "employee_shift_assignments.csv", "employee_shift_assignments")

# =========================================================
# Manufacturing
# =========================================================

load_csv("manufacturing", "machines.csv", "machines")
load_csv("manufacturing", "products.csv", "products")
load_csv("manufacturing", "production_orders.csv", "production_orders")
load_csv("manufacturing", "production_records.csv", "production_records")
load_csv("manufacturing", "machine_status.csv", "machine_status")

# =========================================================
# Inventory
# =========================================================

load_csv("inventory", "materials.csv", "materials")
load_csv("inventory", "warehouses.csv", "warehouses")
load_csv("inventory", "inventory.csv", "inventory")
load_csv("inventory", "stock_movements.csv", "stock_movements")

# =========================================================
# Procurement
# =========================================================

load_csv("procurement", "suppliers.csv", "suppliers")
load_csv("procurement", "purchase_orders.csv", "purchase_orders")
load_csv("procurement", "purchase_order_items.csv", "purchase_order_items")

# =========================================================
# Quality
# =========================================================

load_csv("quality", "quality_inspections.csv", "quality_inspections")
load_csv("quality", "defects.csv", "defects")

# =========================================================
# Energy
# =========================================================

load_csv("energy", "energy_meters.csv", "energy_meters")
load_csv("energy", "energy_usage.csv", "energy_usage")

# =========================================================
# Analytics
# =========================================================

load_csv("analytics", "kpis.csv", "kpis")
load_csv("analytics", "forecasts.csv", "forecasts")
load_csv("analytics", "alerts.csv", "alerts")

print("\n===================================")
print("ForgeIQ Data Loaded Successfully")
print("===================================")