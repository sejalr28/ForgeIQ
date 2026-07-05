"""
ForgeIQ Inventory Generator
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
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "inventory"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Metadata
# ---------------------------------------------------------

with open(METADATA_DIR / "materials.json") as f:
    materials = json.load(f)

with open(METADATA_DIR / "product_recipes.json") as f:
    product_recipes = json.load(f)

# ---------------------------------------------------------
# Recipe Lookup
# ---------------------------------------------------------


products = pd.read_csv(
    MANUFACTURING_DIR / "products.csv"
)


production_records = pd.read_csv(
    MANUFACTURING_DIR / "production_records.csv"
)

# ---------------------------------------------------------
# Recipe Lookup
# ---------------------------------------------------------

recipe_lookup = {}

for recipe in product_recipes["products"]:
    recipe_lookup[recipe["product_id"]] = recipe



# ---------------------------------------------------------
# Warehouses
# ---------------------------------------------------------

warehouses = [
    {
        "warehouse_id": "WH001",
        "warehouse_name": "Pune Raw Material Warehouse",
        "factory_id": "F001",
        "warehouse_type": "Raw Material"
    },
    {
        "warehouse_id": "WH002",
        "warehouse_name": "Pune Finished Goods Warehouse",
        "factory_id": "F001",
        "warehouse_type": "Finished Goods"
    },
    {
        "warehouse_id": "WH003",
        "warehouse_name": "Nashik Raw Material Warehouse",
        "factory_id": "F002",
        "warehouse_type": "Raw Material"
    },
    {
        "warehouse_id": "WH004",
        "warehouse_name": "Nashik Finished Goods Warehouse",
        "factory_id": "F002",
        "warehouse_type": "Finished Goods"
    }
]

warehouses_df = pd.DataFrame(warehouses)

warehouses_df.to_csv(
    OUTPUT_DIR / "warehouses.csv",
    index=False
)

print("warehouses.csv created")

# ---------------------------------------------------------
# Materials
# ---------------------------------------------------------

materials_df = pd.DataFrame(materials)

materials_df.to_csv(
    OUTPUT_DIR / "materials.csv",
    index=False
)

print("materials.csv created")

# ---------------------------------------------------------
# Inventory
# ---------------------------------------------------------

inventory = []

warehouse_cycle = [
    "WH001",
    "WH003"
]

for index, material in enumerate(materials):

    warehouse = warehouse_cycle[index % 2]

    minimum_stock = random.randint(400, 900)

    maximum_stock = minimum_stock * 3

    current_stock = random.randint(
        minimum_stock,
        maximum_stock
    )

    reorder_level = int(
        minimum_stock * 1.25
    )

    inventory.append(
        {
            "inventory_id": f"INV{index+1:04}",
            "material_id": material["material_id"],
            "material_name": material["material_name"],
            "warehouse_id": warehouse,
            "current_stock": current_stock,
            "minimum_stock": minimum_stock,
            "maximum_stock": maximum_stock,
            "reorder_level": reorder_level,
            "unit": material["unit"]
        }
    )

inventory_df = pd.DataFrame(inventory)

inventory_df.to_csv(
    OUTPUT_DIR / "inventory.csv",
    index=False
)

print("inventory.csv created")

# ---------------------------------------------------------
# Stock Movements
# ---------------------------------------------------------

# ---------------------------------------------------------
# Stock Movements
# ---------------------------------------------------------

stock_movements = []

movement_number = 1

for _, record in production_records.iterrows():

    order_id = int(
        record["production_order_id"].replace("PO", "")
    )

    product_index = (
        order_id - 1
    ) % len(product_recipes["products"])

    recipe = product_recipes["products"][product_index]

    for material in recipe["materials"]:

        consumed = round(
            material["quantity"] *
            record["actual_quantity"],
            2
        )

        stock_movements.append(
            {
                "movement_id": f"SM{movement_number:07}",
                "production_order_id": record["production_order_id"],
                "material_id": material["material_id"],
                "material_name": material["material_name"],
                "movement_type": "Consumption",
                "quantity": consumed,
                "unit": material["unit"]
            }
        )

        movement_number += 1

stock_movements_df = pd.DataFrame(stock_movements)

stock_movements_df.to_csv(
    OUTPUT_DIR / "stock_movements.csv",
    index=False
)

print("stock_movements.csv created")
# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print()

print("======================================")
print("ForgeIQ Inventory Module")
print("======================================")

print(f"Materials         : {len(materials_df)}")
print(f"Warehouses        : {len(warehouses_df)}")
print(f"Inventory Rows    : {len(inventory_df)}")
print(f"Stock Movements   : {len(stock_movements_df)}")