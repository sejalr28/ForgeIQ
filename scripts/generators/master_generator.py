"""
ForgeIQ Master Data Generator
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

generators = [
    "organization_generator.py",
    "workforce_generator.py",
    "manufacturing_generator.py",
    "inventory_generator.py",
    "procurement_generator.py",
    "quality_generator.py",
    "energy_generator.py",
    "analytics_generator.py",
]

print("=" * 60)
print("ForgeIQ Data Generation Pipeline")
print("=" * 60)

for generator in generators:

    print(f"\nRunning {generator} ...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            f"scripts.generators.{generator[:-3]}"
        ],
        check=True,
    )

print("\nAll datasets generated successfully.")