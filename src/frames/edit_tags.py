import tkinter as tk
from pathlib import Path
from tkinter import filedialog, simpledialog

from store import data_store

from .navigator import navigate_to


class EditTagsFrame(tk.Frame):
    """EditTagsFrame class is a frame that allows users to edit tags for songs in the library."""

    def __init__(self, master: tk.Frame) -> None:
        """Initialize EditTagsFrame class."""
        super().__init__(master)
        # Create window label
        label = tk.Label(self, text="Edit tags")
        label.pack()
        # Define users' options
        options = [
            ("Genre", "genres"),
            ("Mood", "moods"),
        ]
        # Create buttons for users' options
        for text, arg in options:
            button = tk.Button(
                self,
                text=text,
                command=lambda arg=arg: self.update_tags(arg),
            )
            button.pack()

        # Create return to main menu button
        back_button = tk.Button(
            self,
            text="Back to Song Library",
            command=lambda: navigate_to("song_library", master),
        )
        back_button.pack()

    def update_tags(self, tag: str) -> None:
        """Update tags for songs in the library."""
        audio_files = data_store.get_all()
        files = filedialog.askopenfilenames(
            title="Select MP3 Files",
            filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")),
        )

        if not files:  # if there was no selection return
            return
        filenames = [Path(file).name for file in files]

        user_input = simpledialog.askstring(
            f"Add {tag}",
            f"Enter the {tag} for your song(s):",
        )
        if not user_input:
            print("No tag provided")

        # Update the tag for the selected song
        for audio_file in audio_files:
            if audio_file.filename in filenames:
                if tag == "moods":
                    if user_input in audio_file.moods:
                        break
                    audio_file.add_mood(user_input)
                elif tag == "genres":
                    if user_input in audio_file.genres:
                        break
                    audio_file.add_genre(user_input)
                data_store.update(audio_file)
