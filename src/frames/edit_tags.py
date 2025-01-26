import os
import tkinter as tk
from tkinter import filedialog, simpledialog

from navigator import navigate_to
from config import LIBRARY_DATA_PATH
from utils.files import read_json, write_json
from models.audio_file import AudioFile

class EditTagsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Create window label
        label = tk.Label(self, text="Edit tags")
        label.pack()
        # Define users' options
        options = [
            ("Genre", "genre"),
            ("Mood", "moods"),
        ]
        # Create buttons for users' options
        for text, arg in options:
            button = tk.Button(
                self, text=text, command=lambda arg=arg: self.update_tags(arg))
            button.pack()

        # Create return to main menu button
        back_button = tk.Button(
            self, text="Back to Song Library", command=lambda: navigate_to("song_library", master))
        back_button.pack()

    def update_tags(self, arg):
        audio_files = read_json(LIBRARY_DATA_PATH, AudioFile)
        files = filedialog.askopenfilenames(
            title="Select MP3 Files", filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))

        if not files:  # if there was no selection return
            return
        filenames = [os.path.basename(file) for file in files]

        tag = simpledialog.askstring(
            f"Add {arg}", f"Enter the {arg} for your song(s):")
        if not tag:
            pass

        for audio_file in audio_files:
            if audio_file.filename in filenames:
                if arg == "moods":
                    audio_file.add_mood(tag)
                elif arg == "genre":
                    audio_file.add_genre(tag)

        write_json(audio_files, LIBRARY_DATA_PATH)