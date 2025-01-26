# config.py

import datetime
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get today's date
today_date = datetime.date.today()
DATE_STRING = today_date.strftime("%Y-%m-%d")

# Define directory paths
BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIRECTORY = os.getenv("AUDIO_DIRECTORY") # Set environment variable in .env file
DATA_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")
DAILY_PLAYLIST_DIRECTORY = os.path.join(AUDIO_DIRECTORY, "output", f"{DATE_STRING}")
DOWNLOADS_DIRECTORY = os.path.join(AUDIO_DIRECTORY, "misc")
LIBRARY_DIRECTORY = os.path.join(AUDIO_DIRECTORY, "lofi")

# Define data file paths
LIBRARY_DATA_PATH = os.path.join(DATA_DIRECTORY, "library_data.json")
