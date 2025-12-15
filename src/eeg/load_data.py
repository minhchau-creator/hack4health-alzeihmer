# src/eeg/load.py
import mne

def load_raw_eeg(file_path: str):
    """
    Load raw EEG file.
    """
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    return raw
