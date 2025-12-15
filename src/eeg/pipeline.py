# src/eeg/pipeline.py
import os
import pandas as pd

from .load_data import load_raw_eeg
from .preprocess import preprocess_raw
from .features import extract_eeg_features

def run_eeg_pipeline(data_dir: str):
    """
    Run EEG feature extraction pipeline.
    """
    all_rows = []

    for label in ["AD", "FTD", "HC"]:
        label_dir = os.path.join(data_dir, label)

        for fname in os.listdir(label_dir):
            if not fname.endswith(".edf"):
                continue

            file_path = os.path.join(label_dir, fname)

            raw = load_raw_eeg(file_path)
            epochs = preprocess_raw(raw)
            feats = extract_eeg_features(epochs)

            n_epochs = len(feats["delta"])
            for i in range(n_epochs):
                row = {k: v[i] for k, v in feats.items()}
                row["label"] = label
                row["subject"] = fname.replace(".edf", "")
                all_rows.append(row)

    return pd.DataFrame(all_rows)
