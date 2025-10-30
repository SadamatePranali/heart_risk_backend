import os
import numpy as np
import pandas as pd
import wfdb
import cv2

# ================================
# Paths
# ================================
# Use absolute path instead of relative
DATA_DIR = r"D:\HeartRiskApp\backend\venv\models\data"

# ================================
# 1. Tabular Heart Disease Data
# ================================
def process_tabular():
    csv_path = os.path.join(DATA_DIR, "heart_disease.csv")
    if not os.path.exists(csv_path):
        print("❌ heart_disease.csv not found in data folder!")
        return

    df = pd.read_csv(csv_path)

    # Expecting columns: age, bp, cholesterol, sugar, target/label
    expected_columns = ["age", "bp", "cholesterol", "sugar"]
    for col in expected_columns:
        if col not in df.columns:
            print(f"❌ Missing column in CSV: {col}")
            return

    features = df[expected_columns].values
    labels = df["target"].values if "target" in df.columns else df["label"].values

    np.save(os.path.join(DATA_DIR, "patient_features.npy"), features)
    np.save(os.path.join(DATA_DIR, "patient_labels.npy"), labels)
    print("✅ Saved patient_features.npy and patient_labels.npy")

# ================================
# 2. ECG MIT-BIH Arrhythmia Data
# ================================
def process_ecg():
    mitbih_dir = os.path.join(DATA_DIR, "mitbih")
    if not os.path.exists(mitbih_dir):
        print("❌ MIT-BIH dataset folder not found in data!")
        return

    all_signals = []
    all_labels = []

    for file in os.listdir(mitbih_dir):
        if file.endswith(".dat"):
            record_id = file.split(".")[0]
            record_path = os.path.join(mitbih_dir, record_id)

            try:
                record = wfdb.rdrecord(record_path)
                annotation = wfdb.rdann(record_path, "atr")

                signals = record.p_signal
                labels = annotation.symbol

                all_signals.append(signals)
                all_labels.append(labels)

            except Exception as e:
                print(f"⚠️ Skipping {record_id}: {e}")

    np.save(os.path.join(DATA_DIR, "ecg_signals.npy"), np.array(all_signals, dtype=object))
    np.save(os.path.join(DATA_DIR, "ecg_labels.npy"), np.array(all_labels, dtype=object))
    print("✅ Saved ecg_signals.npy and ecg_labels.npy")

# ================================
# 3. X-ray Images
# ================================
def process_xrays():
    xray_dir = os.path.join(DATA_DIR, "xray_images")
    if not os.path.exists(xray_dir):
        print("❌ X-ray dataset folder not found!")
        return

    images = []
    labels = []

    categories = {"normal": 0, "pneumonia": 1}

    for category, label in categories.items():
        folder = os.path.join(xray_dir, category)
        if not os.path.exists(folder):
            continue

        for img_name in os.listdir(folder):
            img_path = os.path.join(folder, img_name)

            try:
                # Read image in grayscale
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

                # Skip invalid or hidden files (like ._person123.jpeg)
                if img is None:
                    print(f"⚠️ Skipping invalid file: {img_name}")
                    continue

                # Resize to 128x128
                img = cv2.resize(img, (128, 128))

                # Append to dataset
                images.append(img)
                labels.append(label)

            except Exception as e:
                print(f"⚠️ Could not process {img_name}: {e}")

    # Save arrays
    np.save(os.path.join(DATA_DIR, "xray_images.npy"), np.array(images))
    np.save(os.path.join(DATA_DIR, "xray_labels.npy"), np.array(labels))
    print("✅ Saved xray_images.npy and xray_labels.npy")


# ================================
# Main
# ================================
if __name__ == "__main__":
    print("🚀 Preparing datasets...")

    process_tabular()
    process_ecg()
    process_xrays()

    print("🎉 All datasets converted to .npy successfully!")
