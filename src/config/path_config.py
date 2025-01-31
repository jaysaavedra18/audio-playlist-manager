from pathlib import Path

from .date_config import DATE_STRING
from .env_config import AUDIO_DIRECTORY

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = Path(BASE_DIRECTORY) / "data"

DAILY_PLAYLIST_DIRECTORY = Path(AUDIO_DIRECTORY) / "output" / f"{DATE_STRING}"
DOWNLOADS_DIRECTORY = Path(AUDIO_DIRECTORY) / "misc"
LIBRARY_DIRECTORY = Path(AUDIO_DIRECTORY) / "lofi"

LIBRARY_DATA_PATH = Path(DATA_DIRECTORY) / "library_data.json"
