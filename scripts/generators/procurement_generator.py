import json
import random
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

METADATA_DIR = BASE_DIR / "data" / "metadata"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "procurement"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Metadata
# ---------------------------------------------------------

with open(METADATA_DIR / "suppliers.json", "r") as f:
    suppliers = json.load(f)

with open(METADATA_DIR / "materials.json", "r") as f:
    materials = json.load(f)

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

for i in range(1, 1001):

    supplier = random.choice(suppliers)

    purchase_orders.append(
        {
            "purchase_order_id": f"PO{i:05}",
            "supplier_id": supplier["supplier_id"],
            "order_status": random.choice(
                [
                    "Ordered",
                    "Delivered",
                    "In Transit"
                ]
            ),
            "lead_time_days": supplier["lead_time_days"]
        }
    )

purchase_orders_df = pd.DataFrame(purchase_orders)

purchase_orders_df.to_csv(
    OUTPUT_DIR / "purchase_orders.csv",
    index=False
)

print("purchase_orders.csv created")

# ---------------------------------------------------------
# Purchase Order Items
# ---------------------------------------------------------

items = []

item_no = 1

for order in purchase_orders:

    total_items = random.randint(2, 5)

    for _ in range(total_items):

        material = random.choice(materials)

        items.append(
            {
                "purchase_order_item_id": f"POI{item_no:06}",
                "purchase_order_id": order["purchase_order_id"],
                "material_id": material["material_id"],
                "quantity": random.randint(100, 2000),
                "unit_price": material["average_unit_cost"]
            }
        )

        item_no += 1

items_df = pd.DataFrame(items)

items_df.to_csv(
    OUTPUT_DIR / "purchase_order_items.csv",
    index=False
)

print("purchase_order_items.csv created")

print("\nProcurement data generated successfully.")