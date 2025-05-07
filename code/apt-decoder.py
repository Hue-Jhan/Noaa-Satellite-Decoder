import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert, resample
from PIL import Image

fs, audio = wavfile.read("2025-05-03_10-03-19_2400000SPS_137912500Hz.wav")
audio = audio[:, 0]
audio = resample(audio, int(20800 / fs * len(audio)))
hilb = hilbert(audio)
iq_swapped = np.imag(hilb) + 1j * np.real(hilb)
demod = resample(np.abs(iq_swapped), len(iq_swapped) // 5)
low, high = np.percentile(demod, (5, 95))
normalized = np.round((255 * (demod - low)) / (high - low)).clip(0, 255).astype(np.uint8)

# Synchronization sequence
sync_seq = np.array([0, 0, 255, 255, 0, 0, 255, 255,
                     0, 0, 255, 255, 0, 0, 255, 255,
                     0, 0, 255, 255, 0, 0, 255, 255,
                     0, 0, 255, 255, 0, 0, 0, 0, 0,
                     0, 0, 0]) - 128

rows, stats = [], []
last_corr, last_index = -np.inf, 0
min_sep = 2000

# Identify rows based on sync sequence
for i in range(len(normalized) - len(sync_seq)):
    win = normalized[i:i + len(sync_seq)] - 128
    corr = np.dot(sync_seq, win)
    if i - last_index > min_sep:
        last_index = i
        last_corr = -np.inf
        rows.append(normalized[i:i + 2080])
    elif corr > last_corr and rows:
        last_corr = corr
        last_index = i
        rows[-1] = normalized[i:i + 2080]

valid_rows = [r for r in rows if len(r) == 2080]

if not valid_rows:
    raise ValueError("No valid rows of length 2080 found.")

img = np.vstack(valid_rows).astype(np.uint8)

if img.size == 0:
    raise ValueError("No rows of length 2080 found in the data.")

img_a = img[:, 86:990]
Image.fromarray(img_a).show()
