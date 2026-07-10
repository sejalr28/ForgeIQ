"""
ForgeIQ Manufacturing Generator
Part 1
"""

import json
import random
from pathlib import Path
import sys
import pandas as pd



# ---------------------------------------------------------
# Paths
# --------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from config import SIMULATION_DAYS, RANDOM_SEED

random.seed(RANDOM_SEED)


METADATA_DIR = BASE_DIR / "data" / "metadata"
WORKFORCE_DIR = BASE_DIR / "data" / "raw" / "workforce"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "manufacturing"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Blueprint
# ---------------------------------------------------------

with open(METADATA_DIR / "factory_layout.json") as f:
    factory_layout = json.load(f)

with open(METADATA_DIR / "machine_layout.json") as f:
    machine_layout = json.load(f)

with open(METADATA_DIR / "product_recipes.json") as f:
    product_recipes = json.load(f)

employees = pd.read_csv(
    WORKFORCE_DIR / "employees.csv"
)

# ---------------------------------------------------------
# Lookup Dictionaries
# ---------------------------------------------------------

factory_lookup = {}

for factory in factory_layout["factories"]:

    factory_lookup[
        factory["factory_id"]
    ] = factory

recipe_lookup = {}

for recipe in product_recipes["products"]:

    recipe_lookup[
        recipe["product_id"]
    ] = recipe

line_lookup = {}

for factory in factory_layout["factories"]:

    for line in factory["production_lines"]:

        line_lookup[
            line["line_id"]
        ] = line

machine_lookup = {}

for line in machine_layout["production_lines"]:

    machine_lookup[
        line["line_id"]
    ] = line["machines"]

# ---------------------------------------------------------
# Generate Machines
# ---------------------------------------------------------

machines = []

for line in machine_layout["production_lines"]:

    for machine in line["machines"]:

        machines.append(
            {
                "machine_id": machine["machine_id"],
                "machine_name": machine["machine_name"],
                "machine_type": machine["machine_type"],
                "production_line": line["line_id"],
                "power_kw": machine["power_kw"],
                "maintenance_interval_hours":
                    machine["maintenance_interval_hours"],
                "status": "Running"
            }
        )

machines_df = pd.DataFrame(machines)

machines_df.to_csv(
    OUTPUT_DIR / "machines.csv",
    index=False
)

print("machines.csv created")

# ---------------------------------------------------------
# Generate Products
# ---------------------------------------------------------

products = []

for recipe in product_recipes["products"]:

    products.append(
        {
            "product_id": recipe["product_id"],
            "product_name": recipe["product_name"],
            "production_line":
                recipe["production_line"],
            "cycle_time_minutes":
                recipe["cycle_time_minutes"],
            "scrap_rate_percent":
                recipe["scrap_rate_percent"]
        }
    )

products_df = pd.DataFrame(products)

products_df.to_csv(
    OUTPUT_DIR / "products.csv",
    index=False
)

print("products.csv created")

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------




# ---------------------------------------------------------
# Generate Production Orders
# ---------------------------------------------------------

production_orders = []

manufacturing_employees = employees[
    employees["department"] == "Manufacturing"
]

order_number = 1

from config import SIMULATION_DAYS
for day in range(1, SIMULATION_DAYS + 1):

    for recipe in product_recipes["products"]:

        line_id = recipe["production_line"]

        line = line_lookup[line_id]

        factory_id = None

        for factory in factory_layout["factories"]:

            for production_line in factory["production_lines"]:

                if production_line["line_id"] == line_id:

                    factory_id = factory["factory_id"]

        machines_on_line = machine_lookup[line_id]

        machine = random.choice(machines_on_line)

        operators = manufacturing_employees[
            manufacturing_employees["production_line"] == line_id
        ]

        operator = operators.sample(1).iloc[0]

        planned_quantity = random.randint(
            int(line["daily_capacity"] * 0.80),
            line["daily_capacity"]
        )

        production_orders.append(
            {
                "production_order_id": f"PO{order_number:06}",
                "factory_id": factory_id,
                "production_line": line_id,
                "product_id": recipe["product_id"],
                "product_name": recipe["product_name"],
                "machine_id": machine["machine_id"],
                "operator_id": operator["employee_id"],
                "shift": random.choice(["A", "B", "C"]),
                "planned_quantity": planned_quantity,
                "cycle_time_minutes": recipe["cycle_time_minutes"],
                "status": "Completed"
            }
        )

        order_number += 1

