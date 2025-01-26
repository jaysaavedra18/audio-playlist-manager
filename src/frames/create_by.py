import tkinter as tk
from tkinter import simpledialog
from models.playlist import Playlist
from utils.converter import hhmmss_to_seconds
from .navigator import navigate_to

# maybe updating input to select from the possible values
class CreateByFrame(tk.Frame):
    def __init__(self, master):
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
            button = tk.Button(self, text=text, command=lambda arg=arg: self.select_criteria(arg))
            button.pack()
        # Create return to main menu button
        back_button = tk.Button(
            self, text="Back to Playlist Creator", command=lambda: navigate_to("playlist_creator", master))
        back_button.pack()

    def select_criteria(self, arg):
        print("select_criteria()")
        criteria_function = None
        if arg == "genre":
            criteria_function = self.genre_helper
        elif arg == "mood":
            criteria_function = self.mood_helper
        elif arg == "artist":
            criteria_function = self.artist_helper
        self.create_playlist(criteria_function=criteria_function, arg=arg)

    def create_playlist(self, criteria_function=None, arg=None):
        print("create_playlist()")
        print(criteria_function)
        print(arg)

        if criteria_function:
            criteria = simpledialog.askstring(
                "Enter Criteria", f"Enter the {arg}:")
            if not criteria:
                return
        else:
            criteria = None

        max_duration = self.get_time_input()
        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            return

        playlist = Playlist(title=title)
        playlist.create_playlist_by_criteria(
            criteria_function=lambda song: criteria_function(
                song, criteria) if criteria_function else True,
            max_duration=max_duration)
        playlist.export_playlist()

    @staticmethod
    def genre_helper(song, genre):
        return genre in song.genre

    @staticmethod
    def mood_helper(song, mood):
        return mood in song.moods

    @staticmethod
    def artist_helper(song, artist):
        return song.artist.lower() == artist.lower()

    def get_time_input(self):
        while True:
            time_str = simpledialog.askstring(
                "Enter Max Duration", "Enter max duration (hh:mm:ss):")
            try:
                if "-" in time_str:
                    print("Invalid time input. Please enter positive values for hours, minutes, and seconds.")
                else:
                    total_seconds = hhmmss_to_seconds(time_str)
                    return total_seconds
            except ValueError:
                print("Invalid time format. Please use the format hh:mm:ss.")