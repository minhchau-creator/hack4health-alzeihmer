# src/eeg/preprocess.py
import mne

def preprocess_raw(
    raw,
    l_freq=0.5,
    h_freq=45.0,
    epoch_len=4.0,
    overlap=2.0
):
    """
    Basic EEG preprocessing.
    """
    raw.filter(l_freq, h_freq, verbose=False)
    raw.set_eeg_reference("average", verbose=False)

    epochs = mne.make_fixed_length_epochs(
        raw,
        duration=epoch_len,
        overlap=overlap,
        preload=True,
        verbose=False
    )
    return epochs
