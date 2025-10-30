import os
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

DATA_DIR = r"D:\HeartRiskApp\backend\venv\models\data"

X = np.load(os.path.join(DATA_DIR, "patient_features.npy"))
y = np.load(os.path.join(DATA_DIR, "patient_labels.npy"))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = xgb.XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

os.makedirs(os.path.join(DATA_DIR, "..", "models"), exist_ok=True)
model.save_model(os.path.join(DATA_DIR, "..", "models", "xgboost_model.json"))
print("Model saved ✅")
