import os
import tkinter as tk
from tkinter import filedialog, simpledialog

from config import LIBRARY_DATA_PATH, LIBRARY_DIRECTORY
from utils.files import get_audio_info, parse_text_block_into_song, read_json, write_json
from models.audio_file import AudioFile
from models.playlist import Playlist
from frames.main_menu import MainMenuFrame
from utils.converter import hhmmss_to_seconds, seconds_to_mmss



class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Playlist Creator")

        self.center_window()

        self.lift()
        self.attributes("-topmost", True)
        self.after_idle(self.attributes, "-topmost", False)

        self.menu_frame = MainMenuFrame(self)
        self.menu_frame.pack(fill="both", expand=True)
        self.current_frame = self.menu_frame

    def center_window(self):
        """Center the window on the screen."""
        window_width = 500
        window_height = 200

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        new_frame.pack(fill="both", expand=True)
        self.current_frame.destroy()
        self.current_frame = new_frame


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
            self, text="Back to Song Library", command=lambda: master.show_frame(SongLibraryFrame))
        back_button.pack()

    def update_tags(self, arg):
        audio_files = load_data()
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

        save_data(audio_files)


def load_data():
    return read_json(LIBRARY_DATA_PATH, AudioFile)


def save_data(audio_files):
    write_json(audio_files, LIBRARY_DATA_PATH)
    print("Data successfully saved!")


def main():
    app = Application()
    app.mainloop()  # Start the GUI event loop


if __name__ == "__main__":
    main()
