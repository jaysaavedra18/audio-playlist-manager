# ruff: noqa

from utils.files import read_json, write_json
from config import LIBRARY_DATA_PATH
from models.audio_file import AudioFile


class DataStore:
    """A simple key-value store that stores data in memory."""

    def __init__(self) -> None:
        """Initialize the data store with the specified database."""
        self.db = read_json(LIBRARY_DATA_PATH, AudioFile)

    def get(self, song_name: str) -> AudioFile:
        """Get the audio file with the specified song name."""
        for audio_file in self.db:
            if audio_file.song_name == song_name:
                return audio_file
        message = f"Audio file with song name '{song_name}' not found."
        raise ValueError(message)

    def add(self, audio_file: AudioFile) -> None:
        """Add the audio file to the data store."""
        self.db.append(audio_file)
        write_json(LIBRARY_DATA_PATH, self.db)

    def update(self, audio_file: AudioFile) -> None:
        """Update the audio file in the data store."""
        for i, file in enumerate(self.db):
            if file.song_name == audio_file.song_name:
                self.db[i] = audio_file
                write_json(LIBRARY_DATA_PATH, self.db)
                return
        message = f"Audio file with song name '{audio_file.song_name}' not found."
        raise ValueError(message)
