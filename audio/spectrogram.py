# audio/spectrogram.py

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_spectrogram(
    wav_path,
    ax=None,
    sr=22050,
    n_fft=1024,
    hop_length=256,
    fmax=8000,
    cmap="viridis",
    title=None,
    show_colorbar=False,
    max_sec=None,  # ✅ 新增参数
):
    """
    Plot log-mel spectrogram for a single audio file.

    Args:
        wav_path (str or Path): path to wav file
        ax (matplotlib axis): optional axis to draw on
        sr (int): target sample rate
        max_sec (float): only load first N seconds
    """

    wav_path = Path(wav_path)

    # ✅ 关键修改
    if max_sec is not None:
        y, sr = librosa.load(wav_path, sr=sr, duration=max_sec)
    else:
        y, sr = librosa.load(wav_path, sr=sr)

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=80,
        fmax=fmax,
        power=2.0,
    )

    log_mel = librosa.power_to_db(mel, ref=np.max)

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 3))

    img = librosa.display.specshow(
        log_mel,
        sr=sr,
        hop_length=hop_length,
        x_axis="time",
        y_axis="mel",
        fmax=fmax,
        cmap=cmap,
        ax=ax,
    )

    if title is not None:
        ax.set_title(title, fontsize=10)

    ax.tick_params(axis="both", labelsize=8)

    if show_colorbar:
        plt.colorbar(img, ax=ax, format="%+2.0f dB")

    return ax
