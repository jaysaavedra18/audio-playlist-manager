import os
import tkinter as tk
from tkinter import filedialog

from navigator import navigate_to

from config import LIBRARY_DATA_PATH, LIBRARY_DIRECTORY
from models.audio_file import AudioFile
from utils.converter import seconds_to_mmss
from utils.files import (
    get_audio_info,
    parse_text_block_into_song,
    read_json,
    write_json,
)


class CollectionViewer(tk.Toplevel):  # Use Toplevel for a separate window
    """CollectionViewer is a separate window that displays the audio files in the collection."""

    def __init__(self, audio_files: list[AudioFile]) -> None:
        """Initialize the CollectionViewer window."""
        super().__init__()
        self.audio_files = audio_files

        self.title("Audio Collection Viewer")
        self.geometry("600x400")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for audio_file in self.audio_files:
            item_text = (
                f"{audio_file.index}: {audio_file.song_name} - {audio_file.artist}"
            )
            self.listbox.insert(tk.END, item_text)


class SongLibraryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Song Library")
        label.pack()

        # Finder window
        collection_button = tk.Button(
            self, text="Your Collection", command=self.show_collection_viewer
        )
        collection_button.pack()

        add_songs_button = tk.Button(self, text="Add Songs", command=self.add_songs)
        add_songs_button.pack()

        # Frame 1st for selection of tag
        # Finder window
        tags_button = tk.Button(
            self, text="Edit Tags", command=lambda: navigate_to("edit_tags", master)
        )
        tags_button.pack()

        back_button = tk.Button(
            self,
            text="Back to Main Menu",
            command=lambda: navigate_to("main_menu", master),
        )
        back_button.pack()

    def show_collection_viewer(self):
        audio_files = read_json(LIBRARY_DATA_PATH, AudioFile)
        collection_viewer = CollectionViewer(audio_files)
        collection_viewer.mainloop()

    def add_songs(self):
        # Create a new window for adding songs
        add_songs_window = tk.Toplevel(self)
        add_songs_window.title("Add Songs")

        selected_file_path = filedialog.askopenfilename(title="Select Downloaded File")

        # Create an Entry widget for the user to paste data
        data_text = tk.Text(add_songs_window)
        data_text.pack()

        add_button = tk.Button(
            add_songs_window,
            text="Add and Process",
            command=lambda: self.process_data(
                data_text.get("1.0", tk.END), selected_file_path, add_songs_window
            ),
        )
        add_button.pack()

    def process_data(self, text, filepath, window_to_close):
        if text and filepath:
            audio_files = read_json(LIBRARY_DATA_PATH, AudioFile)
            parsed_data = parse_text_block_into_song(text)
            index = len(audio_files)
            # Get audio file data
            song_name = parsed_data["song_name"]
            filename = song_name + ".mp3"
            new_filepath = os.path.join(LIBRARY_DIRECTORY, filename)
            audio_info = get_audio_info([filepath])
            file_size = f"{audio_info[0] / (1024 * 1024):.2f} MB"
            duration = seconds_to_mmss(int(audio_info[1]))

            # Build audio file
            audio_file = AudioFile(
                index=index,
                song_name=song_name,
                artist=parsed_data["artist_name"],
                artist_link=parsed_data["artist_link"],
                duration=duration,
                filename=filename,
                file_size=file_size,
                licenses=parsed_data["licenses"],
                genre=[],
                moods=[],
            )
            os.rename(filepath, new_filepath)
            audio_files.append(audio_file)
            write_json(audio_files, LIBRARY_DATA_PATH)
            print("Song added successfully!")
            window_to_close.destroy()
