import librosa

def analyze_audio(audio_path: str) -> dict:
    """Analyze an audio file and extract its properties."""
    # Load an audio file
    y, sr = librosa.load(audio_path, sr=None)
    print(f"Loaded audio with shape: {y.shape}, sample rate: {sr} Hz")
    # Extract tempo and bpm
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    print(f"Estimated tempo: {tempo} BPM")
    # MFCCs capture the song's timbre and spectral texture, summarizing its tonal qualities over time.
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    print(f"MFCCs shape: {mfccs.shape}")
    # Chroma features capture the harmonic content of the audio signal.
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    print(f"Chroma features shape: {chroma.shape}")
    # Onset detection shows when musical events occur in the audio signal.
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    print(f"Detected {len(onset_times)} onsets at times: {onset_times}")







analyze_audio("/Users/saavedj/Downloads/music/misc/16.mp3")