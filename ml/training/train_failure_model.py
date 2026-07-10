import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

df = pd.read_csv("ml/data/ml_dataset.csv")

# ---------------------------------------------------------
# Features
# ---------------------------------------------------------

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
    "avg_downtime"
]

X = df[features]

y = df["failure"]

# ---------------------------------------------------------
# Train Test Split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------------------------------------------------
# Model
# ---------------------------------------------------------

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ---------------------------------------------------------
# Predictions
# ---------------------------------------------------------

predictions = model.predict(X_test)

print()
print("Accuracy")
print(accuracy_score(y_test, predictions))

print()
print(confusion_matrix(y_test, predictions))

print()
print(classification_report(y_test, predictions))

# ---------------------------------------------------------
# Save Model
# ---------------------------------------------------------

joblib.dump(
    model,
    "ml/saved_models/failure_model.pkl"
)

print()
print("Model Saved Successfully")