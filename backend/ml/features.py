import numpy as np
from scipy.signal import welch


def extract_eeg_features(eeg_data: np.ndarray, fs: int = 256):
    features = []
    for channel in range(eeg_data.shape[1]):
        freqs, psd = welch(eeg_data[:, channel], fs=fs)

        # Extract frequency bands
        delta = np.mean(psd[(freqs >= 0.5) & (freqs <= 4)])
        theta = np.mean(psd[(freqs >= 4) & (freqs <= 8)])
        alpha = np.mean(psd[(freqs >= 8) & (freqs <= 13)])
        beta = np.mean(psd[(freqs >= 13) & (freqs <= 30)])

        features.extend([delta, theta, alpha, beta])

    return np.array(features)


