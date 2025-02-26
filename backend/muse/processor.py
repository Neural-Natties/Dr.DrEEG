import numpy as np
from pylsl import StreamInlet, resolve_byprop
from ml.features import extract_eeg_features


class MuseProcessor:
    def __init__(self):
        self.inlet = self._connect_muse()
        self.buffer_size = 256 * 5  # 5 seconds of data at 256Hz
        self.eeg_buffer = np.zeros((self.buffer_size, 5))

    def _connect_muse(self):
        streams = resolve_byprop("type", "EEG", timeout=2)
        if not streams:
            raise RuntimeError("No Muse stream found!")
        return StreamInlet(streams[0])

    async def get_eeg_features(self):
        chunk, _ = self.inlet.pull_chunk()
        if chunk:
            chunk_array = np.array(chunk)
            self.eeg_buffer = np.roll(self.eeg_buffer, -len(chunk_array), axis=0)
            self.eeg_buffer[-len(chunk_array) :] = chunk_array
            return extract_eeg_features(self.eeg_buffer)
        return None
