import os
import tkinter as tk
from tkinter import filedialog, simpledialog

from models.playlist import Playlist
from .navigator import navigate_to

class PlaylistCreatorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Create a Playlist")
        label.pack()

        select_button = tk.Button(self, text="Browse Files", command=self.browse_files)
        select_button.pack()

        create_by_button = tk.Button(self, text="Create By...", command=lambda: navigate_to("create_by", master))
        create_by_button.pack()

        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: navigate_to("main_menu", master))
        back_button.pack()

    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Select MP3 Files", filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))

        if not files:  # if there was no selection return
            return
        filenames = [os.path.basename(file) for file in files]

        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            pass
        max_duration = self.get_time_input()

        playlist = Playlist(title=title)
        playlist.add_songs_by_filename(filenames=filenames, max_duration=max_duration)
        playlist.export_playlist()

    def get_time_input(self):
        while True:
            time_str = simpledialog.askstring(
                "Enter Max Duration", "Enter max duration (mm:ss):")
            try:
                minutes, seconds = map(int, time_str.split(":"))
                if minutes >= 0 and seconds >= 0:
                    total_seconds = minutes * 60 + seconds
                    return total_seconds
                print(
                    "Invalid time input. Please enter positive values for minutes and seconds.")
            except ValueError:
                print("Invalid time format. Please use the format mm:ss.")