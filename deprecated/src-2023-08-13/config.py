# config.py

import os
import datetime

# Define directory paths
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Get parent dir of script dir
AUDIO_DIRECTORY = os.path.join(BASE_DIRECTORY, "music")
DATA_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")
ASSETS_DIRECTORY = os.path.join(BASE_DIRECTORY, "yt_assets")

# Define file paths
TEXT_FILE_PATH = os.path.join(DATA_DIRECTORY, "references.txt")
SONGS_PATH = os.path.join(DATA_DIRECTORY, "songs.txt")
MUSIC_DATA_PATH = os.path.join(DATA_DIRECTORY, "music_data.json")

# Get today's date
today_date = datetime.date.today()
DATE_STRING = today_date.strftime("%Y-%m-%d")
