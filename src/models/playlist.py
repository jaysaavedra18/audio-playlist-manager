from __future__ import annotations

import random
from pathlib import Path
from typing import Callable

from config import (
    DAILY_PLAYLIST_DIRECTORY,
    DATE_STRING,
    LIBRARY_DATA_PATH,
    LIBRARY_DIRECTORY,
)
from models.audio_file import AudioFile
from utils.converter import (
    bytes_to_formatted_size,
    formatted_size_to_bytes,
    mmss_to_seconds,
    seconds_to_mmss,
)
from utils.files import (
    concatenate_audio,
    export_audio,
    read_json,
)

# Import data
audio_files = read_json(LIBRARY_DATA_PATH, AudioFile)


class Playlist:
    """A class to represent a playlist of audio files."""

    def __init__(
        self,
        title: str,
        songs: list[AudioFile] = None,
        promotions: str = None,
        date_created: str = None,
    ) -> None:
        """Initialize a Playlist object with a title, list of songs, promotions, and date created."""
        self.title = title
        self.songs = songs or []
        self.promotions = promotions or []
        self.date_created = date_created or DATE_STRING
        self.filenames = []

        if self.songs:
            self.calculate_metrics()

    def calculate_metrics(self) -> None:
        """Calculate the total duration and file size of the playlist."""
        total_duration_seconds = sum(
            mmss_to_seconds(song.duration) for song in self.songs
        )
        self.total_duration = seconds_to_mmss(total_duration_seconds)

        total_file_size_bytes = sum(
            formatted_size_to_bytes(song.file_size) for song in self.songs
        )
        self.total_file_size = bytes_to_formatted_size(total_file_size_bytes)

        self.filenames = [song.filename for song in self.songs]

    def to_dict(self) -> dict:
        """Return a dictionary representation of the playlist."""
        return {
            "title": self.title,
            "songs": [song.to_dict() for song in self.songs],
            "promotions": self.promotions,
            "date_created": self.date_created,
        }

    def add_song(self, song: AudioFile) -> None:
        """Add a song to the playlist."""
        self.songs.append(song)

    def remove_song(self, song: AudioFile) -> None:
        """Remove a song from the playlist."""
        self.songs.remove(song)

    # ideally i take out max_duration from arg3 to improve speed
    def create_playlist_by_criteria(
        self,
        criteria_function: Callable[[str], bool],
        max_duration: float,
    ) -> None:
        """Create a playlist based on a criteria function and maximum duration."""
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

    def add_songs_by_filename(self, filenames: list[str], max_duration: float) -> None:
        """Add songs to the playlist based on a list of filenames and maximum duration."""
        playlist_duration = 0
        self.songs = []

        for song in audio_files:
            if playlist_duration + mmss_to_seconds(song.duration) <= max_duration:
                if song.filename in filenames:
                    self.add_song(song)
                    playlist_duration += mmss_to_seconds(song.duration)
            else:
                break

    def export_playlist(self) -> None:
        """Export the playlist to an audio file and a promotions file."""
        # Create daily archive directory if it doesn't exist
        if not Path.exists(DAILY_PLAYLIST_DIRECTORY):
            Path.mkdir(DAILY_PLAYLIST_DIRECTORY)

        self.calculate_metrics()
        output_path = Path(DAILY_PLAYLIST_DIRECTORY) / f"{self.title}-{DATE_STRING}.mp3"

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
        self.promotions = [*track_info, "\n", *list(all_licenses)]

        # Write to the necessary files for audio and promotions
        promotions_path = (
            Path(DAILY_PLAYLIST_DIRECTORY) / f"{self.title}-promotions.txt"
        )
        with Path.open(promotions_path, "w") as file:
            for line in self.promotions:
                file.write(line + "\n")

        print("successfully exported your playlist :D ")
