# audio_io.py
"""Provides functions for audio input/output operations (read, write, concat)."""

import json
import os
from pathlib import Path

from pydub import AudioSegment

from models.audio_file import AudioFile

# Audio input/output functions


def get_audio_files(directory: str) -> list:
    """Retrieve a list of audio file names (MP3 and WAV) from the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith((".mp3", ".wav"))]


def get_audio_info(audio_files: list) -> tuple:
    """Calculate the total size (bytes) and length (seconds) of audio files."""
    # If a single file path is provided as a string, convert it to a list
    if isinstance(audio_files, str):
        audio_files = [audio_files]

    # Sum size and length of audio_files
    total_size = sum(Path.stat(file).st_size for file in audio_files)
    total_length = sum(
        AudioSegment.from_file(file).duration_seconds for file in audio_files
    )
    return total_size, total_length


def concatenate_audio(selected_files: list, audio_directory: str) -> AudioSegment:
    """Concatenate multiple audio files specified in the 'selected_files' list into one AudioSegment."""
    # Initialize an empty AudioSegment object to hold the concatenated audio
    concatenated_audio = AudioSegment.silent(duration=0)

    print("Building your playlist...")

    for file in selected_files:
        audio_path = Path(audio_directory) / file
        audio_segment = AudioSegment.from_file(audio_path)
        concatenated_audio += audio_segment

    return concatenated_audio


def export_audio(audio: AudioSegment, file_path: str) -> None:
    """Export an AudioSegment object to an MP3 audio file at the specified file path."""
    audio.export(get_unique_file_name(file_path), format="mp3")


# Text input/output functions


def get_unique_file_name(file_path: str) -> str:
    """Generate a unique file name by adding a counter suffix to the base file name if the file already exists."""
    path = Path(file_path)
    base_name, extension = path.parent / path.stem, path.suffix
    unique_path = file_path
    counter = 1

    while Path.exists(unique_path):
        unique_path = f"{base_name} ({counter}){extension}"
        counter += 1

    return unique_path


def parse_text_block_into_song(text: str) -> dict:
    """Parse a text block containing song details, extract song name, artist name, artist link, and licenses into a dictionary."""
    lines = text.strip().split("\n")

    # Extract song name, artist name, and artist link from the first line
    song_info = lines[0].split(" by ")
    song_name = song_info[0].strip()
    artist_info = song_info[1].split(" | ")
    artist_name, artist_link = artist_info[0].strip(), artist_info[1].strip()

    # Extract licenses from lines 2 to 4 (if they exist) as a list
    licenses = [line.strip() for line in lines[1:4]]

    return {
        "song_name": song_name,
        "artist_name": artist_name,
        "artist_link": artist_link,
        "licenses": licenses,
    }


# JSON/object input/output functions


def write_json(objects: list, file_path: str) -> None:
    """Serialize a list of objects and write the JSON representation to a file."""
    # Serialize to JSON
    json_data = [
        vars(obj) if not callable(getattr(obj, "to_dict", None)) else obj.to_dict()
        for obj in objects
    ]

    # Write JSON data to the file
    with Path.open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)


def read_json(file_path: str, target_class: any) -> list:
    """Read JSON data from a file and convert it into a list of objects of the specified class."""
    try:
        with Path.open(file_path) as json_file:
            loaded_data = json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

    loaded_objects = []
    for data in loaded_data:
        if "songs" in data:
            songs = [AudioFile(**song_data) for song_data in data["songs"]]
            data["songs"] = songs
        loaded_objects.append(target_class(**data))

    return loaded_objects
