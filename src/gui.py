import os
import tkinter as tk
from tkinter import filedialog, simpledialog

from models.audio_file import AudioFile
from models.playlist import Playlist
from config import LIBRARY_DATA_PATH, LIBRARY_DIRECTORY
from utils import seconds_to_mmss, hhmmss_to_seconds
from file_utils import get_audio_info, parse_text_block_into_song, read_json, write_json


class CollectionViewer(tk.Toplevel):  # Use Toplevel for a separate window
    def __init__(self, audio_files):
        super().__init__()
        self.audio_files = audio_files

        self.title("Audio Collection Viewer")
        self.geometry("600x400")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        for audio_file in self.audio_files:
            item_text = f"{audio_file.index}: {audio_file.song_name} - {audio_file.artist}"
            self.listbox.insert(tk.END, item_text)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Playlist Creator")

        self.menu_frame = MainMenuFrame(self)
        self.menu_frame.pack(fill="both", expand=True)
        self.current_frame = self.menu_frame

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        new_frame.pack(fill="both", expand=True)
        self.current_frame.destroy()
        self.current_frame = new_frame


class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Main Menu")
        label.pack()

        playlist_button = tk.Button(
            self, text="Playlist Creator", command=lambda: master.show_frame(PlaylistCreatorFrame))
        playlist_button.pack()

        option2_button = tk.Button(
            self, text="Song Library", command=lambda: master.show_frame(SongLibraryFrame))
        option2_button.pack()


class PlaylistCreatorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Create a Playlist")
        label.pack()

        select_button = tk.Button(self, text="Browse Files", command=self.browse_files)
        select_button.pack()

        create_by_button = tk.Button(self, text="Create By...", command=lambda: master.show_frame(CreateByFrame))
        create_by_button.pack()

        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenuFrame))
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
                minutes, seconds = map(int, time_str.split(':'))
                if minutes >= 0 and seconds >= 0:
                    total_seconds = minutes * 60 + seconds
                    return total_seconds
                else:
                    print(
                        "Invalid time input. Please enter positive values for minutes and seconds.")
            except ValueError:
                print("Invalid time format. Please use the format mm:ss.")

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
            ("Random", "random")
        ]
        # Create buttons for users' options
        for text, arg in options:
            button = tk.Button(self, text=text, command=lambda arg=arg: self.select_criteria(arg))
            button.pack()
        # Create return to main menu button
        back_button = tk.Button(
            self, text="Back to Playlist Creator", command=lambda: master.show_frame(PlaylistCreatorFrame))
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
                if '-' in time_str:
                    print("Invalid time input. Please enter positive values for hours, minutes, and seconds.")
                else:
                    total_seconds = hhmmss_to_seconds(time_str)
                    return total_seconds
            except ValueError:
                print("Invalid time format. Please use the format hh:mm:ss.")


class SongLibraryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Song Library")
        label.pack()

        # Finder window
        collection_button = tk.Button(
            self, text="Your Collection", command=self.show_collection_viewer)
        collection_button.pack()

        add_songs_button = tk.Button(
            self, text="Add Songs", command=self.add_songs)
        add_songs_button.pack()

        # Frame 1st for selection of tag
        # Finder window
        tags_button = tk.Button(self, text="Edit Tags", command=lambda: master.show_frame(EditTagsFrame))
        tags_button.pack()

        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenuFrame))
        back_button.pack()

    def show_collection_viewer(self):
        audio_files = load_data()
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
            add_songs_window, text="Add and Process", command=lambda: self.process_data(data_text.get("1.0", tk.END), 
            selected_file_path, add_songs_window))
        add_button.pack()

    def process_data(self, text, filepath, window_to_close):
        if text and filepath:
            audio_files = read_json(LIBRARY_DATA_PATH, AudioFile)
            parsed_data = parse_text_block_into_song(text)
            index = len(audio_files)
            # Get audio file data
            song_name = parsed_data["song_name"]
            filename = song_name + '.mp3'
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
                moods=[]
            )
            os.rename(filepath, new_filepath)
            audio_files.append(audio_file)
            save_data(audio_files)
            print("Song added successfully!")
            window_to_close.destroy()


class EditTagsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Create window label
        label = tk.Label(self, text="Edit tags")
        label.pack()
        # Define users' options
        options = [
            ("Genre", "genre"),
            ("Mood", "moods")
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
