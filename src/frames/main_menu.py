import tkinter as tk
from .navigator import navigate_to

class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Main Menu")
        label.pack()

        playlist_button = tk.Button(
            self, 
            text="Playlist Creator", 
            command=lambda: navigate_to("playlist_creator", master))
        playlist_button.pack()

        option2_button = tk.Button(
            self, 
            text="Song Library", 
            command=lambda: navigate_to("song_library", master))
        option2_button.pack()
