import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier


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
    "avg_downtime",
]

X = df[features]
y = df["failure"]

# ---------------------------------------------------------
# Train/Test Split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# ---------------------------------------------------------
# Models
# ---------------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
    ),

    "XGBoost": XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
    ),
}

# ---------------------------------------------------------
# Train & Compare
# ---------------------------------------------------------

results = []

best_model = None
best_name = ""
best_f1 = 0

print("\n==============================")
print("Model Comparison")
print("==============================")

for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc = roc_auc_score(y_test, predictions)

    print(f"\n{name}")
    print("-" * len(name))
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC AUC  : {roc:.4f}")

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "ROC_AUC": roc,
    })

    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_name = name

# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

results_df = pd.DataFrame(results)

print("\n==============================")
print("Summary")
print("==============================")

print(results_df)

# ---------------------------------------------------------
# Save Best Model
# ---------------------------------------------------------

joblib.dump(
    best_model,
    "ml/saved_models/failure_model.pkl"
)

print(f"\nBest Model : {best_name}")
print("Model saved successfully.")