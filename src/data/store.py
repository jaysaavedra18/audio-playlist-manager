# ruff: noqa

from utils.files import read_json, write_json
from config import LIBRARY_DATA_PATH
from models.audio_file import AudioFile


class DataStore:
    """A simple key-value store that stores data in memory."""

    def __init__(self) -> None:
        """Initialize the data store with the specified database."""
        self.db = read_json(LIBRARY_DATA_PATH, AudioFile)
