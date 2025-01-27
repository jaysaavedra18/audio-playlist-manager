import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def analyze_audio(audio_path: str) -> np.ndarray:
    """Analyze an audio file and extract its properties."""
    # Load an audio file
    y, sr = librosa.load(audio_path, sr=None)
    # Extract tempo and bpm
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    # RMS energy is a measure of the audio signal's strength, calculate the avg loudness.
    loudness = librosa.feature.rms(y=y).mean()
    # MFCCs capture the song's timbre and spectral texture, summarizing its tonal qualities over time.
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    # Chroma features capture the harmonic content of the audio signal.
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    # Onset detection shows when musical events occur in the audio signal.
    avg_interval, std_interval = analyze_onset_intervals(y, sr)

    # Build a feature vector by flattening the analysis results
    features = np.concatenate([
        np.mean(mfccs, axis=1),
        np.mean(chroma, axis=1),
        tempo,
        [loudness],
        [avg_interval, std_interval],
    ])

    return features

def print_features(features: np.ndarray) -> None:
    """Print the extracted features of an audio file."""
    print(f"Estimated tempo: {features[-4]} BPM")
    print(f"Average loudness: {features[-3]}")
    print(f"Average onset interval: {features[-2]:.2f} s")
    print(f"Standard deviation of onset intervals: {features[-1]:.2f} s")

def analyze_onset_intervals(y: np.ndarray, sr: int):
    # Onset detection shows when musical events occur in the audio signal.
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    intervals = np.diff(onset_times)
    avg_interval = np.mean(intervals) if len(intervals) > 0 else 0
    std_interval = np.std(intervals) if len(intervals) > 0 else 0
    return avg_interval, std_interval


def plot_waveform(y: np.ndarray, sr: int) -> None:
    """Plot the waveform of an audio signal."""
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()

def plot_spectogram(y: np.ndarray, sr: int) -> None:
    """Plot the spectrogram of an audio signal."""
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max), sr=sr, y_axis='mel', x_axis='time')
    plt.colorbar(format="%+2.0d dB")
    plt.title("Mel Spectogram")
    plt.show()

def plot_loudness(rms, sr: int) -> None:
    """Plot the loudness of an audio signal over time."""
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(rms[0], sr=sr)
    plt.title("Loudness (RMS) Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("RMS Energy")
    plt.show()


features = analyze_audio("/Users/saavedj/Downloads/music/misc/16.mp3")
print_features(features)