import os

from dotenv import load_dotenv

load_dotenv()

AUDIO_DIRECTORY = os.getenv("AUDIO_DIRECTORY")  # Ensure this is set in .env
