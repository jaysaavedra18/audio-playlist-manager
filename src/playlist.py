import random
from typing import List

from audio_file import AudioFile
from utils import formatted_time_to_seconds, seconds_to_formatted_time, bytes_to_formatted_size, formatted_size_to_bytes
from file_utils import concatenate_audio, export_audio, make_directory, read_json
from config import AUDIO_DIRECTORY, MUSIC_DATA_PATH, OUTPUT_PROMOTIONS_PATH, OUTPUT_PLAYLIST_PATH, ARCHIVES_DIRECTORY

# Import audio files
audio_files = read_json(MUSIC_DATA_PATH, AudioFile)


class Playlist:
    def __init__(self, title: str, songs: List[AudioFile] = None):
        self.title = title
        self.songs = songs or []
        self.calculate_duration()
        self.calculate_file_size()
        self.get_files()
        self.promotions = []
        self.catalog = audio_files

    def add_song(self, song: AudioFile):
        self.songs.append(song)
        self.calculate_duration()
        self.calculate_file_size()

    def remove_song(self, song: AudioFile):
        self.songs.remove(song)
        self.calculate_duration()
        self.calculate_file_size()

    def add_license(self, license_text: str):
        self.promotions.append(license_text)

    def calculate_duration(self):
        self.total_duration = seconds_to_formatted_time(sum(formatted_time_to_seconds(song.duration) for song in self.songs))

    def calculate_file_size(self):
        self.total_file_size = bytes_to_formatted_size(sum(formatted_size_to_bytes(song.file_size) for song in self.songs))

    def get_files(self):
        self.filenames = [song.filename for song in self.songs]

    def create_playlist_by_random(self, song_count=24):
        selected_songs = random.sample(audio_files, song_count)
        self.songs = selected_songs
        self.calculate_duration()
        self.calculate_file_size()

    def create_playlist_by_genre(self, genre):
        # Add AudioFiles to list if they match the genre
        for audio_file in audio_files:
            if genre in audio_file.genre:
                self.add_song(audio_file)
    
    def create_playlist_by_mood(self, mood):
        # Add AudioFiles to list if they match the mood
        for audio_file in audio_files:
            if mood in audio_file.mood:
                self.add_song(audio_file)

    def export_playlist(self):
        # Create daily archive directory if dne
        make_directory(ARCHIVES_DIRECTORY)
        self.get_files()

        # Concatenate audio and export to yt_assets
        concatenated_audio = concatenate_audio(self.filenames, AUDIO_DIRECTORY)
        export_audio(concatenated_audio, OUTPUT_PLAYLIST_PATH)

        # Select necessary licenses and export to yt_assets
        for song in self.songs:
            for license in song.licenses:
                if license not in self.promotions:
                    self.add_license(license)
        with open(OUTPUT_PROMOTIONS_PATH, "w") as file:
            for license in sorted(self.promotions, key=len):
                file.write(license + "\n")


