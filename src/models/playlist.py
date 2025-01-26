import os
import random
from typing import List

from config import (
    DAILY_PLAYLIST_DIRECTORY,
    DATE_STRING,
    LIBRARY_DATA_PATH,
    LIBRARY_DIRECTORY,
)
from file_utils import (
    concatenate_audio,
    export_audio,
    read_json,
)
from models.audio_file import AudioFile
from utils import (
    bytes_to_formatted_size,
    formatted_size_to_bytes,
    mmss_to_seconds,
    seconds_to_mmss,
)

# Import data
audio_files = read_json(LIBRARY_DATA_PATH, AudioFile)


class Playlist:
    def __init__(self, title: str, songs: List[AudioFile] = None, promotions=None, date_created=None):
        self.title = title
        self.songs = songs or []
        self.promotions = promotions or []
        self.date_created = date_created or DATE_STRING
        self.filenames = []

        if self.songs:
            self.calculate_metrics()

    def calculate_metrics(self):
        # Calculate total duration
        total_duration_seconds = sum(mmss_to_seconds(song.duration) for song in self.songs)
        self.total_duration = seconds_to_mmss(total_duration_seconds)

        # Calculate total file size
        total_file_size_bytes = sum(formatted_size_to_bytes(song.file_size) for song in self.songs)
        self.total_file_size = bytes_to_formatted_size(total_file_size_bytes)

        # Get filenames for the playlist
        self.filenames = [song.filename for song in self.songs]

    def to_dict(self):
        return {
            "title": self.title,
            "songs": [song.to_dict() for song in self.songs],
            "promotions": self.promotions,
            "date_created": self.date_created,
        }

    def add_song(self, song: AudioFile):
        self.songs.append(song)

    def remove_song(self, song: AudioFile):
        self.songs.remove(song)

    # ideally i take out max_duration from arg3 to improve speed
    def create_playlist_by_criteria(self, criteria_function, max_duration):
        selected_songs = [song for song in audio_files if criteria_function(song)]
        random.shuffle(selected_songs)

        playlist_duration = 0
        self.songs = []

        for song in selected_songs:
            if playlist_duration + mmss_to_seconds(song.duration) <= max_duration:
                self.add_song(song)
                playlist_duration += mmss_to_seconds(song.duration)
            else:
                break

    def add_songs_by_filename(self, filenames, max_duration):
        playlist_duration = 0
        self.songs = []

        for song in audio_files:
            if playlist_duration + mmss_to_seconds(song.duration) <= max_duration:
                if song.filename in filenames:
                    self.add_song(song)
                    playlist_duration += mmss_to_seconds(song.duration)
            else:
                break

    def export_playlist(self):
        # Create daily archive directory if it doesn't exist
        if not os.path.exists(DAILY_PLAYLIST_DIRECTORY):
            os.mkdir(DAILY_PLAYLIST_DIRECTORY)

        self.calculate_metrics()
        output_path = os.path.join(DAILY_PLAYLIST_DIRECTORY, f"{self.title}-{DATE_STRING}.mp3")

        # Concatenate audio and export to the daily playlist directory
        concatenated_audio = concatenate_audio(self.filenames, LIBRARY_DIRECTORY)
        export_audio(concatenated_audio, output_path)

        # Combine timestamps, song information, and licenses in a single pass
        total_duration = 0
        track_info = []
        all_licenses = set()

        for song in self.songs:
            # Generate timestamp for each song
            timestamp = f"{seconds_to_mmss(total_duration)} {song.song_name} by {song.artist} | {song.artist_link}"
            track_info.append(timestamp)

            # Add licenses to the set to avoid duplicates
            all_licenses.update(song.licenses)

            total_duration += mmss_to_seconds(song.duration)

        # Update promotions with the track info and licenses
        self.promotions = track_info + ["\n"] + list(all_licenses)

        # Write to the necessary files for audio and promotions
        promotions_path = os.path.join(
            DAILY_PLAYLIST_DIRECTORY, f"{self.title}-promotions.txt")
        with open(promotions_path, "w") as file:
            for license in self.promotions:
                file.write(license + "\n")

        print("successfully exported your playlist :D ")