production_orders_df = pd.DataFrame(production_orders)

production_orders_df.to_csv(
    OUTPUT_DIR / "production_orders.csv",
    index=False
)

print("production_orders.csv created")


# ---------------------------------------------------------
# Generate Production Records
# ---------------------------------------------------------

production_records = []

record_number = 1

for _, order in production_orders_df.iterrows():

    planned_qty = order["planned_quantity"]

    # Machine health slowly varies
    machine_health = round(random.uniform(82, 99), 2)

    # Downtime increases when health decreases
    downtime = max(
        0,
        int((100 - machine_health) * random.uniform(1.2, 2.0))
    )

    # Runtime depends on cycle time and quantity
    runtime = (
        planned_qty *
        order["cycle_time_minutes"]
    ) + downtime

    # Efficiency depends mostly on machine health
    efficiency = round(
        machine_health - random.uniform(0, 5),
        2
    )

    efficiency = min(max(efficiency, 75), 99)

    # Scrap depends on recipe scrap rate
    recipe = recipe_lookup[order["product_id"]]

    scrap_rate = recipe["scrap_rate_percent"] / 100

    rejected = int(
        planned_qty *
        scrap_rate *
        random.uniform(0.8, 1.3)
    )

    actual = planned_qty - rejected

    production_records.append(
        {
            "record_id": f"PR{record_number:06}",
            "production_order_id": order["production_order_id"],
            "machine_id": order["machine_id"],
            "operator_id": order["operator_id"],
            "planned_quantity": planned_qty,
            "actual_quantity": actual,
            "rejected_quantity": rejected,
            "runtime_minutes": runtime,
            "downtime_minutes": downtime,
            "machine_health": machine_health,
            "efficiency_percent": efficiency
        }
    )

    record_number += 1

production_records_df = pd.DataFrame(
    production_records
)

production_records_df.to_csv(
    OUTPUT_DIR / "production_records.csv",
    index=False
)

print("production_records.csv created")

# ---------------------------------------------------------
# Generate Machine Status History
# ---------------------------------------------------------

# ---------------------------------------------------------
# Generate Machine Status History
# ---------------------------------------------------------

machine_status = []

for day in range(1, SIMULATION_DAYS + 1):

    age_factor = day / SIMULATION_DAYS

    for machine in machines:

        # Runtime
        runtime = random.randint(420, 720)

        utilization = round(
            runtime / 720 * 100,
            2
        )

        # Machine aging
        health = round(
            random.uniform(88, 99)
            - age_factor * random.uniform(8, 20),
            2
        )

        health = max(55, health)

        vibration = round(
            random.uniform(0.8, 2.2)
            + age_factor * random.uniform(0.3, 2.5),
            2
        )

        temperature = round(
            random.uniform(45, 65)
            + age_factor * random.uniform(5, 22),
            1
        )

        power = round(
            machine["power_kw"] *
            random.uniform(0.60, 0.95),
            2
        )

        # -------------------------------------------------
        # Simulate Failure Event
        # -------------------------------------------------

        failure_probability = 0.01

        if health < 80:
            failure_probability += 0.25

        if vibration > 2.8:
            failure_probability += 0.20

        if temperature > 75:
            failure_probability += 0.15

        if utilization > 90:
            failure_probability += 0.10

        failure_event = int(
            random.random() < failure_probability
        )

        machine_status.append(
            {
                "machine_id": machine["machine_id"],
                "day": day,
                "runtime_minutes": runtime,
                "utilization_percent": utilization,
                "health_score": health,
                "temperature_c": temperature,
                "vibration_mm_s": vibration,
                "power_consumption_kw": power,
                "failure_event": failure_event
            }
        )

machine_status_df = pd.DataFrame(machine_status)

machine_status_df.to_csv(
    OUTPUT_DIR / "machine_status.csv",
    index=False
)

print("machine_status.csv created")




print()
print("======================================")
print("ForgeIQ Manufacturing Module")
print("======================================")

print(f"Machines              : {len(machines_df)}")
print(f"Products              : {len(products_df)}")
print(f"Production Orders     : {len(production_orders_df)}")
print(f"Production Records    : {len(production_records_df)}")
print(f"Machine Status Rows   : {len(machine_status_df)}")

print("\nManufacturing module generated successfully.")