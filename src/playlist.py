import os
import random
from typing import List

from audio_file import AudioFile
from utils import (
    mmss_to_seconds,
    seconds_to_mmss,
    bytes_to_formatted_size,
    formatted_size_to_bytes,
)
from file_utils import (
    concatenate_audio,
    export_audio,
    make_directory,
    read_json,
)
from config import (
    LIBRARY_DATA_PATH,
    DAILY_PLAYLIST_DIRECTORY,
    DATE_STRING,
    LIBRARY_DIRECTORY,
)

# Import data
audio_files = read_json(LIBRARY_DATA_PATH, AudioFile)


class Playlist:
    def __init__(self, title: str, songs: List[AudioFile] = None, promotions=None, date_created=None):
        self.title = title
        self.songs = songs or []
        self.promotions = promotions or []
        self.date_created = date_created or DATE_STRING
        self.calculate_metrics()

    def calculate_metrics(self):
        self.calculate_duration()
        self.calculate_file_size()
        self.get_filenames()

    def to_dict(self):
        return {
            "title": self.title,
            "songs": [song.to_dict() for song in self.songs],
            "promotions": self.promotions,
            "date_created": self.date_created,
        }

    def add_song(self, song: AudioFile):
        self.songs.append(song)
        self.calculate_metrics()

    def remove_song(self, song: AudioFile):
        self.songs.remove(song)
        self.calculate_metrics()

    def add_license(self, license_text: str):
        self.promotions.append(license_text)

    def calculate_duration(self):
        for song in self.songs:
            print(song.duration)

        total_duration_seconds = sum(mmss_to_seconds(song.duration) for song in self.songs)
        self.total_duration = seconds_to_mmss(total_duration_seconds)

    def calculate_file_size(self):
        total_file_size_bytes = sum(formatted_size_to_bytes(
            song.file_size) for song in self.songs)
        self.total_file_size = bytes_to_formatted_size(total_file_size_bytes)

    def get_filenames(self):
        self.filenames = [song.filename for song in self.songs]

    # ideally i take out max_duration from arg3 to improve speed
    def create_playlist_by_criteria(self, criteria_function, max_duration):
        # random.shuffle(audio_files)
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
        make_directory(DAILY_PLAYLIST_DIRECTORY)
        self.get_filenames()
        output_path = os.path.join(DAILY_PLAYLIST_DIRECTORY, f"{self.title}-{DATE_STRING}.mp3")
        # Concatenate audio and export to the daily playlist directory
        concatenated_audio = concatenate_audio(self.filenames, LIBRARY_DIRECTORY)
        export_audio(concatenated_audio, output_path)

        # Select necessary licenses and export to the daily playlist directory
        for song in self.songs:
            for license in song.licenses:
                if license not in self.promotions:
                    self.add_license(license)
        
        # Add line break in the description
        self.add_license('\n\n')

        # Create timestamps for songs
        total_duration = 0
        for song in self.songs:
            timestamp = f"{seconds_to_mmss(total_duration)} {song.song_name} by {song.artist} | {song.artist_link}"
            total_duration += mmss_to_seconds(song.duration)
            self.add_license(timestamp)
            print(timestamp)

        # Write to the necessary files for audio and promotions
        promotions_path = os.path.join(
            DAILY_PLAYLIST_DIRECTORY, f"{self.title}-promotions.txt")
        with open(promotions_path, "w") as file:
            for license in self.promotions:
                file.write(license + "\n")

        print("successfully exported your playlist :D ")
