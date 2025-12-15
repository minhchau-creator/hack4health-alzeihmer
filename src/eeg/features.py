# src/eeg/features.py
import numpy as np
import mne
import antropy as ant

def band_power(psds, freqs, fmin, fmax):
    idx = (freqs >= fmin) & (freqs <= fmax)
    return psds[:, :, idx].mean(axis=(1, 2))

def extract_eeg_features(epochs):
    """
    Extract EEG features per epoch.
    """
    psds, freqs = mne.time_frequency.psd_welch(
        epochs,
        fmin=0.5,
        fmax=45,
        verbose=False
    )

    features = {}
    features["delta"] = band_power(psds, freqs, 0.5, 4)
    features["theta"] = band_power(psds, freqs, 4, 8)
    features["alpha"] = band_power(psds, freqs, 8, 13)
    features["beta"]  = band_power(psds, freqs, 13, 30)

    features["theta_alpha_ratio"] = (
        features["theta"] / (features["alpha"] + 1e-6)
    )

    entropy = []
    for ep in epochs.get_data():
        entropy.append(
            np.mean([ant.sample_entropy(ch) for ch in ep])
        )
    features["entropy"] = np.array(entropy)

    return features
