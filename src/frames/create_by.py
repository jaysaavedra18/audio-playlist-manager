from __future__ import annotations

import tkinter as tk
from tkinter import simpledialog
from typing import Callable

from models.playlist import Playlist
from utils.converter import hhmmss_to_seconds

from .navigator import navigate_to


class CreateByFrame(tk.Frame):
    """CreateByFrame class is a frame that allows users to create a playlist based on a specific criteria."""

    def __init__(self, master: tk.Tk) -> None:
        """Initialize CreateByFrame class."""
        super().__init__(master)
        # Create window label
        label = tk.Label(self, text="Create By...")
        label.pack()
        # Define users' options
        options = [
            ("Genre", "genre"),
            ("Mood", "mood"),
            ("Artist", "artist"),
            ("Random", "random"),
        ]
        # Create buttons for users' options
        for text, arg in options:
            button = tk.Button(
                self,
                text=text,
                command=lambda arg=arg: self.select_criteria(arg),
            )
            button.pack()
        # Create return to main menu button
        back_button = tk.Button(
            self,
            text="Back to Playlist Creator",
            command=lambda: navigate_to("playlist_creator", master),
        )
        back_button.pack()

    def select_criteria(self, criteria: str) -> None:
        """Select criteria for creating a playlist based on the user's choice."""
        criteria_function = None
        if criteria == "genre":
            criteria_function = self.genre_helper
        elif criteria == "mood":
            criteria_function = self.mood_helper
        elif criteria == "artist":
            criteria_function = self.artist_helper
        self.create_playlist(criteria_function=criteria_function, criteria=criteria)

    def create_playlist(
        self,
        criteria_function: Callable[[str], bool],
        criteria: str = None,
    ) -> None:
        """Create a playlist based on the criteria provided by the user."""
        print("create_playlist()")
        print(criteria_function)
        print(criteria)

        if criteria_function:
            criteria = simpledialog.askstring(
                "Enter Criteria",
                f"Enter the {criteria}:",
            ).lower()
            if not criteria:
                return
        else:
            criteria = None

        max_duration = self.get_time_input()
        title = simpledialog.askstring(
            "Playlist Title",
            "Enter the title of your playlist:",
        )
        if not title:
            return

        playlist = Playlist(title=title)
        playlist.create_playlist_by_criteria(
            criteria_function=lambda song: criteria_function(song, criteria)
            if criteria_function
            else True,
            max_duration=max_duration,
        )
        playlist.export_playlist()

    @staticmethod
    def genre_helper(song: str, genre: str) -> bool:
        """Return True if the song's genre matches the user's input."""
        return genre in song.genre

    @staticmethod
    def mood_helper(song: str, mood: str) -> bool:
        """Return True if the song's mood matches the user's input."""
        return mood in song.moods

    @staticmethod
    def artist_helper(song: str, artist: str) -> bool:
        """Return True if the song's artist matches the user's input."""
        return song.artist.lower() == artist.lower()

    def get_time_input(self) -> float:
        """Get the maximum duration of the playlist."""
        while True:
            time_str = simpledialog.askstring(
                "Enter Max Duration",
                "Enter max duration (hh:mm:ss):",
            )
            try:
                if "-" in time_str:
                    print(
                        "Invalid time input. Please enter positive values for hours, minutes, and seconds.",
                    )
                else:
                    return hhmmss_to_seconds(time_str)
            except ValueError:
                print("Invalid time format. Please use the format hh:mm:ss.")
