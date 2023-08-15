# config.py

import os
import datetime
from file_utils import get_unique_file_name

# Get today's date
today_date = datetime.date.today()
DATE_STRING = today_date.strftime("%Y-%m-%d")

# Define directory paths
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Get parent dir of src folder
AUDIO_DIRECTORY = os.path.join(BASE_DIRECTORY, "music")
DATA_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")
ASSETS_DIRECTORY = os.path.join(BASE_DIRECTORY, "yt_assets")
ARCHIVES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, f"{DATE_STRING}")

# Define data file paths
TEXT_FILE_PATH = os.path.join(DATA_DIRECTORY, "references.txt")
SONGS_PATH = os.path.join(DATA_DIRECTORY, "songs.txt")
MUSIC_DATA_PATH = os.path.join(DATA_DIRECTORY, "music_data.json")

# Define output File paths
OUTPUT_PROMOTIONS_PATH = get_unique_file_name(os.path.join(ASSETS_DIRECTORY, f"output-references-{DATE_STRING}.txt"))
OUTPUT_PLAYLIST_PATH = get_unique_file_name(os.path.join(ASSETS_DIRECTORY, f"playlist-{DATE_STRING}.mp3"))