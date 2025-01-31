from config.config import LIBRARY_DATA_PATH
from models.audio_file import AudioFile
from utils.files import read_json, write_json


class DataStore:
    """A singleton key-value store that stores data in memory."""

    _instance = None  # Class-level storage for the single instance

    def __new__(cls: any) -> any:
        """Ensure only one instance of DataStore exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()  # Call a separate initializer  # noqa: SLF001
        return cls._instance

    def _initialize(self) -> None:
        """Initialize the data store with the database contents."""
        self.db = read_json(LIBRARY_DATA_PATH, AudioFile)
        print(f"Data store initialized with {len(self.db)} audio files.")

    def get(self, song_name: str) -> AudioFile:
        """Get the audio file with the specified song name."""
        for audio_file in self.db:
            if audio_file.song_name == song_name:
                return audio_file
        message = f"Audio file with song name '{song_name}' not found."
        raise ValueError(message)

    def get_all(self) -> list[AudioFile]:
        """Get all audio files in the data store."""
        return self.db

    def add(self, audio_file: AudioFile) -> None:
        """Add the audio file to the data store and persist."""
        self.db.append(audio_file)
        write_json(LIBRARY_DATA_PATH, self.db)

    def update(self, audio_file: AudioFile) -> None:
        """Update an existing audio file in the data store."""
        for i, file in enumerate(self.db):
            if file.song_name == audio_file.song_name:
                self.db[i] = audio_file
                write_json(LIBRARY_DATA_PATH, self.db)
                return
        message = f"Audio file with song name '{audio_file.song_name}' not found."
        raise ValueError(message)
