"""
ForgeIQ Workforce Generator
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")
random.seed(42)

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

METADATA_DIR = BASE_DIR / "data" / "metadata"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "workforce"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Metadata
# ---------------------------------------------------------

with open(METADATA_DIR / "factory_layout.json", "r") as f:
    factory_layout = json.load(f)

with open(METADATA_DIR / "departments.json", "r") as f:
    departments = json.load(f)

# ---------------------------------------------------------
# Workforce Distribution
# ---------------------------------------------------------

department_distribution = {
    "Manufacturing": 420,
    "Quality Assurance": 70,
    "Maintenance": 55,
    "Inventory": 30,
    "Procurement": 20,
    "Planning": 15,
    "Engineering": 20,
    "Utilities": 10,
    "Human Resources": 5,
    "Safety": 5
}

department_roles = {
    "Manufacturing": [
        "Operator",
        "Senior Operator",
        "Production Supervisor",
        "Production Manager"
    ],
    "Quality Assurance": [
        "Quality Inspector",
        "Quality Engineer"
    ],
    "Maintenance": [
        "Maintenance Technician",
        "Maintenance Engineer"
    ],
    "Inventory": [
        "Store Executive",
        "Warehouse Supervisor"
    ],
    "Procurement": [
        "Procurement Executive"
    ],
    "Planning": [
        "Production Planner"
    ],
    "Engineering": [
        "Manufacturing Engineer"
    ],
    "Utilities": [
        "Utilities Engineer"
    ],
    "Human Resources": [
        "HR Executive"
    ],
    "Safety": [
        "Safety Officer"
    ]
}

skill_levels = [
    ("Beginner", 2),
    ("Intermediate", 5),
    ("Advanced", 10),
    ("Expert", 18)
]

# ---------------------------------------------------------
# Production Lines
# ---------------------------------------------------------

production_lines = []

for factory in factory_layout["factories"]:
    for line in factory["production_lines"]:
        production_lines.append(
            {
                "factory_id": factory["factory_id"],
                "line_id": line["line_id"]
            }
        )

# ---------------------------------------------------------
# Employees
# ---------------------------------------------------------

employees = []

employee_no = 1

for department, total in department_distribution.items():

    for _ in range(total):

        factory = random.choice(factory_layout["factories"])

        if department == "Manufacturing":
            line = random.choice(factory["production_lines"])
            line_id = line["line_id"]
        else:
            line_id = ""

        skill = random.choices(
            skill_levels,
            weights=[25, 40, 25, 10]
        )[0]

        experience = round(
            random.uniform(0.5, skill[1]),
            1
        )

        joining_date = (
            datetime(2018, 1, 1)
            + timedelta(days=random.randint(0, 2500))
        )

        employees.append(
            {
                "employee_id": f"EMP{employee_no:06}",
                "employee_name": fake.name(),
                "factory_id": factory["factory_id"],
                "department": department,
                "role": random.choice(
                    department_roles[department]
                ),
                "production_line": line_id,
                "joining_date": joining_date.date(),
                "experience_years": experience,
                "skill_level": skill[0]
            }
        )

        employee_no += 1

employees_df = pd.DataFrame(employees)

employees_df.to_csv(
    OUTPUT_DIR / "employees.csv",
    index=False
)

print("employees.csv created")

# ---------------------------------------------------------
# Shift Assignment
# ---------------------------------------------------------

shift_codes = ["A", "B", "C"]

shift_data = []

for employee in employees:

    shift_data.append(
        {
            "employee_id": employee["employee_id"],
            "shift_code": random.choice(shift_codes)
        }
    )

shift_df = pd.DataFrame(shift_data)

shift_df.to_csv(
    OUTPUT_DIR / "employee_shift_assignments.csv",
    index=False
)

print("employee_shift_assignments.csv created")

# ---------------------------------------------------------
# Attendance
# ---------------------------------------------------------

attendance = []

attendance_status = [
    "Present",
    "Sick Leave",
    "Casual Leave",
    "Training"
]

attendance_weights = [95, 2, 2, 1]

today = datetime.today().date()

for employee in employees:

    attendance.append(
        {
            "employee_id": employee["employee_id"],
            "date": today,
            "status": random.choices(
                attendance_status,
                weights=attendance_weights
            )[0]
        }
    )

attendance_df = pd.DataFrame(attendance)

attendance_df.to_csv(
    OUTPUT_DIR / "attendance.csv",
    index=False
)

print("attendance.csv created")

# ---------------------------------------------------------
# Training Records
# ---------------------------------------------------------

training = []

training_courses = [
    "Machine Safety",
    "Lean Manufacturing",
    "Quality Standards",
    "Industrial Automation"
]

for employee in random.sample(employees, 120):

    training.append(
        {
            "employee_id": employee["employee_id"],
            "course_name": random.choice(training_courses),
            "completion_year": random.randint(2023, 2026)
        }
    )

training_df = pd.DataFrame(training)

training_df.to_csv(
    OUTPUT_DIR / "training_records.csv",
    index=False
)

print("training_records.csv created")

# ---------------------------------------------------------
# Leave Records
# ---------------------------------------------------------

leave = []

leave_types = [
    "Casual Leave",
    "Sick Leave",
    "Earned Leave"
]

for employee in random.sample(employees, 150):

    leave.append(
        {
            "employee_id": employee["employee_id"],
            "leave_type": random.choice(leave_types),
            "days": random.randint(1, 5)
        }
    )

leave_df = pd.DataFrame(leave)

leave_df.to_csv(
    OUTPUT_DIR / "leave_records.csv",
    index=False
)

print("leave_records.csv created")

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("\n--------------------------------------")
print("Workforce data generated successfully")
print("--------------------------------------")
print(f"Employees              : {len(employees_df)}")
print(f"Shift Assignments      : {len(shift_df)}")
print(f"Attendance Records     : {len(attendance_df)}")
print(f"Training Records       : {len(training_df)}")
print(f"Leave Records          : {len(leave_df)}")