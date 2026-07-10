"""
ForgeIQ Procurement Generator
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
INVENTORY_DIR = BASE_DIR / "data" / "raw" / "inventory"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "procurement"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Metadata
# ---------------------------------------------------------

with open(METADATA_DIR / "suppliers.json") as f:
    suppliers = json.load(f)

materials = pd.read_csv(
    INVENTORY_DIR / "materials.csv"
)

inventory = pd.read_csv(
    INVENTORY_DIR / "inventory.csv"
)

# ---------------------------------------------------------
# Suppliers
# ---------------------------------------------------------

suppliers_df = pd.DataFrame(suppliers)

suppliers_df.to_csv(
    OUTPUT_DIR / "suppliers.csv",
    index=False
)

print("suppliers.csv created")

# ---------------------------------------------------------
# Purchase Orders
# ---------------------------------------------------------

purchase_orders = []

order_number = 1

for _, item in inventory.iterrows():

    orders_for_material = random.randint(40, 80)

    for _ in range(orders_for_material):

        supplier = random.choice(suppliers)

        purchase_orders.append(
            {
                "purchase_order_id": f"PO{order_number:06}",
                "supplier_id": supplier["supplier_id"],
                "supplier_name": supplier["supplier_name"],
                "material_id": item["material_id"],
                "warehouse_id": item["warehouse_id"],
                "order_quantity": random.randint(500, 3000),
                "status": random.choice(
                    [
                        "Delivered",
                        "In Transit",
                        "Pending"
                    ]
                )
            }
        )

        order_number += 1

purchase_orders_df = pd.DataFrame(
    purchase_orders
)

purchase_orders_df.to_csv(
    OUTPUT_DIR / "purchase_orders.csv",
    index=False
)

print("purchase_orders.csv created")

# ---------------------------------------------------------
# Purchase Order Items
# ---------------------------------------------------------

purchase_items = []

item_number = 1

for _, po in purchase_orders_df.iterrows():

    unit_price = round(
        random.uniform(50, 1200),
        2
    )

    total_cost = round(
        po["order_quantity"] * unit_price,
        2
    )

    purchase_items.append(
        {
            "purchase_order_item_id":
                f"POI{item_number:07}",
            "purchase_order_id":
                po["purchase_order_id"],
            "material_id":
                po["material_id"],
            "quantity":
                po["order_quantity"],
            "unit_price":
                unit_price,
            "total_cost":
                total_cost
        }
    )

    item_number += 1

purchase_items_df = pd.DataFrame(
    purchase_items
)

purchase_items_df.to_csv(
    OUTPUT_DIR / "purchase_order_items.csv",
    index=False
)

print("purchase_order_items.csv created")


print()

print("======================================")
print("ForgeIQ Procurement Module")
print("======================================")

print(f"Suppliers              : {len(suppliers_df)}")
print(f"Purchase Orders        : {len(purchase_orders_df)}")
print(f"Purchase Order Items   : {len(purchase_items_df)}")