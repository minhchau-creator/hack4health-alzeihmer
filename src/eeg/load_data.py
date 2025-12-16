import mne
import pandas as pd
from pathlib import Path

def load_raw_eeg(data_root):
    raws = []
    labels = []
    meta = []   # lưu open/close eye

    data_root = Path(data_root)

    participants = pd.read_csv(
        data_root / "participants.tsv",
        sep="\t"
    )

    for _, row in participants.iterrows():
        pid = row["participant_id"]
        label = row["group"]

        eeg_dir = data_root / pid / "eeg"
        if not eeg_dir.exists():
            continue

        # LẤY TẤT CẢ FILE EDF
        edf_files = sorted(eeg_dir.glob("*.edf"))

        for edf_path in edf_files:
            raw = mne.io.read_raw_edf(
                edf_path,
                preload=True,
                verbose=False
            )

            raws.append(raw)
            labels.append(label)

            # metadata: open / close eye
            if "open" in edf_path.name.lower():
                meta.append("open")
            elif "close" in edf_path.name.lower():
                meta.append("close")
            else:
                meta.append("unknown")

    return raws, labels, meta
