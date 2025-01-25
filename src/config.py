# config.py

import os
import datetime

# Get today's date
today_date = datetime.date.today()
DATE_STRING = today_date.strftime("%Y-%m-%d")

# Define directory paths
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Get parent dir of src folder
AUDIO_DIRECTORY = "/Users/saavedj/Downloads/music"
DATA_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")
ASSETS_DIRECTORY = os.path.join(AUDIO_DIRECTORY, "output")
ARCHIVES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, f"{DATE_STRING}")
DOWNLOADS_DIRECTORY = os.path.join(AUDIO_DIRECTORY, "misc")
LIBRARY_DIRECTORY = os.path.join(AUDIO_DIRECTORY, "lofi")

# Define data file paths
REFERENCES_PATH = os.path.join(DATA_DIRECTORY, "references.txt")
LIBRARY_PATH = os.path.join(DATA_DIRECTORY, "library.txt")
LIBRARY_DATA_PATH = os.path.join(DATA_DIRECTORY, "library_data.json")
PLAYLIST_DATA_PATH = os.path.join(DATA_DIRECTORY, "playlist_data.json")