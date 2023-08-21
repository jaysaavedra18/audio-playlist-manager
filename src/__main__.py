# __main__.py

from config import LIBRARY_DATA_PATH
from file_utils import read_json, write_json

from audio_file import AudioFile

all_files = read_json(LIBRARY_DATA_PATH, AudioFile)