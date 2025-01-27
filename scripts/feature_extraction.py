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
    chroma, chroma_cens, chroma_cqt, chroma_stft = analyze_chroma_features(y, sr)

    # Onset detection shows when musical events occur in the audio signal.
    avg_interval, std_interval = analyze_onset_intervals(y, sr)

    # Zero crossing rate is the rate of sign changes along a signal.
    zcr = librosa.feature.zero_crossing_rate(y=y).mean()

    # Spectral features capture the frequency content of the audio signal.
    (
        spectral_rolloff,
        spectral_flatness,
        spectral_contrast,
        spectral_bandwidth,
        spectral_centroid,
    ) = analyze_spectral_features(y=y, sr=sr)

    # Harmonic-to-Noise Ratio (HNR) measures the ratio of harmonic content to noise. (Music vs. Speech)
    harmonics = librosa.effects.harmonic(y=y)
    hnr = np.mean(harmonics) / np.mean(y)

    # Tonnetz features capture tonal content in music.
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

    # print(zcr, "\n")
    # print(spectral_rolloff, "\n")
    # print(spectral_flatness, "\n")
    # print(spectral_contrast, "\n")
    # print(spectral_bandwidth, "\n")
    # print(spectral_centroid, "\n")
    # print(hnr, "\n")
    # print(tonnetz, "\n")

    """
    [[0.31396484 0.34326172 0.35546875 ... 0.61572266 0.64501953 0.51220703]] zcr

    [[19101.5625  6070.3125  6843.75   ... 19078.125  19429.6875 19546.875 ]] spectral_rolloff

    [[0.06047339 0.00093177 0.00024489 ... 0.02621692 0.00874047 0.00761637]] spectral_flatness

    [[10.84041794 11.07663533  9.84344181 ...  7.21280546  9.01777068  spectral_contrast
    16.03950601]
    [ 6.15438251  1.85174831  5.23574288 ...  4.21673308 10.81305202
    4.63176745]
    [ 9.56257891  8.48931785 17.52628761 ...  9.67703335 10.0077066
    3.41444418]
    ...
    [ 8.18306115  6.34117997 15.58661181 ... 13.16491865 12.00751815
    13.45506284]
    [10.01868499 13.5012618  17.91934404 ... 11.21407157 11.17177078
    13.70648357]
    [27.83642292 51.41191284 57.0101875  ... 39.30711508 42.52356058
    36.63467606]] 

    [[6234.0474763  2849.64145195 3091.66463953 ... 4797.78216005 spectral_bandwidth
    3983.00240703 3890.47803846]] 

    [[13610.2420194   3228.6687767   3442.34960675 ... 15558.11550192 spectral_centroid
    16703.24567431 17015.07517292]] 

    -1.0534518 hnr

    [[ 0.00174913  0.00226172  0.00294021 ... -0.01652969 -0.01897287 tonnetz
    -0.01091438]
    [ 0.02189118  0.02175092  0.02238673 ... -0.01764681 -0.03030432
    -0.03041621]
    [ 0.00963793  0.01023453  0.00686653 ...  0.07577645  0.07687026
    0.06360104]
    [ 0.01366424  0.0141401   0.01371375 ... -0.02880611 -0.01115111
    -0.00508894]
    [-0.00544676 -0.00534067 -0.00642907 ... -0.00797193 -0.02268257
    -0.00866216]
    [-0.00964805 -0.01023633 -0.00924302 ...  0.00640648  0.01340689
    0.01442075]] 

    Extracted Features:
    None
    """

    # Return a feature vector by flattening the analysis results
    return np.concatenate(
        [
            np.mean(mfccs, axis=1),  # Spectral properties and timbre of the song (0)
            np.mean(
                chroma,
                axis=1,
            ),  # Harmonic content, indicates musical key, of the song (1)
            np.mean(chroma_cens, axis=1),  # Chroma CENS feature (2)
            np.mean(chroma_cqt, axis=1),  # Chroma CQT feature (3)
            np.mean(chroma_stft, axis=1),  # Chroma STFT feature (4)
            tempo,  # Speed or rhythm of the song, BPM (5)
            [loudness],  # Average loudness of the song (6)
            [avg_interval, std_interval],  # Average gap between musical events (7)
            [np.mean(zcr)],  # Zero crossing rate (8)
            np.mean(spectral_rolloff),  # Spectral rolloff (9)
            np.mean(spectral_flatness),  # Spectral Flatness (10)
            np.mean(spectral_contrast, axis=1),  # Spectral Contrast (11)
            np.mean(spectral_bandwidth),  # Spectral Bandwidth (12)
            np.mean(spectral_centroid),  # Spectral Centroid (13)
            [hnr],  # Harmonic-to-Noise Ratio (14)
            np.mean(tonnetz, axis=1),  # Tonnetz features (tonal content) (15)
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


def analyze_chroma_features(y: np.ndarray, sr: int) -> tuple:
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


def analyze_spectral_features(y: np.ndarray, sr: int) -> tuple:
    """Analyze the spectral features of an audio signal."""
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
    return (
        spectral_rolloff,
        spectral_flatness,
        spectral_contrast,
        spectral_bandwidth,
        spectral_centroid,
    )


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
print("Extracted Features:")
print(features)
