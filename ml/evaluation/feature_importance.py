import joblib
import pandas as pd

model = joblib.load("ml/saved_models/failure_model.pkl")

features = [
    "runtime_minutes",
    "utilization_percent",
    "health_score",
    "temperature_c",
    "vibration_mm_s",
    "power_consumption_kw",
    "avg_energy_kwh",
    "avg_efficiency",
    "avg_rejects",
    "avg_downtime",
]

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance")
print("===================")
print(importance)