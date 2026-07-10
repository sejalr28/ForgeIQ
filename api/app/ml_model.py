from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parents[2]

model = joblib.load(
    BASE_DIR / "ml" / "saved_models" / "failure_model.pkl"
)