import os
import tkinter as tk
from tkinter import filedialog, simpledialog

from config import DATE_STRING
from playlist import Playlist


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
            self, text="MP3 Downloader", command=lambda: master.show_frame(Option2Frame))
        option2_button.pack()

        option3_button = tk.Button(
            self, text="Song Library", command=lambda: master.show_frame(Option3Frame))
        option3_button.pack()


class PlaylistCreatorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Create a Playlist")
        label.pack()

        select_button = tk.Button(
            self, text="Browse Files", command=self.browse_files)
        select_button.pack()

        create_by_button = tk.Button(
            self, text="Create By...", command=lambda: master.show_frame(CreateByFrame))
        create_by_button.pack()

        back_button = tk.Button(
            self, text="Back to Main Menu", command=lambda: master.show_frame(MainMenuFrame))
        back_button.pack()

    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Select MP3 Files", filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
        
        if not files: # if there was no selection return
            return
        filenames = [os.path.basename(file) for file in files]

        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            pass
        max_duration = self.get_time_input()

        playlist = Playlist(title=title)
        # print(filenames)
        playlist.add_songs_by_filename(filenames=filenames, max_duration=max_duration)
        # print(playlist.songs)
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


class CreateByFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Create By...")
        label.pack()

        genre_button = tk.Button(
            self, text="Create By Genre", command=self.create_genre_playlist)
        genre_button.pack()

        mood_button = tk.Button(
            self, text="Create By Mood", command=self.create_mood_playlist)
        mood_button.pack()

        random_button = tk.Button(
            self, text="Create Random Playlist", command=self.create_random_playlist)
        random_button.pack()

        back_button = tk.Button(
            self, text="Back to Playlist Creator", command=lambda: master.show_frame(PlaylistCreatorFrame))
        back_button.pack()

    def create_random_playlist(self):
        max_duration = self.get_time_input()
        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            pass
        playlist = Playlist(title=title)
        playlist.create_playlist_by_criteria(
            criteria_function=self.ignore_helper, max_duration=max_duration)
        playlist.export_playlist()
    
    def ignore_helper(self, arg):
        return True if arg else False
        
    def create_genre_playlist(self):
        # Prompt user for genre
        genre = simpledialog.askstring(
            "Enter Genre", "Enter the genre you're looking for:")
        if not genre:
            pass
        # Prompt user to enter max playlist duration
        max_duration = self.get_time_input()
        # Prompt user for playlist name
        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            pass

        # Create playlist object
        playlist = Playlist(title=title)
        playlist.create_playlist_by_criteria(
            criteria_function=self.ignore_helper, max_duration=max_duration)
        playlist.export_playlist()

    def create_mood_playlist(self):
        # Prompt user for mood
        mood = simpledialog.askstring(
            "Enter Mood", "Enter the mood you're looking for:")
        if not mood:
            pass
        # Prompt user to enter max playlist duration
        max_duration = self.get_time_input()
        # Prompt user for playlist name
        title = simpledialog.askstring(
            "Playlist Title", "Enter the title of your playlist:")
        if not title:
            pass

        if max_duration is not None:
            # Create playlist object
            playlist = Playlist(title=title)
            playlist.create_playlist_by_criteria(
                criteria_function=self.ignore_helper, max_duration=max_duration)
            playlist.export_playlist()

    def get_time_input(self):
        while True:
            time_str = simpledialog.askstring(
                "Enter Max Duration", "Enter max duration (hh:mm:ss):")
            try:
                hours, minutes, seconds = map(int, time_str.split(':'))
                if hours >= 0 and minutes >= 0 and seconds >= 0:
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    return total_seconds
                else:
                    print(
                        "Invalid time input. Please enter positive values for hours, minutes, and seconds.")
            except ValueError:
                print("Invalid time format. Please use the format hh:mm:ss.")


class Option2Screen:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Downloader")

        label = tk.Label(root, text="Download an MP3")
        label.pack()

        back_button = tk.Button(
            root, text="Back to Main Menu", command=self.show_main_menu)
        back_button.pack()

    def show_main_menu(self):
        self.root.destroy()  # Close the current screen
        main_menu_window = tk.Tk()
        MainMenu(main_menu_window)


class Option3Screen:
    def __init__(self, root):
        self.root = root
        self.root.title("Song Library")

        label = tk.Label(root, text="Your Collection")
        label.pack()

        back_button = tk.Button(
            root, text="Back to Main Menu", command=self.show_main_menu)
        back_button.pack()

    def show_main_menu(self):
        self.root.destroy()  # Close the current screen
        main_menu_window = tk.Tk()
        MainMenu(main_menu_window)


def main():
    app = Application()
    app.mainloop()  # Start the GUI event loop


if __name__ == "__main__":
    main()
