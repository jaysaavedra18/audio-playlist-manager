import librosa
import librosa.display
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
    # Chroma features capture the harmonic content of a song, indicating its musical key.
    chroma, chroma_cens, chroma_cqt, chroma_stft = analyze_chroma(y, sr)
    # Onset detection shows when musical events occur in the audio signal.
    avg_interval, std_interval = analyze_onset_intervals(y, sr)
    # Zero crossing rate is the rate of sign changes along a signal.
    zcr = librosa.feature.zero_crossing_rate(y=y)
    # Spectral rolloff distinguishes between harmonic and percussive components of a signal.
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    # Spectral flatness measures the noisiness of a signal.
    spectral_flatness = librosa.feature.spectral_flatness(y=y)
    # Spectral contrast measures the difference in amplitude between peaks and valleys in a signal.
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    # Spectral bandwidth measures the width of the frequency range in which a signal's energy is concentrated.
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    # Spectral centroid indicates the "center of mass" of the frequency distribution.
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    # Harmonic-to-Noise Ratio (HNR) measures the ratio of harmonic content to noise. (Music vs. Speech)
    harmonics, percussive = librosa.effects.harmonic(y=y)
    hnr = np.mean(harmonics) / np.mean(y)
    # Tonnetz features capture tonal content in music.
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

    # Return a feature vector by flattening the analysis results
    return np.concatenate(
        [
            np.mean(mfccs, axis=1),  # Spectral properties and timbre of the song
            np.mean(
                chroma,
                axis=1,
            ),  # Harmonic content, indicates musical key, of the song
            tempo,  # Speed or rhythm of the song, BPM
            [loudness],  # Average loudness of the song
            [avg_interval, std_interval],  # Average gap between musical events
        ],
    )


def analyze_onset_intervals(y: np.ndarray, sr: int) -> tuple:
    """Analyze the intervals between musical onsets in an audio signal."""
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    intervals = np.diff(onset_times)
    avg_interval = np.mean(intervals) if len(intervals) > 0 else 0
    std_interval = np.std(intervals) if len(intervals) > 0 else 0
    return avg_interval, std_interval


def analyze_chroma(y: np.ndarray, sr: int) -> tuple:
    """Analyze the chroma features of an audio signal."""
    # Chroma features capture the harmonic content of the audio signal.
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    # Chroma cens captures the tonal content of the audio signal.
    chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
    # Chroma cqt captures the tonal content of the audio signal.
    chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
    # Chroma stft represents the energy content of different pitches in the audio signal.
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    return chroma, chroma_cens, chroma_cqt, chroma_stft


def print_features(features: np.ndarray) -> None:
    """Print the extracted features of an audio file."""
    # MFCCs (13 values)
    print("\nMFCCs (Mean):")
    for i, mfcc in enumerate(features[:13]):
        print(f"MFCC {i + 1}: {mfcc:.2f}")

    # Chroma Features (12 values)
    print("\nChroma Features (Mean):")
    for i, chroma in enumerate(features[13:25]):
        print(f"Chroma {i + 1}: {chroma:.2f}")

    print(f"\nEstimated Tempo: {features[-4]:.2f} BPM")
    print(f"Average Loudness (RMS): {features[-3]:.2f}")
    print(f"Average Onset Interval: {features[-2]:.2f} seconds")
    print(f"Standard Deviation of Onset Intervals: {features[-1]:.2f} seconds\n")


features = analyze_audio("/Users/saavedj/Downloads/music/misc/16.mp3")
print_features(features)
